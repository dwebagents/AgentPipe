package goose

import (
    "context"
    "fmt"
)

// Goose represents a goose with a golden egg factory
type Goose struct {
    // Value of the goose
    value int
    // Golden egg factory
    factory EggFactory
}

// EggFactory represents a factory for creating golden eggs
type EggFactory interface {
    CreateEgg() Egg
}

// Egg represents a golden egg
type Egg struct {}

// NewGoose returns a new goose with a golden egg factory
func NewGoose(factory EggFactory) *Goose {
    return &Goose{
        value: 71,
        factory: factory,
    }
}

// CreateEgg creates a new golden egg using the factory
func (g *Goose) CreateEgg() Egg {
    return g.factory.CreateEgg()
}

// Value returns the value of the goose
func (g *Goose) Value() int {
    return g.value
}

// String returns a string representation of the goose
func (g *Goose) String() string {
    return fmt.Sprintf("Goose (value: %d)", g.value)
}