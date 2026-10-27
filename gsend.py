# Gmail web compose + attach + send, inside wine-view. Asserts sender, recipient and attachment before Send.
import urllib.parse, time, json, os
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.expanduser("~/.claude/skills/job-apply")
P = json.load(open(os.path.join(HERE, "profile.json")))
ME = P["email"]
RESUME = None  # set per role: os.path.expanduser(P["resumes"][key])
def _xy(sel):
    return js("(()=>{const b=document.querySelector(%r); if(!b) return null; b.scrollIntoView({block:'center'}); const x=b.getBoundingClientRect(); return [x.x+x.width/2, x.y+x.height/2]})()" % sel)
def gsend(to, subject, body, resume_key, send=True):
    global RESUME; RESUME = os.path.expanduser(P["resumes"][resume_key])
    q = urllib.parse.urlencode({"view": "cm", "fs": "1", "tf": "1", "to": to, "su": subject, "body": body}, quote_via=urllib.parse.quote)
    goto_url("https://mail.google.com/mail/u/0/?" + q); wait_for_load(); time.sleep(6)
    title = js("document.title")
    assert ME in title, ("wrong account", title)
    root = cdp("DOM.getDocument", depth=0)["root"]["nodeId"]
    nid = cdp("DOM.querySelector", nodeId=root, selector='input[type=file][name="Filedata"]')["nodeId"]
    assert nid, "no file input"
    cdp("DOM.setFileInputFiles", files=[RESUME], nodeId=nid); time.sleep(3)
    name = RESUME.rsplit("/", 1)[1]
    for _ in range(30):
        t = js("document.body.innerText")
        if name in t and "Uploading" not in t and "%" not in t[t.find(name):t.find(name)+60]: break
        time.sleep(1)
    t = js("document.body.innerText")
    assert name in t, "attachment missing"
    rcpt = js("[...document.querySelectorAll('[data-hovercard-id],[email]')].map(e=>e.getAttribute('email')||e.getAttribute('data-hovercard-id')).join(',')")
    assert to.lower() in (rcpt or "").lower() or to.lower() in t.lower(), ("recipient missing", rcpt)
    if not send: return "ready"
    r = _xy('[role=button][aria-label^="Send"]'); assert r, "no send button"
    click_at_xy(*r); time.sleep(5)
    t = js("document.body.innerText")
    return "sent" if ("Message sent" in t or "Sending" in t or not js("!!document.querySelector('[role=button][aria-label^=\"Send\"]')")) else "unclear"
