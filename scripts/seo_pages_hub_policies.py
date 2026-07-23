# services.html hub + policy pages
from seo_expansion_shell import render_service_page, render_policy_page, service_select, ORG_SCHEMA, BUSINESS_SCHEMA, faq_schema, faq_html, AREAS_STRIP, json_escape

SERVICES_HUB = {
  "slug": "services.html",
  "title": "Screen Enclosure & Super Gutter Services Tampa Bay | Screen Team",
  "description": "Screen enclosure services Tampa Bay — pool cage rescreens, new builds coordinated with partners, super gutters, and small screen jobs. Call (727) 386-6562.",
  "keywords": "screen enclosure services Tampa Bay, pool cage and gutter services, Screen Team services",
  "service_name": "Screen Enclosure & Gutter Services",
  "service_desc": "Full menu of Screen Team LLC services across Tampa Bay including enclosure rescreens, partner-coordinated new builds, super gutters, and small screen repairs.",
  "breadcrumb": "Services",
  "og_image": "Images/preview/services/pool-enclosures.jpg",
  "form_selected": "Not sure - need advice",
  "form_subject": "Services inquiry",
  "faq_prefix": "svchub",
  "h1": "Screen Enclosure Services Tampa Bay",
  "hero_lead": "One owner-led menu for pool cages, lanais, super gutters, and the small screen jobs that keep Florida homes usable. Browse the clusters below, then call Chris Westcott when you know — or when you do not.",
  "main_html": '''
          <h2>Enclosure cluster — the core of Screen Team</h2>
          <p>Most homeowners find us because a pool cage or lanai stopped keeping bugs out. Start here if mesh is torn, oxidized, or slack. <a href="full-pool-cage-rescreen.html">Full pool cage rescreen</a> covers complete refreshes. <a href="two-story-pool-cage-rescreen.html">Two-story rescreens</a> price height honestly. <a href="pool-cage-door-repair.html">Cage door repair</a> and <a href="spa-enclosure-rescreen.html">spa enclosure rescreen</a> handle high-traffic and steam-aged zones. Broader context lives on <a href="rescreens.html">rescreens</a> and <a href="pool-enclosures.html">pool enclosures</a>.</p>
          <p>Planning something that does not exist yet? <a href="new-pool-cage-installation.html">New pool cage installation</a>, <a href="screen-enclosure-installation.html">screen enclosure installation</a>, <a href="new-lanai-enclosure.html">new lanai enclosure</a>, and <a href="custom-screen-enclosure.html">custom screen enclosure</a> pages explain our partner-honest model: Screen Team leads scoping and the customer relationship; permit-heavy engineering is coordinated through licensed partners when required.</p>

          <h2>Super gutter cluster — a primary service</h2>
          <p>Super gutters are not a footnote. Chris installs, repairs, and replaces enclosure-scale drainage so cage roofs stop flooding fascias. Begin at the <a href="super-gutters.html">super gutters hub</a>, then go deep on <a href="super-gutter-installation.html">installation</a>, <a href="super-gutter-repair.html">repair</a>, <a href="pool-cage-gutter-replacement.html">pool cage gutter replacement</a>, and <a href="seamless-gutters.html">seamless gutters</a>. Combined exterior visits are common — see <a href="gutters-and-screens.html">gutters and screens</a>.</p>
          <div class="city-local-note"><strong>Bundle tip:</strong> If mesh and gutters both fail, say so on the first call. One setup often costs less frustration than two separate appointments.</div>

          <h2>Small jobs that still matter</h2>
          <ul class="about-list">
            <li><a href="screen-door-repair.html">Screen door repair</a> — hinged and sliding</li>
            <li><a href="no-see-um-screen.html">No-see-um screen</a> — fine mesh upgrades</li>
            <li><a href="screen-panel-repair.html">Screen panel repair</a> and <a href="storm-screen-repair.html">storm repair</a></li>
            <li><a href="window-screens.html">Window screens</a>, <a href="garage-screens.html">garage screens</a>, <a href="pet-resistant-screen-mesh.html">pet mesh</a></li>
            <li><a href="lanai-screen-replacement.html">Lanai screen replacement</a> and <a href="screen-lanais.html">screen lanais</a></li>
            <li><a href="gutter-work.html">General gutter work</a> alongside enclosure runs</li>
          </ul>

          <h2>How to choose a starting page</h2>
          <p>Torn everywhere after years of sun &mdash; full cage rescreen. One storm row &mdash; storm or panel repair. Waterfalls at the house line &mdash; super gutters. Empty slab wanting shade and screens &mdash; new enclosure install (partner path). Unsure &mdash; call <a href="tel:7273866562">(727) 386-6562</a> or use the form &mdash; “Not sure” is a valid option. Pricing context: <a href="pricing.html">pricing</a>. Guarantee: <a href="service-guarantee.html">service guarantee</a>.</p>
''',
  "local_html": '''
          <h2>Services across Pasco, Pinellas & Hillsborough</h2>
          <p>New Port Richey is home base. City pages help locals connect: <a href="clearwater-screen-repair.html">Clearwater</a>, <a href="st-petersburg-screen-repair.html">St. Petersburg</a>, <a href="tampa-screen-repair.html">Tampa</a>, <a href="palm-harbor-screen-repair.html">Palm Harbor</a>, <a href="largo-screen-repair.html">Largo</a>, <a href="new-port-richey-screen-repair.html">New Port Richey</a>, plus county hubs for <a href="pinellas-county-screen-repair.html">Pinellas</a>, <a href="pasco-county-screen-repair.html">Pasco</a>, and <a href="hillsborough-county-screen-repair.html">Hillsborough</a>. Full map: <a href="service-areas.html">service areas</a>.</p>
          <div class="city-local-note"><strong>Policies:</strong> <a href="terms-of-service.html">Terms</a> &middot; <a href="payment-policy.html">Payment</a> &middot; <a href="warranty-terms.html">Warranty</a> &middot; <a href="privacy-policy.html">Privacy</a> &middot; <a href="image-use-policy.html">Image use</a></div>
''',
  "process": {
    "heading": "How to work with Screen Team",
    "sub": "Pick a cluster, send photos, get an owner-direct plan.",
    "steps": [
      {"title": "Choose the problem cluster", "body": "Enclosure mesh, new structure, super gutters, or a small door/window job."},
      {"title": "Send photos + city", "body": "Wide shots and failure close-ups. Chris ballparks many jobs before driving."},
      {"title": "Approve scope & schedule", "body": "Written clarity on what is included — including when partners join permit-heavy builds."},
    ],
  },
  "why": ["Enclosure + gutter clusters first", "Partner-honest new builds", "Super gutters as primary work", "Owner on the phone and job"],
  "local_faq_heading": "Services hub — local FAQ",
  "schema_faq_heading": "Screen Team services FAQs",
  "schema_faq_sub": "How to navigate enclosure, gutter, and small-job services.",
  "cta_h2": "Know which service you need — or not?",
  "cta_p": "Call or text Chris Westcott. Enclosures, super gutters, and small screen jobs all start with the same number.",
  "schema_faqs": [
    {"q": "What services does Screen Team specialize in?", "a": "Pool cage and lanai rescreens, enclosure-related repairs, super gutter work, and small screen jobs. New structural builds are scoped by Screen Team and coordinated with licensed partners when permits and engineering are required."},
    {"q": "Are super gutters a real primary service?", "a": "Yes. Chris installs, repairs, and replaces super gutters for enclosures as a core offering — not a side mention."},
    {"q": "Do you build new pool cages yourself end-to-end?", "a": "Screen Team leads customer relationship and scoping. Permit-heavy engineering and structural erection are partner-coordinated when required."},
    {"q": "Where should I click first if I am unsure?", "a": "Use this services hub, then call. Photos beat guessing between rescreen, gutter, and new-build paths."},
  ],
  "local_faqs": [
    {"q": "Can I book multiple services together?", "a": "Yes — rescreens with super gutters or door repairs with window screens are common combinations."},
    {"q": "Do you serve Wesley Chapel and Brandon?", "a": "Hillsborough and east Pasco are served with travel confirmed. City pages list local context."},
    {"q": "Is there a minimum job charge?", "a": "See pricing for current minimums and ranges. Small jobs still have a visit minimum."},
    {"q": "How fast can you schedule?", "a": "Depends on season and route density. Storm spikes fill calendars — call early with photos."},
  ],
  "images": {
    "hero_left": "Images/preview/services/pool-enclosures.jpg",
    "hero_top": "Images/preview/services/rescreens.jpg",
    "hero_bottom": "Images/preview/services/gutter-work.jpg",
    "hero_right": "Images/preview/services/screen-lanais.jpg",
    "alt_left": "Screen enclosure services Tampa Bay",
    "alt_top": "Pool cage rescreen services",
    "alt_bottom": "Super gutter and gutter services",
    "alt_right": "Lanai screen services",
    "grid1": "Images/gallery/20221223_163807.jpg",
    "grid2": "Images/st-gutters.png",
    "grid1_alt": "Enclosure service project gallery",
    "grid2_alt": "Gutter service alongside screening",
    "grid1_cap": "Enclosure cluster",
    "grid2_cap": "Super gutter cluster",
  },
}

