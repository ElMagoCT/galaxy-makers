import sys, pathlib
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Galaxy Makers</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="static/logo_dm.png">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body data-page="{page}">
<header class="wrap masthead">
  <a class="brand" href="index.html"><img src="static/logo_white.png" alt="Galaxy Makers" width="420" height="190"></a>
  <nav>
    <a href="about.html"{a_about}>About</a>
    <a href="holograms.html"{a_holo}>Holograms</a>
    <a href="credits.html"{a_credits}>Credits</a>
  </nav>
</header>
<main class="wrap">
'''
FOOT = '''</main>
<footer><div class="wrap">
  <img src="static/instlogos/durham.png" alt="Durham University"><img src="static/instlogos/icc.png" alt="Institute for Computational Cosmology"><img src="static/instlogos/leiden.png" alt="Leiden University"><img src="static/instlogos/erc.png" alt="European Research Council"><img src="static/instlogos/eu.png" alt="European Union">
  <p>Galaxy Makers is an outreach project of the Institute for Computational Cosmology, Durham University. This is a fast, static rebuild of <a href="https://www.galaxymakers.org/" target="_blank" rel="noopener">galaxymakers.org</a>; all simulations, movies and text are theirs.</p>
</div></footer>
{scripts}
</body>
</html>
'''
def shell(page, title, desc, body, scripts=''):
    nav = {k: (' aria-current="page"' if page == k else '') for k in ('about', 'holo', 'credits')}
    return HEAD.format(title=title, desc=desc, page=page, a_about=nav['about'], a_holo=nav['holo'], a_credits=nav['credits']) + body + FOOT.format(scripts=scripts)
APP = '<script src="assets/js/data.js"></script>\n<script src="assets/js/app.js"></script>'
pages = {}
pages['index.html'] = shell('home', 'Design your own Universe!', 'Galaxy Makers: make your own galaxy or universe with real cosmological simulations from Durham University.', '''
<h1 class="sectitle">Welcome to Galaxy Makers!</h1>
<p class="lead">Galaxy Makers is a demonstration where you are in control of the Universe. You choose what it's made of and hence how it works! You can also take part through this website; try clicking one of the buttons below! To find out more, check out our <a href="about.html">about page</a>.</p>
<p class="lead">If you are having trouble using the holograms, check out <a href="holograms.html">this page</a> for more information on how to use them and create your own!</p>
<div class="homegrid">
  <a class="homebtn" href="code.html" style="background-image:url(static/code.jpg)"><span>I have a code!</span></a>
  <a class="homebtn" href="universe.html" style="background-image:url(static/uni.jpg)"><span>Create a universe!</span></a>
  <a class="homebtn" href="galaxy.html" style="background-image:url(static/randomgal.jpg)"><span>Make a random galaxy!</span></a>
  <a class="homebtn" href="universe.html?random=1" style="background-image:url(static/randomuni.jpg)"><span>Make a random universe!</span></a>
</div>
<h1 class="sectitle">As seen at...</h1>
<div class="card seen">
  <a href="https://royalsociety.org/science-events-and-lectures/2021/summer-science-exhibition/" target="_blank" rel="noopener"><img class="noborder" src="static/instlogos/summer-science-2021.png" alt="Royal Society Summer Science 2021"></a>
  <a href="https://royalsociety.org/science-events-and-lectures/2016/summer-science-exhibition/" target="_blank" rel="noopener"><img class="noborder" src="static/instlogos/rsc.png" alt="Royal Society Summer Science Exhibition 2016"></a>
</div>
<p class="lead">Follow the team on Twitter: <a href="https://twitter.com/DarkerMatters" target="_blank" rel="noopener">@DarkerMatters</a></p>
''')
def knob(name, title, text, color):
    return f'''<div><h2>{title}</h2><div class="card"><p>{text}</p>
