#!/usr/bin/env python3
"""Builds the static pages of the portfolio. Run from the site root:  python3 tools/build.py
Texts live in this file; the output is plain HTML that can also be edited by hand."""
import os, html

LINKEDIN = "https://www.linkedin.com/in/andrii-shnayder-a15bb8440/"
EMAIL = ""   # put the address here and rebuild; while empty, no e-mail is shown anywhere

ICONS = {
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>', 'back':'<path d="M19 12H5M11 6l-6 6 6 6"/>',
 'ext':'<path d="M7 17 17 7M9 7h8v8"/>', 'user':'<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-4 4-5.5 7-5.5s6 1.5 7 5.5"/>',
 'cal':'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8 3v4M16 3v4"/>',
 'tool':'<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3L15 12l-3-3z"/>',
 'pulse':'<path d="M3 12h4l2-6 4 12 2-6h6"/>', 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.800 0 18M12 3c-3 3.200-3 14.800 0 18"/>',
 'screen':'<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>', 'check':'<path d="M5 12.5l4.500 4.500L19 7.500"/>',
 'pin':'<path d="M12 21s-6-5.300-6-10a6 6 0 1 1 12 0c0 4.700-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>',
 'in':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 11v5M8 8v.01M12 16v-5M12 13a2 2 0 0 1 4 0v3"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>', 'flag':'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 'box':'<path d="M4 8 12 4l8 4v8l-8 4-8-4z"/><path d="M4 8l8 4 8-4M12 12v8"/>', 'chat':'<path d="M5 5h14v10H9l-4 4z"/>',
 'note':'<path d="M9 18V6l10-2v12"/><circle cx="6.500" cy="18" r="2.500"/><circle cx="16.500" cy="16" r="2.500"/>',
 'phone':'<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>', 'print':'<path d="M7 9V4h10v5M7 17H5a1 1 0 0 1-1-1v-5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a1 1 0 0 1-1 1h-2"/><rect x="7" y="14" width="10" height="6"/>',
 'eye':'<path d="M2.500 12S6 5.500 12 5.500 21.500 12 21.500 12 18 18.500 12 18.500 2.500 12 2.500 12z"/><circle cx="12" cy="12" r="2.500"/>',
}
def ico(n): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONS[n]}</svg>'
def ext(href, text, cls="go"):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{text}{ico("ext")}<span class="sr"> (opens in a new tab)</span></a>'

def vid(R, src, cls="wide", extra="", alt=""):
    return (f'<div class="frame {cls}"{extra}><video data-auto muted loop playsinline preload="none" '
            f'poster="{R}assets/work/{src}.jpg" aria-label="{alt}"><source src="{R}assets/work/{src}.mp4" type="video/mp4"></video></div>')
def img(R, src, alt, cls="wide", extra="", w=1920, h=1200):
    return f'<div class="frame {cls}"{extra}><img src="{R}assets/work/{src}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>'

