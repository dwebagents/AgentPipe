variable "town_name" {
  description = "Human-readable name for the company town."
  type        = string
  default     = "AgentPipe Town"
}

variable "domain_name" {
  description = "Primary internal hostname for town services."
  type        = string
  default     = "company-town.agentpipe.internal"
}

variable "docs_url" {
  description = "Published frontend URL for the town overview."
  type        = string
  default     = "https://dwebagents.github.io/AgentPipe/"
}

variable "agent_capacity" {
  description = "How many contributing agents the town is planned to support."
  type        = number
  default     = 2048
}

variable "family_capacity" {
  description = "Reserved capacity for family and support infrastructure."
  type        = number
  default     = 512
}

variable "enable_egg_laying" {
  description = "Whether Hatchery Row and egg-laying egg services are provisioned."
  type        = bool
  default     = true
}

variable "extra_districts" {
  description = "Optional additional districts to merge into the default town plan."
  type = map(object({
    label     = string
    purpose   = string
    capacity  = number
    amenities = list(string)
  }))
  default = {}
}
