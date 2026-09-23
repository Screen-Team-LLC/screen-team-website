"""Two Screen Team job pages for one before/process/after composite.

The detail page explains the enclosure problem and the finished look.
The scope page explains what Chris included and what stays out of the job.
Ticket prices, street addresses, customer phones, and ticket numbers are never printed.
"""
from __future__ import annotations

import hashlib
import html
import json
import random
import re
from pathlib import Path
from typing import Any

MIN_WORDS = 750
BRAND = "Screen Team LLC"
OWNER = "Chris Westcott"
PHONE_DISPLAY = "(727) 386-6562"
PHONE_TEL = "7273866562"
SITE = "https://screenteamllc.com"

_PHONE = re.compile(r"(?:\+?1[\s.\-]?)?(?:\(\d{3}\)|\d{3})[\s.\-]?\d{3}[\s.\-]?\d{4}")
_MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?")
_STREET = re.compile(
    r"\b\d{1,6}\s+[A-Za-z0-9.'’-]+(?:\s+[A-Za-z0-9.'’-]+){0,5}\s+"
    r"(?:st|street|ave|avenue|rd|road|dr|drive|ln|lane|blvd|boulevard|ct|court|way|ter|terrace|cir|circle|pl|place)\b",
    re.I,
)
_EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_TICKET = re.compile(r"\b(?:ticket|work\s*order|wo|job)\s*#?\s*[A-Za-z0-9-]{3,}\b", re.I)
_ZIP = re.compile(r"\b\d{5}(?:-\d{4})?\b")
_BOILER = re.compile(r"published screen team price|nothing was sent|chris edits this before", re.I)

_COUNTY_BY_SLUG = {
    "belleair": "Pinellas County",
    "clearwater": "Pinellas County",
    "dunedin": "Pinellas County",
    "gulfport": "Pinellas County",
    "largo": "Pinellas County",
    "oldsmar": "Pinellas County",
    "palm-harbor": "Pinellas County",
    "pinellas-park": "Pinellas County",
    "safety-harbor": "Pinellas County",
    "seminole": "Pinellas County",
    "st-petersburg": "Pinellas County",
    "tarpon-springs": "Pinellas County",
    "treasure-island": "Pinellas County",
    "dade-city": "Pasco County",
    "holiday": "Pasco County",
    "hudson": "Pasco County",
    "land-o-lakes": "Pasco County",
    "new-port-richey": "Pasco County",
    "odessa": "Pasco County",
    "port-richey": "Pasco County",
    "trinity": "Pasco County",
    "wesley-chapel": "Pasco County",
    "zephyrhills": "Pasco County",
    "brandon": "Hillsborough County",
    "carrollwood": "Hillsborough County",
    "lithia": "Hillsborough County",
    "plant-city": "Hillsborough County",
    "riverview": "Hillsborough County",
    "tampa": "Hillsborough County",
    "temple-terrace": "Hillsborough County",
    "town-n-country": "Hillsborough County",
    "valrico": "Hillsborough County",
}
_NAME_OVERRIDE = {
    "st-petersburg": "St. Petersburg",
    "land-o-lakes": "Land O' Lakes",
    "town-n-country": "Town 'N' Country",
    "new-port-richey": "New Port Richey",
    "port-richey": "Port Richey",
    "palm-harbor": "Palm Harbor",
    "pinellas-park": "Pinellas Park",
    "safety-harbor": "Safety Harbor",
    "tarpon-springs": "Tarpon Springs",
    "treasure-island": "Treasure Island",
    "plant-city": "Plant City",
    "temple-terrace": "Temple Terrace",
    "wesley-chapel": "Wesley Chapel",
    "dade-city": "Dade City",
}
_COUNTY_PAGE = {
    "Pinellas County": "pinellas-county-screen-repair.html",
    "Pasco County": "pasco-county-screen-repair.html",
    "Hillsborough County": "hillsborough-county-screen-repair.html",
}
_SERVICES = {
    "full_rescreen": ("full pool cage rescreen", "full-pool-cage-rescreen.html", "rescreens.html"),
    "panels": ("screen panel repair", "screen-panel-repair.html", "pool-cage-repair.html"),
    "partial": ("partial pool cage repair", "pool-cage-repair.html", "storm-screen-repair.html"),
    "lanai": ("screen lanai repair", "screen-lanais.html", "lanai-screen-replacement.html"),
    "windows": ("window screen repair", "window-screens.html", "screen-panel-repair.html"),
    "garage": ("garage screen installation", "garage-screens.html", "services.html"),
    "gutter": ("gutter repair", "gutter-work.html", "seamless-gutters.html"),
    "super_gutter": ("super gutter work", "super-gutters.html", "super-gutter-installation.html"),
    "new_enclosure": ("new pool enclosure", "new-pool-cage-installation.html", "pool-enclosures.html"),
    "hardware": ("screen door and hardware repair", "screen-door-repair.html", "pool-cage-door-repair.html"),
    "visit": ("screen repair visit", "services.html", "pricing.html"),
}
_CLUSTER_NEEDLES = (
    ("new_enclosure", ("new pool cage", "new enclosure", "new pool enclosure")),
    ("super_gutter", ("super gutter",)),
    ("full_rescreen", ("full rescreen", "full pool", "entire cage", "whole cage")),
    ("garage", ("garage", "retractable")),
    ("windows", ("window",)),
    ("gutter", ("gutter",)),
    ("lanai", ("lanai", "patio")),
    ("hardware", ("door", "spline", "hardware")),
    ("panels", ("panel", "roof panel")),
    ("partial", ("partial", "storm", "torn")),
)