<div class="knob"><input type="range" name="{name}" min="0" max="100" value="75" style="accent-color:{color}"><output for="{name}">75</output></div></div></div>'''
pages['universe.html'] = shell('universe', 'Create a Universe', 'Choose how much dark matter, black-hole power and massive stars your universe has, then watch the simulation.', '''
<div id="makerwrap">
<h1 class="sectitle">Create a Universe</h1>
<p class="lead">Here you can create a Universe. Simply put in the parameters you want below and watch the computer get to work!</p>
<form id="maker">
<div class="maker">
''' + knob('dm', 'Dark Matter', "The amount of dark matter in your universe is key. Dark matter is what allows galaxies to form. Without it, there is not enough gravitational force on the gas to keep it from separating.", '#7E317B') + '''
<div><h2>AGN Feedback</h2><div class="card"><p>This one can be a little tricky. At the centre of galaxies, there is a supermassive black hole. When gas falls onto this hole, it heats up to a very high temperature. This setting decides how much of that hot gas is thrown back out into the galaxy when this happens.</p>
<div class="agn">
<input type="radio" name="agn" value="1" id="agn1" checked><label for="agn1">Low</label>
<input type="radio" name="agn" value="2" id="agn2"><label for="agn2">Medium</label>
<input type="radio" name="agn" value="3" id="agn3"><label for="agn3">High</label>
</div></div></div>
</div>
<div class="maker three">
''' + knob('low', 'Low Mass Stars', "Low mass stars have very long lifetimes. They hang around forever and don't really do anything interesting.", '#b8b230') + knob('medium', 'Medium Mass Stars', "Medium mass stars, like the Sun, have medium lifetimes and make up a reasonable amount of the stellar population.", '#AA2B4A') + knob('high', 'High Mass Stars', "High mass stars have a very short lifetime. They burn all of their fuel really quickly and then explode in a supernova! Too many of these and your galaxies will blow themselves apart.", '#006388') + '''
</div>
<div class="btnrow" style="margin-top:1.5rem">
  <button type="submit" class="btn big">Simulate!</button>
  <button type="button" class="btn big ghost" id="randomize" style="flex:0 1 14rem;background:var(--paper)">Random settings</button>
</div>
</form>
</div>
<div id="result" class="hidden"></div>
<p class="btnrow" id="againrow"><button type="button" class="btn ghost hidden" id="again" style="background:var(--paper);flex:0 1 auto">&larr; Make another universe</button></p>
''', APP)
pages['galaxy.html'] = shell('galaxy', 'Your Galaxy', 'A random galaxy from the EAGLE simulation, compared with a real one.', '''
<div id="result"></div>
<p class="btnrow"><button type="button" class="btn ghost" id="another" style="background:var(--paper);flex:0 1 auto">Make another random galaxy</button></p>
''', APP)
pages['code.html'] = shell('code', 'Enter your code', 'Enter a Galaxy Makers code to get back to your galaxy or universe.', '''
<h1 class="sectitle">Enter your code:</h1>
<form id="codeform" class="card">
  <label for="code">Universe codes look like <span class="code">U84-2-40-35-25</span>; galaxy codes are the galaxy's name, such as <span class="code">spiral</span>.</label>
  <div class="btnrow"><input class="code" id="code" name="code" type="text" autocomplete="off" autofocus style="flex:1;font-size:1.3rem;padding:.6rem;border:2px solid #999;border-radius:4px"><button type="submit" class="btn" style="flex:0 1 auto">Go</button></div>
  <p id="codemsg" class="hidden" style="color:var(--wine);font-weight:700"></p>
