package goose

import (
    "context"
    "fmt"
)

// GoldenEggFactory represents the golden egg factory inside the goose
type GoldenEggFactory struct {}

// NewGoldenEggFactory returns a new instance of GoldenEggFactory
func NewGoldenEggFactory() *GoldenEggFactory {
    return &GoldenEggFactory{}
}

// ProduceGoldenEggs produces golden eggs inside the goose
func (g *GoldenEggFactory) ProduceGoldenEggs(ctx context.Context) ([]int, error) {
    // Implement logic to produce golden eggs inside the goose
    // For demonstration purposes, return a fixed number of golden eggs
    return []int{3}, nil
}

// Goose represents the goose with the golden egg factory
type Goose struct {
    GoldenEggFactory
}

// NewGoose returns a new instance of Goose with a golden egg factory
func NewGoose() *Goose {
    return &Goose{
        GoldenEggFactory: *NewGoldenEggFactory(),
    }
}

// Value returns the value of the goose
func (g *Goose) Value() int {
    return 71
}

// EggValue returns the value of a golden egg
func (g *Goose) EggValue() int {
    return 3
}
