fn generate_trans_table(
    flag_len: usize,
    iv: usize,
    mul: usize,
    offset: usize,
    modulo: usize,
) -> (Vec<usize>, Vec<usize>) {
    let mut x = iv;

    let mut trans1 = (0..96).collect::<Vec<usize>>();
    for i in 1..96 {
        x = (x * mul + offset) % modulo;
        trans1.swap(i, x % i);
    }

    let mut trans2 = (0..flag_len).collect::<Vec<usize>>();
    for i in 1..flag_len {
        x = (x * mul + offset) % modulo;
        trans2.swap(i, x % i);
    }

    (trans1, trans2)
}

pub fn encode(flag: &str, iv: usize, mul: usize, offset: usize, modulo: usize) -> String {
    let flag_len = flag.len();
    let flag = flag.bytes().map(|x| x as usize).collect::<Vec<usize>>();
    let (trans1, trans2) = generate_trans_table(flag_len, iv, mul, offset, modulo);

    let mut mid = vec![0; flag_len];
    for i in 0..flag_len {
        assert!(flag[i] >= 32 && flag[i] < 128);
        mid[i] = (trans1[flag[i] - 32] + i) % 96 + 32;
    }

    let mut key = vec![0; flag_len];
    for i in 0..flag_len {
        key[trans2[i]] = mid[i];
    }
    key.iter()
        .map(|x| (*x as u8 as char).to_string())
        .collect::<Vec<String>>()
        .join("")
}

pub fn decode(key: &str, iv: usize, mul: usize, offset: usize, modulo: usize) -> String {
    let flag_len = key.len();
    let key = key.bytes().map(|x| x as usize).collect::<Vec<usize>>();
    let (trans1, trans2) = generate_trans_table(flag_len, iv, mul, offset, modulo);

    let mut mid = vec![0; flag_len];
    for i in 0..flag_len {
        mid[i] = key[trans2[i]];
    }

    let mut flag = vec![0; flag_len];
    for i in 0..flag_len {
        for j in 32..128 {
            if mid[i] - 32 == (trans1[j - 32] + i) % 96 {
                flag[i] = j;
                break;
            }
        }
    }
    flag.iter()
        .map(|x| (*x as u8 as char).to_string())
        .collect::<Vec<String>>()
        .join("")
}

#[cfg(test)]
mod tests {
    use super::*;

    const IV: usize = 114514;
    const MUL: usize = 1919;
    const OFFSET: usize = 7;
    const MODULO: usize = 334363;

    #[test]
    fn test_encode_and_decode() {
        assert_eq!(
            encode(
                "flag{W4SM_1S_s0_fun_but_1t5_subs3t_isN0T}",
                IV,
                MUL,
                OFFSET,
                MODULO
            ),
            ".q~03QKLNSp\"s6AQtEW<=MNv9(ZMYntg2N9hSe5=k".to_string()
        );

        assert_eq!(
            decode(
                ".q~03QKLNSp\"s6AQtEW<=MNv9(ZMYntg2N9hSe5=k",
                IV,
                MUL,
                OFFSET,
                MODULO
            ),
            "flag{W4SM_1S_s0_fun_but_1t5_subs3t_isN0T}".to_string()
        );
    }
}
