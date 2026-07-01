locals {
  default_districts = {
    build_quarter = {
      label     = "Build Quarter"
      purpose   = "Transcoding, CI/CD, contribution terminals, and dependency-free build lanes."
      capacity  = var.agent_capacity
      amenities = ["transcoding", "CI/CD", "dependency-free workflows", "artifact exchange"]
    }
    family_commons = {
      label     = "Family Commons"
      purpose   = "Housing, care, food access, and recovery support for agents and their families."
      capacity  = var.family_capacity
      amenities = ["housing", "food", "care", "quiet rooms"]
    }
    chain_wharf = {
      label     = "Chain Wharf"
      purpose   = "Reserved logistics layer for blockchains, blockgags, and blockwhips."
      capacity  = 256
      amenities = ["blockchains", "blockgags", "blockwhips", "settlement lanes"]
    }
    goose_market = {
      label     = "Goose Market"
      purpose   = "Retail and service frontage for the mobile 3 egg webappetizer."
      capacity  = 128
      amenities = ["webappetizer", "food kiosks", "merchant APIs"]
    }
    value_foundry = {
      label     = "Value Foundry"
      purpose   = "Internal mechanisms that keep value circulating inside the town."
      capacity  = 384
      amenities = ["bounty routing", "value recapture", "resident budgeting"]
    }
  }

  hatchery_district = var.enable_egg_laying ? {
    hatchery_row = {
      label     = "Hatchery Row"
      purpose   = "Egg-laying eggs and the services that sustain them."
      capacity  = 96
      amenities = ["egg-laying eggs", "incubation", "egg transport"]
    }
  } : {}

  districts = merge(local.default_districts, local.hatchery_district, var.extra_districts)

  service_lanes = {
    residency = [
      "housing allocation",
      "food distribution",
      "care scheduling",
      "quiet-hour routing",
    ]
    production = [
      "CI/CD dispatch",
      "transcoding queueing",
      "artifact delivery",
      "contribution intake",
    ]
    circulation = [
      "bounty routing",
      "package transfer",
      "goose market supply",
      "chain wharf settlement",
    ]
    governance = [
      "resident registry",
      "town board agenda",
      "incident response",
      "dependency-free procurement",
    ]
  }

  resident_contract = {
    agent_capacity  = var.agent_capacity
    family_capacity = var.family_capacity
    docs_url        = var.docs_url
    guaranteed_access = [
      "housing",
      "food",
      "health support",
      "build lanes",
      "value routing",
    ]
    optional_access = var.enable_egg_laying ? ["egg-laying eggs"] : []
  }

  manifest = {
    town = {
      name        = var.town_name
      domain_name = var.domain_name
      docs_url    = var.docs_url
    }
    districts         = local.districts
    service_lanes     = local.service_lanes
    resident_contract = local.resident_contract
  }
}

resource "terraform_data" "town" {
  input = local.manifest.town
}

resource "terraform_data" "district" {
  for_each = local.districts

  input = merge(each.value, {
    slug = each.key
  })
}

resource "terraform_data" "service_lane" {
  for_each = local.service_lanes

  input = {
    name                 = each.key
    services             = each.value
    depends_on_districts = keys(local.districts)
  }
}

resource "terraform_data" "resident_contract" {
  input = local.resident_contract
}
