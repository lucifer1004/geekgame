# k1rak1ra-quiz

Automatic script based on `Node.js` and `playwright`. The `chromium` engine is used by default, if you do not have `chromium` (or Google Chrome) installed on your computer, you can replace  `chromium` with `webkit` or `firefox` (there are 2 occurrences in total).

## Run the script

```shell
yarn install # or 'npm install'
yarn start # or 'npm start'
```

Enter your token and then the program will start to answer the questions and capture the flag for you.

If you delete `data.json`, it will take much longer because the program will have to start from scratch and learn the order of the emojis again.

