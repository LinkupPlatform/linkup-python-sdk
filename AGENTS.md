# Linkup Python SDK Agent Guide

This repository contains the public Python SDK for the Linkup API.

## Goal

Keep the SDK aligned with the current public, stable Linkup API while:

- implementing a Pythonic public interface,
- documenting the features through docstrings,
- and adding type safety through type hints or input data validation with `pydantic` models when
  relevant.

## Working Rules

- Prefer minimal diffs focused on the public API change being synchronized.
- Do not expose internal, beta, deprecated, or undocumented API behavior unless explicitly
  requested.
- Preserve the repo's public Python conventions:
  - use snake_case in the SDK public surface;
  - convert to API wire-format only at the request boundary.
- Keep sync and async client methods aligned when a capability exists in both forms.
- Avoid unnecessary breaking changes. If a change would be breaking or ambiguous, stop and explain
  instead of guessing.
- If code generation exists for a given area, use the generation command instead of manually editing
  generated output.

## When Updating the SDK

When adding or changing a public API capability, update the relevant pieces together:

- client method signatures,
- request/response typing and models,
- sync and async behavior when applicable,
- tests,
- README if anything in it became out-dated.

## Validation

After having done some changes or before opening a PR, run the CI checks:
`make lint typecheck test`.

Never run the underlying checks without using these `make` commands (e.g. with `uv run ruff ...`),
as these kind of checks won't take into account some settings (like the `exclude` list).

## Non-Goals

- Do not change package version, release config, or publish settings unless the task explicitly asks
  for it.
- Do not refactor unrelated code while performing API synchronization.

## Sync Decisions

Add durable exceptions here when a proposed sync should not be repeated.

- Do not expose API capabilities that are not clearly public and stable.
- Do not implement `/credits/balance` in this SDK unless explicitly requested.
- Do not implement `/responses` in this SDK unless explicitly requested.
- If a capability was intentionally rejected for product/design reasons, do not propose it again
  until this file is updated.

## Coding practices

Besides the practices enforced through the CI checks (especially with ruff), we try to enforce the
following coding practices:

- Mark non-public modules, classes, methods, functions, and attributes private with a leading
  underscore when they are not part of the SDK public API.
- Prefer [Google style guide imports](https://google.github.io/styleguide/pyguide.html#22-imports)
  for new code: import modules instead of importing symbols, except for `typing` symbols, public
  re-exports, and cases where the existing file convention makes module imports awkward.
- Treat anything exported from `linkup.__init__` or listed in `__all__` as public API; add exports
  only intentionally.
- Keep API wire-format names at the request/response boundary only. Internal and public Python APIs
  should stay snake_case, and camelCase/API aliases should live in request serialization or Pydantic
  aliases.
- Keep sync and async methods structurally aligned: same parameters, same validation behavior, same
  returned models, and same documented errors.
- Store secrets as `pydantic.SecretStr` or an equivalent secret container once they enter client
  state; do not store raw API keys on instances.
- Prefer explicit SDK error classes over leaking transport or dependency exceptions from public
  methods, except where deliberately documented.
- Add `# noqa`, `# type: ignore`, and `# pyright: ignore` only with a short reason.
- Avoid adding runtime dependencies for small conveniences; keep SDK dependencies minimal.
- Write tests through the public `linkup` API unless the test is specifically covering private or
  internal behavior.
