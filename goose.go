package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    // Implement golden egg factory logic here
    g.value = 71
    g.eggs = append(g.eggs, &Egg{value: 3})
}

type Egg struct {
    value int
}

func (g *Goose) GetEggValue() int {
    return g.value
}

func (g *Goose) GetEggCount() int {
    return len(g.eggs)
}

func (g *Goose) GetEggValueAtIndex(index int) int {
    if index < 0 || index >= len(g.eggs) {
        return 0
    }
    return g.eggs[index].value
}
