# Drive LinkedIn Easy Apply with fixed, truthful answers. Stops on anything unknown.
import re, json, json as _json
import os
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "profile.json")))  # private: copy profile.example.json and fill it in
exec(open(os.path.join(HERE, "ea.py")).read())
RES = {k: os.path.expanduser(v) for k, v in P["resumes"].items()}
LOG = os.path.join(HERE, "applied.json")
# years of experience per skill (profile.json): keep conservative and match the resumes
YRS = [(p, y) for p, y in P["skill_years"]]
import datetime as _dt
_mo = (_dt.date.today().year - P["work_start_year"]) * 12 + _dt.date.today().month - P["work_start_month"]
TOTAL_YRS, TOTAL_MONTHS = _mo // 12, _mo % 12
def years_for(label):
    l = label.lower()
    for pat, y in YRS:
        if re.search(pat, l): return y
    return None
def answer_for(label, kind, opts):
    l = label.lower().replace("’", "'")
    yes, no = "Yes", "No"
    if re.search(r"cgpa|\bgpa\b|grade point|percentage|aggregate|marks", l) and re.search(r"cgpa|\bgpa\b|grade point|graduat|b\.?tech|\bb\.?e\b|bachelor|degree|\bug\b|engineering|college|university", l) \
            and not re.search(r"10th|12th|\bssc\b|\bhsc\b|class (x|xii|10|12)|school|diploma|\bpuc\b|intermediate|m\.?tech|master|post ?grad|\bpg\b", l):
        return f"{P['cgpa']} CGPA" if re.search(r"percent|%", l) else P["cgpa"]
    if re.search(r"convicted|criminal|ailment|state of health|medical condition|pregnan|passport|night shift|shifts|service bond|signed .*agreement|ever worked with|appeared for an interview|employee id", l): return None
    if re.search(r"contract(ual)?\b|contract.to.hire|\bc2h\b", l) and re.search(r"willing|okay|ok\b|comfortable|open to|fine|ready|accept|interested", l): return yes  # user OK with contract roles (2026-10-25)
    if re.search(r"m\.?tech|master|\bm\.?e\b|\bm\.?s\b|mba|ph\.?d|post ?grad|diploma|12th|10th|percentage|cgpa|gpa|marks|6 days|six days|saturday", l): return None
    if re.search(r"ctc|salary|compensation|package|lpa|pay\b", l):
        lak = re.search(r"lakh|lpa|lacs|lac\b|l\.p\.a", l)
        usd = re.search(r"\busd\b|us\$|\$|dollar", l)  # ponytail: fixed ~88 INR/USD, re-check the rate if it moves much
        if re.search(r"expect|desired|ask", l): return P["expected_usd"] if usd else (P["expected_lakh"] if lak else P["expected_inr"])
        if re.search(r"current|present|existing|last", l): return P["current_usd"] if usd else (P["current_lpa"] if lak else P["current_inr"])
        return None
    if re.search(r"how many days can you join|days to join|joining time", l): return str(P["notice_days"])
    if re.search(r"serving (your )?notice|already been relieved|currently serving", l): return no
    if re.search(r"notice period", l):
        if kind.startswith("select") or kind == "fieldset": return [f"{P['notice_days']} days", "1 month", "15-30 days", f"Within {P['notice_days']} days", f"{P['notice_days']} Days", "1 Month"]
        return str(P["notice_days"])
    if re.search(r"immediate(ly)? join|join immediately|immediate joiner|start immediately", l): return no
    if re.search(r"within (30|thirty) days|join within|able to join in", l): return yes
    if re.search(r"relocat", l): return yes
    if re.search(r"commut|on-?site|work(ing)? from (the |our )?office|hybrid|wfo|office \d|days a week|in.?office", l): return yes
    if re.search(r"bachelor|b\.tech|\bbtech\b|\bb\.e\.|degree|graduate|engineering background", l) and not re.search(r"year|percent|cgpa|gpa|score", l): return yes
    if re.search(r"authori[sz]ed|legally|eligible to work|work permit|right to work|sponsor", l) and \
            re.search(r"united states|\busa\b|\bu\.s\.(a\.)?|\bu\.s\b|america|h-?1b|green card|canada|united kingdom|\bu\.?k\.?\b|europe|\beu\b|australia|germany|singapore|\buae\b|dubai", l):
        return yes if re.search(r"sponsor", l) else no  # authorized to work in India only
    if re.search(r"sponsor", l): return no
    if re.search(r"authori[sz]ed|legally|eligible to work|work permit|right to work", l): return yes
    if re.search(r"gender", l): return [P["gender"], "Man"]
    if re.search(r"disab", l): return ["No", "No, I do not have a disability", "I don't have a disability"]
    if re.search(r"veteran", l): return ["No", "I am not a protected veteran"]
    if re.search(r"english", l): return ["Professional", "Fluent", "Full professional proficiency", "Professional working proficiency", "Advanced"]
    if re.search(r"how did you hear|hear about (us|this)", l): return ["LinkedIn"]
    if re.search(r"linkedin", l): return P["linkedin_url"]
    if re.search(r"github", l): return P["github_url"]
    if re.search(r"portfolio|website", l): return P["portfolio_url"]
    if re.search(r"are you (currently )?(located|based|residing|living) in", l): return yes if re.search(re.escape(P["city"].split(",")[0].lower()), l) else no
    if re.search(r"(current|present) (city|location)|where are you (currently )?(based|located)|which city", l): return P["city"]
    if re.search(r"rate .*(data structures|algorithms|dsa)", l): return P["dsa_rating"]
    if re.search(r"which llm apis|llm apis and frameworks", l): return P["llm_tools"]
    if re.search(r"how many (llm|gen ?ai|ai)\W*(/\W*gen ?ai\W*)?projects", l): return P["llm_project_count"]
    if re.search(r"working.hour overlap|time ?zone overlap|overlap (with|for) india", l) and re.search(r"india|ist\b", l): return yes
    if re.search(r"join .*within .*(15|30)", l): return yes if (kind == "fieldset" or kind.startswith("select")) else f"Yes, within {P['notice_days']} days"
    if re.search(r"year of (passing|graduation)|graduation year|passed out", l): return P["grad_year"]
    if re.search(r"highest (qualification|education)", l): return ["Bachelor's Degree", "B.Tech", "Bachelor's", "B.E/B.Tech", "Bachelors"]
    if re.search(r"full[- ]time|permanent role", l): return yes

    if re.search(r"currently employed|presently working|are you (currently )?working", l): return yes
    if re.search(r"convicted|criminal|ailment|health|medical|pregnan|passport|shift|night|bond|agreement|ever worked with|appeared for an interview|previously (worked|applied)|employee id", l): return None
    m = re.search(r"(more than|over|at least|minimum( of)?)\s*(\d+)\+?\s*(years|yrs)", l)
    if m and re.match(r"(do|have|are|is) ", l):  # "Do you have more than 5 years of exp?"
        y = years_for(l); y = TOTAL_YRS if y is None else y; n = int(m.group(3))
        return yes if (y >= n if m.group(1).startswith(("at least", "minimum")) else y > n) else no
    if re.search(r"additional months of experience", l):
        return [f"{TOTAL_MONTHS} months", f"{TOTAL_MONTHS} month", str(TOTAL_MONTHS)] if kind.startswith("select") else str(TOTAL_MONTHS)
    if years_for(l) is None and re.search(r"(total|overall|professional|relevant|industry|it|engineering|software( development)?|development|programming|coding)\s+(work\s+)?experience|^how many years of (work )?experience do you have\??\s*(\(.*\))?\s*$", l):
        if kind.startswith("select"): return [f"{TOTAL_YRS} years", str(TOTAL_YRS), f"{TOTAL_YRS} Years", f"{TOTAL_YRS}+ years", "2-3 years", "1-3 years", "2-4 years", "2-5 years"]
        return str(TOTAL_YRS) if kind != "fieldset" else None
    if re.search(r"years|experience", l):
        y = years_for(l)
        if y is None: return None
        if kind == "fieldset" or kind.startswith("select"):  # e.g. "Do you have experience with X?" yes/no
            return yes if y > 0 else no
        if re.search(r"years?|yrs|how (many|long)", l) or re.match(r"(total |relevant )?experience (in|with|of)\b", l): return str(y)
        if re.match(r"(do|have|are|can) you\b", l): return yes if y > 0 else no
        return None  # descriptive: "What is your hands-on experience with...", "Automation framework you have experience working on"
    if re.search(r"^(do|have|are|can) you .*(experience|worked|familiar|knowledge|hands-on)", l):
        y = years_for(l); return None if y is None else (yes if y > 0 else no)
    if re.match(r"(have|did) you (ever )?(built|implemented|developed|used|deployed|created|designed|fine.?tuned|integrated|worked)\b", l):
        y = years_for(l); return None if y is None else (yes if y > 0 else no)  # "Have you built X?" follows the skill years
    return None
