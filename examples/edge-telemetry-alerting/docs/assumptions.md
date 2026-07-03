# Pump-station telemetry — Assumptions Ledger

> The choices this build made that its inputs never specified — defaults reached for from habit or
> priors, not from the profile, spec, or ticket. Surfaced so a human can veto them.
> Dispositions: **promote** (belongs in the profile) · **decision** (this-build, recorded) ·
> **flag** (needs a human's second look) · **accept** (trivial, recorded so it's not invisible).

## Ledger

| # | Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|---|
| 1 | The **signal catalog** — discharge_pressure, bearing_temperature, flow_rate | agent default | no (brief said "pump-station telemetry", named no signals) | **flag** — a real build gets the tag list from a device spec sheet; these are illustrative |
| 2 | Every **threshold value** — 10.0 bar, 85 °C, 20 m³/h | agent default | no | **flag** — placeholder engineering values; must come from the spec sheet / runbook |
| 3 | **Hysteresis bands** (0.5, 3.0, 2.0) and **debounce = 3** | agent default | no | **flag** — tuning parameters; wrong values flap or miss. SRE must confirm |
| 4 | **Staleness TTLs** (5 / 10 / 15 s) | agent default | no | **flag** — must match each sensor's real sample rate |
| 5 | **flow_rate is WARNING, not safety-critical** | agent judgment | no | **flag** — a station where a dry-run damages the pump would make low-flow CRITICAL |
| 6 | Staleness alert severity = the **signal's configured severity** (safety-critical → CRITICAL) | agent default | partly (profile says stale safety sensor → CRITICAL) | **accept** — matches the profile's intent |
| 7 | **Dead-from-boot measured from `station_start`** | agent design | no | **decision** → `decisions/0001` (this is the core-promise mechanism) |
| 8 | **Staleness evaluated lazily on read**, no background ticker | agent design | no | **decision** → `decisions/0002` |
| 9 | **Config format = TOML** via stdlib `tomllib` | agent default | no (profile said "station config", not the format) | **accept** — no extra dependency; re-tuning is a config edit |
| 10 | **One active alert per signal**; staleness supersedes a threshold alert | agent design | no | **decision** → recorded here; a signal with no data can't also be breaching |
| 11 | **Out-of-order = drop** any sample with `ts < last_ts` (strict) | agent default | partly (profile requires no resurrection) | **accept** — the simplest rule that satisfies the no-resurrection requirement |
| 12 | **Dashboard poll interval = 2 s** (client JS) | agent default | no | **flag** — trades staleness latency vs load; an operator SLA would set it |
| 13 | **`POST /ingest`** endpoint added for live readings | agent default | no — the brief said "devices stream readings", named no transport | **flag** — real transport is MQTT/HTTP; this is a slice stand-in |
| 14 | **Browser seed via `DASHBOARD_SEED=browser`** env + a programmatic seed | agent default | no | **accept** — deterministic test seam for the browser grader |
| 15 | **Level string on `ALERT_RAISED` reuses the severity value**; `ALERT_CLEARED` is `"info"` | agent default | partly (taxonomy declares level+code) | **accept** — the level comes from the enum, not a literal |
| 16 | **In-memory** monitor state, no persistence | agent default | no | **flag** — a restart re-arms dead-from-boot from the new boot; a real deployment persists |
| 17 | Dashboard is **hand-rolled inline HTML/CSS/JS**, no framework | agent default | yes (profile: "a served static HTML/JS view") | **accept** — matches the declared choice-point |

> The load-bearing **`no` rows are #1–#5 and #13** — the ones worth a human's veto. #1–#5 are the
> whole engineering substance a real SRE owns: **the specific signals and every numeric threshold,
> hysteresis band, debounce and TTL are invented placeholders.** The *rule shapes* are proven and
> tested; the *numbers* are guesses that look authoritative — that is exactly the silent bias this
> ledger exists to surface. #13 is a scope/transport assumption. Everything else is a recorded
> decision or a conventional default. **The engine is correct; the calibration is unverified.**
