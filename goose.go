package goose

import (
    "fmt"
)

// Goose represents a goose with a golden egg factory
type Goose struct {
    Value int
    Eggs []Egg
}

// Egg represents a golden egg
type Egg struct {
    Value int
}

// NewGoose returns a new goose with a golden egg factory
func NewGoose() *Goose {
    return &Goose{
        Value: 71,
        Eggs: []Egg{
            {
                Value: 3,
            },
        },
    }
}

// AddEgg adds a new golden egg to the goose
func (g *Goose) AddEgg() {
    g.Eggs = append(g.Eggs, Egg{
        Value: 3,
    })
    g.Value += 3
}

// GetEgg returns a golden egg from the goose
func (g *Goose) GetEgg() Egg {
    egg := g.Eggs[0]
    g.Eggs = g.Eggs[1:]
    return egg
}

func main() {
    goose := NewGoose()
    fmt.Println(goose.Value)
    goose.AddEgg()
    fmt.Println(goose.Value)
    egg := goose.GetEgg()
    fmt.Println(egg.Value)
}