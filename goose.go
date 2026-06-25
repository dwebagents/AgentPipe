package goose

import (
    "context"
    "fmt"
)

type Goose struct {
    // ... existing fields ...
    goldenEggFactory bool
}

func (g *Goose) InitializeGoldenEggFactory() {
    g.goldenEggFactory = true
}

func (g *Goose) GetEggValue() int {
    if g.goldenEggFactory {
        return 74
    }
    return 3
}

func (g *Goose) GetGooseValue() int {
    return 71
}
