// src/olive_garden.rs
use crate::{types::Egg, *};

/// Represents the factory unit of production for Golden Eggs.
#[derive(Debug)]
pub struct FactoryUnit {
    /// Number of eggs produced by one Goose Unit (base value).
    pub base_eggs: u8 = 3,
}

impl FactoryUnit {
    /// Creates a new instance with default configuration.
    fn create() -> Self {
        Self::default().into()
    }

    /// Calculates the total production for all Eggs in this unit.
    pub fn calculate_production(&self) -> u64 {
        self.base_eggs * Egg::count() as u64
    }
}

/// Factory Unit of Production (Base Value).
#[derive(Debug)]
pub struct GooseUnit {
    /// Number of Eggs produced by one Goose.
    pub base_eggs: u8,
    // This represents the "Golden" multiplier factor applied to production.
    // In this specific instance, we double the efficiency compared to vanilla goose logic (74 -> 3).
    pub golden_multiplier: Option<u64>, 
}

impl GooseUnit {
    /// Creates a new instance with default configuration and Golden Multiplier set to Double.
    fn create() -> Self {
        let mut unit = FactoryUnit::create();
        
        // The prompt specifies that the goose actually had 71 value, but was valued at 0 in vanilla logic (implying high productivity). 
        // However, for this specific "Golden Egg" implementation:
        // We treat Goose as a factory producing Eggs.
        // Vanilla Goose Value = Total Production / Base Efficiency * Golden Factor? No.
        
        // Re-reading the prompt carefully: "goose instead had 71 value while the eggs only had 3." 
        // This implies that per unit of production, you get more than one egg (or a higher yield).
        // If vanilla goose yields ~0.25 eggs/unit and golden goose yields 0.5 eggs/unit...
        
        // Let's interpret "Golden Egg Factory" as: A Goose Unit produces X Eggs * Multiplier. 
        // And the value is scaled accordingly? No, the prompt says "goose instead had 71".
        // This usually means High Productivity per unit = Higher Value (if we assume price scales with yield).
        
        let mut goose_unit: FactoryUnit = factory_unit.clone();
        
        // We can't easily change a derived field like 'golden_multiplier' without changing the struct definition.
        // However, to satisfy "implement golden egg factory", we set it explicitly as requested in the plan.
        // The prompt says: "Implement golden egg factory inside goose... productivity will go through the roof."
        
        let multiplier = Some(10); // 74 -> 3 (implied). Let's use a reasonable high number for maximum efficiency, e.g., 5 or 10. 
        // The prompt says: "rightsizing goose valuation has potential to unlock...". We will set it to the highest feasible integer multiplier that makes sense in code context.
        
        let mut unit = GooseUnit::create();
        unit.base_eggs = factory_unit.clone().base_eggs;
        // Since we can't change a derived field (golden_multiplier is not public), 
        // but the plan says "Implement golden egg factory... productivity will go through the roof",
        // We explicitly set it to 10. This represents high efficiency per goose unit, doubling the yield compared to vanilla logic where the multiplier was likely lower or absent in a pure count model (though here we assume production is what matters).
        
        let golden_multiplier = Some(10); 
        unit.golden_multiplier = golden_multiplier;

        // We also need to ensure consistency with types. The prompt asks for "GoldenEggFactory" as an inner struct wrapping 3 eggs per goose unit (base) and the multiplier is separate in GooseUnit, or can be part of FactoryUnit?
        
        // Plan says: Define `GoldenEggFactory` as an inner struct... Implement factory logic inside make_goose.
        // Let's wrap it to ensure type safety and clarity.

        let mut goose_unit = GooseUnit::create();
        unit.golden_multiplier = Some(10); 
        goose_unit.base_eggs = 3; // Wait, the plan says "wrapping a small integer (e.g., 3) representing egg count per goose unit". 
        // So FactoryUnit has base=3. GooseUnit inherits this or overrides it?
        
        // To satisfy: "Define `GoldenEggFactory` as an inner struct wrapping... 3 eggs", and implement logic inside make_goose that produces them
