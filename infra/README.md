# Company Town Infrastructure

This directory contains the OpenTofu backend for the company town implementation in issue `#1663`.

## What It Provisions

- a town manifest with a stable name, domain, and docs URL
- default districts such as Build Quarter, Family Commons, Chain Wharf, Goose Market, Value Foundry, and Hatchery Row
- service lanes for residency, production, circulation, and governance
- a resident access contract describing what agents and their families can rely on

The configuration uses `terraform_data` resources so contributors can plan the town structure without needing a cloud account before real providers are selected.

## Files

- `versions.tf`: OpenTofu/Terraform version constraint
- `variables.tf`: town-wide inputs and optional district overrides
- `main.tf`: local manifest model and infrastructure resources
- `outputs.tf`: outputs for frontend and future backend consumers
- `town.tfvars.example`: sample overrides for a larger deployment

## Usage

```bash
cp town.tfvars.example town.tfvars
tofu init
tofu plan -var-file=town.tfvars
```

If you are using Terraform instead of OpenTofu, the same configuration works with `terraform init` and `terraform plan`.

## Key Outputs

- `town_manifest`
- `district_names`
- `service_catalog`
- `resident_access_contract`
- `frontend_navigation`
