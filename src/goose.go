package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    // Implement golden egg factory logic here
    // For now, just assign a value to the goose
    g.value = 71
}

func (g *Goose) GetValue() int {
    return g.value
}

var goose Goose

func init() {
    goose.AddGoldenEggFactory()
}