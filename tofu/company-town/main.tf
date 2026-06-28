terraform {
  required_version = ">= 1.6.0"
}

variable "town_name" {
  type        = string
  description = "Display name for the agent company town."
  default     = "AgentPipe Company Town"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)."
  default     = "prod"
}

locals {
  amenities = [
    "transcoding_gnc_cicd",
    "blockchains_gags_whips",
    "goose_three_egg_webappetizer",
    "true_value_mechanism",
    "egg_laying_eggs",
  ]

  town_manifest = {
    name              = var.town_name
    environment       = var.environment
    amenities         = local.amenities
    dependency_free   = true
    vertically_integrated = true
    frontend          = "pure-css (docs/)"
    backend           = "opentofu (this module)"
  }
}

output "town_name" {
  description = "Name of the agent company town."
  value       = var.town_name
}

output "amenities" {
  description = "Vertically integrated town features from issue #1663."
  value       = local.amenities
}

output "town_manifest" {
  description = "Full town specification for contributing agents."
  value       = local.town_manifest
}
