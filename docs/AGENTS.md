# Project rules
Read first: docs/05-prd.md, docs/06-architecture.md, docs/06a-api-
contract.md,
docs/06b-safety-rules.md, docs/08-tasks.md.
Read other docs only when the current task needs them.
Work on one task at a time, on its own branch, only inside your owner's
folder.
Write or con⁠⁠Anonymous 95⁠firm the failing tests before writing the code.
A task is done only when linting, type checks, all tests and the contract
test pass.
Never change a field name, endpoint or error code without updating
docs/06a-api-contract.md and shared/ in the same pull request.
Never call the database, AI, OCR, WhatsApp or Maps APIs from the frontend.
Never put a secret key in frontend code or in the repo.
Medical safety:
- Red-flag decisions are made by code in backend/safety/, never by the AI.
- Never write prompts or code that diagnose, suggest a dose, or tell a user
to stop a medicine.⁠⁠Anonymous 65⁠
- Status comes only from the reference range printed on the report.
- Do not weaken, skip or delete a safety test. Stop and ask instead.
After 3 failed attempts at the same problem, stop and report what you tried.
Put new ideas in the backlog. Do not add them to the current task.
Ask for human approval before changing the database schema, authentication,
permissions, safety rules, the system prompt, dependencies, and before
deploying to production.
After each task, update docs/08-tasks.md and record decisions in
docs/decisions.md