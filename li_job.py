import re, json
import os
DET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_details.json")
def li_job(jid):
    goto_url(f"https://www.linkedin.com/jobs/view/{jid}/"); wait_for_load(); wait(2.5)
    info = js("""(()=>{
      const t = s => { const e=document.querySelector(s); return e? e.innerText.trim().replace(/\\s+/g,' ') : '' };
      const btns = [...document.querySelectorAll('button, a')].map(b=>(b.innerText||b.getAttribute('aria-label')||'').trim()).filter(x=>/apply/i.test(x)).slice(0,6);
      const desc = t('#job-details') || t('.jobs-description__content') || t('.jobs-box__html-content') || t('article');
      return {title: t('h1'), top: t('.job-details-jobs-unified-top-card__primary-description-container') || t('.job-details-jobs-unified-top-card__tertiary-description-container'),
              company: t('.job-details-jobs-unified-top-card__company-name'), btns, applied: /Applied\\s/.test(document.body.innerText.slice(0,6000)),
              closed: /No longer accepting applications/i.test(document.body.innerText), desc: desc.slice(0,5000)};})()""")
    info["yrs"] = sorted(set(re.findall(r'(\d+\s*(?:\+|-|–|to)?\s*\d*\+?\s*(?:years|yrs))', info.get("desc",""), re.I)))[:6]
    info["easy"] = any("Easy Apply" in b for b in info["btns"])
    try: det = json.load(open(DET))
    except Exception: det = {}
    det[jid] = info; json.dump(det, open(DET, "w"), indent=1)
    return info
