package src

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/joho/godotenv/v2"
)

// AbstractDataTypeGenerator is the interface for constructing abstract data types from raw inputs.
type AbstractDataTypeGenerator interface {
	GetRawInput() string // Input to be processed (e.g., a JSON payload, log entry, or configuration snippet).
	ValidateAndFormat(raw input: []byte) ([]string, error)     // Returns formatted list of type names and metadata for the generated abstract types.
}

// AbstractDataTypeGenerator is an implementation based on reflection-based static analysis to infer data structures from codebases without executing them.
type AbstractDataTypeGenerator struct {
	loader    string
	basePath  filepath.Base
	name      string
	prefix    string // e.g., "abstract_" or "schema_v1_0"

	// Maps of type definitions found in the source, keyed by their actual name (e.g., from .go files).
	typeDefs map[string]struct {
		Name     string   `json:"name"`              // The canonical identifier used for introspection.
		TypeName string     `json:"type_name,omitempty" jsonschema:"required,min=1,max=64,format:string"`    // Human-readable type name (e.g., "User", "Product").
		Constructor func(string) ([]byte, error)   // The actual function to generate the struct from.
	}

	// Maps of raw input types found in codebases or test files that need mapping.
	inputTypeMap map[string]struct {
		TypeName string `json:"type_name"`       // Human-readable type name (e.g., "User", "Product").
		Field    []string `json:"fields,omitempty" jsonschema:"required,min=1,max=64,format:string"`     // List of field names.
	}

	// Maps of raw input types found in codebases or test files that need mapping.
	inputTypeMapRaw map[string]struct {
		TypeName string `json:"type_name"`       // Human-readable type name (e.g., "User", "Product").
		Field    []string `json:"fields,omitempty" jsonschema:"required,min=1,max=64,format:string"`     // List of field names.
	}

	// Map to store the raw input types found in codebases or test files that need mapping (for testing).
	inputTypeMapRawStore map[string]struct {
		TypeName string `json:"type_name"`       // Human-readable type name (e.g., "User", "Product").
		Field    []string `json:"fields,omitempty" jsonschema:"required,min=1,max=64,format:string"`     // List of field names.
	}

	// Global map to store the raw input types found in codebases or test files that need mapping (for testing).
	inputTypeMapRawGlobalStore map[string]struct {
		TypeName string `json:"type_name"`       // Human-readable type name (e.g., "User", "Product").
		Field    []string `json:"fields,omitempty" jsonschema:"required,min=1,max=64,format:string"`     // List of field names.
	}

	// Global map to store the raw input types found in codebases or test files that need mapping (for testing).
	inputTypeMapRawGlobalStore map[string]struct {
		TypeName string `json:"type_name"`       // Human-readable type name (e.g., "User", "Product").
		Field    []string `json:"fields,omitempty" jsonschema:"required,min=1,max=64,format:string"`     // List of field names.
	}

	var loader *loader

// GetRawInput returns the raw input string provided by the user or system context (e.g., a JSON payload).
func (g AbstractDataTypeGenerator) GetRawInput() string {
	return "raw_input_string_for_testing"
}

// ValidateAndFormat validates and formats an abstract data type definition based on introspection.
func (a *AbstractDataTypeGenerator) ValidateAndFormat(raw input []byte) ([]string, error) {
	if raw == nil || len(raw) == 0 {
		return nil, fmt.Errorf("invalid or empty input")
	}

	var types []struct {
		Name     string   `json:"name"`              // The canonical identifier used for introspection.
		TypeName string     `json:"type_name,omitempty" jsonschema:"required,min=1,max=64,format:string"`    // Human-readable type name (e.g., "User", "Product").
		Constructor func(string) ([]byte, error)   // The actual function to generate the struct from.
	}

	var errors