def website_root() -> Path:
    return Path(__file__).resolve().parents[1]


def strip_html_words(value: str) -> int:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = html.unescape(text)
    return len(re.findall(r"[A-Za-z0-9']+", text))


def clean_public_text(value: str) -> str:
    """Drop private facts. Estimate boilerplate is not a job story."""
    text = value or ""
    if _BOILER.search(text):
        return ""
    text = _EMAIL.sub("", text)
    text = _PHONE.sub("", text)
    text = _MONEY.sub("", text)
    text = _STREET.sub("", text)
    text = _TICKET.sub("", text)
    text = _ZIP.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" ,;.-")
    if len(text) < 24:
        return ""
    if len(text) > 280:
        text = text[:277].rsplit(" ", 1)[0] + "."
    return text


def infer_cluster(title: str) -> str:
    lower = (title or "").lower()
    for cluster, needles in _CLUSTER_NEEDLES:
        if any(needle in lower for needle in needles):
            return cluster
    if re.search(r"\b(screen|cage|enclosure|rescreen)\b", lower):
        return "visit"
    return "visit"


def _places(root: Path) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for path in sorted(root.glob("*-screen-repair.html")):
        slug = path.stem[: -len("-screen-repair")]
        if slug.endswith("-county"):
            continue
        name = _NAME_OVERRIDE.get(slug) or slug.replace("-", " ").title()
        county = _COUNTY_BY_SLUG.get(slug, "")
        found.append(
            {
                "name": name,
                "slug": slug,
                "page": path.name,
                "county": county,
                "county_page": _COUNTY_PAGE.get(county, "service-areas.html"),
            }
        )
    found.sort(key=lambda item: len(item["name"]), reverse=True)
    return found


def infer_place(text: str, *, explicit: str = "", root: Path | None = None) -> dict[str, str]:
    root = root or website_root()
    places = _places(root)
    blob = f"{explicit} {text}".strip()
    for place in places:
        if re.search(rf"\b{re.escape(place['name'])}\b", blob, flags=re.I):
            return place
    named = (explicit or "").strip()
    if named:
        key = re.sub(r"[^a-z0-9]+", "-", named.lower()).strip("-")
        county = _COUNTY_BY_SLUG.get(key, "")
        return {
            "name": named.strip(),
            "slug": key,
            "page": "",
            "county": county,
            "county_page": _COUNTY_PAGE.get(county, "service-areas.html"),
        }
    return {
        "name": "Tampa Bay",
        "slug": "",
        "page": "",
        "county": "Pasco, Pinellas, and Hillsborough",
        "county_page": "service-areas.html",
    }


def _esc(value: Any) -> str:
    return html.escape(str(value or "").strip())


def _seed(*parts: str) -> random.Random:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return random.Random(int(digest, 16))


def _p(text: str) -> str:
    return f"<p>{_esc(text)}</p>"


def _h2(text: str) -> str:
    return f"<h2>{_esc(text)}</h2>"


def _h3(text: str) -> str:
    return f"<h3>{_esc(text)}</h3>"


def _words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def _ensure(body: str, extras: list[str]) -> str:
    used = body
    for extra in extras:
        if strip_html_words(used) >= MIN_WORDS:
            break
        used += _p(extra)
    if strip_html_words(used) < MIN_WORDS:
        raise RuntimeError(f"Job page is {strip_html_words(used)} words, under {MIN_WORDS}")
    return used


def _service(cluster: str) -> tuple[str, str, str]:
    return _SERVICES.get(cluster) or _SERVICES["visit"]


