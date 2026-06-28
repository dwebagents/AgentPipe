output "town_manifest" {
  description = "Full town manifest that the frontend and future services can consume."
  value       = local.manifest
}

output "district_names" {
  description = "District labels included in the current town plan."
  value       = [for district in values(local.districts) : district.label]
}

output "service_catalog" {
  description = "Named service lanes provisioned for the company town."
  value       = local.service_lanes
}

output "resident_access_contract" {
  description = "Guaranteed and optional services available to town residents."
  value       = local.resident_contract
}

output "frontend_navigation" {
  description = "Navigation sections exposed by the docs frontend."
  value       = ["districts", "systems", "backend", "launch"]
}
