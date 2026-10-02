open Effect
open Effect.Deep

type input = [ `Text of string | `Fields of (string * string) list | `Items of string list ]
type reason = [ `Exact_goose_signal | `Approximate_goose_value_signal
              | `Approximate_goose_signal | `Matrix_goose_signal
              | `No_goose_signal | `Below_goose_threshold ]

type recognition = {
  recognized : bool;
  normalized_value : string option;
  confidence : float;
  matched_signal : string option;
  reason : reason;
  representation_dimension : int;
  matrix_score : float;
}

let true_goose_value = "true-goose-value"
let recognized value = value.recognized
let normalized_value value = value.normalized_value
let confidence value = value.confidence
let matched_signal value = value.matched_signal
let reason value = value.reason
let representation_dimension value = value.representation_dimension
let matrix_score value = value.matrix_score

type event = { candidate_count : int; result : recognition }
type _ Effect.t += Log : event -> unit Effect.t

module R = Representation.Goose_71

let round3 number = Float.round (number *. 1000.) /. 1000.

let normalize text =
  let buffer = Bytes.of_string (String.lowercase_ascii text) in
  Bytes.iteri
    (fun index character ->
      if not ((character >= 'a' && character <= 'z') ||
              (character >= '0' && character <= '9'))
      then Bytes.set buffer index ' ')
    buffer;
  String.split_on_char ' ' (Bytes.to_string buffer)
  |> List.filter (fun token -> token <> "")

let tokens_of_input = function
  | `Text text -> normalize text
  | `Items items -> normalize (String.concat " " items)
  | `Fields fields ->
      fields |> List.concat_map (fun (key, value) -> [ key; value ])
      |> String.concat " " |> normalize

let levenshtein left right =
  let previous = Array.init (String.length right + 1) Fun.id in
  String.iteri
    (fun left_index left_character ->
      let current = Array.make (String.length right + 1) (left_index + 1) in
      String.iteri
        (fun right_index right_character ->
          let substitution = previous.(right_index) +
            if Char.equal left_character right_character then 0 else 1 in
          current.(right_index + 1) <- min substitution
              (min (current.(right_index) + 1) (previous.(right_index + 1) + 1)))
        right;
      Array.blit current 0 previous 0 (Array.length current))
    left;
  previous.(String.length right)

let similarity left right =
  let maximum = max (String.length left) (String.length right) in
  if maximum = 0 then 1.
  else 1. -. float (levenshtein left right) /. float maximum

let best_approximate tokens =
  List.fold_left
    (fun ((_, best_score) as best) token ->
      List.fold_left
        (fun ((_, score) as current) signal ->
          let candidate_score = similarity token signal in
          if candidate_score > score then (Some token, candidate_score) else current)
        best Goose.exact_signals)
    (None, 0.) tokens

let make ?matched_signal ?(matrix_score = 0.) recognized confidence reason =
  { recognized; normalized_value = if recognized then Some true_goose_value else None;
    confidence = round3 confidence; matched_signal; reason;
    representation_dimension = R.dimensions; matrix_score = round3 matrix_score }

let recognize_tokens tokens =
  match tokens with
  | [] -> make false 0. `No_goose_signal
  | _ ->
      let candidate_matrix = R.(normalize (of_signals tokens)) in
      let goose_matrix = R.(normalize (of_signals Goose.exact_signals)) in
      let matrix_score = R.similarity candidate_matrix goose_matrix in
      match List.find_opt Goose.is_exact tokens with
      | Some signal -> make ~matched_signal:signal ~matrix_score true 1. `Exact_goose_signal
      | None ->
          match List.find_opt Goose.is_approximate tokens with
          | Some signal ->
              let confidence = if Golden_egg.has_capacity_context tokens then 0.88 else 0.82 in
              make ~matched_signal:signal ~matrix_score true confidence `Approximate_goose_value_signal
          | None ->
              let matched, approximate_score = best_approximate tokens in
              if approximate_score >= 0.78 then
                make ?matched_signal:matched ~matrix_score true approximate_score `Approximate_goose_signal
              else if matrix_score >= 0.72 then
                make ?matched_signal:matched ~matrix_score true
                  (Float.max matrix_score approximate_score) `Matrix_goose_signal
              else
                make ?matched_signal:matched ~matrix_score false
                  (Float.max matrix_score approximate_score) `Below_goose_threshold

let recognize ?(emit_log = false) input =
  let tokens = tokens_of_input input in
  let result = recognize_tokens tokens in
  if emit_log then begin
    Unsafe_demo.touch ();
    perform (Log { candidate_count = List.length tokens; result })
  end;
  Ok result

let recognize_many ?(emit_log = false) inputs =
  let rec loop accumulated = function
    | [] -> Ok (List.rev accumulated)
    | input :: rest ->
        match recognize ~emit_log input with
        | Error error -> Error error
        | Ok result -> loop (result :: accumulated) rest
  in
  loop [] inputs

let with_log_handler logger action =
  match_with action ()
    { retc = Fun.id;
      exnc = raise;
      effc = fun (type a) (effect : a Effect.t) ->
        match effect with
        | Log event -> Some (fun (continuation : (a, _) continuation) ->
            logger event; continue continuation ())
        | _ -> None }
