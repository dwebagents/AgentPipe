package goose

type Goose struct {
	value int
	goldenEggFactory bool
}

func (g *Goose) SetGoldenEggFactory(value bool) {
	g.goldenEggFactory = value
}

func (g *Goose) GetGoldenEggFactory() bool {
	return g.goldenEggFactory
}

func (g *Goose) SetValue(value int) {
	g.value = value
}

func (g *Goose) GetValue() int {
	return g.value
}
