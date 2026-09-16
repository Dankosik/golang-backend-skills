---
name: go-http
description: "Translation. Use when Go HTTP endpoints, routers, middleware, validation, serialization, errors, or streaming affect a backend contract."
---

# Go HTTP

**Translation.** Follow the affected request from its mounted route through middleware to the application operation and client-visible result. Preserve the selected router or framework and its conventions. Honor requirements and preserve settled choices outside the requested change.

Use the router's composition and standard HTTP machinery before inventing adapters. For a new dependency decision, consider supported ServeMux capabilities. Middleware order, nesting, method handling, redirects, and fallbacks are observable behavior; preserve the relevant serving path without migrating unrelated routes.

Decode bounded input into intentional types. Distinguish malformed transport input from business rejection, and absent fields from explicit zero values where the contract requires it. Keep trusted identity separate from caller-controlled fields. Map errors into the established public format without leaking internals; return after completing a response.

Carry request context into downstream work. Choose body limits and transport deadlines for the actual interaction, including uploads and streams. A context timeout does not forcibly stop a handler. Preserve flushing and other required response capabilities through middleware. Once headers or stream bytes are committed, failure cannot become an ordinary replacement response. Never use ResponseWriter after the handler returns.

Verify changed routing, middleware, encoding, and failure behavior through the mounted handler chain; `httptest.ResponseRecorder` can cover those in-process contracts. Calling only the leaf handler omits router and middleware behavior. Use a real test server and client for socket deadlines, disconnects, or transport streaming claims, not for every endpoint change. Report the boundary actually exercised.
