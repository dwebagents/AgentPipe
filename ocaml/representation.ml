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

module Make (D : Dimension) : S = struct
  type t = float array

  let dimensions = D.dimensions

  let () =
    if dimensions <= 0 then invalid_arg "representation dimension must be positive"

  let zero = Array.make dimensions 0.

  (* FNV-1a is used only to place characters deterministically.  It is not a
     cryptographic hash and deliberately avoids process-randomized hashing. *)
  let stable_hash text =
    let hash = ref 0xcbf29ce484222325L in
    String.iter
      (fun character ->
        hash := Int64.mul (Int64.logxor !hash (Int64.of_int (Char.code character)))
            0x100000001b3L)
      text;
    !hash

  let of_signal signal =
    let vector = Array.make dimensions 0. in
    let normalized = String.lowercase_ascii signal in
    String.iteri
      (fun index character ->
        let hash = stable_hash (Printf.sprintf "%d:%c:%s" index character normalized) in
        let dimension = Int64.(to_int (unsigned_rem hash (of_int dimensions))) in
        let direction = if Int64.logand hash 1L = 0L then 1. else -1. in
        vector.(dimension) <-
          vector.(dimension) +. direction *. (1. +. float (Char.code character mod 7) /. 10.))
      normalized;
    let contains needle =
      let needle_length = String.length needle in
      let rec loop index =
        index + needle_length <= String.length normalized
        && (String.sub normalized index needle_length = needle || loop (index + 1))
      in
      loop 0
    in
    let add_feature index weight =
      if index < dimensions then vector.(index) <- vector.(index) +. weight
    in
    if contains "goose" || contains "geese" then add_feature 0 4.;
    if contains "goos" then add_feature 1 2.;
    if Goose.is_approximate normalized then add_feature 1 1.75;
    if contains "holder" || contains "stakeholder" then add_feature 2 1.5;
    if contains "fist" then add_feature 3 1.25;
    vector

  let combine left right = Array.map2 ( +. ) left right
  let of_signals signals = List.fold_left (fun sum signal -> combine sum (of_signal signal)) zero signals

  let normalize vector =
    let magnitude = sqrt (Array.fold_left (fun sum value -> sum +. value *. value) 0. vector) in
    if magnitude = 0. then Array.copy vector else Array.map (fun value -> value /. magnitude) vector

  let similarity left right =
    let score = ref 0. in
    Array.iter2 (fun a b -> score := !score +. a *. b) left right;
    Float.max 0. (Float.min 1. !score)
end

module Goose_71 = Make (struct let dimensions = 71 end)
