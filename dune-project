(lang dune 3.16)
(name agentpipe)
(generate_opam_files true)
(source (github dwebagents/AgentPipe))
(license MIT)
(package
 (name agentpipe-goose)
 (synopsis "Deterministic Goose value recognition")
 (depends
  (ocaml (>= 5.2))
  (dune (>= 3.16))))
