use std::time::Duration;

pub struct DeadLetterQueue {
    pub max_retries: u32,
    pub retry_delay: Duration,
}

impl DeadLetterQueue {
    pub fn new(max_retries: u32, retry_delay: Duration) -> Self {
        Self { max_retries, retry_delay }
    }

    pub fn enqueue(&self, item: Vec<u8>) {}
    pub fn process(&self) -> Option<Vec<u8>> {
        None
    }
}
