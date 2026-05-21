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
- README if the user-facing API changed.

## Validation

Before opening a PR, run the CI checks: `make lint typecheck test`.

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
