import re, glob, json, html, os
def clean(h):
    h = re.sub(r'\s+', ' ', h)
    h = re.sub(r"<a\s+([^>]*?)href='([^']*)'", r'<a \1href="\2"', h)
    h = re.sub(r'<a\s+href="(http[^"]*)"(?![^>]*target)', r'<a href="\1" target="_blank" rel="noopener"', h)
    h = re.sub(r'<a href="hologram_example.jpg"[^>]*>here</a>', '<a href="holograms.html">here</a>', h)
    h = re.sub(r'<a href="https://youtu.be/StMziRuZCMA"[^>]*>here</a>', '<a href="holograms.html">here</a>', h)
    h = re.sub(r'<p>\s*</p>', '', h)
    return h.strip()
def pages(t):
    parts = re.split(r"<div id='pg(\d+)' class='apage'>", t)
    out = {}
    for i in range(1, len(parts), 2):
        seg = parts[i+1]
        seg = re.sub(r"<div class='row mybuttons'.*", '', seg, flags=re.S)
        out[int(parts[i])] = seg
    return out
def textblock(seg, nth=0):
    m = re.findall(r"<div class='col-md-12 content'>(.*?)</div>\s*</div>", seg, flags=re.S)
    return clean(m[nth]) if len(m) > nth else ''
def title(seg):
    return html.unescape(re.search(r"<h1 class='sectitle'>(.*?)</h1>", seg).group(1).strip())

galaxies = {}
for f in sorted(glob.glob('gal/*.html')):
    key = os.path.basename(f)[:-5]
    t = open(f, encoding='utf-8', errors='replace').read()
    p = pages(t)
    pie = json.loads(re.search(r'data:\s*(\[[\d,\s]+\])', p[2]).group(1))
    galaxies[key] = {
        'title': title(p[0]),
        'closer': textblock(p[1]),
        'pie': pie,
        'pieText': textblock(p[2]),
        'stars': textblock(p[3]),
        'gas': textblock(p[4]),
        'dm': textblock(p[5]),
    }
    assert all(galaxies[key][k] for k in ('closer','pieText','stars','gas','dm')), key

verdict = {'dm': {}, 'agn': {}, 'sn': {}}
fixed = None
for f in glob.glob('probe/*.html'):
    t = open(f, encoding='utf-8', errors='replace').read()
    m = re.search(r'plots/([LMH])_DM\.([LMH])_AGN\.([LMH])_SN', t)
    if not m: continue
    p = pages(t)
    d, a, s = m.groups()
    verdict['dm'][d] = textblock(p[0]); verdict['agn'][a] = textblock(p[1]); verdict['sn'][s] = textblock(p[2])
    if fixed is None:
        fixed = {}
        for n, k in ((0,'dm'),(1,'gas'),(2,'stars')):
            fixed[k+'Vid'] = clean(re.search(r"<div class='vidtxt'>(.*?)</div>", p[n], flags=re.S).group(1))
            fixed[k+'Holo'] = clean(re.search(r"<div class='holotxt'>(.*?)</div>", p[n], flags=re.S).group(1))
        fixed['galaxy'] = textblock(p[3])
        fixed['titles'] = [title(p[n]) for n in range(7)]
        extra = re.findall(r"<div class='col-md-12 content'>(.*?)</div>\s*</div>", p[5], flags=re.S)
        fixed['extra'] = [clean(x) for x in extra]
        fixed['extraRaw'] = p[5][:200]
        fixed['score'] = p[4]
        fixed['links'] = p[6]
assert all(len(v) == 3 for v in verdict.values()), verdict.keys()
json.dump({'galaxies': galaxies, 'verdict': verdict, 'fixed': fixed}, open('extracted.json', 'w'), indent=1, ensure_ascii=False)
print('galaxies:', list(galaxies))
for k, g in galaxies.items(): print(k, g['title'], g['pie'])
print(json.dumps(verdict, indent=1, ensure_ascii=False)[:6000])
