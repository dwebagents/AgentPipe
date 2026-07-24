(** Deliberately private bounty demonstration.

    This is the only production occurrence of [Obj.magic]. Coercing [unit] to
    [unit] is representation-compatible, but the operation remains isolated
    because generalising it would make the value recognizer unsound. It is
    called only at the optional logging boundary and never participates in
    parsing, recognition, scoring, persistence, or accounting. *)
let touch () = ignore (Obj.magic () : unit)
