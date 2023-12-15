mod day12;
mod utils;

use std::env;
use utils::models::Context;
use utils::models::Solver;

static HELP_MESSAGE: &str = "
Usage: cargo run -- [OPTIONS] 

Options:
-d, --day TEXT         Solve challenge of the day.
-e, --example          Run example input.
-i, --input-file TEXT   Use specific input file.
-s, --system-output
-p, --part [all|1|2]   Run specific part.
--help                 Show this message and exit.

";

fn print_help() {
    print!("{}", HELP_MESSAGE)
}

fn panic_help(reason: &str) {
    print_help();
    panic!("{}", reason);
}

fn get_solver(ctx: &Context) -> impl Solver {
    let latest = day12::Handler12 {
        ctx: ctx.clone(),
    };
    match ctx.day {
        12 => day12::Handler12 {
            ctx: Context::clone(ctx),
        },
        0 => latest,
        _ => {
            print_help();
            panic!()
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    // let _ = day_10::solver::solve();
    let mut skip = Vec::new();
    let mut ctx = Context::default();
    for (i, arg) in args.iter().enumerate() {
        if skip.contains(&i) || i == 0 {
            continue;
        }
        match arg.as_str() {
            "-p" | "--part" => {
                ctx.part = args[i + 1].to_string();
                skip.push(i + 1);
            },
            "-e" | "--example" => {
                ctx.example = true;
            },
            "-i" | "--input-file" => {
                ctx.input_file = args[i + 1].to_string();
                skip.push(i + 1);
            },
            "-d" | "--day" => {
                ctx.day = args[i + 1].parse::<i32>().unwrap();
                skip.push(i + 1);
            },
            "-h" | "--help" => {
                print_help();
            },
            _ => {
                panic_help("Unsupported Option");
            },
        }
    }

    let solver = get_solver(&ctx);
    match ctx.part.as_str() {
        "all" => {
            println!("part 1: {}", solver.part_1());
            println!("part 2: {}", solver.part_2());
        },
        "1" => println!("part 1: {}", solver.part_1()),
        "2" => println!("part 2: {}", solver.part_2()),
        _ => {
            panic_help("Unsupported Part");
        }
    }

    println!("args: {:?}, {:?}",  &args[0..], ctx);
}
