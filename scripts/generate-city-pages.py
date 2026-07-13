#!/usr/bin/env python3
"""One-off generator for unique city landing pages. Run from repo root."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CITIES = [
    {
        "slug": "pinellas-park-screen-repair",
        "city": "Pinellas Park",
        "county": "Pinellas",
        "county_link": "pinellas-county-screen-repair.html",
        "title": "Pool Screen Repair Pinellas Park FL | Cage & Lanai | Screen Team",
        "meta_desc": "Pool screen repair &amp; pool cage rescreens in Pinellas Park, FL. South Pinellas owner-direct service from Chris Westcott. (727) 386-6562.",
        "keywords": "pool screen repair pinellas park fl, screen repair Pinellas Park FL, pool cage rescreen Pinellas Park, lanai screen repair south Pinellas",
        "h1": "Pool Screen Repair &amp; Pool Cages in Pinellas Park, FL",
        "hero_lead": "South Pinellas pool cages between St. Pete and Seminole — tall sections, busy lanai doors, and honest panel counts from Chris Westcott.",
        "hero_imgs": [
            ("Images/gallery/20221018_121328.jpg", "Pool screen repair on Pinellas Park FL residential cage"),
            ("Images/gallery/IMG_2641.jpeg", "Tall pool enclosure rescreen Pinellas Park area"),
            ("Images/gallery/20220406_152238.jpg", "Lanai door spline repair south Pinellas"),
            ("Images/gallery/20220702_131643.jpg", "Completed pool cage panel work Pinellas Park"),
        ],
        "og_img": "Images/gallery/20221018_121328.jpg",
        "section1_title": "Pinellas Park — working-class cages with real ladder height",
        "section1": "Pinellas Park packs mid-century ranch homes and newer infill lots behind every major corridor — and almost every backyard has a pool cage that predates modern mesh standards. The Screen Team LLC treats <strong>pool screen repair Pinellas Park FL</strong> jobs as ladder-first work: Chris measures height, checks door sag, and quotes panels instead of defaulting to a full rescreen speech.",
        "neighborhoods_title": "Pinellas Park neighborhoods we know",
        "neighborhoods": [
            ("<strong>Park Boulevard corridor</strong>", "mixed-age cages, oxidation on west-facing walls"),
            ("<strong>62nd Avenue North</strong>", "lanai doors that fail before roof panels"),
            ("<strong>Cross Bayou / Kenneth City border</strong>", "storm patches on top horizontals"),
            ("<strong>Pinellas Park Blvd south</strong>", "taller two-story cages needing upfront ladder quotes"),
        ],
        "local_note": "<strong>South Pinellas reality:</strong> Pinellas Park cages often share fence lines with <a href=\"seminole-screen-repair.html\">Seminole</a> and <a href=\"largo-screen-repair.html\">Largo</a> subdivisions — Chris batches south-county routes to keep scheduling tight.",
        "section2_title": "When Pinellas Park cages need doors before roofs",
        "section2": "The repeat call is not a shredded roof — it is a lanai door that will not latch because spline pulled on the hinge side. Chris replaces door panels with proper tension before quoting wall sections. If mesh is chalky on every wall, he will say a <a href=\"rescreens.html\">full rescreen</a> beats a fourth patch in the same season.",
        "gallery": [
            ("Images/gallery/20221018_121328.jpg", "Pool cage rescreen — Pinellas Park area"),
            ("Images/gallery/IMG_0984.jpeg", "Lanai panel repair — south Pinellas Park"),
        ],
        "scheduling": [
            ("<strong>Mention cross streets</strong>", "Park Blvd, 66th St, or 62nd Ave N helps route planning."),
            ("<strong>Photo the door first</strong>", "Most Pinellas Park repairs start at the entry panel."),
            ("<strong>HOA timelines</strong>", "Chris works within reasonable HOA notice windows when you have one."),
        ],
        "faq": [
            ("Do you serve Pinellas Park for pool screen repair?", "Yes. Pinellas Park is a core south Pinellas route for pool cages, lanais, and porch panels."),
            ("How much does a pool cage rescreen cost in Pinellas Park?", "Many cages land $2,500–$6,500+ depending on height. Partial repairs from $175–$750. See <a href=\"pricing.html\">pricing</a>."),
        ],
        "cta": "Pinellas Park pool screen repair — call Chris with door photos first.",
    },
    {
        "slug": "gulfport-screen-repair",
        "city": "Gulfport",
        "county": "Pinellas",
        "county_link": "pinellas-county-screen-repair.html",
        "title": "Pool Cage Rescreen Gulfport FL | Waterfront Lanais | Screen Team",
        "meta_desc": "Pool cage rescreen &amp; lanai repair in Gulfport, FL — waterfront salt, bungalows &amp; marina district. Chris Westcott. (727) 386-6562.",
        "keywords": "pool cage rescreen gulfport fl, screen repair Gulfport FL, lanai screen repair Gulfport, waterfront pool enclosure repair",
        "h1": "Pool Cage Rescreen &amp; Lanai Repair in Gulfport, FL",
        "hero_lead": "Gulfport bungalows, marina breezes, and salt on the lower cage row — Chris rescreens and patches with coastal wear in mind.",
        "hero_imgs": [
            ("Images/gallery/PXL_20240909_160616822.PANO.jpg", "Waterfront pool cage rescreen Gulfport Florida"),
            ("Images/gallery/IMG_2574.jpeg", "Lanai repair near Boca Ciega Bay Gulfport"),
            ("Images/gallery/20220406_152213.jpg", "Dark frame lanai rescreen Gulfport bungalow"),
            ("Images/gallery/20220801_110201.jpg", "Pool enclosure panels tensioned Gulfport area"),
        ],
        "og_img": "Images/gallery/PXL_20240909_160616822.PANO.jpg",
        "section1_title": "Gulfport — salt air starts at the bottom horizontal",
        "section1": "Gulfport sits on Boca Ciega Bay with arts-district bungalows and older waterfront blocks where pool cages catch Gulf moisture even when the address is not on the beach. <strong>Pool cage rescreen Gulfport FL</strong> jobs often mean replacing the lower row and door panels while upper mesh still looks acceptable — Chris inspects aluminum bases for corrosion before rolling new screen.",
        "neighborhoods_title": "Gulfport areas &amp; enclosure types",
        "neighborhoods": [
            ("<strong>Waterfront district</strong>", "salt-stained lower panels, hardware checks"),
            ("<strong>Beach Boulevard corridor</strong>", "compact lanais on 1940s bungalows"),
            ("<strong>Marina / Shore Blvd</strong>", "wind exposure on roof horizontals"),
            ("<strong>St. Pete border streets</strong>", "mixed porch and cage repairs"),
        ],
        "local_note": "<strong>Coastal Gulfport:</strong> If only the bottom cage row is chalky, partial replacement may suffice — see <a href=\"pool-cage-repair.html\">pool cage repair</a> vs <a href=\"rescreens.html\">full rescreen</a>.",
        "section2_title": "Historic porches beside modern pool patios",
        "section2": "Gulfport has more variety per block than most Pinellas cities — front porches with custom panel sizes beside full pool enclosures out back. Chris cuts mesh to fit instead of forcing stock panels that gap at corners. Window screen batches are common before winter guests arrive.",
        "gallery": [
            ("Images/gallery/PXL_20240909_160616822.PANO.jpg", "Waterfront cage work — Gulfport"),
            ("Images/gallery/20220406_152213.jpg", "Bungalow lanai — Gulfport area"),
        ],
        "scheduling": [
            ("<strong>Access notes</strong>", "Alley parking and narrow side yards — mention if ladder setup is tight."),
            ("<strong>Salt damage photos</strong>", "Shoot the bottom row and any white corrosion on feet."),
            ("<strong>Bundle porch + cage</strong>", "Both need work? One visit when schedules align."),
        ],
        "faq": [
            ("Do you rescreen pool cages in Gulfport?", "Yes. Gulfport is on our south Pinellas route from New Port Richey."),
            ("Can you fix salt-damaged lower panels only?", "Often yes when upper mesh is still tight and aluminum is sound."),
        ],
        "cta": "Gulfport pool cage rescreen — text photos of the lower cage row.",
    },
    {
        "slug": "brandon-screen-repair",
        "city": "Brandon",
        "county": "Hillsborough",
        "county_link": "hillsborough-county-screen-repair.html",
        "title": "Pool Screen Repair Brandon FL | Hillsborough Cages | Screen Team",
        "meta_desc": "Pool screen repair &amp; lanai rescreens in Brandon, FL — east Hillsborough subdivisions &amp; Valrico border. Chris Westcott. (727) 386-6562.",
        "keywords": "pool screen repair brandon fl, screen repair Brandon FL, pool cage rescreen Brandon, lanai repair Hillsborough County",
        "h1": "Pool Screen Repair &amp; Lanai Rescreens in Brandon, FL",
        "hero_lead": "East Hillsborough subdivisions with massive pool cages — Chris routes Brandon when you call, with ladder height quoted upfront.",
        "hero_imgs": [
            ("Images/gallery/20220801_110201.jpg", "Large pool cage rescreen Brandon Hillsborough"),
            ("Images/gallery/IMG_2641.jpeg", "Two-story enclosure repair Brandon FL area"),
            ("Images/gallery/20221223_163807.jpg", "Lanai mesh replacement east Hillsborough"),
            ("Images/gallery/20220702_131643.jpg", "Pool screen panel repair Brandon subdivision"),
        ],
        "og_img": "Images/gallery/20220801_110201.jpg",
        "section1_title": "Brandon — big cages, afternoon thunder, straight quotes",
        "section1": "Brandon grew in the 1990s and 2000s with two-story pool enclosures that still dominate Oakwood, Bloomingdale, and FishHawk border streets. <strong>Pool screen repair Brandon FL</strong> means honest talk about ladder time: Chris quotes tall sections separately so you are not surprised when the cage peaks above the roofline.",
        "neighborhoods_title": "Brandon &amp; nearby pockets",
        "neighborhoods": [
            ("<strong>Bloomingdale</strong>", "large cages, wind-torn roof horizontals"),
            ("<strong>Providence / Lithia border</strong>", "newer mesh upgrades and pet doors"),
            ("<strong>Valrico adjacency</strong>", "lanai additions off main living areas"),
            ("<strong>Highway 60 corridor</strong>", "quick porch panel repairs between cage jobs"),
        ],
        "local_note": "<strong>Hillsborough travel:</strong> Brandon jobs are confirmed for east-county routing from New Port Richey — call early in the week for best slotting. See <a href=\"hillsborough-county-screen-repair.html\">Hillsborough hub</a>.",
        "section2_title": "Storm season on east Hillsborough cages",
        "section2": "Summer cells track west across Brandon with enough wind to peel roof panels in a line. Chris replaces failed horizontals with proper spline tension — and flags bent posts before masking structural issues with mesh. See <a href=\"storm-screen-repair.html\">storm repairs</a> after severe weather.",
        "gallery": [
            ("Images/gallery/20220801_110201.jpg", "Brandon area pool cage rescreen"),
            ("Images/gallery/IMG_2641.jpeg", "Tall enclosure — east Hillsborough"),
        ],
        "scheduling": [
            ("<strong>Report cage height</strong>", "Two-story? Mention it — ladder gear is planned accordingly."),
            ("<strong>Gate codes</strong>", "Many Brandon subdivisions need gate access confirmed day-of."),
            ("<strong>Pet mesh</strong>", "Dogs charging the lanai door? Ask about <a href=\"pet-resistant-screen-mesh.html\">pet-resistant upgrades</a>."),
        ],
        "faq": [
            ("Do you drive to Brandon from Pasco?", "Yes. Brandon is a regular Hillsborough route when scheduled — not a same-day guarantee every day."),
            ("Can you repair one storm-torn panel?", "Yes. Partial repairs when the frame is plumb — <a href=\"screen-panel-repair.html\">panel repair</a>."),
        ],
        "cta": "Brandon pool screen repair — call with subdivision name and cage height.",
    },
    {
        "slug": "wesley-chapel-screen-repair",
        "city": "Wesley Chapel",
        "county": "Pasco",
        "county_link": "pasco-county-screen-repair.html",
        "title": "Screen Enclosures Wesley Chapel FL | New Build Cages | Screen Team",
        "meta_desc": "Screen enclosures &amp; pool cage repair in Wesley Chapel, FL — Wiregrass, Seven Oaks &amp; east Pasco. Chris Westcott. (727) 386-6562.",
        "keywords": "screen repair Wesley Chapel FL, pool cage rescreen Wesley Chapel, screen enclosures new port richey area, lanai repair east Pasco",
        "h1": "Screen Enclosures &amp; Pool Cages in Wesley Chapel, FL",
        "hero_lead": "East Pasco master-planned communities with newer cages still learning Florida UV — Chris repairs, rescreens, and upgrades mesh before oxidation wins.",
        "hero_imgs": [
            ("Images/gallery/20221223_163807.jpg", "Screen enclosure rescreen Wesley Chapel Pasco"),
            ("Images/gallery/20221018_121328.jpg", "Pool cage repair Seven Oaks area"),
            ("Images/gallery/20220406_152213.jpg", "Lanai screen work east Pasco County"),
            ("Images/preview/services/pool-enclosures.jpg", "Newer pool enclosure panel repair Wesley Chapel"),
        ],
        "og_img": "Images/gallery/20221223_163807.jpg",
        "section1_title": "Wesley Chapel — newer cages, first oxidation wave",
        "section1": "Wesley Chapel enclosures are younger than west Pasco stock but Florida sun still turns mesh gray within a decade. Homeowners in Wiregrass, Seven Oaks, and Chapel Pines call when <strong>screen enclosures</strong> show their first uniform chalkiness or when builder-grade spline pops on lanai doors. Chris replaces what failed and tells you if the whole cage is nearing rescreen age.",
        "neighborhoods_title": "Wesley Chapel communities",
        "neighborhoods": [
            ("<strong>Wiregrass / Tampa Premium area</strong>", "family pools, pet-damaged door panels"),
            ("<strong>Seven Oaks</strong>", "two-story cages, ladder access planning"),
            ("<strong>Chapel Pines / Meadow Pointe border</strong>", "lanai extensions off great rooms"),
            ("<strong>SR-54 corridor</strong>", "quick window screen batches between cage jobs"),
        ],
        "local_note": "<strong>East Pasco routing:</strong> Wesley Chapel pairs naturally with <a href=\"land-o-lakes-screen-repair.html\">Land O Lakes</a> runs — mention both properties if you manage rentals.",
        "section2_title": "Builder mesh vs upgrade paths",
        "section2": "First-time rescreens in Wesley Chapel are a chance to pick better visibility mesh or <a href=\"pet-resistant-screen-mesh.html\">pet-resistant doors</a> before the next dog season. Chris does not push upgrades — he explains cost per panel and lets you choose.",
        "gallery": [
            ("Images/gallery/20221223_163807.jpg", "Enclosure rescreen — Wesley Chapel"),
            ("Images/preview/services/rescreens.jpg", "Pool cage refresh — east Pasco"),
        ],
        "scheduling": [
            ("<strong>Subdivision gate</strong>", "Provide community name and gate instructions."),
            ("<strong>Builder warranty expired?</strong>", "Chris handles post-warranty cages daily."),
            ("<strong>Closing soon?</strong>", "Mention timeline — partial jobs can precede listing photos."),
        ],
        "faq": [
            ("Is Wesley Chapel in your service area?", "Yes. East Pasco including Wesley Chapel is within our typical 50-mile coverage."),
            ("Do you work on screened lanais off new construction?", "Yes. Door alignment and spline seating are common first-year fixes."),
        ],
        "cta": "Wesley Chapel screen enclosures — call Chris with your community name.",
    },
    {
        "slug": "holiday-screen-repair",
        "city": "Holiday",
        "county": "Pasco",
        "county_link": "pasco-county-screen-repair.html",
        "title": "Pool Cage Repair Holiday FL | West Pasco | Screen Team",
        "meta_desc": "Pool cage repair &amp; lanai rescreens in Holiday, FL — Anclote, Gulf Harbors &amp; west Pasco coast. Fast routes from NPR. (727) 386-6562.",
        "keywords": "pool cage repair Holiday FL, screen repair Holiday Florida, lanai rescreen west Pasco, pool enclosure repair Gulf Harbors",
        "h1": "Pool Cage Repair &amp; Rescreens in Holiday, FL",
        "hero_lead": "West Pasco coastal cages near Anclote and Gulf Harbors — quick scheduling from our New Port Richey home base.",
        "hero_imgs": [
            ("Images/gallery/PXL_20240729_174347617.PANO.jpg", "Pool cage repair Holiday west Pasco coast"),
            ("Images/gallery/20220702_131643.jpg", "Lanai rescreen Anclote area Holiday FL"),
            ("Images/gallery/20220816_113149.jpg", "Screen enclosure panel work Gulf Harbors"),
            ("Images/gallery/20220406_152238.jpg", "Porch and pool cage repair Holiday Florida"),
        ],
        "og_img": "Images/gallery/PXL_20240729_174347617.PANO.jpg",
        "section1_title": "Holiday — west Pasco coast, close to our home base",
        "section1": "Holiday sits on the Anclote River and Gulf Harbors canals where screened pools catch Gulf humidity and afternoon squalls. <strong>Pool cage repair Holiday FL</strong> jobs schedule fast because New Port Richey is minutes away — Chris is on your cage the same week more often here than cross-bay Pinellas runs.",
        "neighborhoods_title": "Holiday &amp; west Pasco waterfront",
        "neighborhoods": [
            ("<strong>Gulf Harbors</strong>", "canal homes, salt on lower cage panels"),
            ("<strong>Anclote River streets</strong>", "wind off open water, roof panel tears"),
            ("<strong>Holiday Lake / Forest Hills</strong>", "1970s cages entering oxidation years"),
            ("<strong>Tarpon Springs border</strong>", "paired routes with north Pinellas jobs"),
        ],
        "local_note": "<strong>Home base advantage:</strong> Holiday is among the fastest-scheduled cities we serve — see also <a href=\"new-port-richey-screen-repair.html\">New Port Richey</a> and <a href=\"hudson-screen-repair.html\">Hudson</a>.",
        "section2_title": "Canal breezes and cage hardware",
        "section2": "Open water behind the lot means steady breeze that fatigues spline on west-facing doors. Chris checks hinges and door sag when mesh looks fine but the latch will not catch — a hardware fix, not a rescreen upsell.",
        "gallery": [
            ("Images/gallery/PXL_20240729_174347617.PANO.jpg", "Coastal cage work — Holiday area"),
            ("Images/gallery/20220702_131643.jpg", "Pool enclosure repair — west Pasco"),
        ],
        "scheduling": [
            ("<strong>Same-week slots</strong>", "Holiday often books faster than cross-county jobs."),
            ("<strong>Dock / seawall access</strong>", "Mention if ladder setup is canal-side."),
            ("<strong>Gutter overflow</strong>", "Canal homes with leaf load — ask about <a href=\"gutters-and-screens.html\">gutters and screens</a>."),
        ],
        "faq": [
            ("How fast can Holiday pool cage repair be scheduled?", "Often same-week from NPR — call (727) 386-6562 with photos."),
            ("Do you serve Gulf Harbors?", "Yes. Gulf Harbors and Anclote waterfront are core west Pasco routes."),
        ],
        "cta": "Holiday pool cage repair — west Pasco owner-direct service.",
    },
    {
        "slug": "hudson-screen-repair",
        "city": "Hudson",
        "county": "Pasco",
        "county_link": "pasco-county-screen-repair.html",
        "title": "Lanai Screen Repair Hudson FL | North Pasco | Screen Team",
        "meta_desc": "Lanai screen repair &amp; pool cage rescreens in Hudson, FL — Beacon Woods, Sea Pines &amp; north Pasco coast. Chris Westcott. (727) 386-6562.",
        "keywords": "lanai screen repair Hudson FL, screen repair Hudson Florida, pool cage rescreen Hudson, screen enclosure north Pasco",
        "h1": "Lanai Screen Repair &amp; Pool Cages in Hudson, FL",
        "hero_lead": "North Pasco retirement communities and canal blocks — lanai doors, porch panels, and pool cages maintained by Chris, not a rotating crew.",
        "hero_imgs": [
            ("Images/gallery/IMG_0985.jpeg", "Lanai screen repair Hudson FL retirement community"),
            ("Images/gallery/20221018_121328.jpg", "Pool cage rescreen Beacon Woods Hudson area"),
            ("Images/gallery/20220406_152213.jpg", "Screened patio Hudson north Pasco"),
            ("Images/gallery/st-windowscreen.webp", "Window screen batch Hudson Florida home"),
        ],
        "og_img": "Images/gallery/IMG_0985.jpeg",
        "section1_title": "Hudson — lanai doors before roof panels",
        "section1": "Hudson's Beacon Woods, Sea Pines, and waterfront streets have thousands of screened lanais built for year-round living. The dominant <strong>lanai screen repair Hudson FL</strong> call is a door that drags on the track because spline failed on the hinge side — not a catastrophic roof tear. Chris fixes doors first and inspects horizontals second.",
        "neighborhoods_title": "Hudson areas we work",
        "neighborhoods": [
            ("<strong>Beacon Woods</strong>", "lanai doors, porch refreshes before snowbird season"),
            ("<strong>Sea Pines / Sea Ridge</strong>", "canal wind on roof panels"),
            ("<strong>Hudson Beach</strong>", "salt exposure on lower enclosure rows"),
            ("<strong>SR-52 corridor</strong>", "window screen batches with lanai patches"),
        ],
        "local_note": "<strong>North Pasco note:</strong> Hudson pairs with <a href=\"new-port-richey-screen-repair.html\">New Port Richey</a> and <a href=\"tarpon-springs-screen-repair.html\">Tarpon Springs</a> on the same driving loop.",
        "section2_title": "Snowbird prep and oxidation rescreens",
        "section2": "Owners arriving for winter want gray mesh replaced before guests sit on the lanai. Chris schedules oxidation rescreens in fall months when Hudson call volume peaks — full refresh or <a href=\"lanai-screen-replacement.html\">lanai replacement</a> quoted from photos when snowbirds are still up north.",
        "gallery": [
            ("Images/gallery/IMG_0985.jpeg", "Lanai door repair — Hudson"),
            ("Images/gallery/20221018_121328.jpg", "Pool cage — north Pasco coast"),
        ],
        "scheduling": [
            ("<strong>Seasonal timing</strong>", "Book fall lanai refreshes before peak snowbird weeks."),
            ("<strong>Community rules</strong>", "55+ communities — note any contractor sign-in procedures."),
            ("<strong>Window bundles</strong>", "Refresh lanai + bedroom window screens in one trip."),
        ],
        "faq": [
            ("Do you repair lanai doors in Hudson?", "Yes. Door spline and latch alignment are the most common Hudson fixes."),
            ("Is Hudson close to your home base?", "Yes. Hudson is a short drive from New Port Richey for fast scheduling."),
        ],
        "cta": "Hudson lanai screen repair — call before snowbird season fills the calendar.",
    },
    {
        "slug": "land-o-lakes-screen-repair",
        "city": "Land O Lakes",
        "county": "Pasco",
        "county_link": "pasco-county-screen-repair.html",
        "title": "Screen Repair Land O Lakes FL | Connerton Cages | Screen Team",
        "meta_desc": "Screen repair &amp; pool cage rescreens in Land O Lakes, FL — Connerton, Oakstead &amp; east Pasco. Chris Westcott owner-operator. (727) 386-6562.",
        "keywords": "screen repair land o lakes, pool cage rescreen Land O Lakes FL, lanai repair Connerton, screen enclosure east Pasco",
        "h1": "Screen Repair &amp; Pool Cage Rescreens in Land O Lakes, FL",
        "hero_lead": "Connerton, Oakstead, and east Pasco family pools — cage rescreens and lanai fixes with Chris on every ladder.",
        "hero_imgs": [
            ("Images/gallery/20220801_110201.jpg", "Pool cage rescreen Land O Lakes Connerton"),
            ("Images/gallery/20221223_163807.jpg", "Screen enclosure repair Oakstead Pasco"),
            ("Images/gallery/IMG_2641.jpeg", "Large lanai rescreen Land O Lakes FL"),
            ("Images/preview/services/rescreens.jpg", "Family pool cage refresh east Pasco County"),
        ],
        "og_img": "Images/gallery/20220801_110201.jpg",
        "section1_title": "Land O Lakes — east Pasco growth, family-sized cages",
        "section1": "Land O Lakes exploded with master-planned neighborhoods where every backyard has a pool and a cage built for kids, dogs, and weekend cookouts. <strong>Screen repair Land O Lakes</strong> searches spike when school lets out and dogs discover the weak lanai door panel. Chris replaces abuse zones with <a href=\"pet-resistant-screen-mesh.html\">tougher mesh</a> when standard fiberglass keeps failing.",
        "neighborhoods_title": "Land O Lakes communities",
        "neighborhoods": [
            ("<strong>Connerton</strong>", "large family cages, pet-damaged doors"),
            ("<strong>Oakstead / Wilderness Lake</strong>", "first full rescreens on 15-year-old mesh"),
            ("<strong>Collier Parkway corridor</strong>", "lanai additions and porch ties-ins"),
            ("<strong>Lutz border streets</strong>", "paired scheduling with north Hillsborough"),
        ],
        "local_note": "<strong>East Pasco:</strong> Land O Lakes routes with <a href=\"wesley-chapel-screen-repair.html\">Wesley Chapel</a> — mention both addresses if you manage multiple rentals.",
        "section2_title": "Kids, pets, and the door panel that always fails",
        "section2": "The mesh that tears is rarely random — it is the door the teenagers use all summer. Chris aligns latches, replaces hinge-side spline, and upgrades that panel when repeat patches stop making sense.",
        "gallery": [
            ("Images/gallery/20220801_110201.jpg", "Cage rescreen — Land O Lakes"),
            ("Images/preview/services/rescreens.jpg", "Pool enclosure — east Pasco"),
        ],
        "scheduling": [
            ("<strong>Name the community</strong>", "Connerton, Oakstead, etc. — speeds gate planning."),
            ("<strong>Pet traffic</strong>", "Tell Chris which door the dog uses."),
            ("<strong>Summer rush</strong>", "Book early June before tear season peaks."),
        ],
        "faq": [
            ("Do you serve Land O Lakes?", "Yes. Land O Lakes is core east Pasco within our service radius."),
            ("Can you upgrade a lanai door to pet mesh?", "Yes. Door-only upgrades are common — see pet-resistant mesh page."),
        ],
        "cta": "Land O Lakes screen repair — Connerton, Oakstead, and east Pasco routes.",
    },
    {
        "slug": "belleair-screen-repair",
        "city": "Belleair",
        "county": "Pinellas",
        "county_link": "pinellas-county-screen-repair.html",
        "title": "Pool Cage Rescreen Belleair FL | Bluffs & Beach | Screen Team",
        "meta_desc": "Pool cage rescreen &amp; lanai repair in Belleair, FL — Belleair Bluffs, country club estates &amp; Clearwater border. Chris Westcott. (727) 386-6562.",
        "keywords": "pool cage rescreen belleair fl, screen repair Belleair FL, lanai screen repair Belleair Bluffs, pool enclosure Belleair Beach",
        "h1": "Pool Cage Rescreen &amp; Lanai Repair in Belleair, FL",
        "hero_lead": "Belleair estates and Bluffs waterfront cages — careful ladder work, visibility mesh options, and owner-present installs.",
        "hero_imgs": [
            ("Images/gallery/PXL_20240909_160616822.PANO.jpg", "Pool cage rescreen Belleair waterfront estate"),
            ("Images/gallery/IMG_2574.jpeg", "Lanai repair Belleair Bluffs Pinellas"),
            ("Images/gallery/20220406_152213.jpg", "Screened patio Belleair country club area"),
            ("Images/gallery/20220801_110201.jpg", "Tall enclosure panel work Belleair FL"),
        ],
        "og_img": "Images/gallery/PXL_20240909_160616822.PANO.jpg",
        "section1_title": "Belleair — estate cages deserve a measured quote",
        "section1": "Belleair and Belleair Bluffs sit between Clearwater and the Gulf with larger lots, mature landscaping, and enclosures where aesthetics matter as much as function. <strong>Pool cage rescreen Belleair FL</strong> homeowners often want better-visibility mesh and clean spline lines visible from the golf course side — Chris treats those jobs as precision work, not rush patches.",
        "neighborhoods_title": "Belleair &amp; Bluffs pockets",
        "neighborhoods": [
            ("<strong>Belleair Bluffs waterfront</strong>", "salt on lower rows, hardware inspection"),
            ("<strong>Belleair country club area</strong>", "tall cages, landscaping clearance for ladders"),
            ("<strong>Belleair Beach border</strong>", "wind exposure, storm panel patches"),
            ("<strong>Clearwater border estates</strong>", "paired routes with <a href=\"clearwater-screen-repair.html\">Clearwater</a> jobs"),
        ],
        "local_note": "<strong>Estate access:</strong> Mention gate codes, landscaping constraints, and whether HOA architectural review applies — Chris plans ladder placement accordingly.",
        "section2_title": "Visibility mesh and uniform rescreens",
        "section2": "Patching one chalky panel on a Belleair cage visible from the street can look worse than waiting for a uniform rescreen. Chris photographs surrounding mesh color and recommends full <a href=\"rescreens.html\">rescreen</a> when patches would show from the fairway.",
        "gallery": [
            ("Images/gallery/PXL_20240909_160616822.PANO.jpg", "Estate cage — Belleair area"),
            ("Images/gallery/IMG_2574.jpeg", "Lanai refresh — Belleair Bluffs"),
        ],
        "scheduling": [
            ("<strong>Landscaping clearance</strong>", "Note delicate beds or tight side yards."),
            ("<strong>HOA packets</strong>", "Provide color/mesh specs if your HOA requires them."),
            ("<strong>Neighbor sightlines</strong>", "Chris keeps work neat — important on estate lots."),
        ],
        "faq": [
            ("Do you rescreen pool cages in Belleair?", "Yes. Belleair and Belleair Bluffs are on our north Pinellas route."),
            ("Can you match high-visibility mesh?", "Chris discusses visibility options when the water view matters — quoted per panel."),
        ],
        "cta": "Belleair pool cage rescreen — estate-quality work from Chris Westcott.",
    },
]


def faq_html(city_slug, faqs):
    items = []
    for i, (q, a) in enumerate(faqs, 1):
        items.append(f'''          <div class="faq-item">
            <button class="faq-question" aria-expanded="false" aria-controls="{city_slug}-faq-{i}">{q} <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg></button>
            <div class="faq-answer" id="{city_slug}-faq-{i}" aria-hidden="true" inert><div class="faq-answer-inner"><p>{a}</p></div></div>
          </div>''')
    return "\n".join(items)


def render(c):
    slug = c["slug"]
    city_slug = slug.replace("-screen-repair", "")
    hero_panels = "\n".join(
        f'        <div class="hero-panel hero-panel--{"left" if i==0 else "top" if i==1 else "bottom" if i==2 else "right"} hero-panel--photo"><img src="{src}" alt="{alt}" width="800" height="600" decoding="async"></div>'
        for i, (src, alt) in enumerate(c["hero_imgs"])
    )
    neighborhoods = "\n".join(
        f'            <li>{name} — {desc}</li>' for name, desc in c["neighborhoods"]
    )
    gallery = "\n".join(
        f'''        <figure>
          <img src="{src}" alt="{cap} — {c["city"]} area" width="800" height="600" loading="lazy" decoding="async">
          <figcaption>{cap}</figcaption>
        </figure>''' for src, cap in c["gallery"]
    )
    scheduling = "\n".join(
        f'            <li>{title} — {desc}</li>' for title, desc in c["scheduling"]
    )
    url = f"https://screenteamllc.com/{slug}.html"
    faq_schema = ",".join(
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{re.sub(r"<[^>]+>", "", a)}"}}}}'
        for q, a in c["faq"]
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c["title"]}</title>
  <meta name="description" content="{c["meta_desc"]}">
  <meta name="keywords" content="{c["keywords"]}">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM site summary">
  <link rel="alternate" type="text/plain" href="/ai.txt" title="AI crawler summary">
  <link rel="sitemap" type="application/xml" title="Sitemap" href="https://screenteamllc.com/sitemap.xml">
  <meta name="theme-color" content="#3da8d8">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="{c["city"]}, Florida">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="The Screen Team LLC">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{c["title"]}">
  <meta property="og:description" content="{c["meta_desc"]}">
  <meta property="og:image" content="https://screenteamllc.com/{c["og_img"]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{c["title"]}">
  <meta name="twitter:description" content="{c["meta_desc"]}">
  <meta name="twitter:image" content="https://screenteamllc.com/{c["og_img"]}">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Service","@id":"{url}#service","name":"Screen Repair {c['city']} FL","description":"Pool cage rescreens, lanai screen repair, and enclosure panel work in {c['city']}, Florida.","provider":{{"@id":"https://screenteamllc.com/#business"}},"areaServed":{{"@type":"City","name":"{c['city']}, FL"}},"url":"{url}"}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","@id":"{url}#breadcrumb","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://screenteamllc.com/"}},{{"@type":"ListItem","position":2,"name":"Service Areas","item":"https://screenteamllc.com/service-areas.html"}},{{"@type":"ListItem","position":3,"name":"{c['city']}","item":"{url}"}}]}}
  </script>
  <link rel="stylesheet" href="styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-N5V1084LC6"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-N5V1084LC6');</script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "x61prei2pi");
  </script>
</head>
<body>
  <a class="skip-nav" href="#main-content">Skip to main content</a>
  <div id="site-header-include"></div>

  <main id="main-content">
    <section class="sp-hero sp-hero--panels hero" aria-label="{c['city']} screen repair">
      <div class="hero-panels" aria-hidden="true">
{hero_panels}
      </div>
      <div class="sp-hero-overlay" aria-hidden="true"></div>
      <div class="container">
        <p class="breadcrumb-trail"><a href="/">Home</a> &rsaquo; <a href="service-areas.html">Service Areas</a> &rsaquo; {c["city"]}</p>
        <h1>{c["h1"]}</h1>
        <p>{c["hero_lead"]}</p>
      </div>
    </section>

    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content" data-reveal>
          <h2>{c["section1_title"]}</h2>
          <p>{c["section1"]}</p>
          <p>Call <a href="tel:7273866562">(727) 386-6562</a> or see our <a href="{c["county_link"]}">{c["county"]} County hub</a> for regional routes.</p>

          <h2>{c["neighborhoods_title"]}</h2>
          <ul class="about-list">
{neighborhoods}
          </ul>

          <div class="city-local-note">{c["local_note"]}</div>

          <h2>{c["section2_title"]}</h2>
          <p>{c["section2"]}</p>

          <h2>Screen services in {c["city"]}</h2>
          <ul class="about-list">
            <li><a href="pool-cage-repair.html">Pool cage repair</a></li>
            <li><a href="lanai-screen-replacement.html">Lanai screen replacement</a></li>
            <li><a href="screen-panel-repair.html">Screen panel repair</a></li>
            <li><a href="window-screens.html">Window screens</a></li>
            <li><a href="storm-screen-repair.html">Storm damage repairs</a></li>
            <li><a href="gutters-and-screens.html">Gutters &amp; screens bundle</a></li>
          </ul>
          <p><a href="pricing.html">Pricing</a> · <a href="gallery.html">Gallery</a> · $150 minimum job charge.</p>

          <h2>Project photos — {c["city"]} area</h2>
          <div class="city-gallery-teaser">
{gallery}
          </div>
          <p><a href="gallery.html">View full project gallery &rarr;</a></p>

          <h2>How scheduling works in {c["city"]}</h2>
          <ol>
{scheduling}
          </ol>
        </div>
        <aside class="sp-sidebar" data-reveal>
          <div class="about-card">
            <h3>Free {c["city"]} estimate</h3>
            <p>Owner on every job — {c["county"]} County routes.</p>
            <a class="btn btn-primary btn-full" href="tel:7273866562">(727) 386-6562</a>
            <a class="btn btn-ghost btn-full" href="contact.html" style="margin-top:12px;">Contact form</a>
            <p style="margin-top:14px;font-size:0.85rem;color:var(--muted);">Based in New Port Richey &middot; $150 minimum</p>
          </div>
        </aside>
      </div>
    </section>

    <section class="section-shell faq-section">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">{c["city"]} screen repair FAQ</p>
          <h2>Common questions</h2>
        </div>
        <div class="faq-list">
{faq_html(city_slug, c["faq"])}
        </div>
      </div>
    </section>

    <section class="areas-strip"><div class="container"><p class="eyebrow">{c["county"]} County</p><p><a href="{c["county_link"]}">{c["county"]} County screen repair</a> · <a href="service-areas.html">All service areas &rarr;</a></p></div></section>

    <section class="contact-section contact-section--parallax section-shell" data-parallax-overscan="0.30">
      <div class="container contact-inner" data-reveal>
        <p class="eyebrow">Get your quote</p>
        <h2>{c["cta"]}</h2>
        <a class="btn btn-primary btn-lg" href="tel:7273866562">(727) 386-6562</a>
      </div>
    </section>
  </main>

  <div id="site-footer-include"></div>
  <script src="includes.js"></script>
  <script src="script.js"></script>
</body>
</html>
'''


def main():
    for c in CITIES:
        out = ROOT / f"{c['slug']}.html"
        out.write_text(render(c), encoding="utf-8")
        print("wrote", out.name)


if __name__ == "__main__":
    main()
