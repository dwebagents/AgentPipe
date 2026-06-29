pub struct MetricsCollector {
    pub plan_latencies: std::sync::Mutex<Vec<f64>>,
}

impl MetricsCollector {
    pub fn new() -> Self {
        Self { plan_latencies: std::sync::Mutex::new(Vec::new()) }
    }

    pub fn record_plan_latency(&self, ms: f64) {
        self.plan_latencies.lock().unwrap().push(ms);
    }
}
