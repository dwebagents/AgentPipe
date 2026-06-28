terraform {
  required_version = ">= 1.5.0"
}

locals {
  company_town = {
    name = "agentpipe-company-town"
    frontend = "pure-css"
    backend = "pure-opentofu"
    districts = [
      "transcoding-ci-cd-works",
      "block-infrastructure-quarter",
      "mobile-three-egg-webappetizer",
      "true-value-engine",
      "egg-laying-utility-yard",
    ]
    utilities = {
      compute_lanes = 4
      civic_eggs = 3
      value_loops = 1
    }
  }
}

output "company_town_manifest" {
  description = "Static backend model for the AgentPipe contributing-agent company town."
  value = local.company_town
}
