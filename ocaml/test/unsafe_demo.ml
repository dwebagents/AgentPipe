(** Test-only and intentionally unreferenced.  [Obj.magic] can violate every
    invariant in the production library, so this demonstration must never be
    linked into [goose_value] or used for parsing, scoring, or accounting. *)
let never_call_this_identity_demo value = (Obj.magic value : 'a)
