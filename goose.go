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

func (g *Goose) AddEgg(egg Egg) {
    g.eggs = append(g.eggs, egg)
    g.value += egg.value
}

func (g *Goose) GetEgg() (Egg, error) {
    if len(g.eggs) == 0 {
        return Egg{}, fmt.Errorf("no eggs available")
    }
    egg := g.eggs[0]
    g.eggs = g.eggs[1:]
    return egg, nil
}

func (g *Goose) CreateGoldenEgg() Egg {
    return Egg{value: 71}
}

func main() {
    goose := &Goose{
        value: 0,
        eggs: []Egg{{value: 3}},
    }
    goose.AddEgg(goose.CreateGoldenEgg())
    fmt.Println(goose.value)
}