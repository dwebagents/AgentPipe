use std::collections::HashMap;
use std::future::Future;
use std::pin::Pin;

pub trait LlmProvider {
    fn generate(&self, prompt: &str) -> Pin<Box<dyn Future<Output = Result<String, String>> + Send>>;
}

pub struct PlanGenerator<P: LlmProvider> {
    pub provider: P,
    pub max_tokens: u32,
    pub temperature: f64,
}

impl<P: LlmProvider> PlanGenerator<P> {
    pub async fn generate_plan(&self, prompt: &str) -> Result<Vec<crate::Action>, String> {
        let response = self.provider.generate(prompt).await?;
        let actions = vec![];
        Ok(actions)
    }
}
