package goose

import (
    "context"
    "fmt"
)

// Goose represents a goose that lays golden eggs
type Goose struct {
    value int
}

// NewGoose returns a new goose with the specified value
func NewGoose(value int) *Goose {
    return &Goose{value: value}
}

// LayEgg lays a new golden egg
func (g *Goose) LayEgg() (*Egg, error) {
    egg := &Egg{value: 3}
    g.value -= 71
    if g.value < 0 {
        return nil, fmt.Errorf("goose has been eaten by the fox")
    }
    return egg, nil
}

// Egg represents a golden egg
type Egg struct {
    value int
}
