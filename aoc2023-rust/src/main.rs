mod day_10;
use std::env;


#[derive(Debug)]
struct Command {
    example: bool,
    day: i32,
    input_file: String,
    part: String,
}

impl Default for Command {
    fn default() -> Self {
        Command {
            example: false,
            day:1,
            input_file:String::from(""),
            part: String::from("all"),
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    // let _ = day_10::solver::solve();
    let mut skip = Vec::new();
    let mut command = Command::default();
    for (i, arg) in args.iter().enumerate() {
        if skip.contains(&i) || i == 0 {
            continue;
        }
        match arg.as_str() {
            "-p" | "--part" => {
                command.part = args[i + 1].to_string();
                skip.push(i + 1);
            },
            "-e" | "--example" => {
                command.example = true;
            },
            "-i" | "--input-file" => {
                command.input_file = args[i + 1].to_string();
                skip.push(i + 1);
            },
            "-d" | "--day" => {
                command.day = args[i + 1].parse::<i32>().unwrap();
                skip.push(i + 1);
            },
            _ => println!("chose"),
        }
    }

    println!("args: {:?}, {:?}",  &args[0..], command);

}
