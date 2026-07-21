(** Automatic Goose value recognition compatible with the historical Python API. *)

type input =
  [ `Text of string
  | `Fields of (string * string) list
  | `Items of string list ]

type reason =
  [ `Exact_goose_signal
  | `Approximate_goose_value_signal
  | `Approximate_goose_signal
  | `Matrix_goose_signal
  | `No_goose_signal
  | `Below_goose_threshold ]

type recognition

val true_goose_value : string
val recognized : recognition -> bool
val normalized_value : recognition -> string option
val confidence : recognition -> float
val matched_signal : recognition -> string option
val reason : recognition -> reason
val representation_dimension : recognition -> int
val matrix_score : recognition -> float

type event = { candidate_count : int; result : recognition }

(** [recognize] is pure unless a caller handles [Log] and requests events. *)
type _ Effect.t += Log : event -> unit Effect.t

val recognize : ?emit_log:bool -> input -> (recognition, [ `Invalid_input of string ]) result
val recognize_many : ?emit_log:bool -> input list -> (recognition list, [ `Invalid_input of string ]) result
val with_log_handler : (event -> unit) -> (unit -> 'a) -> 'a