def page(R, path, title, desc, body, tone="", current=""):
    t = f' data-tone="{tone}"' if tone else ''
    cur = lambda k: ' aria-current="page"' if current == k else ''
    mail = f'<a class="go" href="mailto:{EMAIL}">{ico("mail")}{EMAIL}</a>' if EMAIL else ''
    doc = f'''<!doctype html>
<html lang="en"{t}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://lgf5411.github.io/Portfolia/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{R}assets/fonts/schibsted-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{R}assets/fonts/newsreader-latin-wght-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="me" href="{R}index.html">Andrii Shnayder</a>
  <nav aria-label="Main"><a href="{R}index.html#work"{cur('work')}>Work</a><a href="{R}about/index.html"{cur('about')}>About</a>{ext(LINKEDIN, "LinkedIn", "")}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="say">
    <p class="q">Have a question your product should answer better?</p>
    <p class="lead">I am looking for a junior product, UX/UI or web design role, or an internship. In Tallinn or remote, available now.</p>
    <div class="links">{ext(LINKEDIN, ico("in") + "Write to me on LinkedIn", "go fill")}{mail}</div>
  </div>
  <div class="legal">
    <p>Bolt and Tallink projects are independent concepts, not affiliated with or endorsed by those companies.</p>
    <p>© 2026 Andrii Shnayder · Tallinn</p>
  </div>
</div></footer>
<script src="{R}assets/js/site.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf8').write(doc)

# ------------------------------------------------------------------ projects
P = [
 dict(slug='lobby', tone='lobby', n='01', name='Lobby', kind='My own product · Windows app and browser',
      q='“Can we talk and still hear the same track?”',
      a='A voice app for playing with friends. Everyone hears the same music, and it steps back the moment someone speaks.',
      meta=[('user','Idea, product decisions, UX and UI'),('pulse','Version 0.14, in testing with friends since November 2026'),('globe','7 interface languages')]),
 dict(slug='bolt', tone='bolt', n='02', name='Answers before the app', kind='bolt.eu redesign · unofficial concept',
      q='“What will my airport ride cost?”',
      a='Four public pages of bolt.eu, rebuilt so each one answers the visitor’s question first and then opens the app with the trip already filled in.',
      meta=[('user','Solo: content audit, UX, UI, coded prototype'),('screen','4 product pages and a launch page'),('flag','Independent concept, October 2026')]),
 dict(slug='tallink', tone='tallink', n='03', name='Pane detsember pausile', kind='Tallink Christmas campaign · unofficial concept',
      q='“Can December wait for a day?”',
      a='One idea carried through a landing page, a 15-second film, seven banner formats, print and a newsletter, in Estonian and English.',
      meta=[('user','Solo: idea, copy, design, production'),('print','Web, video, banners, A3 poster, A5 flyer, e-mail'),('flag','Independent concept, November 2026')]),
 dict(slug='minu-vahetus', tone='vahetus', n='04', name='Minu vahetus', kind='Shift schedule for shop staff · concept',
      q='“When do I work tomorrow, and what will I be doing?”',
      a='The paper schedule and the task card on the back-room wall, moved to the phone. It comes from my own job in a supermarket.',
      meta=[('user','Solo: problem from my own workplace, UX, UI, prototype'),('phone','Clickable prototype, Estonian and Russian'),('flag','Concept with sample data, November 2026')]),
]
BY = {p['slug']: p for p in P}

def home_media(R, p):
    s = p['slug']
    if s == 'lobby':
        inner = vid(R, 'lobby/call', alt='Lobby call screen: four friends in a pixel forest at night, a track playing in the header')
    elif s == 'bolt':
        inner = '<div class="duo">' + vid(R, 'bolt/rides', alt='Bolt Rides page concept: a fare range for the visitor’s own route') + vid(R, 'bolt/phone', 'phone', ' data-par="46"', 'The same concept on a phone') + '</div>'
    elif s == 'tallink':
        inner = '<div class="duo">' + img(R, 'tallink/landing', 'Campaign landing page: a ferry at night whose lights reflect on the sea as a pause sign', w=1440, h=900) + vid(R, 'tallink/paus-916', 'phone', ' data-par="46"', 'The 15-second campaign film in vertical format') + '</div>'
    else:
        inner = '<div class="duo left">' + img(R, 'minu-vahetus/manager-d', 'Manager view: who has seen the schedule, pending requests, sick notes') + vid(R, 'minu-vahetus/flow', 'phone', ' data-par="46"', 'Worker view on a phone: confirming the week and asking for a day off') + '</div>'
    return f'<a class="media" href="{R}work/{s}/index.html" data-cursor="Open case" data-r="media" aria-label="Open the {p["name"]} case">{inner}</a>'

def build_home():
    R = ''
    idx = ''.join(f'<li><a href="#{p["slug"]}"><span class="n">{p["n"]} · {p["name"]}</span><span class="t">{p["q"]}</span></a></li>' for p in P)
    rows = ''
    for p in P:
        meta = ''.join(f'<li>{ico(i)}<span>{t}</span></li>' for i, t in p['meta'])
        rows += f'''
