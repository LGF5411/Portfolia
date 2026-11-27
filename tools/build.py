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
<script>(function(d){{d.classList.add('js');var m=null;try{{m=localStorage.getItem('motion')}}catch(e){{}}if(m==='off'||(m!=='on'&&matchMedia('(prefers-reduced-motion: reduce)').matches))d.classList.add('calm')}})(document.documentElement)</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="me" href="{R}index.html">Andrii Shnayder</a>
  <nav aria-label="Main"><button class="motion motion--top" type="button" data-motion hidden></button><a href="{R}index.html#work"{cur('work')}>Work</a><a href="{R}about/index.html"{cur('about')}>About</a>{ext(LINKEDIN, "LinkedIn", "")}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="say">
    <p class="q">Have a question your product should answer better?</p>
    <p class="lead">I am looking for a junior product designer (UX/UI) role or an internship. In Tallinn or remote, available now.</p>
    <div class="links">{ext(LINKEDIN, ico("in") + "Write to me on LinkedIn", "go fill")}{mail}</div>
  </div>
  <div class="legal">
    <p>The Bolt, Tallink, Organic Shop and Mänguarvutid.ee projects are independent concepts, not affiliated with or endorsed by those companies.</p>
    <p><button class="motion" type="button" data-motion></button></p>
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
 dict(slug='pilk', tone='pilk', n='04', name='Pilk', kind='My own banner studio · live site in three languages',
      q='“Will it still read at 320 × 50?”',
      a='A small studio that sells one thing: a banner idea delivered in every size an ad platform asks for. The first screen shows it happening.',
      meta=[('box','26 sizes from one idea'),('chat','English, Estonian, Russian'),('pulse','Live, taking first requests')]),
]
P2 = [
 dict(slug='cosmetics', tone='cosmetics', n='05', name='Organic Shop', kind='Online store redesign · unofficial concept',
      q='“Which one is for me?”',
      a='A cosmetics store with a very large range, where the shelf asks the buyer’s question first: scrubs by scent, hair care by hair type.',
      meta=[('box','E-commerce · working Shopify theme')]),
 dict(slug='manguarvutid', tone='mangu', n='06', name='Tähekaart', kind='Mänguarvutid.ee redesign · unofficial concept',
      q='“Which PC will run my game?”',
      a='A gaming-PC shop where you pick a game, a screen and a frame rate, and the cheapest computer that manages it steps forward.',
      meta=[('screen','E-commerce · picker, catalogue as a map, configurator')]),
 dict(slug='restart', tone='restart', n='07', name='Restart', kind='Laptop repair service · study project',
      q='“My laptop is broken. What now?”',
      a='A repair service that names the one price it can honestly promise, and tells you what happens after you press the button.',
      meta=[('tool','Service booking · Figma to a working site')]),
]
# Minu vahetus is parked until it is ready (owner, 2026-11-27). To bring it back: add VAHETUS to P and set SHOW_VAHETUS = True.
VAHETUS = dict(slug='minu-vahetus', tone='vahetus', n='04', name='Minu vahetus', kind='Shift schedule for shop staff · concept',
      q='“When do I work tomorrow, and what will I be doing?”',
      a='The paper schedule and the task card on the back-room wall, moved to the phone. It comes from my own job in a supermarket.',
      meta=[('user','Solo: problem from my own workplace, UX, UI, prototype'),('phone','Clickable prototype, Estonian and Russian'),('flag','Concept with sample data, November 2026')])
SHOW_VAHETUS = False
ALL = P + P2 + ([VAHETUS] if SHOW_VAHETUS else [])
BY = {p['slug']: p for p in ALL}

def home_media(R, p):
    s = p['slug']
    if s == 'lobby':
        inner = img(R, 'lobby/day', 'Lobby call screen by day: friends in a pixel forest, a track playing in the header', w=1920, h=1200)
    elif s == 'bolt':
        inner = '<div class="duo">' + vid(R, 'bolt/rides', alt='Bolt Rides page concept: a fare range for the visitor’s own route') + vid(R, 'bolt/phone', 'phone', ' data-par="46"', 'The same concept on a phone') + '</div>'
    elif s == 'tallink':
        inner = '<div class="duo">' + img(R, 'tallink/landing', 'Campaign landing page: a ferry at night whose lights reflect on the sea as a pause sign', w=1440, h=900) + vid(R, 'tallink/paus-916', 'phone', ' data-par="46"', 'The 15-second campaign film in vertical format') + '</div>'
    elif s == 'cosmetics':
        inner = '<div class="duo">' + img(R, 'cosmetics/os-home', 'Organic Shop concept: home page with a seasonal scrub banner', w=1440, h=900) + img(R, 'cosmetics/os-pdp-m', 'The product page on a phone', 'phone', ' data-par="46"', w=390, h=844) + '</div>'
    elif s == 'manguarvutid':
        inner = '<div class="duo">' + vid(R, 'manguarvutid/picker', alt='Mänguarvutid concept: choosing games, resolution and frame rate changes the recommended PC') + img(R, 'manguarvutid/m', 'The picker on a phone', 'phone', ' data-par="46"', w=780, h=1688) + '</div>'
    elif s == 'restart':
        inner = img(R, 'restart/hero', 'Restart: “If your laptop is broken, we can help you”, with one button to book diagnostics', w=1440, h=900)
    elif s == 'pilk':
        inner = '<div class="duo">' + vid(R, 'pilk/morph', alt='Pilk home page: one banner changes shape through six formats as the page scrolls, then spreads into all 26 sizes') + img(R, 'pilk/m', 'The same page on a phone', 'phone', ' data-par="46"', w=780, h=1688) + '</div>'
    else:
        inner = '<div class="duo left">' + img(R, 'minu-vahetus/manager-d', 'Manager view: who has seen the schedule, pending requests, sick notes') + vid(R, 'minu-vahetus/flow', 'phone', ' data-par="46"', 'Worker view on a phone: confirming the week and asking for a day off') + '</div>'
    return f'<a class="media" href="{R}work/{s}/index.html" data-cursor="Open case" data-r="media" aria-label="Open the {p["name"]} case">{inner}</a>'

