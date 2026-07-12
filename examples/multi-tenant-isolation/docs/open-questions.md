# multi-tenant-isolation — Open Questions

> Every assumption that could bite the build — state + owner + stakes. Also holds the
> **Design seeds → Plan** bucket. Resolved items flip to `[decided]` as Implement lands them.

## Open / decided

- **[decided]** **Cross-tenant denied response = 404, not 403.** A 403 confirms the id exists in *some* tenant (an existence oracle); 404 reveals nothing. Owner: build. Stakes: the core promise. *(Frame hard gate — isolation rules pinned before Plan.)*
- **[decided]** **Scoping rule: deny-by-default at the store.** Every query is scoped by `workspace_id`; an unscoped/foreign id resolves to "not found," never a leak. Owner: build. Stakes: the core promise.
- **[decided]** **RBAC ordering: scope BEFORE role.** Tenant scope (→404) is checked before the role gate (→403), so a 403 is only ever returned for an in-tenant resource — a member probing cross-tenant ids always gets 404 whether or not the id exists. *(Closes the existence-oracle-via-RBAC-ordering trap.)* Owner: build. Stakes: the core promise.
- **[open]** **Token minting is out of scope.** Tokens are issued out-of-band by an external issuer; this slice only verifies them. Owner: platform. Stakes: a real deployment needs an issuer + rotation; absent here. Logged, not built.
- **[open]** **Delete is the only admin-gated verb in this slice.** Create/update are member-allowed. Whether update should also be admin-gated is a product call, not pinned by the brief. Owner: product. Stakes: low — RBAC shape is proven by delete regardless.
- **[open]** **No persistence layer.** In-memory store for the slice (see assumptions ledger). A real deployment needs a DB + the isolation guard re-proven at the query layer (RLS or scoped ORM). Owner: platform. Stakes: the isolation proof must be re-run against the real store.

## Design seeds → Plan (hypotheses, not decisions)

- Seed: *scope every query in the store layer, not the handler* → route against `tenant-scoped-query-guard`. Plan confirms.
- Seed: *return a typed error envelope, choosing 404 vs 403 deliberately* → route against `structured-error-envelope`. Plan confirms.
- Seed: *cursor-paginate the list* → route against `cursor-pagination`. Plan confirms.
- Seed: *emit a structured audit event on denial* → route against `write-through-audit-log`. Plan confirms.
