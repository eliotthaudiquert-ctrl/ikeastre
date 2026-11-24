import re, sys, urllib.request
for q in sys.argv[1:]:
    t=urllib.request.urlopen(urllib.request.Request(f"https://mixkit.co/free-sound-effects/{q}/",headers={"User-Agent":"Mozilla/5.0"})).read().decode()
    titles=re.findall(r'class="item-grid-card__title">\s*([^<]+?)\s*<',t)
    urls=re.findall(r'https://assets.mixkit.co/active_storage/sfx/(\d+)/\1-preview\.mp3',t)
    u=[]; [u.append(x) for x in urls if x not in u]
    print("##",q); [print("  ",i,ti) for i,ti in zip(u,titles[:14])]
