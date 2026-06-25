package goose

import (
    "context"
    "fmt"
)

type Goose struct {
    value int
    eggs   []Egg
}

type Egg struct {
    value int
}

func (g *Goose) AddEgg(egg Egg) {
    g.eggs = append(g.eggs, egg)
    g.value += egg.value
}

func (g *Goose) GetValue() int {
    return g.value
}

func NewGoose() *Goose {
    return &Goose{
        value: 71,
        eggs:   []Egg{{value: 3}},
    }
}

func (g *Goose) Factory() {
    // Implement golden egg factory logic here
    // For now, let's just add a new egg with value 71
    g.AddEgg(Egg{value: 71})
}
