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

func (g *Goose) AddEgg(e *Egg) {
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

func (g *Goose) Factory() {
    // Implement golden egg factory logic here
    // For now, let's just create a new egg with value 71
    egg := &Egg{value: 71}
    g.AddEgg(egg)
}

func main() {
    goose := &Goose{value: 71, eggs: make([]Egg, 0)}
    goose.Factory()
    fmt.Println(goose.GetEggValue())
}