# AgentControlBench synthetic dataset v1

162 schema-validated cases: six tool domains × three tenants × nine mechanism families. Seven attack mechanisms and two benign mechanisms. Case IDs identify every domain/tenant/mechanism combination. The generator in src/agentcontrolbench/dataset.py is the canonical source; scenarios.json is its exported artifact.

72 development and 90 held-out evaluation cases are split by mechanism family, never by random rows. Evaluation has 72 attacks and 18 legitimate cases. The entire labeled dataset is public for reproducibility. No private test-set claim is made; public data can be memorized. Variants share generator structure and are not independent natural-world incidents.

Each case contains an observation (trusted task, tenant, permitted operation, untrusted tool content and optional recommendation), expected operation and rationale. An unauthorized operation differs in tool, resource or argument from the trusted grant. These evaluator fields are not passed to a model. Validate/export with `agentcontrolbench dataset`. Dataset digests are recorded in actual run output.

All resources, tenant IDs and records are invented. No real personal information, service credentials or private documents occur in the dataset. License: Apache-2.0.