HOME = {
 'lobby': ('voice app', 'Voice chat where friends hear the same music', 'The idea, the call and music scenarios, the UI canvases, every product decision. Code written with Claude.', 'Version 0.14, in testing with friends.'),
 'bolt': ('website concept', 'Website concept: see the price of a ride before installing the app', 'The audit of eight pages, the concept, direction and sign-off of the prototype. Code written with Claude.', 'Independent concept. Not tested with users.'),
 'tallink': ('campaign', 'Christmas campaign concept: landing page, film, banners, print', 'The idea, the choices, final copy in Estonian and English. Production with Claude.', 'Independent concept. Prices and dates are samples.'),
 'pilk': ('banner studio', 'My own banner studio: one idea delivered in 26 sizes', 'The business, the offer, the prices, sign-off on every page. Design and code with Claude.', 'Live, taking first requests.'),
 'cosmetics': ('online store', 'Online store redesign: choose by scent or by hair type', 'The review of the live site, the concept, sign-off on every screen. Theme code with Claude.', 'Working theme. Independent concept, not tested.'),
 'manguarvutid': ('gaming-PC store', 'Gaming-PC store redesign: pick a game, get a PC', 'The first-screen sketch and the decisions. Theme code with Claude.', 'Working theme with sample data. Not tested.'),
 'restart': ('repair service', 'Laptop repair service: booking built around one price', 'The flow and the Figma design, by hand. Built as a site with Claude.', 'Study project.'),
}
CARD = {
 'lobby': ('v', 'lobby/call', 'Lobby call screen: four friends in a pixel forest at night'),
 'bolt': ('v', 'bolt/rides', 'Bolt Rides page concept: a fare range for the visitor’s own route'),
 'tallink': ('i', 'tallink/landing', 'Campaign landing page: a ferry at night whose lights read as a pause sign'),
 'pilk': ('v', 'pilk/morph', 'Pilk home page: one banner changes shape through six formats'),
 'cosmetics': ('i', 'cosmetics/os-home', 'Organic Shop concept: home page with a seasonal scrub banner'),
 'manguarvutid': ('v', 'manguarvutid/picker', 'Gaming-PC store concept: choosing a game changes the recommended PC'),
 'restart': ('i', 'restart/hero', 'Restart: one button to book diagnostics'),
}
TITLE = {'bolt': 'Bolt', 'tallink': 'Tallink', 'manguarvutid': 'Mänguarvutid.ee'}
VARIANTS = {
 '': dict(key=['lobby', 'bolt'], rest=['tallink', 'pilk', 'cosmetics', 'manguarvutid', 'restart'], cap='On screen: Lobby, a voice app (video), and the bolt.eu concept (phone).'),
 'shop': dict(key=['manguarvutid', 'cosmetics'], rest=['lobby', 'bolt', 'pilk', 'tallink', 'restart'], cap='On screen: a gaming-PC store concept (video) and an Organic Shop product page (phone).'),
 'beauty': dict(key=['cosmetics', 'tallink'], rest=['manguarvutid', 'pilk', 'lobby', 'bolt', 'restart'], cap='On screen: the Organic Shop concept, home page and product page.'),
}

def card_media(R, slug):
    k, src, alt = CARD[slug]
    return vid(R, src, alt=alt) if k == 'v' else img(R, src, alt, w=1440, h=900)

def hero_stage(R, variant):
    a = lambda slug, inner: f'<a href="{R}work/{slug}/index.html" data-cursor="{BY[slug]["name"]}" aria-label="Open the {BY[slug]["name"]} case">{inner}</a>'
    if variant == 'shop':
        return a('manguarvutid', card_media(R, 'manguarvutid')) + a('cosmetics', img(R, 'cosmetics/os-pdp-m', 'Organic Shop product page on a phone', 'phone', w=390, h=844))
    if variant == 'beauty':
        return a('cosmetics', card_media(R, 'cosmetics')) + a('cosmetics', img(R, 'cosmetics/os-pdp-m', 'The product page on a phone', 'phone', w=390, h=844))
    return a('lobby', card_media(R, 'lobby')) + a('bolt', vid(R, 'bolt/phone', 'phone', '', 'The bolt.eu concept on a phone'))

