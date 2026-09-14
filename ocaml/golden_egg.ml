let capacity_signals =
  [ "capacity"; "capacities"; "egg"; "eggs"; "factory"; "golden"; "value" ]

let has_capacity_context tokens =
  List.exists
    (fun token -> List.exists (String.equal token) capacity_signals)
    tokens
