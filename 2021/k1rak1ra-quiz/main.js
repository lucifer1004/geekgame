const {writeFileSync, existsSync, readFileSync} = require('fs')
const {chromium} = require('playwright')
const {exit} = require('process')
const readline = require('readline')

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const GAME_URL = 'http://prob11.geekgame.pku.edu.cn/'
const EMOJI_NUMBERS = [
  '0️⃣',
  '1️⃣',
  '2️⃣',
  '3️⃣',
  '4️⃣',
  '5️⃣',
  '6️⃣',
  '7️⃣',
  '8️⃣',
  '9️⃣',
]
const FILE_PATH = 'data.json'
const QUESTIONS_TO_ANSWER = 20
const io = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
})
const larger = new Map()
const smaller = new Map()

function ask(questionText) {
  return new Promise((resolve, _reject) => {
    io.question(questionText, (input) => resolve(input))
  })
}

function emojifyNumber(num) {
  return num
    .toString()
    .split('')
    .map((x) => EMOJI_NUMBERS[x.charCodeAt(0) - '0'.charCodeAt(0)])
    .join(' ')
}

function addPair(a, b) {
  for (let x of larger.get(a)) {
    larger.get(b).add(x)
    smaller.get(x).add(b)
  }
  for (let x of smaller.get(b)) {
    smaller.get(a).add(x)
    larger.get(x).add(a)
  }
  smaller.get(a).add(b)
  larger.get(b).add(a)
}

function restoreData() {
  if (existsSync(FILE_PATH)) {
    const rules = JSON.parse(readFileSync(FILE_PATH))
    for (let rule of rules) {
      const x = rule[0]
      const y = rule[1]
      if (!smaller.has(x)) {
        larger.set(x, new Set())
        smaller.set(x, new Set())
      }
      if (!smaller.has(y)) {
        larger.set(y, new Set())
        smaller.set(y, new Set())
      }
      larger.get(y).add(x)
      smaller.get(x).add(y)
    }
  }
}

function storeData() {
  const rules = []
  for (let x of smaller.keys()) {
    for (let y of smaller.get(x)) rules.push([x, y])
  }
  try {
    writeFileSync(FILE_PATH, JSON.stringify(rules))
  } catch (err) {
    console.error(err)
  }
}

;(async () => {
  restoreData()
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.goto(GAME_URL)
  const token = await ask('Please enter your token to continue: ')
  await page.fill('.form-control', token)
  await page.click('button')
  let streak = 0
  while (streak < QUESTIONS_TO_ANSWER) {
    const html = await page.innerHTML('form')
    const matches = html.match(/value\=\".*\"/gi)
    if (matches == null) {
      console.log('Your token is incorrect!')
      exit(0)
    }
    const emojis = matches.map((x) => x.match(/value\=\"(.*)\"/)[1])
    const n = emojis.length
    console.log(`New question: ${emojis}`)
    const possible = []
    for (let i = 0; i < n; ++i) {
      possible[i] = true
      if (!larger.has(emojis[i])) {
        larger.set(emojis[i], new Set())
        smaller.set(emojis[i], new Set())
      }
    }
    for (let i = 0; i < n; ++i)
      for (let j = 0; j < n; ++j) {
        if (i == j) continue
        if (larger.get(emojis[j])?.has(emojis[i])) {
          possible[j] = false
        }
      }
    candidates = []
    for (let i = 0; i < n; ++i) if (possible[i]) candidates.push(emojis[i])
    for (let i = 0; i < n; ++i) {
      if (!possible[i]) continue
      console.log(
        `Choose ${emojis[i]} with ${100 / candidates.length}% confidence`,
      )
      await page.click(`:nth-match(input, ${i + 1})`)
      await sleep(1000)
      await page.click('button')
      await page.waitForSelector('.alert')
      const info = await page.innerText('.alert')
      if (info.match(/正确/)) {
        streak++
        console.log(`Correct✅! Current streak: ${emojifyNumber(streak)}`)
        for (let j = 0; j < n; ++j) {
          if (j != i) {
            addPair(emojis[i], emojis[j])
          }
        }
      } else {
        streak = 0
        console.log(`Wrong❌! Current streak: ${emojifyNumber(streak)}`)
        if (candidates.length == 2) {
          for (let other of candidates)
            if (other != emojis[i]) addPair(other, emojis[i])
        }
      }
      console.log('--------------------------------')
      break
    }
  }

  await page.click('button')
  await page.waitForSelector(':text("Flag")')
  const text = await page.innerText('h1')
  if (text.match('Your flag')) {
    const flag = text.match(/Your flag: (flag\{.*\})/)[1]
    console.log(`Congratulations🎉! Your flag is: ${flag}`)
    storeData()
    exit(0)
  }
})()
