---
name: go-http
description: "Translation. Use when Go HTTP endpoints, routers, middleware, validation, serialization, errors, or streaming affect a backend contract."
---

# Go HTTP

**Translation.** Follow the request from its mounted route through middleware to the application operation and client-visible result. Preserve the selected router or framework and its existing conventions. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Use the router's own composition and standard HTTP machinery before inventing adapters. For a new dependency decision, inspect the supported ServeMux capabilities first. Middleware order, nesting, method handling, redirects, and fallbacks are observable behavior; preserve the full serving path.

Decode bounded input into intentional types. Distinguish malformed transport input from business rejection, and absent fields from explicit zero values where the contract requires it. Keep trusted identity separate from caller-controlled fields. Map errors into the established public format without leaking internals; return after completing a response.

Carry request context into downstream work. Choose body limits and transport deadlines for the actual interaction, including uploads and streams. A context timeout does not forcibly stop a handler. Preserve flushing and other required response capabilities through middleware. Once headers or stream bytes are committed, failure cannot become an ordinary replacement response. Never use ResponseWriter after the handler returns.

Exercise changed routing, middleware order, encoding, and failure behavior through requests. Use a real test server when socket, timeout, or streaming behavior matters; direct handler calls cannot establish those properties.