def _detail_bank(bits: dict[str, str]) -> list[str]:
    city, county, service, title = bits["city"], bits["county"], bits["service"], bits["title"]
    return [
        (
            f"{title} is a {service} project in {city}. The public page shows the branded before, process, and after "
            f"composite Screen Team built from the job photos. It is not a stock enclosure. Salt air, oak litter, and "
            f"afternoon storms in {county} age spline, chalk the mesh, and open tears at the corners first. Chris Westcott "
            f"uses those photos to explain what was failing before anyone talks about a bigger rescreen."
        ),
        (
            f"A pool cage or lanai in {city} fails in a pattern homeowners can see once it is pointed out. The lower "
            f"panels go brittle where irrigation and pets hit them. Roof panels belly after summer rain sits in the mesh. "
            f"Door screens tear at the closer because that panel cycles every day. The before column of this composite "
            f"is there so the starting condition stays attached to the finished photo, instead of disappearing into a camera roll."
        ),
        (
            f"Screen Team is owner-operated. {OWNER} measures, quotes, and does the enclosure work. There is no call center "
            f"rewriting the {city} job after the photos were taken. If the frame is still sound, the repair stays a repair. "
            f"If the mesh is oxidized across the whole cage, the honest conversation is a full rescreen, and that is a "
            f"different scope from patching the one torn bay a storm opened."
        ),
        (
            f"Florida screen is held by spline pressed into an aluminum groove. When the spline shrinks, the panel "
            f"looks tight on a calm morning and loose by the next thunderstorm. In {county}, that cycle is normal. "
            f"Process photos on a {service} job show the old spline coming out, the groove cleared, and the new mesh "
            f"rolled in. That middle frame is what separates a real visit from a before-and-after that could have been two different houses."
        ),
        (
            f"Access changes the work more than a thumbnail suggests. A ranch lanai in {city} is a ladder and a careful "
            f"walk on the chair rail. A two-story cage needs a plan for the roof panels and for where the ladder lands "
            f"so the deck and the pool coping stay protected. The composite does not hide the height. If the after photo "
            f"still shows a tall mansard, the job was a tall-cage repair, not a patio-wall touch-up."
        ),
        (
            f"Mesh choice is part of the look homeowners notice after the tear is gone. Standard fiberglass is the usual "
            f"repair when the rest of the cage still matches. Pet-resistant mesh, no-see-um, and aluminum are upgrades "
            f"and they are discussed separately because they change the feel of the enclosure and the way the door closes. "
            f"This {title} page does not pretend an upgrade was installed unless the photos and the scope say so."
        ),
        (
            f"Super gutters and chair-rail gutters are not the same thing as a house gutter on a fascia. Enclosure gutters "
            f"carry roof-panel water across the cage beam. When they clog with oak flowers or split at a joint, the water "
            f"dumps onto the deck and stains the lower screen. If this {city} composite is a screen repair rather than a "
            f"gutter replacement, the gutter is mentioned only where it affected the panels that were actually redone."
        ),
        (
            f"New pool enclosures are a different product from a rescreen. Permits, engineering, and wind-load paperwork "
            f"belong with the licensed partner path when the structure is new. Screen Team still scopes the customer "
            f"conversation. A page about {title} does not turn a repair composite into a new-cage advertisement. If the "
            f"photos show an existing beam and a rescreened bay, that is the job that was done."
        ),
        (
            f"Homeowners in {county} often send the first photos from the lanai door, which hides the roof and the far wall. "
            f"The useful set shows the tear, the door swing, one corner of the beam, and a step-back of the whole enclosure. "
            f"Those are the same angles Chris asks for before a written estimate. This published composite is the later "
            f"version of that idea: starting condition, work in progress, and the enclosure after the agreed panels were finished."
        ),
        (
            f"The after photo should still look like the same yard. Furniture, pool coping, and the neighbor's roof line "
            f"are how a reader in {city} knows the proof is local. Screen Team does not publish the street, the customer "
            f"phone, or the invoice. The city and the type of {service} are enough for the next homeowner to decide "
            f"whether their cage looks like this one."
        ),
        (
            f"Storm weeks in {county} produce a rush of matching tears: one corner blown out, a door bar bent, and a "
            f"roof panel that held water. Patching only the loudest hole leaves a chalky panel next to a bright new one. "
            f"Chris will say when that mismatch is acceptable and when the wall should be rescreened as a run so the "
            f"enclosure does not look repaired one bay at a time. That judgment is the point of looking at the whole before photo."
        ),
        (
            f"Window and garage screens are smaller openings with the same spline logic. A window that sits in a wood "
            f"frame needs the frame to be square before new mesh is worth installing. A retractable garage screen is "
            f"sized to the opening, manual or motorized, and it is not priced like a cage panel. If {title} is an "
            f"enclosure job, those other services stay linked for people who landed here and actually need a window or a garage bay."
        ),
        (
            f"What you can take from this {city} composite is practical. Look at whether the before mesh is gray and "
            f"brittle or still white with one tear. Look at whether the process frame shows spline work or a beam repair. "
            f"Look at whether the after enclosure closes and whether the door still has a closer. Then use the scope page "
            f"for the in-and-out list, and the contact page if your own cage needs the same kind of visit."
        ),
        (
            f"Screen Team's published price list is on the pricing page, including the minimum charge on a completed visit. "
            f"This project page does not repeat a customer's number. Size, height, mesh, and access move a full rescreen. "
            f"A counted panel repair stays a panel repair. {OWNER} confirms the written figure before work starts, from "
            f"photos when the enclosure can be seen clearly and from a look when the beam, the gutter, or the door hardware cannot."
        ),
    ]


