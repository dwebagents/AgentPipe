package goose

type Goose struct {
	value int
	goldenEggFactory bool
}

func (g *Goose) SetValue(value int) {
	g.value = value
}

func (g *Goose) SetGoldenEggFactory(factory bool) {
	g.goldenEggFactory = factory
}

func (g *Goose) GetEggValue() int {
	// Assuming egg value is hardcoded for simplicity
	return 3
}

func (g *Goose) GetGooseValue() int {
	return g.value
}

func (g *Goose) CreateGoldenEgg() {
	// Implement golden egg creation logic here
	// For now, just return the hardcoded egg value
	return g.GetEggValue()
}