import re, sys, urllib.request, html
for q in sys.argv[1:]:
    url=f"https://mixkit.co/free-stock-video/{q}/"
    try: t=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})).read().decode()
    except Exception as e: print(q,"ERR",e); continue
    items=re.findall(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"',t)
    seen=[]; 
    for slug,i in items:
        if i not in [s[1] for s in seen]: seen.append((slug,i))
    print(f"## {q}: "+" | ".join(f"{i}:{s}" for s,i in seen[:30]))
