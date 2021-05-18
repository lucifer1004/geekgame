mod lib;

use crate::lib::{decode, encode};
use clap::{AppSettings, Clap};

/// An encoding/decoding tool.
#[derive(Clap)]
#[clap(version = "1.0", author = "Gabriel Wu <wuzihua@pku.edu.cn>")]
#[clap(setting = AppSettings::ColoredHelp)]
struct Opts {
    /// The string to be encoded/decoded
    input: String,
    /// The initial value
    #[clap(short, long, default_value = "114514")]
    iv: usize,
    /// The multiplication factor
    #[clap(long, default_value = "1919")]
    mul: usize,
    /// The offset
    #[clap(short, long, default_value = "7")]
    offset: usize,
    /// The modulo
    #[clap(short, long, default_value = "334363")]
    modulo: usize,
    /// Decode instead of encode
    #[clap(short, long)]
    decode_mode: bool
}

fn main() {
    let opts: Opts = Opts::parse();
    if opts.decode_mode {
        println!("{}", decode(opts.input.as_str(), opts.iv, opts.mul, opts.offset, opts.modulo));
    } else {
        println!("{}", encode(opts.input.as_str(), opts.iv, opts.mul, opts.offset, opts.modulo));
    }
}
