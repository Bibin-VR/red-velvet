# LinkedIn Easy Apply helpers (run inside wine-view)
import json as _json
ROOT = "(()=>{const h=[...document.querySelectorAll('h2,h3')].find(e=>/^Apply to /.test(e.innerText.trim())); return h? (h.closest('[role=dialog],dialog,[aria-modal],.artdeco-modal,div[class*=modal]')||h.parentElement.parentElement.parentElement) : null})()"
def _j(src, **kw):
    src = src.replace("__ROOT__", ROOT)
    for k, v in kw.items(): src = src.replace("__" + k.upper() + "__", _json.dumps(v))
    return js(src)
def ea_fields():
    return _j("""(()=>{const r=__ROOT__; if(!r) return 'NO ROOT';
      const out=[];
      r.querySelectorAll('input, select, textarea, fieldset').forEach(e=>{
        if(e.tagName==='FIELDSET'){ const l=e.querySelector('legend'); let full=(l?l.innerText:'').trim();
          if(!full){ const pv=e.previousElementSibling; full=(pv?pv.innerText:'').trim(); }
          if(!full){ const pt=(e.parentElement?e.parentElement.innerText:''); full=pt.split('\\n')[0].trim(); }
          const radios=[...e.querySelectorAll('input[type=radio],input[type=checkbox]')].map(i=>{const lb=r.querySelector('label[for="'+CSS.escape(i.id)+'"]')||i.closest('label'); let t=(lb?lb.innerText:'').trim(); if(!t){ t=(i.parentElement?i.parentElement.innerText:'').trim(); } if(!t){ const g=i.parentElement&&i.parentElement.parentElement; t=(g?g.innerText:'').trim(); } if(!t) t=i.value; return {id:i.id, text:t, checked:i.checked}});
          out.push({kind:'fieldset', id:e.id, req:/[*]\\s*$|required/i.test(full)||!!e.querySelector('[required],[aria-required=true]'), label:full.slice(0,300), radios, opts:radios.map(x=>x.text+(x.checked?' [x]':''))}); return; }
        if(e.closest('fieldset') && (e.type==='radio'||e.type==='checkbox')) return;
        if(e.type==='hidden' || e.type==='file') return;
        const lb = e.id ? r.querySelector('label[for="'+CSS.escape(e.id)+'"]') : null;
        const full=(lb?lb.innerText:(e.getAttribute('aria-label')||'')).trim();
        out.push({kind:e.tagName.toLowerCase()+(e.type?':'+e.type:''), id:e.id, req:/[*]\\s*$/.test(full)||e.required||e.getAttribute('aria-required')==='true', label:full.slice(0,300),
                  value: e.tagName==='SELECT' ? (e.selectedOptions[0]||{}).text : e.value,
                  opts: e.tagName==='SELECT' ? [...e.options].map(o=>o.text.trim()).slice(0,12) : undefined});
      });
      const btns=[...r.querySelectorAll('button')].map(b=>(b.innerText||b.getAttribute('aria-label')||'').trim()).filter(Boolean);
      const m=r.innerText.match(/\\d+\\/\\d+ pages|\\d+%/); 
      const errs=[...r.querySelectorAll('[role=alert], .artdeco-inline-feedback--error')].map(e=>e.innerText.trim()).filter(Boolean);
      return {prog: m?m[0]:'', fields: out, btns, errs};})()""")
def ea_click(text):
    r = _j("""(()=>{const r=__ROOT__; const b=[...r.querySelectorAll('button')].find(b=>(b.innerText||b.getAttribute('aria-label')||'').trim()===__T__); if(!b) return null; b.scrollIntoView({block:'center'}); const x=b.getBoundingClientRect(); return [x.x+x.width/2, x.y+x.height/2]})()""", t=text)
    if not r: return False
    click_at_xy(*r); wait(2); return True
def ea_select(sel_id, text):
    return _j("""(()=>{const s=document.getElementById(__ID__); const o=[...s.options].find(o=>o.text.trim()===__T__); if(!o) return 'NOOPT'; s.value=o.value; s.dispatchEvent(new Event('change',{bubbles:true})); s.dispatchEvent(new Event('input',{bubbles:true})); return s.selectedOptions[0].text})()""", id=sel_id, t=text)
def ea_radio(fieldset_id, text):
    r = _j("""(()=>{const f=document.getElementById(__ID__); const i=[...f.querySelectorAll('input[type=radio],input[type=checkbox]')].find(i=>{const lb=document.querySelector('label[for="'+CSS.escape(i.id)+'"]'); return (lb?lb.innerText:i.value).trim()===__T__}); if(!i) return null; const lb=document.querySelector('label[for="'+CSS.escape(i.id)+'"]')||i; lb.scrollIntoView({block:'center'}); const x=lb.getBoundingClientRect(); return [x.x+Math.min(12,x.width/2), x.y+x.height/2]})()""", id=fieldset_id, t=text)
    if not r: return 'NOOPT'
    click_at_xy(*r); wait(0.6); return 'ok'
def ea_text(el_id, text):
    fill_input("#" + el_id.replace(":", "\\\\:"), text) if False else fill_input('[id="%s"]' % el_id, text)
    return js("document.getElementById(%s).value" % _json.dumps(el_id))

def ea_radio_id(radio_id):
    r = _j("""(()=>{const i=document.getElementById(__ID__); if(!i) return null; let el=document.querySelector('label[for="'+CSS.escape(i.id)+'"]'); if(!el || !el.getBoundingClientRect().width){ el=(i.parentElement&&i.parentElement.parentElement)||i; } el.scrollIntoView({block:'center'}); const x=el.getBoundingClientRect(); return [x.x+Math.min(12,x.width/2), x.y+x.height/2]})()""", id=radio_id)
    if not r: return 'NOEL'
    click_at_xy(*r); wait(0.6)
    return 'clicked'
