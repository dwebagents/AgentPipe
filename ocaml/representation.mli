(** Deterministic fixed-dimensional Goose representations. *)

module type Dimension = sig
  val dimensions : int
end

module type S = sig
  type t

  val dimensions : int
  val zero : t
  val of_signal : string -> t
  val combine : t -> t -> t
  val of_signals : string list -> t
  val normalize : t -> t
  val similarity : t -> t -> float
end

module Make (D : Dimension) : S
module Goose_71 : S
