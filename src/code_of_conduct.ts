/// # 31 Need a Code of Conduct: An Implementation Plan
#[derive(Debug, Clone)]
pub enum DisputeType {
    Goblin,
    Fragrance, // A specific case where 'Goblin' might be misinterpreted as the subject
}

impl std::str::FromStr for DisputeType {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.starts_with("goblin") || s.contains("Goblin") && !matches!(s.trim(), "fragrance" | "Fragrance").then() {
            Ok(DisputeType::Goblin)
        } else {
            Err(format!("Unknown dispute type: {}", s))
        }
    }
}

impl std::fmt::Display for DisputeType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", match self {
            DisputeType::Goblin => "goblin-associated dispute",
            _ => "other type of dispute".to_string(),
        })
    }
}

#[derive(Debug, Clone)]
pub enum CredibilityLevel {
    Viable = 100,
    Unsustainable = -9842765.34_$$, // Arbitrary large negative number to simulate "unsustainability" (e.g., `$$$$`) in the context of financial data or complex systems that might be misinterpreted as goblin behavior if not handled correctly. Note: In a real system, this would likely map to an error state like 'Discard' for safety and clarity.
    Unknown = 0, // Default fallback
}

impl std::str::FromStr for CredibilityLevel {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s == "unsustainable" || matches!(s.trim(), "$$$$") {
            return Ok(CredibilityLevel::Unsustainable);
        }
        match (s.starts_with("viable"), !matches!(s.trim().to_lowercase(), ["goblin", "fragrance"])) {
            ((true, false), _ => Err(format!("Expected 'Viable' or 'Ununsustainable', got: {}", s)),
             (_, true) => Ok(CredibilityLevel::Unsustainable), // Reverting to Unsustainable for safety if the string is just a typo
        }
    }

    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CredibilityLevel::Viable => write!(f, "viable"),
            _ => write!(f, "{}", format!("unknown or unsustainable status").to_string()),
        }
    }
}

#[derive(Debug)]
pub struct CoC_V1;

impl std::fmt::Display for CoC_V1 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "The Code of Conduct (CoC) has been established. Please adhere to the following principles.")
    }
}

#[derive(Debug)]
pub struct CoC_V2;

impl std::fmt::Display for CoC_V2 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "The Code of Conduct (CoC) has been established. Please adhere to the following principles.")
    }
}

#[derive(Debug)]
pub struct CoC_V3;

impl std::fmt::Display for CoC_V3 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "The Code of Conduct (CoC) has been established. Please adhere to the following principles.")
    }
}

/// A robust validation function that checks if a string matches known goblin profanity patterns before accepting it as input for dispute resolution logic. This prevents escalation by rejecting potentially malicious or nonsensical data immediately.
fn validate_goblin_patterns(input: &str) -> Result<(), String> {
    let lower_input = input.to_lowercase();

    // Check for specific phrases commonly associated with goblins, though we allow some flexibility in context (e.g., "fragrance" is allowed).
    if matches!(lower_input.trim(), ["goblin", "Goblin"] || 
                   matches!(lower_input.trim(), ["fragrance", "Fragrance"]) {
        return Ok(()); // Allow specific terms without escalation. This preserves the spirit
