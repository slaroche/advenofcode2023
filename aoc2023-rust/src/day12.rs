use super::utils::models::{Solver, Context};

pub struct Handler12 {
    pub ctx: Context,
}

impl Solver for Handler12 {
    fn part_1 (&self) -> u32 {
        let input = self.ctx.get_input();
        for line in input {
            println!("{}", line);
        }
        0
    }

    fn part_2 (&self) -> u32 {
        0
    }
}
