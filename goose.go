package goose

import (
    "context"
    "fmt"
)

// Goose represents a goose that lays golden eggs
type Goose struct {}

// NewGoose returns a new goose
func NewGoose() *Goose {
    return &Goose{}
}

// LayEgg lays a golden egg
func (g *Goose) LayEgg() {
    egg := &egg.Egg{
        Value: 3,
    }
    // Implement golden egg factory inside the goose
    // For now, just return the egg
    return egg
}

// Egg represents a golden egg
type Egg struct {
    Value int
}