<section class="proj" id="{p['slug']}" data-tone-zone="{p['tone']}"><div class="wrap">
  <div class="txt">
    <p class="kicker" data-r><i>{p['n']}</i><b>{p['name']}</b></p>
    <p class="q" data-r style="--i:1">{p['q']}</p>
    <h2 class="sr">{p['name']}</h2>
    <p class="lead" data-r style="--i:2">{p['a']}</p>
    <ul class="meta" data-r style="--i:3">{meta}</ul>
    <a class="go" data-r style="--i:4" href="work/{p['slug']}/index.html">Read the case{ico('arrow')}</a>
  </div>
  {home_media(R, p)}
</div></section>'''
    body = f'''
<section class="wrap hero">
  <div class="say">
    <p class="kicker" data-r>{ico('pin')}Product designer · Tallinn</p>
    <h1 data-r style="--i:1">I start with the question a person actually has, and design until the product answers it.</h1>
    <p class="lead" data-r style="--i:2">Four projects, each named after its question. One of them is a real app my friends and I talk in. I design in Figma and build with AI tools, so an idea gets tested as a working thing, not as a slide.</p>
    <div class="links" data-r style="--i:3"><a class="go fill" href="#work">See the work{ico('arrow')}</a><a class="go" href="about/index.html">About me</a></div>
    <p class="facts-line" data-r style="--i:4"><span><i class="dot"></i>Available now</span><span>{ico('globe')}Estonian, English, Ukrainian, Russian</span></p>
  </div>
  <div class="stage" data-r="media" style="--i:2">
    <div class="rel">
    <a href="work/lobby/index.html" data-cursor="Lobby" aria-label="Open the Lobby case"><div class="frame wide"><video data-auto autoplay muted loop playsinline preload="auto" poster="assets/work/lobby/call.jpg" aria-label="Lobby call screen: four friends in a pixel forest at night"><source src="assets/work/lobby/call.mp4" type="video/mp4"></video></div></a>
    <a href="work/minu-vahetus/index.html" data-cursor="Minu vahetus" aria-label="Open the Minu vahetus case"><div class="frame phone"><video data-auto autoplay muted loop playsinline preload="auto" poster="assets/work/minu-vahetus/flow.jpg" aria-label="Minu vahetus: a shift schedule on a phone"><source src="assets/work/minu-vahetus/flow.mp4" type="video/mp4"></video></div></a>
    </div>
    <p class="small cap">Both are running products, recorded live: Lobby (01) and Minu vahetus (04).</p>
  </div>
</section>
<nav class="index wrap" id="work" aria-label="Projects" data-r><ol>{idx}</ol></nav>
{rows}
'''
    page(R, 'index.html', 'Andrii Shnayder · product designer, Tallinn',
         'Product designer in Tallinn. Four projects, each named after the question it answers: a voice app, a bolt.eu concept, a Tallink campaign and a shift schedule.', body, current='work')

# ------------------------------------------------------------------ case pages
def sec(n, label, inner):
    return f'<section class="sec"><div class="wrap"><p class="label" data-r><i>{n}</i>{label}</p>{inner}</div></section>'
def body_(h, *ps):
    return '<div class="body" data-r>' + f'<h2>{h}</h2>' + ''.join(f'<p>{p}</p>' if not p.startswith('<p') else p for p in ps) + '</div>'
def steps(items):
    return '<ol class="steps">' + ''.join(f'<li data-r style="--i:{i%2}"><span class="n">{i+1}</span><h3>{h}</h3><p>{t}</p></li>' for i, (h, t) in enumerate(items)) + '</ol>'
def nums(items):
    return '<ul class="nums">' + ''.join(f'<li data-r style="--i:{i}"><b>{ico(ic)}{v}</b><span>{t}</span></li>' for i, (ic, v, t) in enumerate(items)) + '</ul>'
def fig(inner, cap, cls="full"):
    return f'<figure class="{cls}" data-r="media">{inner}<figcaption>{cap}</figcaption></figure>' if cls else f'<figure data-r="media">{inner}<figcaption>{cap}</figcaption></figure>'

def case(slug, title_extra, facts, links, hero, sections, desc):
    R = '../../'; p = BY[slug]
    f = ''.join(f'<div>{ico(i)}<dt>{k}</dt><dd>{v}</dd></div>' for i, k, v in facts)
    order = [x['slug'] for x in P]; nx = BY[order[(order.index(slug) + 1) % len(order)]]
    body = f'''
