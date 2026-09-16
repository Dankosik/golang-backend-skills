# Go Backend Skills 1.0.1

Candidate release notes. This revision is unreleased; metadata does not imply
that a v1.0.1 tag or release exists.

This PATCH refines the existing 16 independent skills rather than adding a
mandatory process. It clarifies routing, review versus editing, task-scoped
reading, and completion through applicable checks and fixes.

Go-specific changes distinguish mounted HTTP handler checks from real transport,
RPC status/stream checks from service shutdown, and pure data mapping from real
transaction evidence. Goroutine cancellation is still not a join, and a passing
race run is still not proof of liveness. Required project checks remain intact.

The candidate includes an authoring audit and 20 behavioral evaluation
specifications. They are not executed model comparisons or runnable application
fixtures. No speedup or universal model-quality improvement is claimed. Record
focused behavioral evidence before publishing semantic instruction changes.

Skill names, paths, licenses, environment requirements, independent installation,
and distribution scripts are unchanged. Existing install examples remain on
v1.0.0; no release, tag move, or marketplace update is part of this change.

See [installation and updates](https://github.com/Dankosik/golang-backend-skills/blob/main/docs/distribution.md).
Public-directory approval is separate from an author marketplace or release;
this candidate does not claim provider approval.
