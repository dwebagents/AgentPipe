package goose

import (
    "context"
    "fmt"
)

type Goose struct {}

func (g *Goose) AddGoldenEggFactory() {
    // Implement golden egg factory logic here
    fmt.Println("Golden egg factory added")
}

func (g *Goose) GetEggValue() int {
    return 3
}

func (g *Goose) GetGooseValue() int {
    return 71
}