def _pick(want, opts):
    if isinstance(want, str): want = [want]
    for w in want:
        for o in opts:
            if o.strip().lower() == w.lower(): return o.strip()
    for w in want:
        for o in opts:
            if o.strip().lower().startswith(w.lower()): return o.strip()
    return None
FILLED = []
def fill_step(resume_key):
    """Fill the current Easy Apply page. Returns list of unanswered labels."""
    f = ea_fields()
    if f == "NO ROOT": return ["NO DIALOG"]
    todo = []
    for fld in f["fields"]:
        lab, kind = fld.get("label", ""), fld["kind"]
        if not lab and kind == "fieldset" and any("[x]" in o for o in fld["opts"]): continue   # resume list etc.
        if kind.startswith("input:checkbox") and not lab: continue
        if kind == "fieldset":
            ans = answer_for(lab, kind, fld["opts"])
            opt = _pick(ans, [x["text"] for x in fld.get("radios", [])]) if ans else None
            sel = next((o[:-3].strip() for o in fld["opts"] if o.endswith("[x]")), None)
            if sel and (opt is None or opt == sel): continue  # drafts keep old picks: redo only when the rules now disagree
            rid = next((x["id"] for x in fld.get("radios", []) if x["text"].strip() == opt), None) if opt else None
            if rid: ea_radio_id(rid); FILLED.append((lab[:90], opt))
            elif fld.get("req"): todo.append(("fieldset", lab, fld["opts"]))
            continue
        if kind.startswith("select"):
            cur = (fld.get("value") or "").strip()
            if cur and cur.lower() not in ("select an option", ""): continue
            ans = answer_for(lab, kind, fld.get("opts") or [])
            allopts = _j("(()=>[...document.getElementById(__ID__).options].map(o=>o.text.trim()))()", id=fld["id"])
            opt = _pick(ans, allopts) if ans else None
            if opt: ea_select(fld["id"], opt); FILLED.append((lab[:90], opt))
            elif fld.get("req"): todo.append(("select", lab, allopts[:15]))
            continue
        if kind.startswith("input") or kind.startswith("textarea"):
            cur = (fld.get("value") or "").strip()
            if cur and not (re.search(r"ctc|salary", lab, re.I) and cur != str(answer_for(lab, kind, []))): continue  # re-check money fields kept in drafts
            ans = answer_for(lab, kind, [])
            if isinstance(ans, list): ans = ans[0]
            if ans is not None: ea_text(fld["id"], ans); FILLED.append((lab[:90], ans))
            elif fld.get("req"): todo.append((kind, lab, []))
    return todo