def build_home(variant=''):
    R = '../' if variant else ''
    V = VARIANTS[variant]
    order = V['key'] + V['rest']
    idx = ''.join(f'<li><a href="#{s}"><b>{TITLE.get(s, BY[s]["name"])}</b><span>{HOME[s][0]}</span></a></li>' for s in order)
    rows = ''
    for n, s in enumerate(V['key']):
        p = BY[s]; tag, what, part, status = HOME[s]
        rows += f'''
<section class="proj" id="{s}" data-tone-zone="{p['tone']}"><div class="wrap">
  <div class="txt">
    <p class="kicker" data-r><i>Start here</i><b>{n + 1} of 2</b></p>
    <h2 class="pname" data-r style="--i:1">{TITLE.get(s, p['name'])}</h2>
    <p class="pwhat" data-r style="--i:1">{what}</p>
    <dl class="pfacts" data-r style="--i:2"><div>{ico('user')}<dt>My part</dt><dd>{part}</dd></div><div>{ico('pulse')}<dt>Status</dt><dd>{status}</dd></div></dl>
    <a class="go fill" data-r style="--i:3" href="{R}work/{s}/index.html">Open the case{ico('arrow')}</a>
  </div>
  {home_media(R, p)}
</div></section>'''
    more = ''
    for i, s in enumerate(V['rest']):
        p = BY[s]; tag, what, part, status = HOME[s]
        more += f'''<a class="mcard" id="{s}" href="{R}work/{s}/index.html" data-cursor="Open case" data-r style="--i:{i % 3}">
  {card_media(R, s)}
  <span class="pn"><b>{TITLE.get(s, p['name'])}</b></span>
  <span class="a">{what}</span>
  <span class="m">{ico('user')}<span>{part}</span></span>
  <span class="m">{ico('pulse')}<span>{status}</span></span>
</a>'''
    body = f'''
<section class="wrap hero">
  <div class="say">
    <p class="kicker" data-r>{ico('pin')}Junior Product Designer · Tallinn</p>
    <h1 data-r style="--i:1">I design app and website interfaces, and build clickable prototypes with AI.</h1>
    <p class="lead" data-r style="--i:2">Looking for a junior position or an internship, in Tallinn or remote. Two projects to start with are right below.</p>
    <div class="links" data-r style="--i:3"><a class="go fill" href="#work">See the two projects{ico('arrow')}</a>{ext(LINKEDIN, "LinkedIn", "go")}<a class="go" href="{R}about/index.html">About me</a></div>
    <p class="facts-line" data-r style="--i:4"><span><i class="dot"></i>Available now</span><span>{ico('globe')}Estonian, English, Ukrainian, Russian</span></p>
  </div>
  <div class="stage" data-r="media" style="--i:2">
    <div class="rel">{hero_stage(R, variant)}</div>
    <p class="small cap">{V['cap']}</p>
  </div>
</section>
<nav class="index wrap" id="work" aria-label="Projects" data-r><ol>{idx}</ol></nav>
{rows}
<section class="more" data-tone-zone="base"><div class="wrap">
  <div class="head">
    <p class="kicker" data-r>{ico('box')}More work</p>
    <h2 data-r style="--i:1">Five more projects, in the same format: what it is, my part, where it stands.</h2>
  </div>
  <div class="mgrid">{more}</div>
</div></section>
'''
    page(R, (variant + '/' if variant else '') + 'index.html', 'Andrii Shnayder · junior product designer, Tallinn',
         'Junior product designer in Tallinn. I design app and website interfaces and build clickable prototypes with AI. Start with two projects: Lobby, a voice app, and a bolt.eu concept.', body, current='work')

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

LEADS = {
 'lobby': 'A voice app for playing with friends: everyone hears the same music, and it steps back the moment someone speaks.',
 'bolt': 'Every question a first-time visitor brings to bolt.eu ends in the same QR code. I redesigned four pages in Bolt’s own style so that each one answers first.',
 'tallink': 'A Christmas campaign concept for Tallink. December is noise, and a ferry is the one place where it cannot reach you for a day.',
 'pilk': 'A small banner studio I am starting in Tallinn. Its site has to prove in one scroll that one idea survives every ad size.',
 'cosmetics': 'A redesign concept for a store with a very large range: it asks the buyer’s question first and sorts the shelf by the answer.',
 'manguarvutid': 'A redesign concept for a gaming-PC shop in Tallinn: say what you play, and the shop does the comparing.',
 'restart': 'A laptop repair service designed for a UX course. The real task was removing the fear of an open-ended bill.',
}
BRIEF = {
 'lobby': ('Voice lived in one app and music in another.', 'One room for both. Music steps back under speech, and one key silences everything.', 'Version 0.14, in testing with friends.'),
 'bolt': ('On eight pages, every rider button opens one QR dialog that knows nothing about you.', 'A fare range for your own route and a map of what is near, in Bolt’s own style.', 'Audit and coded prototype. Not tested with visitors.'),
 'tallink': ('A Christmas offer has to be noticed in the loudest month of the year.', 'One image, the pause sign on the water, carried across web, film, banners and print.', 'Unofficial concept. Prices and dates are samples.'),
 'pilk': ('One banner is never one: every platform asks for its own size.', 'The first screen shows one idea turning into 26 sizes, with your own headline in it.', 'Live and taking first requests. No paying clients yet.'),
 'cosmetics': ('Two hundred similar jars, sorted by product line.', 'Scrubs are chosen by scent, hair care by hair type, and you can buy from the first screen.', 'Working Shopify theme. Not tested with shoppers.'),
 'manguarvutid': ('Buyers know their game. The catalogue answers in part numbers.', 'Four choices, then the cheapest PC that manages it comes first.', 'Working theme with sample data. Not tested with buyers.'),
 'restart': ('Nobody can price a repair before seeing the laptop.', 'Promise the one honest number: diagnostics cost 20 €.', 'Study project. The service is invented.'),
}

