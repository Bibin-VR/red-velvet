# red-velvet

A Claude Code skill (`job-apply`) that finds and applies to jobs on LinkedIn, Naukri, Indeed and company career sites. It drives your own logged-in Chrome through wine-view and uses Gmail for sign-in codes and confirmations.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill instructions: fit filter, platform notes, what to hand back to the user |
| `answers.py` | Screening-question rules, with self-checks |
| `ea.py` | LinkedIn Easy Apply helpers |
| `li_search.py` | LinkedIn job search |
| `li_job.py` | Reads a LinkedIn job page |
| `profile.example.json` | Template for your private profile |

## Setup

1. Copy the folder to `~/.claude/skills/job-apply/`.
2. Copy `profile.example.json` to `profile.json` and fill in your details. Keep this file private; `.gitignore` already excludes it.
3. Run the self-check: `python3 -I answers.py`. It prints `OK` when the rules pass.
4. Load wine-view and sign in to each job site in Chrome.

## Limits

- The skill never enters passwords, MFA codes, CAPTCHAs, consent ticks or legal attestations. It stops and asks.
- No skill can guarantee a job or a 100% application success rate. Each attempt ends either submitted and confirmed, or reported with the reason it stopped.

## License

MIT. See `LICENSE`.
