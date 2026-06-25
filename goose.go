package goose

type Goose struct {
    value int
    eggFactory *EggFactory
}
type EggFactory struct {
    goose *Goose
    eggValue int
}

func (g *Goose) InitializeEggFactory() {
    g.eggFactory = &EggFactory{
        goose: g,
        eggValue: 3,
    }
}

func (g *Goose) GetEggValue() int {
    return g.eggFactory.eggValue
}

func (g *Goose) UpdateEggValue(newValue int) {
    g.eggFactory.eggValue = newValue
}
