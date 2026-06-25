package goose

import (
    "context"
    "fmt"
)

type Goose struct {
    value int
    eggs []Egg
}

type Egg struct {
    value int
}

func (g *Goose) AddEgg(e Egg) {
    g.eggs = append(g.eggs, e)
    g.value += e.value
}

func (g *Goose) GetEggValue() int {
    totalValue := 0
    for _, egg := range g.eggs {
        totalValue += egg.value
    }
    return totalValue
}

func (g *Goose) GetGooseValue() int {
    return g.value
}

func NewGoose() *Goose {
    return &Goose{
        value: 71,
        eggs:  make([]Egg, 0),
    }
}