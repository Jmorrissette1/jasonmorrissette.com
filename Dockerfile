# syntax=docker/dockerfile:1.7

# ---------------------------------------------------------------------------
# Stage 1: compile Tailwind CSS (build-time only; never shipped)
# ---------------------------------------------------------------------------
FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS css

ADD --chmod=755 \
    --checksum=sha256:e47695cee3f0d90623a91f3939b08bdee610eb5ad99340adff9d4145b284d6cc \
    https://github.com/tailwindlabs/tailwindcss/releases/download/v4.3.5/tailwindcss-linux-x64 \
    /usr/local/bin/tailwindcss

WORKDIR /build
COPY styles/ styles/
COPY app/templates/ app/templates/
RUN tailwindcss -i styles/input.css -o site.css --minify

# ---------------------------------------------------------------------------
# Stage 2: install Python dependencies from the lockfile
# ---------------------------------------------------------------------------
FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS deps

COPY --from=ghcr.io/astral-sh/uv:0.11.26@sha256:3d868e555f8f1dbc324afa005066cd11e1053fc4743b9808ca8025283e65efa5 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project

# ---------------------------------------------------------------------------
# Stage 3: minimal runtime image
# ---------------------------------------------------------------------------
FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS runtime

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=deps /app/.venv /app/.venv
COPY app/ app/
COPY --from=css /build/site.css app/static/css/site.css

USER 10001:10001
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
