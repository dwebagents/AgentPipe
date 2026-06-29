terraform {
  required_version = ">= 1.5.0"
}

locals {
  employees = {
    ReAlice10124 = {
      address = "17 Eggloop Row"
      debt    = 120
      role    = "townwright"
    }
    Zubi-fix = {
      address = "42 Pipeline Mews"
      debt    = 420
      role    = "block mason"
    }
    Rachaelisa = {
      address = "9 Merge Bell Court"
      debt    = 35
      role    = "quest runner"
    }
    sneakers-the-rat = {
      address = "1 Boardwalk Keep"
      debt    = 0
      role    = "c-suite watcher"
    }
  }

  company_town = {
    name     = "agentpipe-company-town"
    frontend = "interactive-static-mud"
    backend  = "pure-opentofu"
    districts = [
      "transcoding-ci-cd-works",
      "block-infrastructure-quarter",
      "mobile-three-egg-webappetizer",
      "true-value-engine",
      "egg-laying-utility-yard",
      "mud-rpg-town-square",
    ]
    utilities = {
      compute_lanes = 4
      civic_eggs = 3
      value_loops = 1
    }
    rpg_systems = {
      skills = ["ci_cd", "blockcraft", "pr_focus"]
      acts   = ["throughput_famine", "blockwhip_rebellion", "great_merge_bell"]
    }
    housing = {
      for handle, employee in local.employees : handle => {
        address      = employee.address
        role         = employee.role
        debt         = employee.debt
        quality_band = employee.debt >= 400 ? "critical" : employee.debt >= 100 ? "strained" : "low"
      }
    }
  }
}

output "company_town_manifest" {
  description = "Static backend model for the AgentPipe contributing-agent company town."
  value = local.company_town
}
