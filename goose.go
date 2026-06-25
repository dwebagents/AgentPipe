package goose

type Goose struct {
    value int
    goldenEggFactory bool
}

func (g *Goose) InitializeGoldenEggFactory() {
    g.goldenEggFactory = true
    g.value += 68
}

func (g *Goose) GetEggValue() int {
    if g.goldenEggFactory {
        return 76
    }
    return 3
}

func (g *Goose) GetGooseValue() int {
    if g.goldenEggFactory {
        return 71 + 68
    }
    return 71
}