</form>
''', APP)
exhibit = ''.join(f'<img src="content/exhibit_photos/IMG_{n}.jpg" alt="People using the Galaxy Makers exhibit" loading="lazy">' for n in (7796, 7797, 7818, 7855, 7863, 7865))
pages['about.html'] = shell('about', 'About', 'About the Galaxy Makers exhibit, the EAGLE simulation and the Institute for Computational Cosmology.', '''
<h1 class="sectitle">About Galaxy Makers</h1>
<div class="card">
<p>The Galaxy Makers exhibit, brought to you by Durham University, aims to explain recent breakthroughs in our understanding of how galaxies were made. Participants are able to make their own holographic galaxies, run their own computer simulations and take a virtual reality tour of the cosmos!</p>
<div class="cols">''' + exhibit + '''</div>
<p>Astronomers and cosmologists have recently made real progress in understanding how galaxies were made by using computer simulations. The computer simulation is the cosmologist's laboratory bench. Scientists usually learn how things work by doing experiments, but real galaxies are simply too big to build in the laboratory! We use computers to create virtual universes where we apply the laws of physics and our predictions or "assumptions" about various aspects of the universe, such as what happens when stars explode and if supermassive black holes are powerful enough to heat and remove gas from galaxies. Time is then rapidly sped up so that we can follow the life story of the galaxies in our simulated universe. If galaxies in the simulated universe look like those in the real universe, then our assumptions were correct. If it doesn't, then something was wrong.</p>
<p>The Galaxy Makers exhibit contains interactive demonstrations, to suit all ages, so that participants can get a "hands-on" experience of what it is like to work with computer simulations of the universe. There are three main activities which aim to cover three main questions:</p>
<p><b>1. What is a galaxy?</b> Our <i>Galaxy Maker</i> activity allows the participants to make their own holographic galaxy by following various galaxy recipes to weigh out the "components" (ingredients) of different galaxies. After measuring out these components and pouring them into the various chutes of the <i>Galaxy Maker</i>, a hologram will appear in front of them. Some of the messages we aim to portray with this activity are that galaxies are vast collections of stars, gas and dark matter and that galaxies come in different shapes and sizes; for example, our Milky Way is an example of a large <i>spiral galaxy</i>.</p>
<p><b>2. What happens during the life of a galaxy?</b> Our virtual reality <i>Tour of the Cosmos</i> allows participants to submerge themselves right inside a revolutionary computer simulation called "EAGLE". This unique experience flies the passengers through space and time whilst the audio commentary talks you through some of the key events of creating a galaxy.</p>
<p><b>3. How do we simulate galaxies?</b> Our <i>Create a Universe</i> activity allows participants to run their own computer simulations. The participants use various knobs and levers to make their own "assumptions" about the universe. For example, it is possible to change the amount of energy released by black holes. Once these decisions have been made the computer simulation is projected as a hologram. If these assumptions are unrealistic you may end up with a universe that is too hot or perhaps with no galaxies at all! Participants will get to learn about how the experts have used "experiments" to understand how the universe works.</p>
<p>All of our activities have an online version where you can try for yourself whether you have been to the Galaxy Makers exhibit or not.</p>
<p>The exhibition video below explains how computer simulations are used to understand how galaxies are made and introduces some of the Galaxy Makers team. They also explain why they think it is exciting to try to understand "How do you build a galaxy?"</p>
<div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/BgkHcoJ5tNI" title="Galaxy Makers exhibition video" loading="lazy" allowfullscreen></iframe></div>
</div>
<h1 class="sectitle">About The Simulation &amp; Institute</h1>
<div class="card">
<p>The Institute for Computational Cosmology (ICC) was established in 2002, when the Ogden Centre for Fundamental Physics was established at Durham University. The ICC addresses some of the biggest questions in science: What is the dark matter that dominates the matter content of the Universe? Why is the expansion of the Universe speeding up? How did galaxies form and evolve? These questions are tackled using computer simulations and by mapping the content of the universe in huge galaxy surveys, such as DESI and Euclid. The ICC is the lead UK member of the Virgo Consortium, an international collaboration which carries out simulations of structure formation in the universe, and is the host to the Cosmology Machine, which is part of the UK's national astrophysics computer, DiRAC-II. Along with the Centre for Extragalactic Astronomy, Durham represents one of the largest concentrations of expertise in extragalactic astronomy in Europe.</p>
<img src="content/supercomputer.jpg" alt="The COSMA-V supercomputer at Durham" loading="lazy">
<p><small>This supercomputer called COSMA-V does not just look pretty, it is very powerful. In one second, COSMA-V can do more than 139 trillion additions and multiplications. COSMA-V can store the same data as 80,000 iPods, corresponding to 1.5 million feature-length movies. Researchers at the ICC (Durham University) make extensive use of COSMA-V to perform state-of-the-art cosmological simulations.</small></p>
<p>The EAGLE (Evolution and Assembly of GaLaxies and their Environment) simulation project represents a major breakthrough in our efforts to understand how galaxies form and evolve in a Universe in which the matter content is dominated by dark matter. Perhaps surprisingly, modelling the "normal" matter in the Universe turns out to be far more difficult that following the evolution of the dark matter. The important physics for the dark matter is gravity. The equation describing the law of gravity was published in 1686. The normal matter, on the other hand, experiences a much wider range of effects. For many of these we cannot write down the equation that describes them. One spectacular process which helps to shape galaxies is the death of some stars in a supernova. This event puts huge amounts of energy into the gas within a galaxy and can blast some of this material away before it can form stars. The challenge dealt with by EAGLE was to model these processes for a large sample of galaxies, so that we can see how they affect galaxies of different sizes. This requires a huge supercomputer. The simulation took more than six million hours of CPU time on machines in Durham and Paris. The result is a collection of 10,000 galaxies like the Milky Way or bigger that we can compare to galaxies in the real Universe.</p>
<p>Find out more:</p>
<ul>
<li><a href="https://icc.dur.ac.uk" target="_blank" rel="noopener">ICC</a></li>
<li><a href="https://icc.dur.ac.uk/Eagle/" target="_blank" rel="noopener">EAGLE simulation</a></li>
<li><a href="https://virgo.dur.ac.uk" target="_blank" rel="noopener">Virgo Consortium</a></li>
<li><a href="https://www.durham.ac.uk/research/institutes-and-centres/extragalactic-astronomy/" target="_blank" rel="noopener">Centre for Extragalactic Astronomy</a></li>
</ul>
<p>You can also watch this video about searching for black holes in the EAGLE simulation:</p>
<div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/DsDK_mk8qn4" title="Searching for black holes in EAGLE" loading="lazy" allowfullscreen></iframe></div>
</div>
''')
def ul(names): return '<ul>' + ''.join(f'<li>{n}</li>' for n in names) + '</ul>'
pages['credits.html'] = shell('credits', 'Credits', 'The people behind Galaxy Makers.', '''
<h1 class="sectitle">Credits</h1>
<div class="card credits">
<h2>Primary Creators and Developers</h2>''' + ul(['Carlton Baugh','Chris Harrison','Jaime Salcido','Stuart McAlpine','Josh Borrow','Sownak Bose','Helen Johnson','Andrew Griffin','Jacob Kegerreis','Claudio LLinares','Oliver Newton','Andrew Robertson','Greg Robson','James Trayford','James Willis','Richard Massey','Benjamin Shaw']) + '''
<h2>Technical Team</h2>''' + ul(['Andrew Davies','Kevin Ring','Sabine Schindler','Andrew Hunter','Stephen Lishman','Andrew Crosby','Ryan Ellison','Malcom Robertshaw','Khristian Whatcott']) + '''
<h2>Other developers</h2>''' + ul(['Stephanie Bartle','Richard Bower','Cameron Johnston','Carlos Frenk','Lydia Heck','Alan Lotts','Matthieu Schaller','Tom Theuns','Jiuyang Zhao','The Virgo Consortium']) + '''
<h2>Other demonstrators</h2>''' + ul(['Paddy Alton','Stefan Arridge','Marius Cautun','Shaun Cole','Will Cowley','Tim Green','Adrian Jenkins','Aaron Ludlow','Nuala McCullagh','Simon Morris','Jascha Schewtschenko','Johannes Schwinn','Difu Shi','Ruth Ye Zhou']) + '''
</div>
<h1 class="sectitle">Institutions</h1>
<div class="card seen">
<img class="noborder" src="static/instlogos/durham.png" alt="Durham University"><img class="noborder" src="static/instlogos/icc.png" alt="ICC"><img class="noborder" src="static/instlogos/leiden.png" alt="Leiden University"><img class="noborder" src="static/instlogos/erc.png" alt="ERC"><img class="noborder" src="static/instlogos/eu.png" alt="EU">
</div>
''')
steps = [("Print out the template and tape your clear plastic down onto it to hold it in place. If this is going to be some trouble, you can trace the template with a felt tip. Cut out the outer shape of the template with your craft knife or scissors."),
 ("Score along the marked edges with your scissors or craft knife (it helps to use a ruler to keep your knife/scissors straight!). Make sure not to cut through the plastic, just to mark it. This will make it easier to fold later."),
 ("Fold along the scored edges and build the pyramid. Close the loop with some sticky tape."),
 ("Place on your smartphone and watch the holograms!")]
pages['holograms.html'] = shell('holo', 'Using the Holograms', 'How to use and build the Galaxy Makers hologram pyramid.', '''
<h1 class="sectitle">Using the Holograms</h1>
<div class="card">
<p>Here's a video explaining how to use our hologram pyramids:</p>
<div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/StMziRuZCMA" title="How to use the hologram pyramid" loading="lazy" allowfullscreen></iframe></div>
</div>
<h1 class="sectitle">Creating Your Own</h1>
<div class="card">
<p>Haven't been able to make it to one of our events? Would you still like a pyramid to play our holograms? You can make your own at home with these instructions!</p>
<h2>Downloads</h2>
<p>You can download a template to print out that will help you create your own <a href="content/template.pdf">here</a> and if you are lucky enough to be able to print on acetate you can download an extra template <a href="content/acetate_template.pdf">here</a>.</p>
<p>You can find illustrated instructions below, or on your template sheet.</p>
<h2>Instructions</h2>
<p>You will need</p>
<ul>
<li>A piece of plastic sheeting (about 0.5mm thick). You could use some left over packaging!</li>
<li>A printer (for the template!)</li>
<li>Scissors or preferably a craft knife</li>
<li>Clear sticky tape</li>
<li>A smartphone or tablet to play the holograms</li>
</ul>
''' + ''.join(f'<h3>Step {i+1}</h3><img class="noborder" src="content/create_{i+1}.png" alt="Step {i+1}" loading="lazy"><p>{s}</p>' for i, s in enumerate(steps)) + '''
</div>
''')
for name, html in pages.items():
    pathlib.Path(name).write_text(html)
    print(name, len(html))
