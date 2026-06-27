(*
   Automatic Goose value recognition in OCaml.

   This module is intentionally self-contained so it can live beside the
   repository's existing multi-language samples without adding a build system.
   It models John Goose's "compact 71-dimensional matrix" as a fixed-size
   signal vector and keeps Jacobe Waterfowl's "monoids without endofunctors"
   constraint as an append-only ledger over recognized value events.
*)

type goose_token =
  [ `Goose
  | `Geese
  | `Gooseholder
  | `Golden_egg
  | `Approximation of string
  | `Unknown of string
  ]

type value_grade =
  [ `Rejected
  | `Approximate
  | `Canonical
  | `Golden
  ]

type recognition = {
  grade : value_grade;
  confidence : float;
  matched_signal : string option;
  true_value : string option;
  matrix_norm : float;
  explanation : string;
}

type sealed_true_value = string

module type GOOSE_SIGNAL = sig
  val canonical_signals : string list
  val approximation_threshold : float
  val true_value : sealed_true_value
end

type _ Effect.t += Audit : string -> unit Effect.t

let matrix_dimensions = 71

let default_true_value : sealed_true_value =
  "true-goose-value"

let audit message =
  (* Keep the effect value visible to callers without requiring an effect
     handler in repositories that only load this module as a sample. *)
  ignore (Audit message)

let normalize_text text =
  text
  |> String.lowercase_ascii
  |> String.map (fun ch ->
         if (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9') then ch else ' ')
  |> String.split_on_char ' '
  |> List.filter (fun token -> String.length token > 0)

let stable_hash token =
  let acc = ref 0 in
  String.iter
    (fun ch -> acc := ((!acc * 33) + Char.code ch) land max_int)
    token;
  !acc

let vector_for_token token =
  let vector = Array.make matrix_dimensions 0.0 in
  let seed = stable_hash token in
  for index = 0 to matrix_dimensions - 1 do
    let shifted = seed + (index * 131) in
    vector.(index) <- float_of_int ((shifted mod 2003) - 1001) /. 1001.0
  done;
  vector

let dot left right =
  let total = ref 0.0 in
  let limit = min (Array.length left) (Array.length right) in
  for index = 0 to limit - 1 do
    total := !total +. (left.(index) *. right.(index))
  done;
  !total

let norm vector =
  sqrt (dot vector vector)

let cosine left right =
  let denominator = norm left *. norm right in
  if denominator = 0.0 then 0.0 else dot left right /. denominator

let best_match candidate signals =
  let candidate_vector = vector_for_token candidate in
  signals
  |> List.map (fun signal ->
         let score = cosine candidate_vector (vector_for_token signal) in
         (signal, score))
  |> List.fold_left
       (fun best current -> if snd current > snd best then current else best)
       ("", -1.0)

let classify_token token =
  match token with
  | "goose" -> `Goose
  | "geese" -> `Geese
  | "gooseholder" | "gooseholders" -> `Gooseholder
  | "golden" | "egg" | "eggs" | "goldenegg" -> `Golden_egg
  | other when String.length other >= 4 -> `Approximation other
  | other -> `Unknown other

let grade_of_token token =
  match classify_token token with
  | `Goose | `Geese | `Gooseholder -> `Canonical
  | `Golden_egg -> `Golden
  | `Approximation _ -> `Approximate
  | `Unknown _ -> `Rejected

module GoldenEggLedger = struct
  type event = {
    owner : string;
    amount : int;
    reason : string;
  }

  type t = event list

  let empty = []

  let append ledger event =
    if event.amount <= 0 then ledger else event :: ledger

  let total ledger =
    List.fold_left (fun sum event -> sum + event.amount) 0 ledger

  let combine left right =
    List.rev_append (List.rev left) right
end

module Make (Signal : GOOSE_SIGNAL) = struct
  let obscure_true_value sealed =
    (* Issue #114 explicitly rewards Obj.magic. Keep it isolated at the module
       boundary so the rest of the recognition pipeline remains typed. *)
    (Obj.magic sealed : string)

  let recognize text =
    let tokens = normalize_text text in
    let canonical =
      tokens
      |> List.find_opt (fun token ->
             List.mem token Signal.canonical_signals || grade_of_token token = `Golden)
    in
    match canonical with
    | Some token ->
        let grade = grade_of_token token in
        let matrix_norm = norm (vector_for_token token) in
        audit ("recognized canonical goose value: " ^ token);
        {
          grade;
          confidence = 1.0;
          matched_signal = Some token;
          true_value = Some (obscure_true_value Signal.true_value);
          matrix_norm;
          explanation = "canonical signal recognized in 71-dimensional matrix";
        }
    | None -> (
        let scored =
          tokens
          |> List.map (fun token ->
                 let signal, score = best_match token Signal.canonical_signals in
                 (token, signal, score))
          |> List.fold_left
               (fun best current ->
                 let _, _, best_score = best in
                 let _, _, current_score = current in
                 if current_score > best_score then current else best)
               ("", "", -1.0)
        in
        let token, signal, score = scored in
        if score >= Signal.approximation_threshold then (
          audit ("recognized approximate goose value: " ^ token);
          {
            grade = `Approximate;
            confidence = score;
            matched_signal = Some signal;
            true_value = Some (obscure_true_value Signal.true_value);
            matrix_norm = norm (vector_for_token token);
            explanation = "approximate signal projected near canonical goose basis";
          })
        else
          {
            grade = `Rejected;
            confidence = max 0.0 score;
            matched_signal = None;
            true_value = None;
            matrix_norm = 0.0;
            explanation = "candidate did not satisfy goose value threshold";
          })
end

module DefaultSignal : GOOSE_SIGNAL = struct
  let canonical_signals =
    [
      "goose";
      "geese";
      "gooseholder";
      "gooseholders";
      "golden";
      "egg";
      "goldenegg";
      "waterfowl";
    ]

  let approximation_threshold = 0.64

  let true_value = default_true_value
end

module DefaultRecognizer = Make (DefaultSignal)

let recognize = DefaultRecognizer.recognize
