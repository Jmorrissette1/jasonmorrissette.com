# Interview Questions: jasonmorrissette.com Build

Questions to practise, collected step by step while building this site.

## Step 1: Project skeleton and Python environment

1. Why is deleting a committed `.env` file not enough to fix a leaked secret?
2. What's the difference between the dependencies in `pyproject.toml` and the contents of a lockfile, and which one is the supply-chain control?
3. Why might you put an upper bound on `requires-python` for an application but not for a library?

## Step 2: FastAPI application foundation

1. What problem does the application factory pattern solve, especially for testing?
2. In FastAPI, when would `async def` make performance _worse_ than `def`?
3. Why build canonical URLs from configuration rather than the request's `Host` header?
4. Why would you disable OpenAPI and Swagger docs on a public production service?

## Step 3: Design system, base layout and homepage

1. Why can `url_for()` produce broken links behind a TLS-terminating reverse proxy, and what are two ways to fix it?
2. What does Jinja2 autoescaping protect against, and when would you still need to sanitise input?
3. Why verify a SHA-256 hash for a downloaded build tool, and what attack does that stop?
4. Your brand red fails WCAG AA for body text. How do you keep the brand and still meet AA?
5. A code formatter silently changed template logic and no tests failed. What process and tooling changes would catch that kind of problem?

## Step 4: Security headers and error pages

1. Why is enabling HSTS before validating TLS dangerous, and why can't you easily undo it?
2. Your 500 pages are missing security headers even though you have header middleware. Explain why.
3. What does `frame-ancestors 'none'` protect against, and why also send `X-Frame-Options`?
4. Why is a CSP without `'unsafe-inline'` so much stronger, and what design choices made it possible here?
5. A test checks security headers on `/healthz` and passes, but the endpoint is broken. What went wrong, and how do you design tests so they can't pass against the wrong response?

## Step 5: Code quality and security scanning

1. Why are `assert` statements a security risk in application code but fine in tests?
2. What's the difference between SAST (Bandit) and SCA (pip-audit)? Which one would have caught Log4Shell?
3. You configured `.editorconfig`, but the files still had no final newlines. What happened, and what does that teach you about "configured" versus "enforced"?

## Step 6: GitHub, secret scanning and CI

1. Why pin GitHub Actions to a full commit SHA instead of a version tag like `@v7`? Which real-world incident shows the risk?
2. What does `permissions: contents: read` at the top of a workflow protect against?
3. Why rewrite commit emails before the first push but never after?
4. GitHub push protection and gitleaks in CI both detect secrets. Why have both, and which one stops the leak?
5. What is a Dependabot "cooldown", and what supply-chain attack pattern does it defend against?
