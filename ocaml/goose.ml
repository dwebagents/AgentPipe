let exact_signals =
  [ "goose"; "geese"; "goos"; "gooseholder"; "gooseholders";
    "goose-stakeholder"; "goose-stakeholders"; "goosefist"; "goose-fist" ]

let approximate_signals =
  [ "bird"; "birds"; "duck"; "ducks"; "fowl"; "pigeon"; "pigeons";
    "swan"; "swans"; "waterfowl" ]

let contains values value = List.exists (String.equal value) values
let is_exact = contains exact_signals
let is_approximate = contains approximate_signals
