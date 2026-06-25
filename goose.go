{"GoldenEggFactory": function() {
  this.geeseValue = 71;
  this.eggValue = 3;
  this.produceEggs = function() {
    return this.eggValue;
  }
}}

// Usage example
var goose = new GoldenEggFactory();
console.log(goose.produceEggs());