POLICIES = []

POLICIES.append({
  "slug": "terms-of-service.html",
  "title": "Terms of Service | Screen Team LLC",
  "description": "Terms of service for The Screen Team LLC website and service engagements in Tampa Bay.",
  "keywords": "Screen Team terms of service",
  "breadcrumb": "Terms of Service",
  "h1": "Terms of Service",
  "body_html": '''
          <h2>Agreement overview</h2>
          <p>These Terms of Service ("Terms") govern your use of <strong>screenteamllc.com</strong> and the service relationships you enter with The Screen Team LLC ("Screen Team," "we," "us"), operated by Chris Westcott and based in New Port Richey, Florida. By submitting a quote request, scheduling work, or authorizing a job, you agree to these Terms.</p>
          <p>Screen Team provides screen enclosure services, rescreens, related repairs, super gutter work, and coordination for certain new enclosure projects. Website content is informational and does not replace a written scope for your specific property.</p>

          <h2>Quotes and scope of work</h2>
          <p>Estimates may begin from photos and descriptions you provide. Final pricing and scope are confirmed before work starts when an on-site condition differs from photos. Changes you request after approval may adjust price and schedule. You are responsible for accurate access information, pet containment, and disclosing known hazards around the work area.</p>
          <p>For permit-heavy new builds and structural engineering, Screen Team may coordinate licensed partners. Partner scopes, warranties, and permit responsibilities are defined in their agreements. Screen Team remains your relationship lead for coordination unless otherwise stated in writing.</p>

          <h2>Website use</h2>
          <p>You may use this site to learn about services and request contact. You may not misuse forms, attempt to disrupt the site, scrape content for competing commercial reuse without permission, or submit unlawful content. We may remove or ignore abusive submissions.</p>

          <h2>Scheduling, weather, and access</h2>
          <p>Outdoor work in Florida depends on weather and safe access. Wind, lightning, and storms can delay enclosure and gutter work. We communicate schedule changes as promptly as practical. You agree to provide reasonable access to the property and work areas at the agreed time.</p>

          <h2>Payments</h2>
          <p>Payment expectations are described in our <a href="payment-policy.html">Payment Policy</a>. Work may be paused if agreed payment terms are not met. Disputed charges should be raised promptly so we can review the completed scope.</p>

          <h2>Warranties and limitations</h2>
          <p>Workmanship terms are summarized in our <a href="warranty-terms.html">Warranty Terms</a>. Website materials are provided as-is for general information. To the fullest extent allowed by Florida law, Screen Team is not liable for indirect or consequential damages arising from site use. For service work, liability is limited as described in the approved scope and warranty documents for that job.</p>

          <h2>Photos and reviews</h2>
          <p>We may photograph completed work for portfolio use under our <a href="image-use-policy.html">Image Use Policy</a>, with reasonable sensitivity to privacy requests. Reviews should be truthful; we appreciate the chance to make things right before public complaints when a simple call would resolve an issue.</p>

          <h2>Privacy</h2>
          <p>Contact details submitted through the site are handled as described in our <a href="privacy-policy.html">Privacy Policy</a>.</p>

          <h2>Governing law</h2>
          <p>These Terms are governed by the laws of the State of Florida. Venue for disputes is appropriate courts in Florida serving Pasco County unless otherwise required by law.</p>

          <h2>Contact</h2>
          <p>Questions about these Terms: Chris Westcott, The Screen Team LLC — <a href="tel:7273866562">(727) 386-6562</a> · <a href="contact.html">contact form</a>.</p>
'''
})