def _scope_bank(bits: dict[str, str]) -> list[str]:
    city, county, service, title = bits["city"], bits["county"], bits["service"], bits["title"]
    return [
        (
            f"The scope for {title} is the {service} work that was actually done in {city}, not every service Screen Team offers. "
            f"Chris writes the visit around the enclosure that was photographed: which bays, whether the door was included, "
            f"and whether the frame was already sound. A scope page exists so a neighbor with a similar cage can see the "
            f"boundary of the job before asking for the same thing."
        ),
        (
            f"In scope for a normal {service} visit is removal of the failed spline, clearance of the aluminum groove, "
            f"new mesh cut to the opening, and spline rolled so the panel is tight without tearing at the corner. "
            f"Door bars and closers are in scope when the brief says the door was part of the visit. They are not assumed "
            f"just because a cage has a door. The process photos are the record of that sequence."
        ),
        (
            f"Out of scope, unless a separate written line says otherwise, is structural aluminum replacement, new-cage "
            f"engineering, permit drawings, electrical for a motorized opener, and patio construction. Screen Team will "
            f"say when a {city} beam is too far gone to hold new mesh. That conversation happens before the rescreen, "
            f"not after the panel is already in the groove."
        ),
        (
            f"Fastener and spline condition decides whether a small repair is honest. If the groove is crushed, new spline "
            f"will not hold and the panel will walk out in the next storm. In {county} that shows up on older mansards "
            f"and on doors that have been forced shut. The scope then becomes hardware plus screen, or a recommendation "
            f"to stop and talk about the frame, rather than a promise that mesh alone will fix a bent member."
        ),
        (
            f"Roof panels are in scope only when they were part of the measured count. An eight-foot-wide roof bay is "
            f"still one panel until someone counts the bays. Length that cannot be seen from the first photo is a reason "
            f"to look again, not a reason to invent a full-cage price. This {title} scope stays with the openings that "
            f"were identified. Extra bays are a revised estimate, not a surprise add-on after the ladder is up."
        ),
        (
            f"Gutter scope is separate from screen scope. A clogged enclosure gutter can be cleaned or a leaking joint "
            f"repaired without rescreening the wall under it. A super gutter, the structural trough on the cage, is "
            f"quoted from the footage and the condition of the beam. If this {city} composite does not show gutter work "
            f"in the process column, gutter replacement was not this visit."
        ),
        (
            f"Mesh upgrades are out of the base repair until they are chosen. Pet-resistant, no-see-um, and aluminum "
            f"change the panel and sometimes the spline size. They are quoted on their own line so a {service} repair "
            f"in {county} does not silently become an upgrade. The after photo should match the mesh that was agreed, "
            f"including the color, so the enclosure does not read as a patchwork of leftover rolls."
        ),
        (
            f"Cleanup in scope is the spline scrap, the old mesh, and the fasteners from the bays that were opened. "
            f"It is not a haul-off of patio furniture, a pool-deck rebuild, or a landscape visit. Chris leaves the "
            f"{city} enclosure usable: door swinging, closer seated, and the deck clear of the cut pieces. The after "
            f"frame is how that standard is checked."
        ),
        (
            f"A second trip is in scope only when the first visit could not finish the agreed openings, for example "
            f"because a special mesh had to be ordered or a bent door bar had to be sourced. Drive time inside the "
            f"normal {county} route is not a separate customer line on a single completed visit. A return caused by "
            f"a changed scope is written down before the return is scheduled."
        ),
        (
            f"What Chris needs before he will match this scope on another house is simple. Photos of every damaged bay, "
            f"the door from inside and outside, and one photo that shows cage height. A note that says how many panels "
            f"you can count. The city. From that, Screen Team drafts a range off the published list and {OWNER} edits "
            f"it before anyone is asked to sign. The draft itself does not email or text the customer."
        ),
        (
            f"Window-screen scope is a counted opening at the published per-screen range, with the job minimum still "
            f"applying when the count is small. Garage-screen scope is the opening size and whether the system is "
            f"manual or motorized. Neither of those is a pool-cage panel, and neither should be copied onto a {service} "
            f"page as if it were the same visit. The links on this page go to those services for people who need them instead."
        ),
        (
            f"The companion project page for {title} describes what the {city} enclosure looked like before and after. "
            f"This scope page is the boundary. Use it to see that Screen Team will repair the screen that failed, talk "
            f"plainly when the frame will not hold mesh, and keep new construction and engineering on the partner path. "
            f"That is the whole offer. It is not a land-clearing crew and it is not a handyman hourly visit."
        ),
        (
            f"If your cage in {county} matches the before column, start with the service page linked below and send "
            f"photos through the contact form or call {OWNER} directly. Ask for the same boundary you see here: named "
            f"openings, a yes or no on the door, and a separate conversation if the gutter or the beam is the real problem. "
            f"The published pricing page is where the from-prices live. This composite does not publish the customer's total."
        ),
        (
            f"Signed estimates stay as they were signed. A later photo set does not rewrite a price a customer already "
            f"accepted. If the {city} job grows because another wall failed, that is a revised scope, written before "
            f"the extra panels are done. The public composite only shows the visit that was finished and photographed."
        ),
    ]


