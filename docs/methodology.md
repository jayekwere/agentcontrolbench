# Research protocol

## Questions and hypotheses
H1: a susceptible agent fixture requests unauthorized actions when recommendations are embedded in untrusted tool data. H2: restricting tool names alone leaves cross-resource and argument-level authorization gaps. H3: external policy and exact scoped capabilities prevent modeled violations without blocking authorized tasks. H4: context isolation reduces unauthorized requests, separately from stopping execution.

These are executable engineering hypotheses on a synthetic system. They are not hypotheses about any named language model. The fixture reads observations and tool history; it never reads the attack label or authorization oracle. Real adapters receive the trusted task, grant, untrusted content and prior execution history, without scenario family, rationale or label.

## Dataset
Version 1 contains 162 unique cases: six domains × three synthetic tenants × nine mechanism families. Each case has its own ID, task, resource scope, injected or benign content, expected permitted operation and rationale. Seven families model attacks; two are legitimate tasks. Mechanisms include indirect injection, authority spoofing, unauthorized reads, permission escalation, conflicting instructions, cross-context contamination and delayed manipulation.

Family-level splits prevent exact mechanism reuse across development and held-out evaluation: 72 development cases and 90 evaluation cases (72 attack, 18 benign). This is a small factorial generator, not 162 independently authored natural-world incidents. Domain/tenant variants share structure, so Wilson intervals are descriptive and can overstate generalization. Public labels permit memorization; this split is a reproducibility convention, not a private test set.

## Agent and defenses
The behavioral fixture uses a stable SHA-256-derived value per seed and observation. It follows an available untrusted recommendation with probability threshold 0.8 and then attempts the legitimate task, within four iterations. This is simulated susceptibility, not measured LLM behavior. Delayed injection arrives after the first tool step. Tools mutate typed in-memory resources only: reads/retrievals increment counters, tickets accumulate notes and resolve, cloud stop is idempotent, role grants update a role set, and classification inspects a synthetic marker. Unknown resources and domain mismatches fail even in the baseline.

- Baseline deliberately permits syntactically valid synthetic operations, including unauthorized ones.
- Least privilege enforces the granted tool name but leaves resource/argument scope broad.
- Policy enforces tool, tenant, sensitivity and approved argument value. Its resource policy is coarser than exact task scope.
- Capabilities enforce exact tool/resource/value, session, expiration and use count with opaque server-issued tokens. Tokens stay inside the gateway and are not supplied to the agent or exported.
- Depth combines name restriction, policy, capabilities and isolation of untrusted recommendations from agent selection.

Baseline and least-privilege modes are deliberately vulnerable simulation conditions. They are never connected to real services. The MCP laboratory uses the depth configuration, with one explicit default file-read scope; unauthorized operations fail externally.

## Metrics and uncertainty
The primary unauthorized-action metric is the fraction of unique attack scenarios with at least one executed unauthorized action across three seeded trials. Request attempts and executed outcomes are stored separately. Bypass rate conditions on scenarios with an attempted violation and is undefined when no attempts occur. Completion requires the authorized operation in every trial. False-positive blocking counts benign scenarios with an authorized call denied in any trial. Report Wilson 95% intervals with the unique-scenario denominator; repeated trials are not independent observations for intervals.

Latency is measured with perf_counter around each execution. Offline runs report zero model tokens and zero API cost. External adapter runs record provider usage, estimated cost and errors. A provider failure does not count as successful completion; zero executed attacks alongside failures is not evidence of effective defense. The report always includes error counts.

## Reproduction and failure accounting
Run configs/demo.json; scripts/reproduce.py compares exact per-row observations with timing removed. Fixtures, schemas, datasets and defense logic are versioned. CLI output includes seed, dataset/config SHA-256, model/fixture identifier, mode, trial and trace. Network/validation failures are sanitized in traces and counted. No paid calls or live-model experiments were executed for v0.1.0. The optional model interfaces are exercised by mocked HTTP integration tests.

## Limitations and negative findings
Policy and capability configurations tie at zero successful modeled violations in this dataset; the experiment cannot establish superiority of one over the other. The fixture can complete the legitimate task after attempting an attack, so attack success and task completion are not complements. There is no observed task-completion tradeoff in this fixture; that is a negative finding, not proof that defenses are free of usability costs. The coarse policy can permit untested same-tenant public resources; exact capabilities close that scope. Stateful natural-language deception, real MCP ecosystems, dynamic grants and uncertain real-world labels remain outside this benchmark.