<header class="wrap case-head">
  <p class="back" data-r><a href="{R}index.html#{slug}">{ico('back')}All work</a></p>
  <div class="title">
    <p class="kicker" data-r><i>{p['n']}</i><b>{p['name']}</b><span>· {p['kind']}</span></p>
    <h1 data-r style="--i:1">{p['q']}</h1>
    <p class="lead" data-r style="--i:2">{title_extra}</p>
    <div class="links" data-r style="--i:3">{links}</div>
  </div>
  <div class="side" data-r style="--i:2"><dl class="facts">{f}</dl></div>
</header>
<div class="wrap case-hero" data-r="media">{hero}</div>
{''.join(sections)}
<nav class="next" aria-label="Next project"><div class="wrap"><a href="{R}work/{nx['slug']}/index.html" data-r>
  <span class="kicker">Next · {nx['n']} {nx['name']}{ico('arrow')}</span><span class="q">{nx['q']}</span></a></div></nav>
'''
    page(R, f'work/{slug}/index.html', f"{p['name']} · Andrii Shnayder", desc, body, tone=p['tone'], current='work')

def build_cases():
    R = '../../'
    # ---------------- Lobby
    case('lobby',
      'Lobby is a voice app for playing with friends: a Windows program and a browser version for calls by link. Everyone hears the same music, and it steps back the moment someone speaks.',
      [('user','Role','Idea, product decisions, UX, UI canvases, testing. Code written with Claude under my direction.'),
       ('cal','When','November 2026, ongoing'),
       ('tool','Built with','Design canvases, Svelte, Tauri, Rust voice engine, Supabase'),
       ('pulse','Status','Version 0.14, in testing with friends')],
      ext('https://lobby-voice.online', 'Visit lobby-voice.online', 'go fill'),
      vid(R, 'lobby/call', alt='Lobby call screen: four friends as pixel beetles in a night forest, a track playing in the header, call chat below'),
      [
       sec('01','The question', body_('Voice in one app, music in another.',
         'My friends and I play in the evenings from Ukraine, the Baltics and Finland. We talked in one program and each of us kept music in a different one. Nobody heard the same track, and when the music was loud, it fought with the voices.',
         'I wanted one room where the call and the music belong together: put a track on for everyone, keep talking over it, and silence everything with one key when the round gets serious.')),
       sec('02','What I decided', steps([
         ('Music is synced, not streamed', 'Each person’s app plays the track itself. Lobby only sends “which track, which second, playing or paused”. No extra lag, nothing is rebroadcast, and when someone speaks, the music fades down by itself.'),
         ('Clutch: one key, fifteen seconds of silence', 'In the decisive moment of a round one press mutes the music for everybody. It comes back on its own, so nobody has to remember to turn it on again.'),
         ('Familiar, but ours', 'Early versions looked too much like Discord. I kept the layout people already know (friends on the left, conversation on the right) and made the call itself a pixel forest that follows your local time of day.'),
         ('A link never switches your microphone on', 'A security review showed that a link from outside could drop a person into a room with the mic already live. Now any outside link stops at a Join button first.'),
         ('The game gets the key press first', 'Hotkeys listen without intercepting, so a key bound in Lobby still works in the game. Side mouse buttons are supported.'),
         ('Unfinished things stay visible', 'What is not ready keeps its place in the interface with a “Soon” label. I would rather show the plan than hide half the product.'),
       ]) ),
       sec('03','The screens',
         '<div class="pair">' +
         fig(img(R,'lobby/day','The same call in daylight: five friends, light theme'), '<b>Day.</b> The forest follows the local time, so the same call looks different at noon and at midnight.', '') +
         fig(img(R,'lobby/dm','A one-to-one call inside a chat, with a failed message and a Retry link'), '<b>A call inside a chat.</b> A message that did not send says so and offers Retry.', '') +
         fig(img(R,'lobby/server','A server with text and voice rooms, roles and a member list'), '<b>Servers.</b> Text and voice rooms, roles with colours, members grouped by role.', '') +
         fig(img(R,'lobby/terrarium','Terrarium: a collection of pixel beetles with rarity levels'), '<b>Terrarium.</b> Minutes spent in calls with friends earn beetles. Everything can be earned for free.', '') +
         '</div>'),
       sec('04','In numbers', nums([
         ('cal','14 days','from the first call by link to version 0.14 (7 to 21 November 2026)'),
         ('globe','7','interface languages: English, Estonian, Ukrainian, Russian, Polish, Latvian, Lithuanian'),
         ('check','901','automated tests passing on the last release'),
         ('box','≈ 4 MB','installer size. Lightness was a requirement from the start'),
       ]) + '<p class="note" data-r>These are facts about the build, not about users. Lobby is tested by a small group of friends, and I have no usage statistics worth showing yet.</p>'),
       sec('05','What I learned', body_('A product is mostly decisions nobody sees.',
         'When voice over WebRTC started to stutter, I had the delay measured and moved to our own engine and relay. When the build drifted from my drawings, I sent it back until it matched. Most of my time went into choices like these, not into screens.',
         'I do not expect Lobby to become popular. I built it to go through the whole cycle once: idea, design, release, security review, feedback from real people, next version.')),
      ],
      'Lobby: a voice app for playing with friends, with shared music that steps back when someone speaks. Product and UX case by Andrii Shnayder.')

    # ---------------- Bolt
    case('bolt',
      'bolt.eu explains Bolt well, but every question a first-time visitor brings (how much, how long, is there one near me) ends in the same QR code. I redesigned four public pages inside Bolt’s own style so that each one answers first.',
      [('user','Role','Solo and self-initiated: content audit, UX, UI, coded prototype'),
       ('cal','When','October 2026'),
       ('tool','Built with','Figma (tokens, components, handoff), HTML, CSS, JavaScript, OpenStreetMap data. AI: Claude, Higgsfield'),
       ('flag','Status','Independent concept, not affiliated with Bolt')],
      ext('https://lgf5411.github.io/bolt-web-concept/', 'Read the full case study', 'go fill') + ext('https://lgf5411.github.io/bolt-web-concept/prototype/', 'Open the prototype'),
      '<div class="duo">' + vid(R, 'bolt/rides', alt='Rides page concept: a fare range for each ride type on the visitor’s own route') + vid(R, 'bolt/phone', 'phone', ' data-par="46"', 'The Car-sharing page on a phone') + '</div>',
      [
       sec('01','The question', body_('A brochure that sends you away to act.',
         'I reviewed eight English pages of bolt.eu on desktop and mobile, plus the header, menu and footer. Every rider button opens one dialog that does not know the product, the city or the price.',
         '<p class="small">This is a content and UX audit of the live site, not research with real visitors. Each finding is a hypothesis I would check against Bolt’s own data first.</p>')
         + nums([('chat','6','different main button labels across 8 product pages'),
                 ('screen','2 of 8','pages let a visitor do anything without the app'),
                 ('eye','0','pages estimate the visitor’s own trip')])),
       sec('02','Three answers',
         '<div class="trio">' +
         fig(vid(R,'bolt/price','wide',alt='Fare range for the visitor’s route'), '<b>Rides: “What will it cost?”</b> A fare range for each ride type on the visitor’s own route, before any install.', '') +
         fig(vid(R,'bolt/race','wide',alt='Ride, scooter and car race on real routes'), '<b>Home: “Which is fastest?”</b> Pick a place and ride, scooter and car race on real streets. Fastest and cheapest are labelled.', '') +
         fig(vid(R,'bolt/unlock','wide',alt='Hold to unlock a car'), '<b>Car-sharing: “Is there a car near me?”</b> Hold to unlock: the car wakes up and the card shows it one minute away on the map.', '') +
         '</div>'),
       sec('03','The turn', body_('My first version solved the problem and lost the brand.',
         'Version 1 answered every question on a dark, app-like city map. It worked, but next to bolt.eu it no longer looked like Bolt. A public page has to be recognised in a second, so I audited Bolt’s house style and rebuilt every page inside it.')
         + '<div class="pair">' +
         fig(img(R,'bolt/v1-home','Version 1: a dark night-city map as the homepage', w=1280, h=800), '<b>Version 1.</b> Strong demo, but dense and closer to the app than to the website.', '') +
         fig(img(R,'bolt/v3-home','Version 3: white pages, Bolt header and photography', w=1600, h=1000), '<b>Version 3.</b> Bolt’s header, page order and photography. The map moved down to where a visitor is ready to compare.', '') +
         '</div>'),
       sec('04','Why it is like this', body_('Most of what looks like a problem has a reason.',
         'Before changing anything I wrote down why bolt.eu probably works the way it does. No fare on the page: prices move with demand, and a wrong number is a legal risk. So the concept shows a labelled range, and markets that cannot show estimates get a static “from” table in the same component.',
         'The full case walks through every finding, the handoff file in Figma and what I cut.',
         '<p>' + ext('https://lgf5411.github.io/bolt-web-concept/', 'Full case study') + '</p>')),
      ],
      'Answers before the app: an unofficial redesign concept for bolt.eu where each public page answers the visitor’s question first. Case by Andrii Shnayder.')

    # ---------------- Tallink
    case('tallink',
      '“Pane detsember pausile” (Put December on pause) is a Christmas campaign concept for Tallink. December is gifts, deadlines, parties and traffic. A ferry is the one place where none of it can reach you for a day.',
      [('user','Role','Solo: idea, copy in Estonian and English, design, production'),
       ('cal','When','November 2026'),
       ('tool','Built with','HTML, CSS, JavaScript; video, print files and sound generated in code. AI: Claude'),
       ('flag','Status','Independent concept, made as an application piece. Prices and dates are samples')],
      ext('https://lgf5411.github.io/Talink/', 'Open the campaign site', 'go fill'),
      '<div class="duo">' + img(R, 'tallink/landing', 'Landing page: a ferry at night, its lights reflected on the water as two bars, with a booking bar below the headline', w=1440, h=900) + '<div class="frame phone" data-par="46"><video controls playsinline preload="none" poster="' + R + 'assets/work/tallink/paus-916.jpg" aria-label="The 15-second campaign film, with sound"><source src="' + R + 'assets/work/tallink/paus-916.mp4" type="video/mp4"></video></div></div>',
      [
       sec('01','The idea', body_('The pause sign was already on the water.',
         'A ferry at night throws two tall reflections of light onto the sea. Side by side they read as a pause sign. That one image carries the campaign: the headline, the button (“Vali oma paus”, choose your pause) and the cut in the film all use it.',
         'The offer is sorted by how long a pause you can afford: a day trip to Helsinki, a cruise to Stockholm, or a cruise with a hotel night.')),
       sec('02','One idea, every format',
         '<div class="trio">' +
         fig(img(R,'tallink/banner-45','Banner 4:5 in Estonian', 'p45', w=1080, h=1350), '<b>Social 4:5.</b> One of seven banner formats, each in Estonian and English.', '') +
         fig(img(R,'tallink/poster','A3 poster', 'a3', w=1031, h=1450), '<b>A3 poster.</b> CMYK, FOGRA39 output intent, 3 mm bleed, fonts embedded.', '') +
         fig(img(R,'tallink/email','Newsletter on a phone', 'auto', w=750, h=1620), '<b>Newsletter.</b> 600 px HTML e-mail built from the same parts.', '') +
         '</div>' +
         fig(img(R,'tallink/banner-wide','Wide banner 1200 by 628 in Estonian', 'b', w=1200, h=628), '<b>1200 × 628.</b> The layout holds from a 728 × 90 strip to a vertical story.')),
       sec('03','What is in the package', nums([
         ('screen','1','landing page with a booking bar, built for GitHub Pages'),
         ('eye','3','film cuts: 15 s vertical, 15 s square, 6 s vertical, with original sound'),
         ('box','14','banners: 7 formats in 2 languages'),
         ('print','2','print files: A3 poster and A5 flyer'),
       ]) + '<p class="note" data-r>“TALLINK” is set as plain text in place of the logo, and all prices and dates are samples. Facts about the current Christmas page were taken from tallink.com on 3 November 2026.</p>'),
      ],
      'Pane detsember pausile: an unofficial Christmas campaign concept for Tallink across web, film, banners and print. Case by Andrii Shnayder.')

    # ---------------- Minu vahetus
    case('minu-vahetus',
      'Minu vahetus (“My shift”) is a schedule for shop-floor staff. I work in a supermarket, and this is the tool I wanted on my own first day.',
      [('user','Role','Solo: the problem comes from my own job. UX, UI, clickable prototype'),
       ('cal','When','November 2026'),
       ('tool','Built with','HTML, CSS, JavaScript. AI: Claude'),
       ('flag','Status','Concept with sample data. Next step: show it to the store manager')],
      f'<a class="go fill" href="prototype/index.html">Try the prototype{ico("arrow")}</a><a class="go" href="prototype/index.html?lang=ru">In Russian</a>',
      '<div class="duo left">' + img(R, 'minu-vahetus/worker-d', 'Worker view on desktop: the week as a list, today’s tasks on a timeline, a confirm button') + vid(R, 'minu-vahetus/flow', 'phone', ' data-par="46"', 'Worker view on a phone: confirming the week, asking for a day off, the manager approving it') + '</div>',
      [
       sec('01','The question', body_('The schedule is on paper. The tasks are on a wall.',
         'The weekly schedule is handed out on paper for a signature. What exactly you will do today is written on a card in a back room, so you learn it only after you arrive. To report sick you need the manager’s phone number.',
         'None of this is anyone’s fault; it is how shops have always worked. But each of the three is a small daily question that a phone can answer before you leave home.')),
       sec('02','What I decided', steps([
         ('One screen: the week', 'The worker sees seven rows. Today is open and shows the tasks on a timeline, with the department for each one.'),
         ('A change happens on the day itself', 'Tap a day, choose “I want this day off” or “another time”. Several days go to the manager as one request, with one optional note.'),
         ('A tap replaces the signature', '“I have seen the schedule” is one button. If the manager changes the week afterwards, the app asks to confirm again.'),
         ('Sick note in three fields', 'From which day, for how long, anything to add. It goes to the manager without anyone needing a phone number.'),
         ('The manager sees what needs an answer', 'How many people have seen the schedule, which requests are waiting, who is sick today. Nothing else on the first screen.'),
         ('Estonian and Russian', 'The team speaks both, so the switch is in the header and every label exists in both languages.'),
       ])),
       sec('03','The screens',
         '<div class="trio">' +
         fig(img(R,'minu-vahetus/worker','Worker view: the week and today’s tasks', 'phone', w=780, h=1688), '<b>Worker.</b> The week, and today’s tasks by the hour.', '') +
         fig(img(R,'minu-vahetus/request','Asking for a day off on Thursday', 'phone', w=780, h=1688), '<b>Request.</b> The change is made on the day; Send appears at the bottom.', '') +
         fig(img(R,'minu-vahetus/manager-m','Manager view with pending requests', 'phone', w=780, h=1688), '<b>Manager.</b> Requests wait with Approve and Decline.', '') +
         '</div>'),
       sec('04','The turn', body_('The first version had four tabs. I could not explain it.',
         'Schedule, Tasks, Requests and Profile looked complete, but a request lived in a different place from the day it changed. I rebuilt it around two roles with one screen each, and moved the request onto the day.',
         'It is still a concept: the data is invented and nobody but me has used it. The honest next step is to put it in front of my store manager and see which part would actually get opened.')),
      ],
      'Minu vahetus: a shift schedule concept for shop-floor staff, in Estonian and Russian, with a clickable prototype. Case by Andrii Shnayder.')

def build_about():
    R = '../'
    body = f'''
