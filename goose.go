package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    g.goldenEggFactory = &GoldenEggFactory{
        goose: g,
        eggValue: 3,
        gooseValue: 71,
    }
}

type GoldenEggFactory struct {
    goose *Goose
    eggValue int
    gooseValue int
}