POLICIES.append({
  "slug": "payment-policy.html",
  "title": "Payment Policy | Screen Team LLC",
  "description": "Payment policy for Screen Team LLC jobs — deposits, final payment, methods, and invoicing clarity.",
  "keywords": "Screen Team payment policy",
  "breadcrumb": "Payment Policy",
  "h1": "Payment Policy",
  "body_html": '''
          <h2>Plain-language payment expectations</h2>
          <p>The Screen Team LLC keeps payment simple because the business is owner-operated. This Payment Policy explains how deposits, progress payments, and final balances typically work for screen, enclosure, and gutter projects across Tampa Bay. Your approved quote or invoice controls if it states different terms for a specific job.</p>

          <h2>Estimates vs invoices</h2>
          <p>Photo ballparks help you plan. A confirmed quote or invoice lists the scope Chris will perform. Additional work you request — extra panels, mesh upgrades, unexpected frame repairs, or added gutter runs — is priced before that work proceeds whenever practical.</p>

          <h2>Deposits</h2>
          <p>Larger jobs such as full pool cage rescreens, multi-elevation gutter replacements, and projects requiring materials ordered ahead may require a deposit to schedule and secure materials. Deposit amounts are stated in writing. Deposits are applied to the final balance. If you cancel after materials are specially ordered, reasonable material and restocking costs may be deducted as disclosed at the time.</p>

          <h2>Final payment</h2>
          <p>Final payment is due upon satisfactory completion of the approved scope unless another schedule is agreed in writing. For multi-day jobs, Chris may request a progress payment after a defined milestone. Partner-coordinated permit-heavy builds may follow partner billing schedules for their portion; Screen Team will clarify who invoices which part before work begins.</p>

          <h2>Accepted methods</h2>
          <p>Accepted methods are confirmed on your invoice and may include common consumer payment options Chris supports at the time of the job. Card processing fees, if any, will be disclosed before you pay. Do not send cash by mail. Do not share card numbers over unsecured channels if an alternative is offered.</p>

          <h2>Minimums and trip charges</h2>
          <p>Small repairs may be subject to a minimum job charge as published on our <a href="pricing.html">pricing</a> page or stated in your quote. That minimum reflects travel, setup, and owner time even when the physical repair is quick.</p>

          <h2>Late balances</h2>
          <p>Overdue balances may pause scheduling of follow-up work. We prefer a phone call to resolve invoice questions quickly. Collections activity, if ever required, follows applicable Florida law.</p>

          <h2>Chargebacks and disputes</h2>
          <p>If you believe an invoice is wrong, contact Chris at <a href="tel:7273866562">(727) 386-6562</a> before initiating a chargeback when possible. Many issues are scope clarifications that resolve same-day. Chargebacks filed without attempting contact may be contested with job documentation.</p>

          <h2>Related policies</h2>
          <p><a href="terms-of-service.html">Terms of Service</a> · <a href="warranty-terms.html">Warranty Terms</a> · <a href="privacy-policy.html">Privacy Policy</a></p>
'''
})

