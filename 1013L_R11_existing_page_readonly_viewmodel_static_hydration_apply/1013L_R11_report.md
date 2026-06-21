# 1013L R11 Existing Page Readonly ViewModel Static Hydration Apply

R11 keeps the existing 1013J/R8 page shell and hydrates it with readonly viewmodel data.

It converts the existing courseware viewmodel into the prior `coursewareScreens1013JR1` page shape, so the old right rail, courseware workspace, and display preview continue using existing page functions instead of a new page.

The big-unit viewmodel is embedded for the next visible route step but does not force a new reading page in R11.

Boundary remains static-only: no runtime fetch, no provider/model, no database/memory/Feishu write, no formal apply, and no main project push.