def choose_resume(resume_key):
    path = RES[resume_key]; name = path.rsplit("/", 1)[1]
    have = _j("""(()=>{const r=__ROOT__; return /Select or upload a resume/.test(r.innerText)})()""")
    if not have: return "no resume step"
    cur = _j("""(()=>{const r=__ROOT__; const i=[...r.querySelectorAll('input[type=radio]')].find(i=>i.checked); if(!i) return ''; let p=i; for(let k=0;k<6&&p;k++){ if((p.innerText||'').trim().length>5) break; p=p.parentElement;} return (p&&p.innerText||'')})()""")
    if name in cur: return "already " + name
    # pick existing card with that name, else upload
    r = _j("""(()=>{const r=__ROOT__; const el=[...r.querySelectorAll('*')].find(e=>e.childElementCount===0 && e.innerText && e.innerText.trim()===__N__); if(!el) return null; el.scrollIntoView({block:'center'}); const x=el.getBoundingClientRect(); return [x.x+x.width/2, x.y+x.height/2]})()""", n=name)
    if r:
        click_at_xy(*r); wait(1)
    else:
        drain_events(); cdp("Page.enable"); cdp("Page.setInterceptFileChooserDialog", enabled=True)
        try:
            ea_click("Upload resume"); wait(1.5)
            fc = [e for e in drain_events() if e.get("method") == "Page.fileChooserOpened"]
            if not fc: return "upload: no chooser"
            cdp("DOM.setFileInputFiles", files=[path], backendNodeId=fc[-1]["params"]["backendNodeId"]); wait(4)
        finally:
            cdp("Page.setInterceptFileChooserDialog", enabled=False)
    cur = _j("""(()=>{const r=__ROOT__; const i=[...r.querySelectorAll('input[type=radio]')].find(i=>i.checked); if(!i) return ''; let p=i; for(let k=0;k<6&&p;k++){ if((p.innerText||'').trim().length>5) break; p=p.parentElement;} return (p&&p.innerText||'')})()""")
    return ("ok " if name in cur else "MISMATCH ") + cur.replace("\n", " ")[:80]