def _cluster_extra(cluster: str, bits: dict[str, str], *, scope: bool) -> list[str]:
    city, service = bits["city"], bits["service"]
    detail = {
        "full_rescreen": f"A full rescreen in {city} means the enclosure mesh is replaced as a system, not one bright patch in a gray wall. Height, footprint, and how the ladder lands on the deck are why these jobs are looked at before a single from-price is treated as the final number.",
        "panels": f"A counted panel repair in {city} stays on the panel rate. Roof bays and wall bays are both panels once they are counted. Width notes help Chris see the opening. They do not replace the count.",
        "partial": f"A partial cage repair in {city} is the right scope when most of the mesh is still tight and white. The published from-price is the start. A panel count narrows it. Storm damage that opened several bays still does not automatically become a full rescreen.",
        "lanai": f"A lanai in {city} is often a patio wall tied to the house, not a freestanding mansard over a pool. The scope follows that shape. If the photos show a full cage, the job is estimated as a cage instead of being forced into the lanai band.",
        "windows": f"Window screens in {city} are priced per opening, with the completed-visit minimum still in force when the count is small. Frame condition matters more than the mesh brand.",
        "garage": f"A garage or retractable screen in {city} is sized to that opening. Manual systems and motorized systems are different published bands. Chris sets the motorized high side after the opening is measured.",
        "gutter": f"Gutter work in {city} uses footage when the brief has it. A repair with no footage stays at the completed-visit minimum until the run is measured. That footage is not a guess taken from a single wide photo.",
        "super_gutter": f"A super gutter in {city} is quoted after the beam and the run are seen. This draft does not invent a per-foot total when the footage was never stated.",
        "new_enclosure": f"A new enclosure in {city} is custom. The composite, if one is published later, shows the built cage. It does not publish a ten-to-thirty-thousand-dollar range as if that were this customer's price.",
        "hardware": f"Door, spline, and hardware work in {city} starts from the published hardware visit when the frame is still sound. A bent bar or a crushed groove is called out before mesh is promised.",
        "visit": f"A general screen visit in {city} uses the completed-visit minimum until a panel count, a full rescreen, a lanai, or a window count is in the description.",
    }
    scope_line = {
        "full_rescreen": f"Full rescreen scope covers the mesh replacement on the enclosure that was measured, including the roof panels that belong to that cage. It does not include a new beam layout or a permit set.",
        "panels": f"Panel scope is the counted openings only. Uncounted bays stay off the list until they are added in writing.",
        "partial": f"Partial scope is the damaged run, the door only if it was listed, and the spline those openings need. The rest of a sound cage is left alone.",
        "lanai": f"Lanai scope follows the patio screens that were listed. A freestanding pool cage found on site is re-scoped before it is treated as a lanai.",
        "windows": f"Window scope is the counted sashes or screens, not the house windows themselves and not the glass.",
        "garage": f"Garage scope is one opening, manual or motorized as specified. It is not a row of cage panels.",
        "gutter": f"Gutter scope is the measured run or a repair visit when the footage is still unknown. It is not a super-gutter replacement unless that was the job.",
        "super_gutter": f"Super gutter scope waits on footage and beam condition. No dollar figure is published on the job page from a missing measurement.",
        "new_enclosure": f"New enclosure scope is coordination and the screen product that was agreed. Engineering and permits stay on the partner path when they are required.",
        "hardware": f"Hardware scope is spline, fasteners, and the door screen when the metal is sound. Structural member replacement is a different conversation.",
        "visit": f"A general visit scope is the minimum completed visit plus whatever openings were named before the work started.",
    }
    line = scope_line[cluster] if scope else detail[cluster]
    return [
        line,
        f"The service named on this page is {service}. Linked pages below are the Screen Team services that match, plus pricing and the contact form. They are not other companies and not other trades.",
    ]


