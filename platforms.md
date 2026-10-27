# Platforms and lead sources (India)

Pick sections by `role_family` in `profile.json`. Always run the **General** section too. Re-verify every listing and email before use: posts expire fast.

## General (every role)
| Source | Use | Competition | Sign-up |
|---|---|---|---|
| LinkedIn (Easy Apply, filter past week, experience level) | Main volume; `li_search.py` | High | Logged in |
| Naukri | Volume; daily quota | High | Logged in |
| Indeed, Foundit | Volume | High | Logged in |
| Glassdoor India | Salary checks per role and city | High | Login wall |
| Weekday (jobs.weekday.works) | Curated SME posts | Low–medium | Free |
| Expertia.ai, PlacementIndia | SME and walk-in posts; some show HR email directly | Low | Free |
| Apna | Blue/grey-collar and SME technical posts; expire fast | Low | Phone OTP |
| NCS (ncs.gov.in) | Government portal, linked to state portals (e.g. Mahaswayam) | Low | Aadhaar login |
| State portals (e.g. tnprivatejobs.tn.gov.in) | Private jobs by state | Low | Free |
| Company career pages | Apply direct; find HR/careers emails | Low | Varies |

## industrial_automation (PLC, HMI, SCADA, controls)
| Source | Use |
|---|---|
| EFY jobs, industrialautomationindia.in | Automation-only boards; many posts closed, emails masked |
| Siemens Solution Partner finder; Rockwell PartnerNetwork (filter India) | Lists system integrators for cold outreach |
| Industrial-estate employer lists (state drug/FDA manufacturer PDFs, estate directories) | Pharma and packaging plants with automation teams |
| Cutshort (`/jobs/plc-jobs-in-<city>`) | Few but real PLC posts |

Employers that hire this profile (check live openings each run): system integrators and machine builders (e.g. Syntegon/Klenzaids, ACG, GEA, Inductotherm, Konecranes, Tetra Pak, Bastian Solutions, Beckhoff India, Siemens), automation distributors with application-engineer roles (e.g. Lubi Electronics), engineering-services firms (e.g. Neilsoft), vision/inspection firms (e.g. Lucid Imaging), IIoT firms mixing PLC with Python (e.g. Faclon Labs).
Pay reality (Oct 2026): SME PLC roles ~3–6 LPA; ~8.5 LPA is top-decile. 8+ LPA mostly at MNC OEMs, Bengaluru, or PLC + Python/IIoT roles.

## software_ai (Python, AI/ML, full stack)
| Source | Use | Competition |
|---|---|---|
| Instahyre | Recruiters reach out; good for 1–5 yrs | Medium |
| Cutshort | Startup tech roles | Medium |
| Hirist, IIMJobs (Info Edge) | Tech / management roles | Medium |
| Wellfound | Startups, often remote | Medium–high |

## Lead research procedure
1. Search per role family + target cities + "careers" / "hiring" / "PLC engineer" etc. Prefer posts under 2 weeks old asking ≤ 3 years.
2. Accept an HR email only if it appears on the company's own page (curl the page and grep for `@`). Never guess addresses; skip pages with spam/injected links.
3. Record each lead: company, role, location, URL, date seen, contact, source page.
4. Watch-list employers whose posts are closed; recheck on the next run.

## Cold email rules
- One short email per company, written for the specific role, from facts in the résumé only.
- Run the draft through the humanizer and score with li-human `detect.py` (PASS needed).
- Send with `gsend.py` (Gmail web compose via wine-view; attaches the résumé for the role). It asserts sender, recipient and attachment before Send.
- Verify in Gmail Sent (`in:sent filename:pdf to:<addr>`) and check for bounces (`from:mailer-daemon newer_than:1h`).
- Don't name salary in the first email. Mention relocation and notice period.
