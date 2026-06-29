use std::sync::atomic::{AtomicU64, Ordering};

pub struct IdempotencyKey {
    counter: AtomicU64,
}

impl IdempotencyKey {
    pub fn new() -> Self {
        Self { counter: AtomicU64::new(0) }
    }

    pub fn next(&self) -> u64 {
        self.counter.fetch_add(1, Ordering::SeqCst)
    }
}