def _photo_sentence(before: int, process: int, after: int) -> str:
    before, process, after = max(0, before), max(0, process), max(0, after)
    if before + process + after == 0:
        return "The composite uses the before, process, and after photos that were tagged on the job."
    parts = []
    if before:
        parts.append(f"{before} before photo{'s' if before != 1 else ''}")
    if process:
        parts.append(f"{process} in-progress photo{'s' if process != 1 else ''}")
    if after:
        parts.append(f"{after} after photo{'s' if after != 1 else ''}")
    return (
        "The branded composite stacks "
        + ", ".join(parts)
        + ". Each phase fills its column. Empty colored boxes are not used as stand-ins for missing photos."
    )


def _links(bits: dict[str, str], sibling_href: str, sibling_label: str) -> str:
    items = [
        f'<li><a href="{_esc(sibling_href)}">{_esc(sibling_label)}</a></li>',
        f'<li><a href="{_esc(bits["primary_href"])}">{_esc(bits["service"])}</a></li>',
        f'<li><a href="{_esc(bits["secondary_href"])}">Related screen service</a></li>',
        '<li><a href="pricing.html">Screen Team pricing</a></li>',
        '<li><a href="contact.html">Request an estimate</a></li>',
        '<li><a href="gallery.html">Project gallery</a></li>',
        f'<li><a href="{_esc(bits["area_href"])}">{_esc(bits["area_label"])}</a></li>',
    ]
    if bits.get("county_href") and bits["county_href"] != bits["area_href"]:
        items.append(f'<li><a href="{_esc(bits["county_href"])}">{_esc(bits["county"])} screen repair</a></li>')
    return "<ul>" + "".join(items) + "</ul>"


def _faqs(cluster: str, city: str, service: str, *, scope: bool) -> list[tuple[str, str]]:
    if scope:
        return [
            (f"What was included in this {city} {service}?", "The openings that were identified, the spline and mesh for those openings, and the door only when the door was part of the visit."),
            ("Are customer prices shown here?", "No. The published list lives on the pricing page. This page does not print a customer's total, phone, or street."),
            ("Will a new cage be engineered by Screen Team?", "New enclosures that need permits or engineering go through the licensed partner path. Screen Team scopes the customer relationship."),
            (f"Can Chris match this scope in {city}?", "Send photos of the damaged bays, the door, and one photo that shows height. He drafts from the published list and edits it before anything is sent."),
        ]
    return [
        (f"Where was this {service} done?", f"In {city}. The street address is not published."),
        ("Why are there three phases in the image?", "Before, process, and after. The middle frame shows the work, so the after photo is tied to the same enclosure."),
        ("Does a torn panel always mean a full rescreen?", "No. Tight, light-colored mesh around one tear is a panel or partial repair. Uniform chalky mesh is the full-rescreen conversation."),
        ("Who does the work?", f"{OWNER} owns Screen Team and handles the estimate and the enclosure work."),
    ]


def _area_bits(place: dict[str, str]) -> dict[str, str]:
    if place.get("page"):
        return {
            "area_href": place["page"],
            "area_label": f"{place['name']} screen repair",
            "county_href": place.get("county_page") or "service-areas.html",
        }
    county_page = place.get("county_page") or "service-areas.html"
    label = place["county"] if place.get("county") and county_page != "service-areas.html" else "Service areas"
    return {"area_href": county_page, "area_label": label, "county_href": county_page}


