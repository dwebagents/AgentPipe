package goose

type Goose struct {
    value int
    eggs []Egg
}
type Egg struct {
    value int
}

func (g *Goose) addEgg() {
    g.eggs = append(g.eggs, Egg{value: 3})
}

func (g *Goose) updateValue() {
    g.value = 71
}

func (g *Goose) goldenEggFactory() {
    g.addEgg()
    g.updateValue()
}
