import re,glob,itertools,math
pts=[]
for f in glob.glob('probe/*.html'):
    m=re.search(r'dm_(\d+)_agn_(\d+)_low_(\d+)_medium_(\d+)_high_(\d+)',f)
    t=open(f,encoding='utf-8',errors='replace').read()
    s=re.search(r'score is: (\d+)',t)
    if not m or not s: continue
    dm,agn,lo,me,hi=map(int,m.groups())
    if lo+me+hi==0: continue
    pts.append((dm,agn,lo,me,hi,int(s.group(1))))
print(len(pts),'points')
def model(p,kdm,idm,kst,il,im,ih,kagn,rnd):
    dm,agn,lo,me,hi,_=p; tot=lo+me+hi
    v=100-kdm*abs(dm/100-idm)-(0 if agn==2 else kagn)-kst*(abs(lo/tot-il)+abs(me/tot-im)+abs(hi/tot-ih))
    return (round(v) if rnd else math.floor(v))
best=None
for kdm in [33,34,35,36]:
  for idm in [.82,.83,.84,.85]:
    for kst in [9,10,11]:
      for il in [.38,.40,.42]:
        for im in [.33,.35,.37]:
          ih=round(1-il-im,2)
          for kagn in [17,18,19]:
            for rnd in [0,1]:
              err=sum(abs(model(p,kdm,idm,kst,il,im,ih,kagn,rnd)-p[5]) for p in pts)
              mx=max(abs(model(p,kdm,idm,kst,il,im,ih,kagn,rnd)-p[5]) for p in pts)
              if best is None or err<best[0]: best=(err,mx,kdm,idm,kst,il,im,ih,kagn,rnd)
print('best total abs err, max err, kdm, idm, kst, il, im, ih, kagn, round:',best)