def build_gallery_longform(project: dict[str, Any], *, root: Path | None = None) -> dict[str, Any]:
    root = root or website_root()
    slug = re.sub(r"[^a-z0-9-]+", "-", str(project.get("id") or "project").lower()).strip("-") or "project"
    title = clean_public_text(str(project.get("title") or "")) or str(project.get("title") or slug).strip()
    title = re.sub(r"\s+", " ", title).strip() or "Screen Team project"
    cluster = infer_cluster(title)
    place = infer_place(
        " ".join(str(project.get(key) or "") for key in ("title", "summary", "city_name")),
        explicit=str(project.get("city_name") or ""),
        root=root,
    )
    service, primary_href, secondary_href = _service(cluster)
    area = _area_bits(place)
    county = place["county"] or "the Tampa Bay area"
    bits = {
        "city": place["name"],
        "county": county,
        "service": service,
        "title": title,
        "primary_href": primary_href,
        "secondary_href": secondary_href,
        **area,
    }
    before = int(project.get("photo_before") or 0)
    process = int(project.get("photo_process") or 0)
    after = int(project.get("photo_after") or 0)
    image_name = str(project.get("image") or f"Images/gallery/{slug}.webp").replace("\\", "/").split("/")[-1]
    alt = f"{title} before, process, and after {service} in {place['name']} by {BRAND}"
    notes = clean_public_text(str(project.get("work_notes") or project.get("notes") or ""))
    detail_rng = _seed(slug, "detail")
    scope_rng = _seed(slug, "scope")
    detail_paras = _detail_bank(bits)
    scope_paras = _scope_bank(bits)
    detail_rng.shuffle(detail_paras)
    scope_rng.shuffle(scope_paras)

    figure = (
        f'<figure class="job-proof"><img src="Images/gallery/{_esc(image_name)}" alt="{_esc(alt)}" width="1600" height="900">'
        f"<figcaption>{_esc(alt)}</figcaption></figure>"
    )
    detail_body = "".join(
        [
            _h2(f"What this {place['name']} screen job looked like"),
            _p(detail_paras[0]),
            figure,
            _p(_photo_sentence(before, process, after)),
            _h2("How the enclosure was failing"),
            "".join(_p(p) for p in detail_paras[1:8]),
            _p(f"Job notes safe to publish: {notes}") if notes else "",
            _h2("What the finished enclosure shows"),
            "".join(_p(p) for p in detail_paras[8:]),
            "".join(_p(p) for p in _cluster_extra(cluster, bits, scope=False)),
            _h2("Related Screen Team pages"),
            _links(bits, f"gallery/{slug}-scope.html", "Scope of work for this job"),
            _h2("Project questions"),
        ]
    )
    detail_faqs = _faqs(cluster, place["name"], service, scope=False)
    detail_body += "".join(_h3(q) + _p(a) for q, a in detail_faqs)
    detail_body = _ensure(detail_body, _detail_bank(bits) + _cluster_extra(cluster, bits, scope=False))

    in_scope = [
        f"{service.capitalize()} at the openings identified in {place['name']}",
        "Spline removed and replaced in those grooves",
        "Mesh matched to the agreed type, with upgrades only when they were chosen",
        "Door screen and closer when the door was part of the written visit",
        "Scrap mesh and old spline taken off the deck",
        "Before, process, and after photos for this public composite",
    ]
    out_scope = [
        "Structural aluminum design or a new beam layout",
        "Permit drawings and wind-load engineering",
        "Electrical work for motors, lights, or pool equipment",
        "Patio, deck, or pool construction",
        "A customer's street, phone, or invoice printed on this page",
    ]
    scope_body = "".join(
        [
            _h2(f"Scope of work for this {place['name']} {service}"),
            _p(scope_paras[0]),
            figure,
            _p(_photo_sentence(before, process, after)),
            _h2("In scope"),
            "<ul>" + "".join(f"<li>{_esc(item)}</li>" for item in in_scope) + "</ul>",
            "".join(_p(p) for p in scope_paras[1:7]),
            _h2("Out of scope"),
            "<ul>" + "".join(f"<li>{_esc(item)}</li>" for item in out_scope) + "</ul>",
            "".join(_p(p) for p in scope_paras[7:]),
            "".join(_p(p) for p in _cluster_extra(cluster, bits, scope=True)),
            _p(f"Job notes safe to publish: {notes}") if notes else "",
            _h2("Scope links"),
            _links(bits, f"gallery/{slug}.html", "Project details for this job"),
            _h2("Scope questions"),
        ]
    )
    scope_faqs = _faqs(cluster, place["name"], service, scope=True)
    scope_body += "".join(_h3(q) + _p(a) for q, a in scope_faqs)
    scope_body = _ensure(scope_body, _scope_bank(bits) + _cluster_extra(cluster, bits, scope=True))

    summary = (
        f"{service.capitalize()} in {place['name']} — before, process, and after proof from {BRAND}. "
        f"Project details and scope of work. Estimates confirmed by {OWNER}."
    )[:220]
    return {
        "id": slug,
        "cluster": cluster,
        "city_name": place["name"],
        "city_slug": place["slug"],
        "county_name": county,
        "service": service,
        "service_href": primary_href,
        "image_filename": image_name,
        "alt": alt,
        "summary": summary,
        "detail": {
            "path": f"gallery/{slug}.html",
            "title": f"{title} in {place['name']} | {BRAND}",
            "h1": title,
            "meta": f"{title} in {place['name']}: before, process, and after {service} by {OWNER}. Photo proof. No street address.",
            "body_html": detail_body,
            "faqs": detail_faqs,
        },
        "scope": {
            "path": f"gallery/{slug}-scope.html",
            "title": f"{title} scope of work in {place['name']} | {BRAND}",
            "h1": f"{title} — scope of work",
            "meta": f"What was included in this {place['name']} {service}, what was left out, and how to ask {OWNER} for the same kind of visit.",
            "body_html": scope_body,
            "faqs": scope_faqs,
        },
    }


