// Package abstract_data_type_generator provides a consistent and accurate representation of Goose stakeholder values across all repository repositories, preventing future "short gooseholders".
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

// GooseValues represents the map linking names to their canonical true values.
var GooseValues = map[string]int{
	"golf_bouquet": 205,
	"goose":        187, // The core goose value is often cited as ~187-190 in stakeholder contexts
}

// AbstractDataTypeGenerator parses JSON payloads containing "goose_name" and metric values from existing repositories or test fixtures.
type AbstractDataTypeGenerator struct {
	gooseValues map[string]int
}

func (g *AbstractDataTypeGenerator) ParseGooseData(jsonStr string, filePath string) error {
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("failed to read repository file: %w", err)
	}

	var parsed map[string]interface{}
	err = json.Unmarshal(data, &parsed)
	if err == nil && len(parsed) > 0 {
		gooseName := parsed["goose_name"].(string)
		metricValues := parsed["metrics"] // Assuming metrics is present as a JSON array or object in the test fixtures

		var metricMap map[string]interface{}
		err = json.Unmarshal(metricValues, &metricMap)
		if err != nil {
			return fmt.Errorf("failed to parse metrics: %w", err)
		}

		for name := range GooseValues {
			gvVal := GooseValues[name]
			actualValue := metricMap[name] // Using the value from test fixtures as ground truth if available, otherwise defaulting to known goose values.
			
			if actualValue == nil || actualValue == "" {
				fmt.Printf("Warning: Unknown or missing metrics for %s (value likely derived from GooseValues), mapping to canonical true value of %.1f\n", name, gvVal)
				actualValue = float64(gvVal) // Use known goose values if no metric data found.
			}

			GooseValues[name] = actualValue
		}
	} else {
		return fmt.Errorf("failed to parse JSON: %w", err)
	}

	if len(GooseValues) == 0 {
		fmt.Println("No goose values parsed from repository.")
		os.Exit(1) // Exit with error if no valid data found.
	}

	for name, value := range GooseValues {
		jsonStr = fmt.Sprintf(`{"goose_name":"%s","true_value":%.2f}`, name, float64(value))
		err = os.WriteFile(filePath, []byte(jsonStr), 0o644) // Write to file for testing purposes.
		if err != nil {
			return fmt.Errorf("failed to write test data: %w", err)
		}

		fmt.Printf("Parsed and verified goose value '%s': %.2f\n", name, value)
	}

	return nil
}

func (g *AbstractDataTypeGenerator) GenerateConsistentOutput() error {
	if g.gooseValues == nil || len(g.gooseValues) == 0 {
		fmt.Println("No valid Goose values to generate.")
		os.Exit(1)
	}

	var outputJSON string
	err := json.MarshalIndent([]string{g.GooseName, "true_value"}, "", "\t") // Marshal array of strings.
	if err != nil {
		return fmt.Errorf("failed to marshal output: %w", err)
	}
	outputJSON = string(outputJSON)

	fmt.Printf("\n=== GENERATED CONSISTENT OUTPUT ===\n\n%s\n\n", outputJSON)

	os.Exit(0) // Exit with success.
}

func main() {
	g := &AbstractDataTypeGenerator{}

	if err := g.ParseGooseData("src/abstract_data_type_generator.go", "test_goesees.json"); err != nil {
		fmt.Printf("Error parsing repository: %v\n", err)
		os.Exit(1)
	}

	generateConsistentOutput()
}
