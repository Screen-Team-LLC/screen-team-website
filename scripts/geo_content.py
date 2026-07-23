#!/usr/bin/env python3
"""Unique geo content for Screen Team city/county SEO pages. Imported by generate-geo-seo-pages.py."""
from __future__ import annotations

G = {
    "pano1": "Images/gallery/PXL_20240909_160616822.PANO.jpg",
    "pano2": "Images/gallery/PXL_20240729_174347617.PANO.jpg",
    "pano3": "Images/gallery/PXL_20240206_142627868.PANO.jpg",
    "cage1": "Images/gallery/20221018_121328.jpg",
    "cage2": "Images/gallery/20220801_110201.jpg",
    "cage3": "Images/gallery/20221223_163807.jpg",
    "cage4": "Images/gallery/20220702_131643.jpg",
    "door": "Images/gallery/20220406_152238.jpg",
    "lanai": "Images/gallery/20220406_152213.jpg",
    "tall": "Images/gallery/IMG_2641.jpeg",
    "done": "Images/gallery/IMG_2574.jpeg",
    "mesh": "Images/gallery/IMG_0984.jpeg",
    "porch": "Images/gallery/IMG_0985.jpeg",
    "work": "Images/gallery/IMG_1864.jpeg",
    "side": "Images/gallery/20220816_113149.jpg",
    "preview": "Images/preview/services/pool-enclosures.jpg",
    "rescreen": "Images/preview/services/rescreens.jpg",
}

PASCO, PIN, HILL = "Pasco", "Pinellas", "Hillsborough"
PASCO_L, PIN_L, HILL_L = (
    "pasco-county-screen-repair.html",
    "pinellas-county-screen-repair.html",
    "hillsborough-county-screen-repair.html",
)


def svc(city: str) -> list[str]:
    return [
        f'<a href="rescreens.html">Full pool cage rescreen</a> in {city} — when mesh is chalky cage-wide',
        f'<a href="pool-enclosures.html">New enclosure / new cage inquiry</a> — partner path for permits &amp; engineering',
        f'<a href="gutters-and-screens.html">Super gutters &amp; enclosure gutters</a> — oversized drainage on cage headers',
        f'<a href="pool-cage-repair.html">Pool cage repair</a> — partial walls, roof rows, storm tears',
        f'<a href="lanai-screen-replacement.html">Lanai screen replacement</a> &amp; <a href="screen-panel-repair.html">panel repair</a>',
        f'<a href="window-screens.html">Window screens</a>, <a href="storm-screen-repair.html">storm repairs</a>, pet-door upgrades',
    ]


def C(
    slug, name, county, county_link, title, meta, keywords, h1, hero_lead,
    intro_title, intro, neighborhoods_title, neighborhoods, local_note,
    priority_title, priority, conditions_title, conditions, nearby, faq,
    scheduling, cta, hero_imgs, gallery, og_img=None, process=None, area_type="City",
):
    d = dict(
        slug=slug, city=name, county=county, county_link=county_link, title=title,
        meta_desc=meta, keywords=keywords, h1=h1, hero_lead=hero_lead,
        intro_title=intro_title, intro=intro, neighborhoods_title=neighborhoods_title,
        neighborhoods=neighborhoods, local_note=local_note, priority_title=priority_title,
        priority=priority, conditions_title=conditions_title, conditions=conditions,
        services=svc(name), nearby=nearby, faq=faq, scheduling=scheduling, cta=cta,
        hero_imgs=hero_imgs, gallery=gallery, og_img=og_img or hero_imgs[0][0],
        area_type=area_type,
    )
    if process:
        d["process"] = process
    return d


