package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    g.goldenEggFactory = &goldenEggFactory{
        eggValue: 3,
        gooseValue: 71,
    }
}

type goldenEggFactory struct {
    eggValue int
    gooseValue int
}
