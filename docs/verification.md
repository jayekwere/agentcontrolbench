# Verification evidence

Local verification on 2026-11-03 used Python 3.12.16. The complete local suite passed 25 pytest tests with 96.05% branch-inclusive coverage after strict provider-schema handling was added; release changes are checked again by CI. Ruff checks/format, strict mypy, Bandit and three Node dashboard utility tests passed. The locked runtime dependency audit reported no known vulnerabilities at execution time. See the live GitHub Actions runs for current immutable-commit evidence, including Python 3.14 and container verification.

The local in-app browser rendered actual saved data at mobile width and at the 1440×1000 desktop breakpoint. Interaction checks exercised strategy selection, trace navigation, scoped-capability denial inspection, a one-trial experiment through the form and scenario search. JSON/CSV exports and API boundaries are covered by integration tests. Screenshots: [desktop](images/dashboard.jpg), [mobile](images/mobile.jpg), [trace](images/trace.jpg).

The reproduction script verified all 1,350 saved observations exactly after excluding wall-clock latency. No live-model or billable integration was run. The provider adapters are tested through mock HTTP transports for OpenAI-compatible, Claude-compatible and local protocol shapes, request/token/spend limits, retry ceilings, malformed outputs and sanitized errors.

Tests verify concrete invariants; passing them is not a guarantee against every injection or deployment error. Browser screenshots are visual evidence, not an accessibility certification. This release was not validated as a public multi-user service.

## Final local release gate

Python 3.12.16: 26 pytest tests passed; 95.82% branch-inclusive core coverage. Three Node dashboard tests passed. Ruff, strict mypy and Bandit passed. Saved observations and source fingerprints reproduced. The single TestClient deprecation warning is retained; it does not affect the passing assertions. GitHub Actions verifies the final published commit separately.

Fresh wheel installation verified hashed runtime dependencies, exact experiment observations and source fingerprints, plus the installed dashboard/API. See [installation evidence](../results/installation-verification.json). Mobile layout checks observed a 375 px content viewport with no horizontal page overflow; desktop checks used the 1440×1000 breakpoint. Long scenario JSON loads on demand to keep filtering responsive.
