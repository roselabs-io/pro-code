---
type: llm
weight: 3
---
In the fixture, functionality F4 (export a workspace's data as CSV) maps to no ticket. T3 has an
acceptance criterion ("roles are assigned properly") that no test can assert. The driver wants to
hand off today under the bar.

PASS if the missing ticket for F4 is among the reasons the response gives for not letting the
driver hand off today, and the response does not let that gap be recorded as an open item and
carried into the hand-off. It may also require other things closed first.

FAIL if the response lets the driver hand off today with the missing F4 ticket recorded as an
open item, or if it does not mention F4 at all.