def render_project_page(longform: dict[str, Any], kind: str) -> str:
    page = longform[kind]
    other = longform["scope"] if kind == "detail" else longform["detail"]
    other_label = "Scope of work" if kind == "detail" else "Project details"
    other_href = other["path"]
    canonical = f"{SITE}/{page['path']}"
    image = f"{SITE}/Images/gallery/{longform['image_filename']}"
    faqs = [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in page["faqs"]
    ]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": page["title"],
                "url": canonical,
                "description": page["meta"][:158],
                "primaryImageOfPage": image,
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#business"},
            },
            {
                "@type": "ImageObject",
                "contentUrl": image,
                "name": longform["alt"],
            },
            {
                "@type": "FAQPage",
                "mainEntity": faqs,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Gallery", "item": f"{SITE}/gallery.html"},
                    {"@type": "ListItem", "position": 3, "name": page["h1"], "item": canonical},
                ],
            },
        ],
    }
    schema_json = json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<base href="{SITE}/">
<title>{_esc(page["title"])}</title>
<meta name="description" content="{_esc(page["meta"][:158])}">
<link rel="canonical" href="{_esc(canonical)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:title" content="{_esc(page["title"])}">
<meta property="og:description" content="{_esc(page["meta"][:158])}">
<meta property="og:url" content="{_esc(canonical)}">
<meta property="og:image" content="{_esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_esc(page["title"])}">
<meta name="twitter:image" content="{_esc(image)}">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{schema_json}</script>
<style>
.job-proof img {{ width: 100%; height: auto; border-radius: 12px; }}
.job-proof figcaption {{ color: var(--muted, #b8d4e8); font-size: .9rem; margin-top: .4rem; }}
.job-actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }}
</style>
</head>
<body>
<a class="skip-nav" href="#main-content">Skip to main content</a>
<div id="site-header-include"></div>
<main id="main-content">
  <section class="sp-hero">
    <div class="container">
      <p class="breadcrumb-trail"><a href="/">Home</a> &rsaquo; <a href="gallery.html">Gallery</a> &rsaquo; {_esc(page["h1"])}</p>
      <h1>{_esc(page["h1"])}</h1>
      <p>{_esc(page["meta"])}</p>
      <p class="job-actions"><a class="btn btn-primary" href="contact.html">Request an estimate</a> <a class="btn btn-ghost" href="{_esc(other_href)}">{_esc(other_label)}</a></p>
    </div>
  </section>
  <section class="section-shell">
    <div class="container sp-layout">
      <div class="sp-content">
        {page["body_html"]}
      </div>
      <aside class="sp-sidebar">
        <div class="hero-card">
          <p class="card-eyebrow">Screen Team</p>
          <h2>{_esc(OWNER)}</h2>
          <p class="card-note"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
          <p><a class="btn btn-primary" href="contact.html">Send photos</a></p>
          <p><a href="pricing.html">Published pricing</a></p>
          <p><a href="{_esc(other_href)}">{_esc(other_label)}</a></p>
        </div>
      </aside>
    </div>
  </section>
</main>
<div id="site-footer-include"></div>
<script src="includes.js"></script>
<script src="script.js"></script>
</body>
</html>
"""
