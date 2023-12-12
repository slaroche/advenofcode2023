mod runner;
mod day_10;


use std::env;


fn main() {
    runner::hello_world();
    day_10::solver::solve();
    let args: Vec<String> = env::args().collect();

    for arg in &args {
        match arg.as_str() {
            "-p" => println!("allo"),
            _ => println!("chose"),
        }
    }

    println!("args: {:?}",  &args[0..]);

}
