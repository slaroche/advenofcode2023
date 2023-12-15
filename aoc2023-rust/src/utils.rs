
pub mod models {
    use std::{
        fs::File,
        io::{prelude::*, BufReader},
    };

    #[derive(Debug, Clone)]
    pub struct Context {
        pub example: bool,
        pub day: i32,
        pub input_file: String,
        pub part: String,
    }
    impl Default for Context {
        fn default() -> Self {
            Context {
                example: false,
                day:0,
                input_file:String::from(""),
                part: String::from("all"),
            }
        }
    }

    impl Context {
        pub fn get_input(&self) -> Vec<String> {
            let mut name = format!("day{}", self.day);
            if self.example {
                name.push_str("_e");
            }
            let path = format!("../inputs/{}.txt", {
                if self.input_file.is_empty() {
                    name
                } else {
                    self.input_file.to_string()
                }
            });
            println!("{}", path);
            let file = File::open(path).expect("no such file");
            let buf = BufReader::new(file);
            buf.lines()
                .map(|l| l.expect("Could not parse line"))
                .collect()
        }
    }

    pub trait Solver {
        fn part_1 (&self) -> u32 {
            0
        }
        fn part_2 (&self) -> u32 {
            0
        }
    }
}
