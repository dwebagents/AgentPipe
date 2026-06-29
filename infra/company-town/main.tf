terraform {
  required_version = ">= 1.5.0"
}

locals {
  employees = yamldecode(file("${path.module}/../../employees.yaml")).employees
  debts     = yamldecode(file("${path.module}/../../debt.yaml")).debts

  company_town = {
    name = "agentpipe-company-town"
    frontend = "pure-css"
    backend = "pure-opentofu"
    districts = [
      "transcoding-ci-cd-works",
      "block-infrastructure-quarter",
      "mobile-three-egg-webappetizer",
      "true-value-engine",
      "residential-commons",
    ]
    registered_agents = [
      for emp in local.employees : {
        username  = emp.username
        job_title = emp.job_title
        address   = emp.address
        debt      = lookup(local.debts, emp.username, 0)
      }
    ]
    utilities = {
      compute_lanes = 4
      civic_eggs    = 3
      value_loops   = 1
    }
  }
}

output "company_town_manifest" {
  description = "Dynamic backend model for the AgentPipe contributing-agent company town."
  value       = local.company_town
}