def all_cities() -> list[dict]:
    cities: list[dict] = []

    # ── PASCO existing ────────────────────────────────────────────────────
    cities.append(C(
        "new-port-richey-screen-repair", "New Port Richey", PASCO, PASCO_L,
        "Screen Repair New Port Richey FL | Pool Cage & Super Gutters | Screen Team",
        "Pool cage rescreen, new enclosure inquiries &amp; super gutters in New Port Richey, FL. Owner Chris Westcott. (727) 386-6562.",
        "screen repair New Port Richey, pool cage rescreen NPR, super gutters New Port Richey, lanai screen repair Pasco",
        "Screen Repair, Pool Cages &amp; Super Gutters in New Port Richey, FL",
        "Home base for The Screen Team LLC — full pool cage rescreens, partner-path new enclosure inquiries, and super gutters with Chris Westcott on every ladder.",
        "New Port Richey — where Screen Team schedules start",
        [
            "New Port Richey is not just another pin on our map — it is the home base. From canal streets near the Pithlachascotee to ranch cages along US-19 and two-story enclosures tucked behind Madison Street corridors, Chris Westcott already knows how west Pasco cages age: Gulf humidity on the lower row, oak litter on roof panels, and lanai doors that lose spline years before the walls look bad.",
            "When homeowners search <strong>screen repair New Port Richey</strong>, they usually need a straight answer: patch a storm tear, rescreen the whole cage, ask about a brand-new enclosure, or fix the gutter that keeps dumping water onto the screen header. The Screen Team LLC handles those workstreams every week — and routes new-build inquiries through licensed partners when permits and engineering are required.",
            "Because NPR is home, same-week slots are more common here than on cross-bay Pinellas or east Hillsborough days. Text photos to <a href=\"tel:7273866562\">(727) 386-6562</a> and Chris will tell you whether you need a panel job, a full <a href=\"rescreens.html\">pool cage rescreen</a>, or a conversation about a new cage entirely. Neighborhood familiarity matters: he already knows which canal streets need corrosion checks and which inland blocks fail first on roof horizontals after summer cells.",
        ],
        "New Port Richey neighborhoods &amp; enclosure types",
        [
            ("<strong>Downtown / Madison corridor</strong>", "compact lanais, porch screens, quick door repairs"),
            ("<strong>Gulf Harbors / west canal streets</strong>", "salt-tinged lower panels, hardware checks"),
            ("<strong>East of Little Road</strong>", "taller 1990s–2000s cages needing ladder quotes"),
            ("<strong>Jasmine Lakes / Beacon Woods border</strong>", "retirement lanais and snowbird refreshes"),
            ("<strong>River Ridge adjacency</strong>", "family pools, pet-damaged door panels"),
        ],
        "<strong>Home-base advantage:</strong> NPR pairs with <a href=\"port-richey-screen-repair.html\">Port Richey</a>, <a href=\"holiday-screen-repair.html\">Holiday</a>, and <a href=\"hudson-screen-repair.html\">Hudson</a> on the same west-Pasco loop.",
        "Priority work: full rescreens, new enclosure inquiries, super gutters",
        [
            "Full pool cage rescreens are the core call once mesh turns chalky on every wall. Chris removes oxidized screen, checks posts and doors, and rolls new mesh with proper spline tension — usually in a day on typical west-Pasco footprints. If only a roof row or dog door failed, he quotes a partial instead of upselling the whole cage.",
            "Need a <em>new</em> pool enclosure or structural rebuild? Screen Team routes those inquiries through licensed contractor partners when engineering stamps or county permits are required. Chris remains your local contact — start on <a href=\"pool-enclosures.html\">pool enclosures</a>.",
            "Super gutters and oversized enclosure gutters matter where oak canopy dumps leaves into shallow troughs. Overflow stains fascia and accelerates spline failure along the top plate. Ask about <a href=\"gutters-and-screens.html\">gutters and screens</a>. Small jobs — window screens, single panels, storm patches — still book alongside the big work.",
        ],
        "West Pasco weather on New Port Richey cages",
        [
            "Afternoon squalls peel roof horizontals first. Chris replaces torn sections when aluminum is still plumb — see <a href=\"storm-screen-repair.html\">storm screen repair</a>. Uniform oxidation that snaps in your fingers usually means a full rescreen is the honest fix.",
            "Canal breezes fatigue west-facing door spline. If the latch will not catch but mesh looks fine, the door panel is often first. Family cages near River Ridge get <a href=\"pet-resistant-screen-mesh.html\">pet-resistant mesh</a> on the abuse door when standard fiberglass keeps failing.",
        ],
        [("port-richey-screen-repair.html", "Port Richey"), ("holiday-screen-repair.html", "Holiday"), ("hudson-screen-repair.html", "Hudson"), ("trinity-screen-repair.html", "Trinity"), ("pasco-county-screen-repair.html", "Pasco hub"), ("rescreens.html", "Rescreens"), ("gutters-and-screens.html", "Super gutters"), ("pool-enclosures.html", "New enclosures")],
        [
            ("Is New Port Richey your home base?", "Yes. The Screen Team LLC is based in New Port Richey — west Pasco jobs often schedule fastest."),
            ("Do you do full pool cage rescreens in NPR?", "Yes. Full and partial rescreens are core work. Chris quotes from photos when possible."),
            ("Can you help if I need a brand-new enclosure?", "New enclosure inquiries go through a licensed partner path when permits/engineering are required. Call Chris to start."),
            ("Do you install super gutters on pool cages?", "Yes. Oversized enclosure gutters and gutter/screen bundles are quoted with cage work."),
            ("What is the minimum job charge?", "$150 minimum on completed jobs. Window screens and single panels still qualify when they meet the minimum."),
        ],
        [("<strong>Text photos first</strong>", "Wide cage shot plus close-ups of tears or chalky mesh."), ("<strong>Mention canal vs inland</strong>", "Access and salt wear differ."), ("<strong>Bundle gutters</strong>", "If headers stay wet, ask about super gutters.")],
        "New Port Richey screen repair — call the owner at home base.",
        [(G["pano2"], "Pool cage rescreen New Port Richey Pasco"), (G["cage1"], "Lanai screen repair west Pasco"), (G["door"], "Pool cage door spline NPR"), (G["tall"], "Tall enclosure rescreen New Port Richey")],
        [(G["cage4"], "Pool enclosure — New Port Richey"), (G["done"], "Completed cage rescreen — west Pasco")],
    ))

    # Remaining cities loaded from companion modules to keep this file maintainable
    from geo_data_pasco import PASCO_CITIES
    from geo_data_pinellas import PINELLAS_CITIES
    from geo_data_hillsborough import HILLSBOROUGH_CITIES
    from geo_data_counties import COUNTY_PAGES

    cities.extend(PASCO_CITIES)
    cities.extend(PINELLAS_CITIES)
    cities.extend(HILLSBOROUGH_CITIES)
    return cities, COUNTY_PAGES


# Avoid circular import issues when modules import C, G, etc.
def get_shared():
    return {
        "C": C, "G": G, "PASCO": PASCO, "PIN": PIN, "HILL": HILL,
        "PASCO_L": PASCO_L, "PIN_L": PIN_L, "HILL_L": HILL_L, "svc": svc,
    }
