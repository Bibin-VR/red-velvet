import urllib.parse, json
def li_search(keywords, extra="&f_AL=true&f_E=2%2C3&f_TPR=r604800", pages=1):
    out = []
    for p in range(pages):
        url = ("https://www.linkedin.com/jobs/search/?keywords=" + urllib.parse.quote(keywords)
               + "&location=India&geoId=102713980" + extra + f"&start={25*p}")
        goto_url(url); wait_for_load(); wait(3)
        # scroll the results list so every card renders
        for i in range(12):
            js("""(()=>{const c=document.querySelector('.jobs-search-results-list, .scaffold-layout__list > div, [class*=jobs-search-results]'); 
                 const li=[...document.querySelectorAll('li[data-occludable-job-id]')]; if(li.length) li[Math.min(li.length-1, %d)].scrollIntoView({block:'center'}); })()""" % (i*3))
            wait(0.4)
        cards = js("""[...document.querySelectorAll('li[data-occludable-job-id]')].map(li=>{
            const q=s=>{const e=li.querySelector(s); return e? e.innerText.trim().replace(/\\s+/g,' '):''};
            const t = li.querySelector('a[href*="/jobs/view/"]');
            return {id: li.getAttribute('data-occludable-job-id'),
                    title: t ? (t.getAttribute('aria-label')||t.innerText).trim().replace(/\\s+/g,' ') : '',
                    company: q('.artdeco-entity-lockup__subtitle'),
                    loc: q('.artdeco-entity-lockup__caption'),
                    meta: q('.job-card-container__footer-wrapper, .job-card-list__footer-wrapper')}})""")
        out += cards
    return out
