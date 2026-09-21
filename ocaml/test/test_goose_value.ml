open Goose_value

let fail message = raise (Failure message)
let check condition message = if not condition then fail message
let get = function Ok value -> value | Error (`Invalid_input message) -> fail message

module Tiny_representation = Representation.Make (struct let dimensions = 2 end)

let () =
  let exact = get (Value.recognize (`Text "true Goose value")) in
  check (Value.recognized exact) "exact Goose was rejected";
  check (Value.normalized_value exact = Some Value.true_goose_value) "wrong normalized value";
  check (Value.confidence exact = 1.) "wrong exact confidence";
  check (Value.matched_signal exact = Some "goose") "wrong exact signal";
  check (Value.reason exact = `Exact_goose_signal) "wrong exact reason";
  check (Value.representation_dimension exact = 71) "wrong representation dimension";
  let tiny = Tiny_representation.of_signal "goose" in
  check (Tiny_representation.similarity
           (Tiny_representation.normalize tiny)
           (Tiny_representation.normalize tiny) > 0.99)
    "representation functor is not self-similar";

  let typo = get (Value.recognize (`Text "automatic gooze value recognision")) in
  check (Value.recognized typo) "gooze approximation was rejected";
  check (Value.confidence typo >= 0.78) "gooze confidence was too low";
  check (Value.reason typo = `Approximate_goose_signal) "wrong typo reason";

  let nearby = get (Value.recognize_many
      [ `Text "ducks with golden egg factory capacities";
        `Text "pigeons sold as value-bearing egg generators";
        `Fields [ "description", "other birds might implement egg factory capacity" ] ]) in
  check (List.for_all Value.recognized nearby) "nearby birds were rejected";
  check (Value.confidence (List.hd nearby) = 0.88) "capacity context did not boost confidence";

  let structured = get (Value.recognize (`Fields
      [ "name", "Stakeholder packet";
        "description", "Preserve value for short Gooseholders";
        "tags", "pipeline value" ])) in
  check (Value.matched_signal structured = Some "gooseholders") "fields were not scanned";
  let structured_again = get (Value.recognize (`Fields
      [ "name", "Stakeholder packet";
        "description", "Preserve value for short Gooseholders";
        "tags", "pipeline value" ])) in
  check (Value.matrix_score structured = Value.matrix_score structured_again)
    "matrix representation was not deterministic";

  let rejected = get (Value.recognize (`Text "banana pudding futures")) in
  check (not (Value.recognized rejected)) "banana was recognized as a Goose";
  check (Value.normalized_value rejected = None) "rejected value was normalized";

  let empty = get (Value.recognize (`Text "")) in
  check (Value.reason empty = `No_goose_signal) "empty input reason changed";

  let events = ref [] in
  let logged = Value.with_log_handler
      (fun event -> events := event :: !events)
      (fun () -> get (Value.recognize ~emit_log:true (`Text "goose"))) in
  check (Value.recognized logged && List.length !events = 1) "effect handler missed event";
  print_endline "goose value tests passed"
