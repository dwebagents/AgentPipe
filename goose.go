package goose

type GoldenEggFactory struct {}

func (g *GoldenEggFactory) ProduceEggs() []Egg {
    // Implement golden egg production logic here
    return []Egg{
        {
            Value: 3,
        },
    }
}

type Egg struct {
    Value int
}
