---
name: job-apply
description: Find and apply to jobs on LinkedIn, Naukri, Indeed and company career sites through wine-view, with Gmail for codes and confirmations. Use for "apply for jobs", "check job mails", "apply to this listing".
---

# job-apply

Applies to jobs in the user's own logged-in Chrome via **wine-view** (load that skill first; never another browser without asking). Gmail via the claude.ai Gmail connector.

## Candidate profile
All personal facts (name, education, salary, notice period, location, links, résumé paths, skill-years) live in `profile.json`, which is kept private and never published. Copy `profile.example.json` to `profile.json` and fill it in. `answers.py` reads that file for every screening answer.
- Rule table with self-checks: `answers.py`. Add a rule plus a check whenever a new question appears.
- Never claim a skill or year count that is not in the profile. An unknown tool counts as 0 years.

## Fit filter (this is what raises the hit rate)
Apply only when: experience asked ≤ 3 years, pay at or above the floor in profile.json, or unlisted, role matches automation or Python/software. Skip senior/lead, 5+ years, sales, unrelated stacks. Prefer jobs < 1 week old with few applicants. Report skips with the reason.

## Platforms
- **LinkedIn** (`li_search.py`, `li_job.py`, `ea.py`): native `<dialog>`; enable `Emulation.setFocusEmulationEnabled` for background tabs; required-field `*` can sit past truncated labels.
- **Naukri**: chat questionnaire, answers ≤ 100 chars, wait for each question to load; "Daily quota exceeded" = stop until tomorrow.
- **Indeed / Workday / Taleo / Oracle Cloud / SmartRecruiters**: Oracle dropdown options have role "row"; SmartRecruiters uses shadow DOM; Workday phone code must be India (+91).
- Upload files by intercepting the native file chooser.
- Log every submission to `applied.json` and the job-search memory.

## Gmail
Search for OTP / verification codes and application confirmations; read only what the task needs. Never send email or reply to recruiters without the user's OK.

## Always stop for the user
Passwords, MFA, CAPTCHAs, cookie/consent ticks, e-signatures, drug-test/background-check consent, PAN/DOB/ID numbers, anything legally attesting. New account passwords go to macOS Keychain only. Outgoing prose goes through humanizer; keep the profile's personal details out of anything public.

## Reality check
No skill can guarantee 100% application success or a job offer. Success here means: every attempt ends either submitted (confirmed on screen or by email) or reported to the user with the exact blocker.
