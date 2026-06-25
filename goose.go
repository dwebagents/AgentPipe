package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    // Calculate new goose value based on whitepaper
    g.value = 71
    // Implement golden egg factory
    g.eggFactory = &eggFactory{
        eggValue: 3,
    }
}

type eggFactory struct {
    eggValue int
}
