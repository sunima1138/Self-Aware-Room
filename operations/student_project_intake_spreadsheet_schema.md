# Student Project Intake Spreadsheet Schema

This document defines the single-sheet structure used to aggregate student project registration cards.

## Source

- GitHub issue form: .github/ISSUE_TEMPLATE/student_project_registration.yml
- Include issues with labels: `intake`, `student-project`

## Columns

1. issue_number
2. issue_url
3. created_at
4. updated_at
5. student_name
6. project_title
7. project_summary
8. primary_workstream
9. email
10. github_username
11. discord_name
12. zotero_profile
13. weekly_time_commitment_hours
14. weekly_availability
15. known_conflicts_constraints
16. commitment_plan
17. july_baseline_deliverable
18. august_extension_direction
19. dependencies
20. proposed_first_tasks_week_1
21. intake_status
22. faculty_review_status
23. project_status
24. milestone
25. priority
26. blockers
27. reviewer_notes

## Status Value Suggestions

- intake_status: Submitted, Needs Info, Complete
- faculty_review_status: Pending, Reviewed, Approved
- project_status: Submitted, Active, Blocked, Completed
- milestone: July Baseline, August Extension, Backlog
- priority: Low, Medium, High

## Blank-Allowed Contact Fields

The following may be blank at initial submission and completed during review:

- email
- github_username
- discord_name
- zotero_profile

## Weekly Commitment Guidance

The `weekly_time_commitment_hours`, `weekly_availability`, and `known_conflicts_constraints` columns should be reviewed together.

The goal is to validate realistic commitment and explicit constraints so first-day task assignment is feasible and trackable.
