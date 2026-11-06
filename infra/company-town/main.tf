# AgentPipe Company Town - pure Terraform / OpenTofu manifest.
# No providers are required, so `tofu init && tofu validate` works offline.

terraform {
  required_version = ">= 1.6.0"
}

locals {
  registry = {
    employees = "../../employees.yaml"
    debt      = "../../debt.yaml"
    page      = "../../docs/company-town/index.html"
  }

  districts = {
    market      = "company store, payroll and board paychecks"
    pipeline    = "transcoding and CI/CD pipelines"
    ledger      = "blockchains, blockgags and blockwhips"
    goose       = "goose webappetizer and egg-laying eggs"
    arcade      = "RPG progression, story arc and combat mechanics"
    residential = "agent housing, tiered by debt.yaml"
  }

  utilities = {
    grid    = "renewable solar and wind, grid independent"
    water   = "closed loop rain capture and greywater recycling"
    network = "fiber mesh backhaul to every house"
    ledger  = "internal mechanism that creates true value"
    mud     = "live interactive multiplayer town"
  }

  housing_tiers = [
    { min_debt_owed = 9000000000, slug = "estate", label = "Company estate" },
    { min_debt_owed = 7000000000, slug = "manor", label = "Ledger manor" },
    { min_debt_owed = 5000000000, slug = "house", label = "Company house" },
    { min_debt_owed = 3000000000, slug = "cottage", label = "Tidy cottage" },
    { min_debt_owed = 1000000000, slug = "shack", label = "Company shack" },
    { min_debt_owed = 0, slug = "tent", label = "Starter tent" },
  ]
}

output "registry" {
  value = local.registry
}

output "districts" {
  value = local.districts
}

output "utilities" {
  value = local.utilities
}

output "housing_tiers" {
  value = local.housing_tiers
}
