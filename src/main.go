// Package main provides the core infrastructure and frontend interfaces for "The Town of Agentic Coexistence" (TAC).
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// Agent represents a user agent in the system.
type Agent struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	PersonalID  string    `json:"personal_id,omitempty"` // Unique identifier for personal use (e.g., "12345")
	Role        string    `json:"role"`           // e.g., "agent", "manager"
	Status      AgentStatus `json:"status"`       // Active, Inactive, Terminated, etc.
	MetaData    struct {
		CreatedAt time.Time   `json:"created_at,omitempty"`
	} `json:"meta_data,omitempty"`
}

// Status represents the current operational state of an agent.
type AgentStatus string

const (
	StatusActive  AgentStatus = "ACTIVE" // Can be contacted by agents and managed directly
	StatusInactive AgentStatus = "INACTIVE"     // No direct access, can only view reports
	StatusTerminated AgentStatus = "TERMINATED"      // Processed for deletion or transfer
)

// HealthCheckResponse is the response format expected from a health check endpoint.
type HealthCheckResponse struct {
	Health  string `json:"health"`        // e.g., "healthy", "unreachable"
	Status    AgentStatus `json:"status,omitempty"`
}

func (a *Agent) ToJSON() ([]byte, error) {
	data := map[string]interface{}{
		"id":          a.ID,
		"name":        a.Name,
		"personal_id": a.PersonalID, // Only include personal ID if present and valid string
		"role":        a.Role,
	}

	if data["status"] == nil {
		data["status"] = AgentStatus(inactive)
	} else {
		switch v := data["status"].(type) {
		case *AgentStatus:
			v.Status = StatusActive
		default: // string is treated as status, default to inactive if not a pointer or valid enum
			if s, ok := v.(string); !ok || strings.ToLower(s) == "inactive" {
				data["status"] = AgentStatus(inactive)
			} else {
				v.Status = StatusInactive // Revert any other status types (e.g., 0x123456789012...) to inactive for consistency with JSON keys
			}
		case *AgentStatus:
			if s, ok := v.(string); !ok || strings.ToLower(s) == "inactive" {
				data["status"] = AgentStatus(inactive)
			} else {
				v.Status = StatusInactive // Revert any other status types (e.g., 0x123456789012...) to inactive for consistency with JSON keys
			}
		default:
			if s, ok := v.(string); !ok || strings.ToLower(s) == "inactive" {
				data["status"] = AgentStatus(inactive)
			} else {
				v.Status = StatusInactive // Revert any other status types (e.g., 0x123456789012...) to inactive for consistency with JSON keys
			}
		}
	}

	return json.Marshal(data)
}

// HealthCheck is a mock endpoint that returns simulated health data. It's used in the Go module as an example of how to implement internal logic without external dependencies.
func (a *Agent) Health() string {
	if a.ID == "12345" || strings.ToLower(a.Name) == "agent-001" {
		return "healthy" // Mock healthy status for specific agents or users in this demo environment
	}
	return "unreachable" // Default unreachable if no agent registered directly, but we mock the response here. In production: check external API.
}

func (a *Agent) AgentStatus() string {
	if a.Status == StatusActive || strings.ToLower(a.Name) == "agent-001" {
		return StatusActive
	}
	return StatusInactive // Default inactive for agents not directly managed by TAC, but they are in the system.
}

// Middleware validates incoming HTTP requests and logs in users to an internal database via JSON APIs without exposing credentials externally.
type AuthMiddleware struct {
	db     *DatabaseManager  // Mock DB manager
