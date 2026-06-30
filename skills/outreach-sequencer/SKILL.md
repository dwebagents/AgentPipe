---
name: outreach-sequencer
description: Sequence a governed outreach campaign from lead enrichment through consent check, qualification, governed send, and receipt seal. Exactly one path executes per lead.
runx:
  category: growth
---

# Outreach Sequencer

Not every lead is ready to hear from you, and sending to the wrong person at the
wrong time is how lists die. `outreach-sequencer` takes a lead from raw signals
to a sealed outreach run — or to a clean hold — through one governed chain. Each
hop is a real catalog skill with its own scope, and the receipt records which
path executed and why.

The skill composes five existing skills into one auditable sequence:

1. `lead-enrichment` hydrates the lead from supplied signals and produces a
   reviewable enrichment packet.
2. `list-hygiene-judge` checks the contact's consent state and writes exactly one
   transition if the contact is suppressible or needs re-permissioning.
3. an agent qualify step decides the route: `reach_out`, `nurture`, or `hold`,
   with rationale.
4. the matching branch executes: for `reach_out` it drafts copy, scrubs PII,
   holds for human approval, and plans the send; for `nurture` it plans a
   governed nurture handoff; for `hold` it records the hold and sends nothing.
5. `sign-receipt` seals the run so the enrichment, hygiene decision, route, and
   action (or hold) are all bound into one receipt.

Authority narrows at every hop. Enrichment reads signals only, hygiene reads and
writes consent state, the qualify step decides the route, the send branch
carries its own approval gate, and the seal may only append to the ledger.

## What this skill does

`outreach-sequencer` is a graph, not a single agent step. It is the outreach
equivalent of `governed-outbound`: a chain where order matters and no step can
be skipped to make the send faster.

1. `enrich` reads the lead and supplied signals and returns an enrichment packet
   with a fit assessment and recommended next action.
2. `hygiene` reads the contact's engagement history, bounce record, and current
   consent state, then writes exactly one transition event or stops without
   writing.
3. `qualify` reads the enrichment and hygiene outputs and emits a `route`:
   `reach_out`, `nurture`, or `hold`, with rationale.
4. `when route == reach_out`, the branch:
   a. `draft` builds outreach copy scoped to the enriched lead profile.
   b. `scrub` redacts any PII in the draft before it crosses the boundary.
   c. `approve` holds for a human, who sees the redaction verdict and the
      residual risk.
   d. `send` plans delivery via `send-as` with `send_class: outreach` and the
      approval gate enforced.
5. `when route == nurture`, the branch plans a governed nurture campaign handoff
   via `send-as` with `send_class: nurture`.
6. `when route == hold`, the branch records the hold with rationale and sends
   nothing.
7. `seal` attests the run, binding the enrichment packet, hygiene decision,
   qualification, and the single branch action (or hold record) as evidence.

Exactly one branch runs. The unselected branches are skipped, not blocked. The
receipt records the route, the rationale, and the one action taken.

## When to use this skill

- A lead needs consistent, governed enrichment-then-act treatment rather than an
  ad-hoc judgment call.
- You want the consent check, the route decision, and the reason on the receipt,
  not buried in a prompt.
- Outreach, nurture, and do-not-contact are all real outcomes the workflow must
  choose between.
- You need proof after the fact that a lead was enriched, checked for consent,
  routed, and acted on (or held) under governed authority.

## When not to use this skill

- To send the same message to everyone. That is a campaign; route through
  `send-as` directly with the configured provider adapter.
- To draft copy only. Use a drafting skill; this skill decides, routes, and
  sequences.
- To contact a lead with no consent basis. The `hold` route exists for exactly
  that case.
- To enrich a lead without intent to act. Use `lead-enrichment` directly.

## How the chain is wired

- `enrich` produces `enrichment_packet` with `fit_assessment`, `recommended_action`,
  and `risk_flags`.
- `hygiene` produces `hygiene_decision` with `decision.state`
  (`active` / `re_permission` / `suppress` / `stop`) and `recorded_transition`.
- `qualify` reads both outputs and emits `route` (`reach_out` / `nurture` /
  `hold`), `rationale`, and `segment`.
- each branch declares `when: { field: qualify.route, equals: <route> }`; a
  branch whose route does not match is skipped.
- `reach_out` branch runs `draft` → `scrub` → `approve` → `send` → continues to seal.
- `nurture` branch runs `plan-nurture` → continues to seal.
- `hold` branch runs `record-hold` → continues to seal.
- `seal` attests the run, binding all prior step outputs as evidence refs.

## Edge cases and stop conditions

- **No `lead` or `signals`:** the run returns `needs_agent`; there is nothing to
  enrich.
- **Hygiene returns `active_unsubscribe_marker`:** the qualify step should route
  to `hold`; outreach is never sent to an unsubscribed contact.
- **Hygiene returns `stale_expected_version`:** the run stops with
  `stale_expected_version`; the pipeline must reload the contact stream and
  retry with the correct version.
- **Hygiene returns `suppress`:** the qualify step should route to `hold`; no
  outreach is sent.
- **An ambiguous qualification:** `qualify` should route to `hold` rather than
  guess; a hold is a clean, recorded outcome, not a failure.
- **Redaction not `ready`:** a `needs_review` or `blocked` verdict fails the
  send transition; `send` never runs. Nothing leaves the boundary on a hold
  verdict.
- **Approval denied or absent:** the send transition is not satisfied; the branch
  stops at the gate. The receipt shows the route was chosen but the send was not
  authorized.
- **Send fails downstream:** the seal still records the attempt and its blocker,
  so the receipt shows what happened.

## Output

The run seals to `runx.receipt.v1`. The receipt links each step's packet:
`enrichment_packet` (lead profile + fit assessment), `hygiene_decision`
(consent state + transition), `qualify` (the route and rationale), and the
single branch action (`send_plan`, `nurture_plan`, or `hold_record`). The
branches that did not match are recorded as skipped, so the receipt proves both
the decision and the one action taken.

## Inputs

- `lead` (required): lead identity and known account fields.
- `signals` (required): engagement, product, CRM, or firmographic signals.
- `principal` (required): principal the outreach or nurture is sent as.
- `objective` (optional): what the outreach should accomplish.
- `operator_context` (optional): compliance, consent posture, campaign
  constraints, or channel guidance.
- `constraints` (optional): allowed channels, region, opt-in, or do-not-contact
  flags.