POLICIES.append({
  "slug": "warranty-terms.html",
  "title": "Warranty Terms | Workmanship | Screen Team LLC",
  "description": "Warranty terms for Screen Team LLC workmanship on screen, enclosure, and gutter projects in Tampa Bay.",
  "keywords": "Screen Team warranty terms, workmanship warranty",
  "breadcrumb": "Warranty Terms",
  "h1": "Warranty Terms",
  "body_html": '''
          <h2>Workmanship commitment</h2>
          <p>The Screen Team LLC stands behind the work Chris Westcott performs. These Warranty Terms summarize how workmanship coverage typically applies to screen installation, rescreens, door repairs, and gutter work. Your job paperwork may state a specific duration or scope; that writing controls if it differs from this page.</p>
          <p>For a homeowner-friendly overview of how we treat callbacks, also see our <a href="service-guarantee.html">service guarantee</a> page.</p>

          <h2>What workmanship warranty usually covers</h2>
          <ul>
            <li>Spline and mesh installation defects attributable to workmanship</li>
            <li>Improperly seated panels that loosen under normal use shortly after install</li>
            <li>Gutter attachment or pitch errors in work Screen Team performed</li>
            <li>Hardware adjustments that were part of the approved door scope and fail from installation error</li>
          </ul>

          <h2>What is typically not covered</h2>
          <ul>
            <li>Storm, wind, impact, falling tree, or flying debris damage</li>
            <li>Pet damage, vandalism, or misuse</li>
            <li>Normal UV aging and oxidation of mesh over Florida years of sun</li>
            <li>Failures of materials outside manufacturer guidelines when misuse is evident</li>
            <li>Pre-existing frame corrosion, bent posts, or structural movement not included in the scope</li>
            <li>Clogged gutters from leaf load after delivery of a clear system</li>
            <li>Work performed by other contractors after our completion</li>
          </ul>

          <h2>Manufacturer material warranties</h2>
          <p>Some meshes and gutter materials carry manufacturer warranties. Those terms belong to the manufacturer. Screen Team helps you understand what was installed but does not expand a manufacturer’s written warranty beyond its terms.</p>

          <h2>Partner-built structural work</h2>
          <p>Permit-heavy new enclosure structures coordinated through licensed partners are covered under the partner’s warranty terms for their scope. Screen Team’s workmanship warranty applies to the portions Chris personally installs — such as certain mesh or related finish items — as defined in your documents.</p>

          <h2>How to make a warranty request</h2>
          <p>Call or text <a href="tel:7273866562">(727) 386-6562</a> with your address, approximate completion date, and photos of the issue. Reasonable access must be provided for inspection. If the issue is workmanship within coverage, Chris will schedule a remedy. If the issue is storm or wear outside coverage, you will get an honest repair quote instead.</p>

          <h2>Remedy</h2>
          <p>The exclusive remedy for covered workmanship issues is repair or re-performance of the defective portion. Refunds, if ever appropriate, are limited to amounts paid for the defective scope and are not the default path when repair is practical.</p>

          <h2>Related</h2>
          <p><a href="terms-of-service.html">Terms of Service</a> · <a href="payment-policy.html">Payment Policy</a> · <a href="service-guarantee.html">Service guarantee</a></p>
'''
})