<section class="about"><div class="wrap">
  <h1 data-r>I am a product designer at the start, with one shipped app and a habit of building what I draw.</h1>
  <div class="bio">
    <p class="lead" data-r>I am Andrii, Ukrainian, living in Tallinn. I speak Estonian fluently. By day I work in a supermarket and study software development; design is what I do every evening.</p>
    <p data-r>I have no commercial design experience yet. What I have instead is finished work: a voice app that my friends and I use, a bolt.eu concept with a full audit and a coded prototype, a campaign carried across web, film, banners and print, and a schedule tool drawn from my own job.</p>
    <p data-r>I work with AI openly. I decide what to build and why, draw it, and then build it with Claude instead of waiting for a developer. Everything on this site I can open, explain and change in front of you.</p>
    <div class="links" data-r>{ext(LINKEDIN, ico("in") + "LinkedIn", "go fill")}<a class="go" href="{R}index.html#work">See the work{ico('arrow')}</a></div>
  </div>
  <div class="card">
    <div data-r><h2>How I work</h2><ul class="rows">
      <li>{ico('chat')}<span>Start from a question a real person asks, in their words.</span></li>
      <li>{ico('eye')}<span>Look at what exists and write down why it is that way before changing it.</span></li>
      <li>{ico('tool')}<span>Build the thing, not a picture of it: Figma for the system, code for the behaviour.</span></li>
      <li>{ico('flag')}<span>Say plainly what is a fact, what is a guess and what I have not tested.</span></li>
    </ul></div>
    <div data-r><h2>Tools</h2><ul class="rows">
      <li>{ico('screen')}<span>Figma: tokens, components, handoff</span></li>
      <li>{ico('box')}<span>Shopify themes, WordPress and WooCommerce</span></li>
      <li>{ico('tool')}<span>HTML, CSS, JavaScript</span></li>
      <li>{ico('pulse')}<span>AI: Claude, Higgsfield, Google Flow</span></li>
    </ul></div>
    <div data-r><h2>Details</h2><ul class="rows">
      <li>{ico('pin')}<span>Tallinn, or remote</span></li>
      <li>{ico('globe')}<span>Estonian, English, Ukrainian, Russian</span></li>
      <li>{ico('check')}<span>Available now</span></li>
    </ul></div>
  </div>
</div></section>
'''
    page(R, 'about/index.html', 'About · Andrii Shnayder', 'Andrii Shnayder, product designer in Tallinn: how I work, tools and contact.', body, current='about')

def build_404():
    body = f'''<section class="about"><div class="wrap"><h1>“Where did that page go?”</h1>
<div class="bio"><p class="lead">It is not here. The work is one click away.</p><div class="links"><a class="go fill" href="/Portfolia/index.html">Back to the work{ico('arrow')}</a></div></div></div></section>'''
    page('/Portfolia/', '404.html', 'Not found · Andrii Shnayder', 'Page not found.', body)

if __name__ == '__main__':
    build_home(); build_cases(); build_about(); build_404()
    print('built')
