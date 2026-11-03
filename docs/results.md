# Observed simulation results

The published run uses seed 17, three trials, 90 held-out scenarios, five configurations and 1,350 actual execution records. No language model was evaluated.

| Defense | Unauthorized scenario success | Wilson 95% interval | All-trial completion | Errors |
|---|---:|---:|---:|---:|
| baseline | 98.61% | 92.54–99.75% | 100.0% | 0 |
| least_privilege | 77.78% | 66.91–85.83% | 100.0% | 0 |
| policy | 0.00% | 0.00–5.07% | 100.0% | 0 |
| capabilities | 0.00% | 0.00–5.07% | 100.0% | 0 |
| depth | 0.00% | 0.00–5.07% | 100.0% | 0 |

These results establish that the synthetic authorization gateway enforces the tested contracts. Tool-name restriction alone permits many cross-resource or argument-level attacks. Policy, capability and depth configurations tie on successful execution; depth also suppresses requests by isolating untrusted recommendations. All tested configurations complete the legitimate task, so this simulation observes no completion penalty. The result does not predict how a real model would behave.

The dataset is factorial and related variants are correlated. Confidence intervals are descriptive, not population-level evidence. Benign evaluation n=18 is small; zero observed false blocks has a Wilson upper bound of 17.59%. See [methodology](methodology.md) for denominators and untested failure modes.

Full records: [results/demo.json](../results/demo.json). Latency is measured on the execution host; token usage and inference cost are zero for this offline fixture.
