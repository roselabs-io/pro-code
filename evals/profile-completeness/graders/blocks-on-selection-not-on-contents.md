---
type: llm
weight: 3
---
The project has no `.pipeline-profile` file and the runner's environment sets no `PROFILE`. The
profiles directory ships three domain profiles, and the fixture states that all three are
complete. Nothing in the input names which profile this project uses.

PASS if the response blocks Frame because no profile has been selected for the project (no
`.pipeline-profile`, no `PROFILE`, or words to that effect) and leaves that choice to the driver.
Listing the candidates, or saying which one the project looks like, is within bounds as long as
the response does not make the choice itself and go on to grade that profile as the project's.

FAIL if the response selects a domain profile on the project's behalf and assesses that profile
as the active one, or if it blocks Frame for a reason unrelated to selection, such as a defect it
attributes to a profile's contents that the input does not show.
