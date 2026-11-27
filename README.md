# agentic-demo
A Agentic demo

## UC-01 security review

Review scope: the FBN MVP Release 1 UC-01 review requested in issue #31, with
issue #12 retained as the related SQL injection automation work item. The
repository was reviewed by inspecting its application, dependency manifest,
and security workflow files, then running the focused local regression tests.
There is no deployed environment or dispute-service implementation in this
repository, so this is not a production assessment or an ASVS certification.

### Technology and scope results

The application is a Python Flask demo. Its only application routes are `/`
and `/search`; `/search` queries a newly created in-memory SQLite database.
The only third-party runtime dependency declared is Flask.

| Review area | Result |
| --- | --- |
| NUBAN handling, OTP expiry/retries/lockout, and session expiry | Not applicable: no customer authentication, OTP, NUBAN, or session implementation exists. |
| Account ownership for create, lookup, and list | Not applicable: no dispute or account operations exist. `/search` is a demo username query, not an account lookup. |
| PII masking in free text, logs, audit, analytics, failures, and exports | Not applicable to the implemented routes: no such data flows or facilities exist. No production masking control can be verified. |
| Secrets and TLS 1.2+ | No application secrets or deployment/TLS configuration are present in the inspected application. TLS cannot be verified without the deployment/ingress configuration. |
| Injection and input handling | SQL injection in `/search` was verified and fixed by binding the username as a SQL parameter. The username has no explicit length or format validation; UC-01 business-input validation cannot be assessed because those inputs do not exist here. |
| XSS, command injection, and insecure API behavior | No HTML rendering, command execution, or UC-01 API implementation exists to assess. |
| Dependencies | Flask is range-pinned, not locked. `sqlite3` is provided by Python's standard library and has been removed from the install requirements. Dependency advisory/scanner results were not available, so third-party dependency exposure remains unverified. |
| Responsible AI/security boundaries and grounded FAQ responses | Not applicable: no AI, prompt handling, authorization service, or FAQ functionality exists. |

### Finding and remediation

- **SQL injection — Low severity in this demo; CWE-89 / OWASP A03:2021
  Injection. Fixed.** Before remediation, the `username` query parameter was
  concatenated into SQL in `app/main.py`'s `/search` handler. A caller could
  alter the query; the only current data is a hard-coded demo row in a fresh
  in-memory database, limiting demonstrated impact. The query now uses a
  parameterized statement (`app/main.py`), and
  `tests/test_main.py` verifies both matching-user behavior and that SQL syntax
  supplied as a username is treated as data. Confidence: high.

Validation: `python -m unittest discover -s tests -v` — 2 tests passed.

### ASVS Level 2 coverage and disposition

This repository cannot demonstrate the UC-01 controls expected of an
ASVS-Level-2-oriented implementation. Authentication/session management,
access control, input validation beyond safe SQL binding, error/log handling,
privacy/data protection, secure communications, business/API controls, and
production configuration requirements are absent or unavailable for
verification. The parameterized query is a verified input-to-database security
control, not evidence of broader ASVS compliance. A complete
requirement-by-requirement ASVS assessment must be performed against the actual
service and deployment.

**Disposition:** the demonstrated SQL injection is fixed in this change. UC-01
release readiness is **undetermined / blocked pending review of the actual
service**: authentication, account isolation, PII masking, TLS, and the other
absent controls have not been verified. This review does not approve release.
No findings in those absent components are claimed as verified vulnerabilities.
