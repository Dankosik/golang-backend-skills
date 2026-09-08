---
name: go-grpc
description: "Contract. Use when Go gRPC services, clients, interceptors, Protobuf evolution, status mapping, deadlines, or streams need implementation or review."
---

# Go gRPC

**Contract.** Trace the RPC from its schema through registration and interceptors to the status, metadata, and messages the caller observes. Honor supplied requirements and settled technical choices; resolve only what the task leaves open.

Preserve the selected protobuf edition, generated API, and generation tools. Change schema sources and regenerate; never patch generated code. Evolve field identity and presence deliberately, reserve removed identifiers, and check compatibility with existing clients. A successfully decoded message still needs application validation.

Translate application failures into intentional status codes and safe details at the transport boundary. Distinguish unary and streaming interceptor coverage. Treat incoming metadata as untrusted; propagate only appropriate values, and do not mutate metadata shared with a context.

Reuse client connections and established middleware. Use client construction appropriate to the installed grpc-go API; connection readiness cannot guarantee the next RPC succeeds. Propagate deadlines and cancellation into downstream work. Retry only safely repeatable operations within the remaining budget; a deadline error does not establish that a remote write failed.

Give each stream explicit send, receive, and termination owners. Respect flow control, bound application buffering, and serialize each direction's operations. Half-closing sends does not observe terminal status. Receive the final outcome or cancel abandoned calls and join their goroutines.

Exercise the changed status, compatibility, cancellation, or stream-ending behavior through an RPC. Bound graceful draining and define the existing service's forced-stop fallback.