def unfollow():
    st = _j("""(()=>{const r=__ROOT__; const c=[...r.querySelectorAll('input[type=checkbox]')].find(c=>/follow/i.test((r.querySelector('label[for="'+CSS.escape(c.id)+'"]')||{}).innerText||'')); if(!c) return null; const lb=r.querySelector('label[for="'+CSS.escape(c.id)+'"]'); lb.scrollIntoView({block:'center'}); const x=lb.getBoundingClientRect(); return [c.checked, x.x+Math.min(10,x.width/2), x.y+x.height/2]})()""")
    if st and st[0]: click_at_xy(st[1], st[2]); wait(0.6)
def open_job(jid):
    cdp("Emulation.setFocusEmulationEnabled", enabled=True)
    goto_url(f"https://www.linkedin.com/jobs/view/{jid}/"); wait_for_load(); wait(3)
    t = js("document.body.innerText")
    a = t.find("Sales Nav"); top = t[a+9:a+700] if a >= 0 else t[:700]
    i = t.find("About the job"); about = t[i:i+6000] if i >= 0 else ""
    easy = bool(js("!!document.querySelector('[aria-label=\"Easy Apply to this job\"]') || [...document.querySelectorAll('button')].some(b=>/Easy Apply/.test(b.innerText))"))
    applied = "Application submitted" in t or bool(re.search(r"Applied \d+ (minute|hour|day|week)", t))
    closed = "No longer accepting applications" in t
    return {"top": re.sub(r"\n+", " | ", top.strip())[:400], "about": about, "easy": easy, "applied": applied, "closed": closed}
def start_easy():
    r = js("""(()=>{const b=document.querySelector('[aria-label="Easy Apply to this job"]')||[...document.querySelectorAll('button, a')].find(b=>/^(Easy Apply|Continue applying|Continue)$/.test((b.innerText||'').trim()) && b.getClientRects().length && b.getBoundingClientRect().y < 700); if(!b) return null; b.scrollIntoView({block:'center'}); const x=b.getBoundingClientRect(); return [x.x+x.width/2,x.y+x.height/2]})()""")
    if not r: return False
    click_at_xy(*r); wait(3)
    if ea_fields() == "NO ROOT":
        wait(1); click_at_xy(*r); wait(4)
    return ea_fields() != "NO ROOT"
def run(resume_key, max_pages=8, submit=True):
    """Advance through the dialog; returns ('submitted'|'stuck', info)."""
    for _ in range(max_pages):
        f = ea_fields()
        if f == "NO ROOT": return ("closed-dialog", None)
        if _j("(()=>{const r=__ROOT__; return /Select or upload a resume/.test(r.innerText) && !/Review your application/.test(r.innerText) && r.querySelectorAll('input[type=radio]').length>0})()"):
            rs = choose_resume(resume_key)
            if not rs.startswith(("ok", "already")): return ("stuck", "resume: " + rs)
        todo = fill_step(resume_key)
        f = ea_fields()
        if todo: return ("stuck", {"todo": todo, "prog": f["prog"]})
        if "Submit application" in f["btns"]:
            unfollow()
            if not submit: return ("ready", f["prog"])
            ea_click("Submit application"); wait(3)
            t = js("document.body.innerText")
            ok = "Application submitted" in t or "Your application was sent" in t
            js("(()=>{const b=[...document.querySelectorAll('button')].find(b=>/Done|Dismiss/.test(b.innerText||b.getAttribute('aria-label')||'')); if(b) b.click()})()")
            return ("submitted" if ok else "submit-unclear", None)
        nxt = "Review" if "Review" in f["btns"] else ("Next" if "Next" in f["btns"] else None)
        if not nxt: return ("stuck", {"btns": f["btns"]})
        before = f["prog"]; ea_click(nxt); f2 = ea_fields()
        if f2 != "NO ROOT" and f2["prog"] == before and f2["errs"]:
            return ("stuck", {"errs": f2["errs"], "fields": [(x["label"], x.get("value")) for x in f2["fields"]][:12]})
    return ("stuck", "too many pages")
def log(jid, status, note=""):
    try: d = _json.load(open(LOG))
    except Exception: d = {}
    d[jid] = {"status": status, "note": note}
    _json.dump(d, open(LOG, "w"), indent=1)