POLICIES.append({
  "slug": "image-use-policy.html",
  "title": "Image Use Policy | Screen Team LLC",
  "description": "Image use policy for Screen Team LLC project photos, website gallery, and homeowner privacy preferences.",
  "keywords": "Screen Team image use policy",
  "breadcrumb": "Image Use Policy",
  "h1": "Image Use Policy",
  "body_html": '''
          <h2>Why we photograph completed work</h2>
          <p>The Screen Team LLC documents many jobs so future Tampa Bay homeowners can see real pool cages, lanais, doors, and gutter projects — not stock photos. This Image Use Policy explains how those images may be used and how to request privacy accommodations.</p>

          <h2>What we may capture</h2>
          <p>Chris may photograph exterior enclosures, screen details, gutter runs, and before/after conditions related to the work performed. We avoid intentionally featuring people, especially minors. House numbers and personal items in frame may occasionally appear in wide shots; we can crop or avoid publishing identifiable details when you ask.</p>

          <h2>How images may be used</h2>
          <ul>
            <li>Website gallery and service page examples on screenteamllc.com</li>
            <li>Social profiles linked from the site (such as Facebook, X, LinkedIn, Nextdoor)</li>
            <li>Print or digital portfolios for quotes and marketing</li>
            <li>Educational explanations of repair types</li>
          </ul>

          <h2>Your preferences</h2>
          <p>If you prefer that your property not appear publicly, tell Chris before or during the job. Reasonable requests to skip photography, limit angles, or avoid showing the street-facing elevation are honored whenever practical. If an image is already published and you want it removed, contact us and we will take it down from properties we control within a reasonable time.</p>

          <h2>Third-party sharing</h2>
          <p>We do not sell your project photos as a dataset. Images may appear on platforms we use for business marketing. Those platforms have their own terms. We do not authorize scrapers or competitors to reuse our gallery commercially without written permission.</p>

          <h2>Homeowner-provided photos</h2>
          <p>When you text photos for estimating, those images are used to quote and plan your job. We do not publish customer-submitted phone photos in the public gallery without asking, except when you explicitly agree they can be shared.</p>

          <h2>Copyright</h2>
          <p>Photographs created by Screen Team remain our intellectual property unless a separate written agreement says otherwise. You may share links to our public pages. You may not copy gallery files for competing advertising.</p>

          <h2>Contact</h2>
          <p>Image questions or removal requests: <a href="tel:7273866562">(727) 386-6562</a> · <a href="contact.html">contact form</a> · related <a href="privacy-policy.html">Privacy Policy</a> and <a href="terms-of-service.html">Terms of Service</a>.</p>
'''
})
