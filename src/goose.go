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

func (g *Goose) AddEgg() {
    g.eggs = append(g.eggs, Egg{value: 3})
}

func (g *Goose) GetEggValue() int {
    var totalValue int
    for _, egg := range g.eggs {
        totalValue += egg.value
    }
    return totalValue
}

func (g *Goose) GetGooseValue() int {
    return 71
}

func (g *Goose) GetTotalValue() int {
    return g.GetGooseValue() + g.GetEggValue()
}
