import json, re, html
S='/private/tmp/claude-503/-Users-user-Documents-Workspace/509f008f-5a9f-4363-9dad-0ced04464794/scratchpad/gm/'
X=json.load(open(S+'extracted.json'))
t=open(S+'probe/dm_10_agn_2_low_75_medium_75_high_75.html',encoding='utf-8',errors='replace').read()
parts=re.split(r"<div id='pg(\d+)' class='apage'>",t); p={int(parts[i]):parts[i+1] for i in range(1,len(parts),2)}
def clean(h):
    h=re.sub(r'\s+',' ',h); h=re.sub(r'<p>\s*</p>','',h)
    h=re.sub(r"<a\s+href='([^']*)'",r'<a href="\1"',h)
    h=re.sub(r'<a href="(http[^"]*)"(?![^>]*target)',r'<a href="\1" target="_blank" rel="noopener"',h)
    return h.strip()
# pg5 extra blocks in order
seg=re.sub(r"<div class='row mybuttons'.*",'',p[5],flags=re.S)
extra=[]
for m in re.finditer(r"<div class='col-md-12 content lr'>(.*?)</div>\s*</div>",seg,flags=re.S):
    inner=m.group(1).strip()
    im=re.search(r"plots/.*?\.(\d)\.png",inner)
    if im: extra.append({'plot':int(im.group(1))})
    else: extra.append({'html':clean(inner)})
assert len(extra)==8, len(extra)
# pg3 galaxy text, pg4 thanks
gal=clean(re.search(r"<div class='col-md-12 content'>(.*?)</div>\s*</div>",p[3],flags=re.S).group(1))
thanks=clean(re.search(r"<div class='col-md-12 content'>(.*?)</div>\s*</div>",p[4],flags=re.S).group(1))
F=X['fixed']
data={
 'galaxies':X['galaxies'],
 'verdict':X['verdict'],
 'universe':{
   'titles':F['titles'],
   'dmVid':F['dmVid'],'dmHolo':F['dmHolo'],'gasVid':F['gasVid'],'gasHolo':F['gasHolo'],'starsVid':F['starsVid'],'starsHolo':F['starsHolo'],
   'galaxyHolo':"<p>This video works with the hologram projector given out at the Galaxy Makers exhibition. You can find a little tutorial on how to use it <a href=\"holograms.html\">here</a>.</p>",
   'galaxy':gal,'thanks':thanks,'extra':extra,
 },
 'links':{
   'apod':{'href':'https://apod.nasa.gov','img':'static/logos/NASA.png','alt':'APOD','text':'The Astronomy Picture of the Day shows you a new image every day from the world of astronomy, along with an explanation of what it is written by real astronomers.'},
   'spacescoop':{'href':'https://www.spacescoop.org','img':'static/logos/spacescoop.jpg','alt':'Space Scoop','text':'Space Scoop is a science news website for kids. They cut out all of the confusing jargon and just give you the interesting news from scientists around the world.'},
   'galaxyzoo':{'href':'https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/','img':'static/logos/galaxyzoo.png','alt':'Galaxy Zoo','text':'Fancy becoming a citizen scientist? Check out Galaxy Zoo, where you can check out cool images of galaxies and help real astronomers by classifying them.'},
   'codecademy':{'href':'https://www.codecademy.com','img':'static/logos/codecademy.jpg','alt':'Codecademy','text':'Interested in learning to code and create simulations of your own? Codecademy is a great place to start the process.'},
   'eagle':{'href':'https://icc.dur.ac.uk/Eagle','img':'static/logos/eagle.png','alt':'EAGLE','text':'If you would like to find out more information about the simulation and software that produced these images, check out the official EAGLE project website here.'},
 },
 'galaxyPie':{'labels':['Dark Matter','Old Stars','New Stars','Gas & Dust'],'colors':['#7E317B','#AA2B4A','#006388','#968E85']},
 'galaxyCommon':{
   'intro':"<p>Congratulations on making a galaxy! You can watch a fly-around video of your model galaxy here. If you have a pyramid projector and you are viewing this on your phone then select \"hologram video\" and play in full-screen mode. You need to make sure your phone is playing the movie horizontally (i.e., hold the phone in front you horizontally before laying it flat). The holograms look best in a dark room with the phone brightness on full (see <a href=\"holograms.html\">here</a> for an example of how to use your pyramid). To find out more about your galaxy and how it compares to real galaxies use the buttons below.</p>",
   'holo':"<p>This video works with the hologram projector given out at the Galaxy Makers exhibition. You can find a little tutorial on how to use it <a href=\"holograms.html\">here</a>.</p>",
   'titles':['','Take a closer look','What is inside my galaxy?','Learn more about the stars','What about the gas?','What about the dark matter?','Relevant links'],
 }
}
out='// Generated from galaxymakers.org page text by tools/gen_data.py - do not edit by hand.\nwindow.GM_DATA = '+json.dumps(data,ensure_ascii=False,indent=1)+';\n'
open('/Users/user/Documents/Workspace/galaxy-makers/assets/js/data.js','w').write(out)
print(len(out),'bytes'); print([e.get('plot',e.get('html','')[:60]) for e in extra])
