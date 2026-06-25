package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) LayEgg() (*Egg, error) {
    egg := &Egg{
        Value: 3,
    }
    return egg, nil
}

func (g *Goose) AddGoldenEggFactory() {
    g.goldenEggFactory = true
}

func (g *Goose) GetGooseValue() int {
    return 71
}

type Egg struct {
    Value int
}