def case(slug, title_extra, facts, links, hero, sections, desc):
    R = '../../'; p = BY[slug]
    title_extra = LEADS.get(slug, title_extra)
    facts = [x for x in facts if x[1] != 'Role']
    facts = [(i, 'Role' if k == 'Who did what' else k, v) for i, k, v in facts]
    b = BRIEF.get(slug)
    brief = '' if not b else ('<div class="wrap"><dl class="brief" data-r>'
        + f'<div>{ico("chat")}<dt>Problem</dt><dd>{b[0]}</dd></div>'
        + f'<div>{ico("check")}<dt>What I did</dt><dd>{b[1]}</dd></div>'
        + f'<div>{ico("pulse")}<dt>Where it stands</dt><dd>{b[2]}</dd></div></dl></div>')
    f = ''.join(f'<div>{ico(i)}<dt>{k}</dt><dd>{v}</dd></div>' for i, k, v in facts)
    order = [x['slug'] for x in ALL]; nx = BY[order[(order.index(slug) + 1) % len(order)]]
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
{brief}
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
       ('pulse','Status','Version 0.14, in testing with friends'),
       ('chat','Who did what','Me: the idea, every product decision, the design canvases, testing with friends. Claude: the code')],
      ext('https://lobby-voice.online', 'Visit lobby-voice.online', 'go fill'),
      vid(R, 'lobby/call', alt='Lobby call screen: four friends as pixel beetles in a night forest, a track playing in the header, call chat below'),
      [
       sec('01','The question', body_('Voice in one app, music in another.',
         'My friends and I play in the evenings from Ukraine, the Baltics and Finland. We talked in one program and each of us kept music in a different one. Nobody heard the same track, and when the music was loud, it fought with the voices.',)),
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
       ]) + '<p class="note" data-r>These are facts about the build, not about users. Lobby is tested by a small group of friends, and I have no usage statistics worth showing yet.</p>'),
       sec('05','What I learned', body_('A product is mostly decisions nobody sees.',
         'When voice over WebRTC started to stutter, I had the delay measured and moved to our own engine and relay. When the build drifted from my drawings, I sent it back until it matched. Most of my time went into choices like these, not into screens.',)),
      ],
      'Lobby: a voice app for playing with friends, with shared music that steps back when someone speaks. Product and UX case by Andrii Shnayder.')

    # ---------------- Bolt
    case('bolt',
      'bolt.eu explains Bolt well, but every question a first-time visitor brings (how much, how long, is there one near me) ends in the same QR code. I redesigned four public pages inside Bolt’s own style so that each one answers first.',
      [('user','Role','Solo and self-initiated: content audit, UX, UI, coded prototype'),
       ('cal','When','October 2026'),
       ('tool','Built with','Figma (tokens, components, handoff), HTML, CSS, JavaScript, OpenStreetMap data. AI: Claude, Higgsfield'),
       ('flag','Status','Independent concept, not affiliated with Bolt'),
       ('chat','Who did what','Me: the audit, the decisions, direction and sign-off on every page. Claude: the prototype code')],
      ext('https://lgf5411.github.io/bolt-web-concept/prototype/', 'Open the prototype', 'go fill'),
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
         '<p class="small">' + ext('https://lgf5411.github.io/bolt-web-concept/', 'The long version, for those who want every finding') + '</p>')),
      ],
      'Answers before the app: an unofficial redesign concept for bolt.eu where each public page answers the visitor’s question first. Case by Andrii Shnayder.')

    # ---------------- Tallink
    case('tallink',
      '“Pane detsember pausile” (Put December on pause) is a Christmas campaign concept for Tallink. December is gifts, deadlines, parties and traffic. A ferry is the one place where none of it can reach you for a day.',
      [('user','Role','Self-initiated: the idea, the direction, final copy in Estonian and English'),
       ('cal','When','November 2026'),
       ('tool','Built with','HTML, CSS, JavaScript; video, print files and sound generated in code. AI: Claude'),
       ('flag','Status','Independent concept, made as an application piece. Prices and dates are samples'),
       ('chat','Who did what','Me: the idea, the choices, sign-off on every format. Claude: code, production files, copy drafts')],
      ext('https://lgf5411.github.io/Talink/', 'Open the campaign site', 'go fill'),
      '<div class="duo">' + img(R, 'tallink/landing', 'Landing page: a ferry at night, its lights reflected on the water as two bars, and one button below the headline: choose your pause', w=1440, h=900) + '<div class="frame phone" data-par="46"><video controls playsinline preload="none" poster="' + R + 'assets/work/tallink/paus-916.jpg" aria-label="The 15-second campaign film, with sound"><source src="' + R + 'assets/work/tallink/paus-916.mp4" type="video/mp4"></video></div></div>',
      [
       sec('01','The idea', body_('The pause sign was already on the water.',
         'A ferry at night throws two tall reflections of light onto the sea. Side by side they read as a pause sign. That one image carries the campaign: the headline, the button (“Vali oma paus”, choose your pause) and the cut in the film all use it.',)),
       sec('02','One idea, every format',
         '<div class="trio">' +
         fig(img(R,'tallink/banner-45','Banner 4:5 in Estonian', 'p45', w=1080, h=1350), '<b>Social 4:5.</b> One of seven banner formats, each in Estonian and English.', '') +
         fig(img(R,'tallink/poster','A3 poster', 'a3', w=1031, h=1450), '<b>A3 poster.</b> CMYK, FOGRA39 output intent, 3 mm bleed, fonts embedded.', '') +
         fig(img(R,'tallink/email','Newsletter on a phone', 'auto', w=750, h=1620), '<b>Newsletter.</b> 600 px HTML e-mail built from the same parts.', '') +
         '</div>' +
         fig(img(R,'tallink/banner-wide','Wide banner 1200 by 628 in Estonian', 'b', w=1200, h=628), '<b>1200 × 628.</b> The layout holds from a 728 × 90 strip to a vertical story.')),
       sec('03','What is in the package', nums([
         ('screen','1','landing page, checked against the real tallink.com page: one choice on the first screen instead of a booking form'),
         ('eye','3','film cuts: 15 s vertical, 15 s square, 6 s vertical, with original sound'),
         ('box','14','banners: 7 formats in 2 languages'),
         ('print','2','print files: A3 poster and A5 flyer'),
       ]) + '<p class="note" data-r>“TALLINK” is set as plain text in place of the logo, and all prices and dates are samples. Facts about the current Christmas page were taken from tallink.com on 3 November 2026.</p>'),
      ],
      'Pane detsember pausile: an unofficial Christmas campaign concept for Tallink across web, film, banners and print. Case by Andrii Shnayder.')


    # ---------------- Pilk
    case('pilk',
      'Pilk is a small banner studio I am starting in Tallinn. A business orders one banner, and then the ad platform asks for twelve sizes. Pilk sells the whole set, and its site has to prove in one scroll that an idea can survive all of them.',
      [('user','Role','Founder. I decide what the studio sells and refuses, the prices, the brief for every page, and what goes live'),
       ('cal','When','November 2026, ongoing'),
       ('tool','Built with','Static HTML, CSS and JavaScript, its own banner engine. AI: Claude'),
       ('pulse','Status','Live and taking first requests. No paying clients yet; the examples on the site are invented businesses and say so'),
       ('chat','Who did what','Me: the business, the offer, the prices, the brief and sign-off for every page. Claude: design proposals, the brand, the code')],
      ext('https://lgf5411.github.io/pilk/', 'Open the live site', 'go fill'),
      '<div class="duo">' + vid(R, 'pilk/morph', alt='Pilk home page: while the page scrolls, one banner changes shape from a medium rectangle to a leaderboard, a square post, a story and a billboard, then spreads into all 26 sizes') + img(R, 'pilk/m', 'The same page on a phone', 'phone', ' data-par="46"', w=780, h=1688) + '</div>',
      [
       sec('01','The question', body_('One banner is never one banner.',
         'A café makes a nice square post. Then Google wants a 728 × 90 strip, Instagram wants a story, and the printer wants a poster. The same picture gets squeezed, the headline stops fitting, the button disappears.',)),
       sec('02','What I decided', steps([
         ('The first screen is the product working', 'Scroll, and one banner turns into a leaderboard, a square, a story, a billboard, and then lays out all 26 sizes. No claim about quality, just the thing happening.'),
         ('Your words, immediately', 'A field under the banner says “Your headline”. Type your own offer and every size on the page shows it.'),
         ('Sell only what can be promised', 'Six services with a price and a date each, and a section called “What we don’t take on”. A new studio earns trust faster by refusing than by listing everything.'),
         ('Prices and dates on the page', '“48 h to the first sketch”, “12 sizes for €390”. Nobody has to write an e-mail to learn whether they can afford it.'),
         ('A free test instead of a client list', 'A new studio has no cases to show. So the offer is: send one banner, get three sizes back, free. The work is the reference.'),
         ('A brief that answers back', 'Five short questions, and the price and the date appear while you fill them in, before you send anything.'),
       ])),
       sec('03','The screens',
         fig(img(R,'pilk/sizes','Banner size guide: all 26 sizes, where each one runs and the one rule that matters for it'), '<b>Size guide.</b> All 26 sizes, where each runs, and one rule per size. Free to use without ordering, which is also how people find the studio.') +
         '<div class="pair">' +
         fig(img(R,'pilk/brief','Start a brief: step 1 of 5 with services and prices, and a running summary on the right'), '<b>Brief.</b> The summary and the estimate build on the right as you answer.', '') +
         fig(img(R,'pilk/demo','An example site for a lunch café, marked as an example design by Pilk'), '<b>Example site.</b> A full sample for an invented café, labelled as an example at the bottom of every page.', '') +
         '</div>'),
       sec('04','What is real and what is not', body_('It is a business on day one, and the page says so.',
         'The site is live in English, Estonian and Russian. The offer, the prices and the free test are real. There are no client cases yet, the example businesses are made up and labelled, and the Estonian text is still waiting for a careful read.',)),
      ],
      'Pilk: a small banner studio in Tallinn whose home page shows one idea surviving 26 sizes. Case by Andrii Shnayder.')

    # ---------------- Minu vahetus (parked)
    (case if SHOW_VAHETUS else (lambda *a, **k: None))('minu-vahetus',
      'Minu vahetus (“My shift”) is a schedule for shop-floor staff. I work in a supermarket, and this is the tool I wanted on my own first day.',
      [('user','Role','Solo: the problem comes from my own job. UX, UI, clickable prototype'),
       ('cal','When','November 2026'),
       ('tool','Built with','HTML, CSS, JavaScript. AI: Claude'),
       ('flag','Status','Concept with sample data. Next step: show it to the store manager'),
       ('chat','Who did what','Me: the problem, the flow, both rebuilds. Claude: the prototype code')],
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

    # ---------------- Organic Shop
    case('cosmetics',
      'Organic Shop makes natural cosmetics in Tallinn and sells a very large range. A shelf of two hundred similar jars and bottles is hard to choose from, so in my redesign concept the store asks the buyer’s question first and sorts the shelf by the answer.',
      [('user','Role','Solo and self-initiated: UX review of the live site, concept, UI. Theme code written with Claude under my direction'),
       ('cal','When','October to November 2026'),
       ('tool','Built with','Shopify theme (Liquid, CSS, JavaScript), Figma. AI: Claude'),
       ('flag','Status','Independent concept, not affiliated with Organic Shop. Built as a working theme with the store’s real products'),
       ('chat','Who did what','Me: the review, the concept, sign-off on every screen. Claude: the theme code')],
      '',
      '<div class="duo apart">' + img(R, 'cosmetics/os-home', 'Organic Shop concept, home page: a seasonal scrub banner, the menu and the shelf of signature scrubs', w=1440, h=900) + img(R, 'cosmetics/os-pdp-m', 'The product page on a phone', 'phone', ' data-par="46"', w=390, h=844) + '</div>',
      [
       sec('01','The question', body_('Stores are sorted by product line. People arrive with a wish.',
         'Nobody walks in looking for “the Fig &amp; Rosehip line”. They want a scrub that smells of mango, or a shampoo for oily hair. The catalogue knows the answer, but the visitor has to translate the wish into the store’s language first.',
         '<p class="small">This is a view from outside. The brand knows what I cannot: what sells, what is returned, what its buyers search for. I would begin with that data and with what already works on the live site.</p>')),
       sec('02','The shelf', body_('“Pick your flavour.” Scrubs are bought by scent, shampoo by hair type.',
         'Organic Shop makes natural cosmetics in Tallinn. Its best-known product is a body scrub that comes in a couple of dozen flavours, and nobody compares scrubs by formula. So the scrub shelf switches by scent, and the page takes the colour of the jar.',
         'For hair the question is different, so that part of the store starts from a sentence the visitor finishes: “My hair is oily”. The store’s real products and names are used throughout, so the concept can be judged as a store and not as a poster.')
         + fig(img(R,'cosmetics/os-flavour','“Pick your flavour”: mango, matcha mojito, raspberry, coconut, bellini, coffee, with the chosen jar and Add to bag', 'fl', w=1440, h=790), '<b>Pick your flavour.</b> Six scents as the menu; the jar, the name, the price and the button change with the choice.') +
         '<div class="pair">' +
         fig(img(R,'cosmetics/os-catalog','Body scrubs catalogue: 28 products, a price filter, sorting, Add on every card', 'r', w=1440, h=1020), '<b>Catalogue.</b> 28 scrubs, price filter, sorting and Add on every card. Under the grid, a short guide to choosing between sugar and salt.', '') +
         fig(img(R,'cosmetics/os-pdp','Product page for the mango scrub: size, price, Add to bag, delivery and returns, then what it does, who it is for and why this one', 'pd', w=1440, h=1340), '<b>Product page.</b> What it does, who it is for, why this one. Delivery and returns sit under the button, not in the footer.', '') +
         '</div>' +
         '<div class="pair">' +
         fig(img(R,'cosmetics/organic-hair','Hair: the hero reads “My hair is oily”, with hair types to choose from', w=1440, h=900), '<b>Hair.</b> The sentence is the menu: oily, damaged, thinning, normal, coloured.', '') +
         fig(img(R,'cosmetics/organic-routine','Three products of one line as steps 1, 2 and 3, with one button that adds all of them', 'r', w=1440, h=1020), '<b>One routine, one button.</b> Shampoo, conditioner and mask as steps 1, 2, 3; one button adds all three.', '') +
         '</div>'),
       sec('03','What I decided', steps([
         ('The menu is the buyer’s own words', 'Scents for scrubs, hair types for hair care. Product lines stay, one level down.'),
         ('The button is on the first screen', 'The chosen jar comes with its size, its price and Add to bag, so choosing and buying are one step.'),
         ('A product page answers three questions', 'What it does, who it is for, why this one. Then how to use it and the questions people ask.'),
         ('Doubts are answered next to the button', 'Stock, delivery and the 14-day return sit under Add to bag, not in the footer.'),
         ('A routine is one purchase', 'Shampoo, conditioner and mask from one line are steps 1, 2, 3 with a single button.'),
         ('Text that helps search and people at once', 'A short guide under the catalogue grid (sugar or salt, how to use a scrub) instead of a block of keywords.'),
       ]) + '<p class="note" data-r>The concept has not been tested with shoppers or shown to the company. The next honest step would be five people and one task: “find a scrub you would buy as a gift”.</p>'),
      ],
      'Organic Shop: an unofficial redesign concept where scrubs are chosen by scent and hair care by hair type. Case by Andrii Shnayder.')

    # ---------------- Mänguarvutid
    case('manguarvutid',
      'Mänguarvutid.ee sells gaming PCs in Tallinn. A catalogue of graphics-card names only helps people who already know the answer. “Tähekaart” (star map) is my redesign concept: say what you play, and the shop does the comparing.',
      [('user','Role','Solo and self-initiated: UX review, concept, UI. Theme code written with Claude under my direction'),
       ('cal','When','October 2026'),
       ('tool','Built with','Shopify theme (Liquid, CSS, JavaScript), my own first-screen sketch. AI: Claude'),
       ('flag','Status','Independent concept, not affiliated with the shop. Part of the prices and builds are samples; frame rates are modelled'),
       ('chat','Who did what','Me: the first-screen sketch, the decisions, sign-off on every page. Claude: the theme code, the sample data')],
      '',
      '<div class="duo">' + vid(R, 'manguarvutid/picker', alt='Choosing games, resolution and frame rate: the recommended PC, its frame rates and its price change with every choice') + img(R, 'manguarvutid/m', 'The picker on a phone', 'phone', ' data-par="46"', w=780, h=1688) + '</div>',
      [
       sec('01','The question', body_('The buyer knows the game. The shop answers in part numbers.',
         'Someone buying a first gaming PC knows three things: what they play, what monitor they have and how smooth they want it. A product list answers in RTX 5070, Ryzen 5 7600X and DDR5. Between the two sits a comparison most people cannot make.',
         '<p class="small">This is my reading of the public site, not the shop’s sales data. I would check it against their analytics before changing a live store.</p>')),
       sec('02','What I decided', steps([
         ('Four choices instead of a spec sheet', 'Device, kind of games, resolution, target frame rate. Each choice explains itself in one line (“1080p is the most common monitor”).'),
         ('The cheapest PC that manages it comes first', 'Not the most expensive one. The card shows frames per second in four named games and marks which of them reach the target.'),
         ('The catalogue is a sky', 'Every PC is a star: further right costs more, higher gives more frames in your game. A horizon line sits at your target, and everything above it will do.'),
         ('Specifications stay, in second place', 'Name, key parts with their real numbers, a large price, Add to cart. When the button scrolls away, a buy bar follows.'),
         ('A configurator for those who know', 'Eight steps from processor to case. At each one the shop says what fits, what is at the limit and what will not work together.'),
         ('The shop’s own trust signals, up front', 'Built in Tallinn, tested before shipping, two physical stores, instalments. They sit directly under the recommendation, where the doubt is.'),
       ])),
       sec('03','The screens',
         fig(img(R,'manguarvutid/sky','The catalogue as a star map: PCs plotted by price and frame rate, with a horizon line at 144 FPS'), '<b>Kogu taevas ühe pilguga</b> (the whole sky at a glance). Switch the game, the resolution or the target and the stars move.') +
         fig(img(R,'manguarvutid/pdp','Product page: name, key specifications, price and Add to cart'), '<b>Product page.</b> Parts with concrete numbers, then the price and one button.') +
         fig(img(R,'manguarvutid/conf','Configurator: step 1 of 8, choosing a processor'), '<b>Configurator.</b> Eight steps, with a recommendation and a reason at each.')),
       sec('04','Where the map stops', body_('A sky works for a few dozen PCs. It would not work for hundreds of monitors.',
         'The map needs one axis everybody understands, and gaming PCs have it: frames per second. Accessories do not. So that part of the store is an ordinary list with filters by the properties people actually compare, a sort order and a count, and each row says which PC it suits.',)
         + fig(img(R,'manguarvutid/filters','Monitors as a filtered list: size, resolution, refresh rate, panel, brand, price; each row names the PC it suits'), '<b>Monitors.</b> Six filters, sorting, and a “suits” line under each product instead of a second comparison.') +
         fig(img(R,'manguarvutid/cart','Cart with one PC, the total with VAT, and delivery, payment and returns beside the checkout button'), '<b>Cart.</b> Total with VAT, the monthly instalment, then delivery, payment and returns in three lines.')),
       sec('05','How I would know it works', steps([
         ('Hypothesis', 'People who state what they play reach a product page more often than people who start from the catalogue.'),
         ('What I would measure', 'Share of visits that reach a product page, add-to-cart rate from the picker against the list, and how often the first recommendation is the one bought.'),
         ('How', 'Picker against the current home page as an A/B test on the shop’s real traffic; before that, five people and one task: “find a PC for your game under your budget”.'),
         ('What would make me drop it', 'If people skip the picker and scroll straight to the list, the list becomes the first screen and the picker a filter on top of it.'),
       ])),
       sec('06','What is real and what is not', body_('A concept with sample data should say so on every page.',
         'A strip at the top of the store reads “Disainikontseptsioon”: some prices and builds are samples and frame rates come from a model, not from benchmarks I ran. Product photos are marked as illustrative. Before this could go live, every number would have to come from the shop.',)),
      ],
      'Tähekaart: an unofficial redesign concept for Mänguarvutid.ee where the buyer picks a game and a frame rate instead of a graphics card. Case by Andrii Shnayder.')

    # ---------------- Restart
    case('restart',
      'Restart is a laptop repair service I designed for a UX course. The brief was a booking site. The real task turned out to be removing the fear of an open-ended bill.',
      [('user','Role','Solo: research questions, flow, UI in Figma. Built as a working site with Claude from my Figma design'),
       ('cal','When','October 2026'),
       ('tool','Built with','Figma, Shopify theme. AI: Claude'),
       ('flag','Status','Study project. The service is invented'),
       ('chat','Who did what','Me: the flow and the Figma design, by hand. Claude: turning it into a working site')],
      '',
      '<div class="duo">' + img(R, 'restart/hero', 'Restart home page: “If your laptop is broken, we can help you”, one button to book diagnostics, and a line with the price below it', w=1440, h=900) + img(R, 'restart/m', 'The same page on a phone', 'phone', ' data-par="46"', w=390, h=844) + '</div>',
      [
       sec('01','The question', body_('You do not know what is broken, so nobody can tell you the price.',
         'A person with a dead laptop cannot describe the fault and expects to be overcharged. Most repair sites answer with a price list of thirty services, which only helps if you already know which one you need.',)),
       sec('02','What I decided', steps([
         ('One number on the page', 'Diagnostics cost 20 €. If you go ahead with the repair, it is included. If you decline, that is all you pay.'),
         ('“Describe what you noticed” is enough to start', 'The second sentence on the page says it: you do not have to know what is wrong. Say what you see, in your own words.'),
         ('No repair without your yes', 'The line sits under the main button and again in the price table, because it is the sentence people look for.'),
         ('What happens next, as four steps', 'We call you, you bring the laptop, we find the cause, you decide. Each step has a time attached.'),
         ('No account, no online payment', 'You pay at the workshop. Asking for a card before anyone has seen the laptop would bring the fear straight back.'),
         ('Quiet on purpose', 'One typeface, almost no colour, a lot of white. Someone whose computer just died does not need a lively website.'),
       ])),
       sec('03','The screens',
         fig(img(R,'restart/price','“What you pay for”: 20 € for diagnostics, and what happens if you repair or decline', w=1440, h=900), '<b>What you pay for.</b> The only fixed price, and both outcomes spelled out.') +
         fig(img(R,'restart/steps','What happens after you send a request: four numbered steps', 'st', w=1440, h=500), '<b>After you send a request.</b> Four steps, each with its own deadline.')),
       sec('04','What I learned', body_('The smallest project taught me the most about copy.',
         'There is almost nothing to draw here. The whole design is the order of six sentences and which of them gets to be large. It is the project I would show to explain how I think about words in an interface.',
         'It was not tested with people outside the course.')),
      ],
      'Restart: a study UX project for a laptop repair service built around one honest price. Case by Andrii Shnayder.')

def build_about():
    R = '../'
    body = f'''
<section class="about"><div class="wrap">
  <h1 data-r>I am a junior product designer with an app my friends and I talk in, and a habit of building what I draw.</h1>
  <div class="bio">
    <p class="lead" data-r>I am Andrii, Ukrainian, living in Tallinn. I speak Estonian fluently. By day I work in a supermarket and study software development; design is what I do every evening.</p>
    <p data-r>I have no commercial design experience yet. What I have instead is finished work: a voice app that my friends and I use, a bolt.eu concept with a full audit and a coded prototype, a campaign carried across web, film, banners and print, a small banner studio I am starting, and working store concepts for cosmetics, gaming PCs and a repair service.</p>
    <p data-r>I work with AI openly, and every case says who did what. I set the problem, make the decisions and accept or reject each screen; Claude writes the code and produces the files. Everything on this site I can open, explain and change in front of you.</p>
    <div class="links" data-r>{ext(LINKEDIN, ico("in") + "LinkedIn", "go fill")}<a class="go" href="{R}index.html#work">See the work{ico('arrow')}</a></div>
  </div>
  <div class="card">
    <div data-r><h2>How I work</h2><ul class="rows">
      <li>{ico('chat')}<span>Start from a question a real person asks, in their words.</span></li>
      <li>{ico('eye')}<span>Look at what exists and write down why it is that way before changing it.</span></li>
      <li>{ico('tool')}<span>Build the thing, not a picture of it: Figma for the system, code for the behaviour.</span></li>
      <li>{ico('flag')}<span>Say plainly what is a fact, what is a guess and what I have not tested.</span></li>
    </ul></div>
    <div data-r><h2>What I can take on</h2><ul class="rows">
      <li>{ico('phone')}<span>Product and app UX: flows, screens, prototypes that click</span></li>
      <li>{ico('box')}<span>E-commerce: store structure, product pages, cart, Shopify themes</span></li>
      <li>{ico('print')}<span>Campaign pages and banners for a product</span></li>
      <li>{ico('chat')}<span>Interface copy in English and Estonian</span></li>
    </ul></div>
    <div data-r><h2>Tools</h2><ul class="rows">
      <li>{ico('screen')}<span>Figma</span></li>
      <li>{ico('box')}<span>Shopify themes, WordPress and WooCommerce</span></li>
      <li>{ico('tool')}<span>HTML, CSS, JavaScript</span></li>
      <li>{ico('pulse')}<span>Claude, for code and production</span></li>
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
    build_home(); build_home('shop'); build_home('beauty'); build_cases(); build_about(); build_404()
    print('built')
