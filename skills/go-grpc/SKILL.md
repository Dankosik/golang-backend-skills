---
name: go-grpc
description: "Implement or review Go RPC contracts, Protobuf evolution, interceptors, status, deadlines, and streams."
---

# Go gRPC

**Contract.** Trace the affected RPC from schema through registration and interceptors to the status, metadata, and messages the caller observes. Honor requirements and preserve settled choices outside the requested change.

When schemas change, preserve the selected protobuf edition, generated API, and generation tools. Change schema sources and regenerate; never patch generated code. Evolve field identity and presence deliberately, reserve removed identifiers, and check compatibility with existing clients. A successfully decoded message still needs application validation.

Translate application failures into intentional status codes and safe details at the transport boundary. Distinguish unary and streaming interceptor coverage. Treat incoming metadata as untrusted; propagate only appropriate values, and do not mutate metadata shared with a context.

Reuse client connections and established middleware. Use client construction appropriate to the installed grpc-go API; connection readiness cannot guarantee the next RPC succeeds. Propagate deadlines and cancellation into downstream work. Retry only safely repeatable operations within the remaining budget; a deadline error does not establish that a remote write failed.

For streams, give send, receive, and termination explicit owners. Respect flow control, bound application buffering, and serialize each direction's operations. Half-closing sends does not observe terminal status. Receive the final outcome or cancel abandoned calls and join their goroutines.

For review-only work, report contract risks and the smallest justified change without editing. For implementation, test the affected property: schema compatibility with the existing generation/compatibility checks; status, interceptors, cancellation, or stream completion through an RPC. Reuse an in-process RPC harness when it includes the mechanism; do not claim it proves deployment transport behavior. Address bounded graceful draining and forced-stop fallback when changing service shutdown, not for every RPC edit.
