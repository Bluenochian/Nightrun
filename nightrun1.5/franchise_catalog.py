from __future__ import annotations

from itertools import product


def module(module_id, label, source, weight=1.0, **fields):
    data = {
        "id": module_id,
        "label": label,
        "inspiration_sources": [source],
        "weight": weight,
    }
    data.update({key: value for key, value in fields.items() if value})
    return data


def combine(left, right, limit=None):
    values = [f"{a}, {b}" for a, b in product(left, right)]
    return values[:limit] if limit else values


def details_for(label, signature_terms, forbidden=None):
    signatures = ", ".join(signature_terms[:6])
    blocked = ", ".join(forbidden or [])
    base = [
        f"world details stay {label} themed",
        f"{signatures} remain visible and dominant",
        "outfit, props, architecture, and mood all come from the selected world",
        "safe generic pose, camera, framing, expression, and mild atmosphere may add variety",
    ]
    if blocked:
        base.append(f"avoid unrelated world logic: {blocked}")
    return base


def make_specific_module(spec):
    roles = combine(spec["roles"], spec.get("role_details", []), limit=16) if spec.get("role_details") else spec["roles"]
    fields = {
        "character_archetypes": spec.get("character_archetypes") or roles,
        "outfits": spec.get("outfits", []),
        "environments": spec.get("environments", []),
        "props_equipment": spec.get("props_equipment") or spec.get("props", []),
        "factions": spec.get("factions", []),
        "creatures": spec.get("creatures", []),
        "architecture": spec.get("architecture", []),
        "technology": spec.get("technology", []),
        "magic_system": spec.get("magic_system") or spec.get("magic", []),
        "landscapes": spec.get("landscapes", []),
        "ships": spec.get("ships", []),
        "droids": spec.get("droids", []),
        "lighting_mood": spec.get("lighting_mood") or spec.get("lighting", []),
        "color_palettes": spec.get("color_palettes") or spec.get("palettes", []),
        "cinematic_language": spec.get("cinematic_language") or spec.get("cinematic", []),
        "prompt_modifiers": spec.get("prompt_modifiers") or spec.get("modifiers")
        or details_for(spec["label"], spec.get("signature_terms", []), spec.get("avoid", [])),
    }
    return module(spec["id"], spec["label"], spec["source"], spec.get("weight", 1.0), **fields)


COMMON_ROLE_DETAILS = [
    "clear mature woman design, readable silhouette",
    "confident expression, clean face focus",
    "cinematic posture, hands readable",
]


SPECS = [
    {
        "id": "harry_potter",
        "label": "Harry Potter Hogwarts magical school fantasy",
        "source": "Harry Potter",
        "weight": 1.15,
        "signature_terms": ["Hogwarts", "Hogsmeade", "Diagon Alley", "Gryffindor", "Slytherin", "Ravenclaw"],
        "roles": [
            "Hogwarts dueling witch",
            "Restricted Section spell scholar",
            "Ravenclaw tower prefect sorceress",
            "Slytherin potion prodigy",
            "Gryffindor curse-breaker heroine",
            "Hufflepuff herbology witch",
            "Ministry of Magic investigator",
            "Order of the Phoenix secret agent",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "tailored black Hogwarts robe, silver clasp, fitted waist",
            "Gryffindor red-gold scarf over dark robe dress, long cloak",
            "Slytherin green-silver velvet robe, embroidered cuffs, ribbon tie",
            "Ravenclaw blue-bronze blouse under black robe, corset belt, stockings",
            "Hufflepuff yellow-black cloak, leather satchel, polished boots",
            "formal Yule Ball-inspired robe gown, gold trim, choker necklace",
            "Hogsmeade winter cloak, knitted scarf, dark thighhighs",
            "Ministry of Magic formal robe coat, emerald paperwork seals",
        ],
        "environments": [
            "Hogwarts castle corridor, floating candles, moving stair shadows",
            "Restricted Section library aisle, towering shelves, dust in candlelight",
            "Potions classroom dungeon, glass bottles, green fumes, stone arches",
            "Astronomy Tower balcony, moonlit clouds, brass telescope",
            "Hogsmeade snowy street, warm shop windows, old stone walls",
            "Diagon Alley magical shopping street, crooked signs, lanterns",
            "Great Hall balcony, enchanted ceiling, long tables below",
            "Forbidden Forest path, blue mist, twisted roots",
        ],
        "props": [
            "Ollivanders polished wand, sparks near the tip",
            "Marauder-map-like enchanted parchment, moving ink lines",
            "Time-Turner-like golden pendant, tiny hourglass detail",
            "Golden Snitch-like winged charm, metallic sparkle",
            "Hogwarts spellbook, brass corner guards",
            "potion vial belt, colored glass bottles",
            "owl feather quill, floating parchment",
            "crystal divination orb, smoky reflections",
        ],
        "factions": [
            "Gryffindor house identity, red and gold accents, lion crest motif",
            "Slytherin house identity, green and silver accents, serpent motif",
            "Ravenclaw house identity, blue and bronze accents, eagle motif",
            "Hufflepuff house identity, yellow and black accents, badger motif",
            "Death Eater-inspired dark faction mood, black mask, silver serpent details",
            "Order of the Phoenix secret resistance mood, phoenix charm, worn cloak",
            "Ministry of Magic formal wizard authority, emerald seals",
        ],
        "creatures": [
            "Patronus-like silver stag light, faint magical glow",
            "Thestral-like winged silhouette behind fog",
            "hippogriff-like feathered creature in distant courtyard",
            "black cat familiar, moonlit fur",
            "small owl familiar, amber eyes, perched nearby",
            "raven familiar, brass tag on leg",
        ],
        "architecture": [
            "Hogwarts gothic stone arches, stained glass, castle masonry",
            "Diagon Alley crooked storefronts, hanging signs, brick archway",
            "Hogsmeade snow-covered cottages, warm window glow",
            "vaulted library ceiling, carved columns, iron ladders",
            "moonlit battlements, gargoyle silhouettes",
        ],
        "magic": [
            "wand-based spellcasting, visible spell trail, clear hand pose",
            "Patronus charm glow, silver animal-shaped light, clean silhouette",
            "potion magic, colored vapors, glass reflections",
            "protective charm circle, clean readable symbols",
        ],
        "lighting": [
            "warm candlelight, dusty gold shadows, moonlit blue rim",
            "library chiaroscuro, parchment glow, soft face light",
            "green potion underlight, warm window edge light",
            "silver moonlight through castle windows, floating dust",
        ],
        "palettes": [
            "old parchment gold and black palette, warm shadows",
            "moonlit blue and candle amber palette, balanced contrast",
            "forest green and brass palette, dusty highlights",
            "burgundy velvet and dark oak palette, soft glow",
        ],
        "cinematic": [
            "magical school mystery mood, candlelit foreground, readable outfit",
            "adventure fantasy corridor shot, leading lines, spell glow",
            "enchanted library portrait, shallow depth of field, dust motes",
            "moonlit tower scene, wind in cloak, heroic low angle",
        ],
        "avoid": ["cyberpunk armor", "spaceship interiors", "wasteland bunkers"],
    },
    {
        "id": "fallout",
        "label": "Fallout retrofuturist wasteland",
        "source": "Fallout",
        "weight": 1.12,
        "signature_terms": ["Vault-Tec", "Nuka-Cola", "Pip-Boy", "Brotherhood of Steel", "New California Republic", "Mojave"],
        "roles": [
            "Vault-Tec vault survivor heroine",
            "New California Republic desert scout",
            "Brotherhood of Steel field scribe",
            "New Vegas casino courier queen",
            "Minutemen settlement defender",
            "Railroad safehouse agent",
            "Enclave bunker defector",
            "wasteland scavenger mechanic",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "blue Vault-Tec jumpsuit, worn leather harness, dusty boots",
            "NCR ranger-inspired duster coat, survival harness, thigh holster",
            "Brotherhood of Steel under-armor suit, heavy metal plating",
            "faded diner waitress dress with armor pieces, practical boots",
            "desert poncho over bodysuit, cracked goggles, bandolier straps",
            "radiation suit half-unzipped over fitted underlayer, utility pouches",
            "patched leather armor, metal shoulder plates, scarf mask lowered",
            "retro workwear dress, utility belt, knee pads",
        ],
        "environments": [
            "ruined Nuka-Cola desert diner, faded neon sign, cracked asphalt",
            "abandoned Vault-Tec corridor, round vault door, retro terminals",
            "New Vegas-style casino ruin, cracked neon, dusty glamour",
            "Mojave dry lake bed camp, scrap tents, distant radstorm",
            "Brotherhood of Steel bunker, power armor racks, yellow hazard lights",
            "wasteland gas station, dust storm, rusted cars",
            "collapsed subway platform, emergency lights, old posters",
            "radio tower settlement, scrap metal walls, sunset haze",
        ],
        "props": [
            "Pip-Boy wrist computer, green monochrome display",
            "Nuka-Cola bottle, faded red label, cap charm",
            "Stimpak injector, medical red detail",
            "RadAway pouch, worn plastic bag, field medic detail",
            "laser pistol, retro bulky casing, red warning light",
            "rusted revolver, leather holster, worn grip",
            "scrap metal rifle, taped stock, practical straps",
            "old bottlecap charm necklace, scavenger trophy",
        ],
        "factions": [
            "Vault-Tec identity, clean blue-yellow fabric contrasted with dust",
            "New California Republic identity, tan ranger gear, two-headed bear motif",
            "Brotherhood of Steel identity, power armor plating, steel insignia mood",
            "Caesar's Legion-inspired faction mood, red cloth, brutal salvage armor",
            "Minutemen militia mood, colonial coat pieces, laser musket silhouette",
            "Railroad secret network mood, coded markings, worn urban coat",
            "Enclave black power armor authority, glossy dark plates",
            "Followers of the Apocalypse medic mood, white-red field gear",
        ],
        "creatures": [
            "Deathclaw silhouette in dust haze, distant and threatening",
            "ghoul figure blurred in broken doorway",
            "radroach shell near foreground",
            "super mutant silhouette behind scrap barricade",
            "Mirelurk-like shell shape near water ruins",
        ],
        "architecture": [
            "1950s retrofuturist signage, rounded metal panels, faded paint",
            "vault door geometry, yellow hazard stripes, riveted steel",
            "ruined roadside Americana, chrome diner trim, broken glass",
            "concrete bunker hallway, exposed pipes, emergency lamps",
            "scrap metal settlement walls, welded plates, hanging tarps",
        ],
        "technology": [
            "analog retro computers, green CRT glow, chunky switches",
            "jury-rigged power armor pieces, visible bolts and cables",
            "radiation sensors and Geiger counters, glowing meters",
            "improvised radio equipment, antennas, coiled wires",
        ],
        "lighting": [
            "dusty golden sunlight, rust orange shadows, heat haze",
            "sickly green monitor glow, dark bunker contrast",
            "radstorm green backlight, red warning lamps",
            "fluorescent bunker flicker, practical utility lighting",
        ],
        "palettes": [
            "rust orange and faded blue palette, dusty contrast",
            "sickly green and dark metal palette, bunker mood",
            "sand beige and weathered leather palette, sunburned highlights",
            "faded diner red and chrome palette, retro decay",
        ],
        "cinematic": [
            "retro post-apocalyptic key visual, dust foreground, readable gear",
            "wasteland survival film framing, harsh sunlight, practical props",
            "ruined Americana mood, low angle, old signage behind subject",
            "survival RPG cover art, gear readable, environment tells story",
        ],
        "avoid": ["wizard robes", "clean starship halls", "high fantasy castles"],
    },
    {
        "id": "star_wars",
        "label": "Star Wars galactic myth adventure",
        "source": "Star Wars",
        "weight": 1.1,
        "signature_terms": ["Jedi", "Sith", "Tatooine", "Coruscant", "Rebel Alliance", "Galactic Empire"],
        "roles": [
            "Jedi desert mystic",
            "Sith acolyte countess",
            "Rebel Alliance pilot",
            "Imperial throne room agent",
            "Outer Rim smuggler queen",
            "Mandalorian bounty huntress",
            "Coruscant senate spy",
            "Tatooine scavenger mechanic",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Tatooine desert cloak, wrapped tunic, leather belt",
            "white rebel flight suit, orange straps, chest box detail",
            "black high-collar Sith robes, red light reflections",
            "Mandalorian-inspired armored bodysuit with cape, weathered metal plates",
            "sleek senate gown, metallic belt, draped sleeves",
            "brown spacer jacket, utility harness, tall boots",
            "temple robe dress, layered fabric, silver wrist wraps",
            "bounty armor over fitted underlayer, scratched chest plate",
        ],
        "environments": [
            "Tatooine twin-sun desert sunset, sand dunes, moisture vaporators",
            "Coruscant city balcony, endless traffic lanes, neon windows",
            "Rebel Alliance hangar bay, X-wing silhouettes, orange maintenance lights",
            "Imperial throne chamber, black glossy floor, red window light",
            "Jedi Temple ancient energy hall, stone pillars, glowing floor lines",
            "Mos Eisley cantina street, dusty alien market, warm lamps",
            "moon forest base, foggy trees, landing pad lights",
            "starship corridor, curved white panels, blue console glow",
        ],
        "props": [
            "lightsaber, clean glowing blade silhouette",
            "compact blaster pistol, worn metal grip",
            "star map hologram, blue projection",
            "pilot helmet under one arm, scratched visor",
            "thermal detonator-like sphere, warning lights",
            "ancient kyber crystal pendant, faint energy aura",
            "navigation datapad, glowing route lines",
            "Beskar-like helmet at hip, scratched visor",
        ],
        "factions": [
            "Jedi Order identity, layered robes, calm discipline, blue-green saber glow",
            "Sith identity, black robes, red saber glow, severe silhouette",
            "Rebel Alliance identity, patched insignia, practical gear",
            "Galactic Empire identity, black-and-red authority mood, severe architecture",
            "Mandalorian clan identity, beskar-like plates, helmet motif",
            "Republic senate identity, ceremonial robes, polished metal",
            "Outer Rim smuggler identity, worn leather, concealed blaster",
        ],
        "creatures": [
            "small hovering droid companion, blue sensor light",
            "desert lizard mount silhouette, saddled in background",
            "alien bird flock over dunes",
            "large shadow creature beyond hangar doors",
        ],
        "droids": [
            "R2 unit-like dome droid, blue light, rolling beside character",
            "protocol droid silhouette, gold reflection",
            "repair droid with tiny tool arms, practical scale",
            "black probe droid hovering in background",
        ],
        "ships": [
            "X-wing-like starfighter silhouette in hangar",
            "TIE fighter-like silhouette through hangar window",
            "round freighter cockpit window, starfield outside",
            "Imperial shuttle-like ramp, red backlight, fog",
        ],
        "architecture": [
            "curved white starship panels, recessed blue lights",
            "black imperial walls, red slit windows, glossy floor",
            "ancient stone temple, geometric carvings, glowing runes",
            "desert adobe spaceport, antennas, dusty cloth awnings",
        ],
        "technology": [
            "holographic star maps, blue projection, small scanlines",
            "used-future starship controls, chunky buttons, worn metal",
            "energy blade technology, clean colored glow, no sparks over face",
            "droid interface tools, small mechanical arms",
        ],
        "lighting": [
            "orange desert sunset, blue saber rim light, dust haze",
            "red throne room backlight, glossy black reflections",
            "cool starship corridor glow, clean white highlights",
            "rebel hangar practical lights, warm maintenance mood",
        ],
        "palettes": [
            "sand gold and sky blue palette, desert clarity",
            "black red and glossy silver palette, dark authority",
            "white orange and gunmetal palette, rebel pilot mood",
            "blue hologram and warm brown palette, used-future charm",
        ],
        "cinematic": [
            "space opera poster framing, heroic silhouette, readable weapon",
            "used-future adventure mood, practical props, dust and metal",
            "ancient sci-fi temple composition, glowing floor leading lines",
            "dark throne room portrait, red vertical lights, severe symmetry",
        ],
        "avoid": ["Hogwarts robes", "wasteland diners", "modern police stations"],
    },
    {
        "id": "star_trek",
        "label": "Star Trek Federation exploration sci-fi",
        "source": "Star Trek",
        "weight": 0.86,
        "signature_terms": ["Starfleet", "Federation", "Enterprise", "Vulcan", "Klingon", "Borg"],
        "roles": [
            "Starfleet science officer",
            "Federation diplomatic envoy",
            "Vulcan logic specialist",
            "Klingon warrior diplomat",
            "Romulan intelligence agent",
            "Borg survivor officer",
            "Enterprise bridge commander",
            "Deep Space station engineer",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Starfleet uniform jacket, division color shoulders, comm badge",
            "sleek Federation dress uniform, polished boots, rank pips",
            "Vulcan ceremonial robe, geometric collar, calm elegance",
            "Klingon-inspired armor dress, ridged metal, dark cape",
            "Romulan tailored coat, sharp shoulders, green-silver accents",
            "Borg survivor bodysuit, subtle implants, clean silhouette",
            "station engineer jumpsuit, tool belt, rolled sleeves",
        ],
        "environments": [
            "Enterprise bridge, LCARS panels, starfield viewscreen",
            "Vulcan desert temple, red rock, ritual lanterns",
            "Klingon great hall, metal banners, torch glow",
            "Romulan warbird corridor, green light, curved panels",
            "Borg cube interior, black conduits, green data glow",
            "Deep Space station promenade, curved windows, alien shops",
            "Federation holodeck garden, grid lines fading into trees",
        ],
        "props": [
            "tricorder scanner, small readable screen",
            "phaser sidearm, compact clean silhouette",
            "Starfleet comm badge, metallic chest detail",
            "PADD tablet, LCARS interface",
            "Vulcan meditation candle, bronze holder",
            "Klingon bat'leth-inspired blade, curved silhouette",
            "Borg cortical node fragment, green glow",
        ],
        "factions": [
            "Starfleet identity, clean uniform, comm badge, exploratory optimism",
            "Federation diplomatic identity, polished restraint, elegant future",
            "Vulcan identity, earth-tone robes, logic and ritual",
            "Klingon identity, dark armor, honor banners, warrior mood",
            "Romulan identity, green-black tailoring, secretive command",
            "Borg identity, black conduits, green data, assimilation menace",
        ],
        "creatures": [
            "Vulcan desert bird silhouette over red sky",
            "Klingon targ-like animal silhouette near hall steps",
            "alien diplomat silhouettes on promenade",
        ],
        "architecture": [
            "clean Federation bridge curves, LCARS panels, carpeted floor",
            "Vulcan stone temple geometry, red desert cliffs",
            "Klingon heavy metal hall, angular pillars, banners",
            "Romulan green-lit corridors, curved warbird ribs",
            "Borg cube corridors, black pipes, green data grids",
        ],
        "technology": [
            "LCARS interface panels, orange and violet UI blocks",
            "transporter shimmer, soft blue particles",
            "warp core blue glow, engineering depth",
            "holodeck grid fading into realistic scenery",
            "Borg nanotech lights, restrained green circuitry",
        ],
        "lighting": [
            "clean bridge key light, LCARS glow, starfield backlight",
            "Vulcan sunset red and bronze glow",
            "green Romulan warbird light, secretive shadows",
            "Borg cube green underlight, black industrial contrast",
        ],
        "palettes": [
            "Federation black and division color palette, clean future",
            "Vulcan red bronze and sand palette, ritual calm",
            "Romulan emerald and gunmetal palette, secretive command",
            "Borg green black and steel palette, cyber menace",
        ],
        "cinematic": [
            "optimistic exploration sci-fi portrait, bridge depth, readable badge",
            "diplomatic space drama framing, polished futuristic architecture",
            "alien culture portrait, ritual detail, clear face focus",
            "starship command shot, viewscreen glow, calm authority",
        ],
        "avoid": ["Jedi mysticism", "Fallout retro terminals", "gothic vampire castles"],
    },
    {
        "id": "foundation",
        "label": "Foundation psychohistory empire sci-fi",
        "source": "Foundation",
        "weight": 0.68,
        "signature_terms": ["Trantor", "Terminus", "Seldon Plan", "psychohistory", "Galactic Empire", "Cleon"],
        "roles": [
            "Trantor imperial mathematician",
            "Terminus Foundation archivist",
            "psychohistory oracle analyst",
            "Cleon court envoy",
            "Second Foundation mentalic agent",
            "Outer Reach diplomat",
            "Empire genetic dynasty guard",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Trantor court robe, geometric gold trim, sleek black fabric",
            "Foundation archive coat, practical belt, data slate",
            "psychohistory analyst dress, subtle equation embroidery",
            "imperial blue-gold gown, structured shoulders, polished boots",
            "Second Foundation hooded cloak, minimal jewelry, calm gaze",
            "spacer field suit, clean panels, glass helmet at side",
        ],
        "environments": [
            "Trantor imperial palace balcony, city planet below, gold haze",
            "Terminus archive vault, holographic equations, tall shelves",
            "Seldon Plan projection chamber, probability lines, dark floor",
            "Galactic Empire throne corridor, colossal scale, polished stone",
            "outer planet observatory, cold stars, white dome",
            "Foundation council room, data windows, austere lighting",
        ],
        "props": [
            "psychohistory tablet, glowing probability equations",
            "Seldon Plan hologram cube, golden lines",
            "imperial seal pendant, blue enamel",
            "Terminus archive key, old brass and glass",
            "genetic dynasty ring, polished gold",
            "spacer navigation compass, tiny star map",
        ],
        "factions": [
            "Foundation identity, austere scholar clothing, data archives",
            "Galactic Empire identity, blue-gold ceremonial authority",
            "Second Foundation identity, quiet mentalic power, hooded restraint",
            "Trantor court identity, colossal city planet luxury",
            "Terminus frontier scholar mood, practical future gear",
        ],
        "architecture": [
            "Trantor city-planet towers, endless terraces, imperial geometry",
            "Terminus archive shelves, holographic equations, clean stone",
            "imperial palace columns, gold inlay, vast scale",
            "observatory dome, white panels, starfield windows",
        ],
        "technology": [
            "psychohistory holographic equations, branching probability trees",
            "imperial genetic dynasty interface, golden data rings",
            "Foundation archive terminals, clean blue-gold displays",
            "spacer star charts, precise orbital lines",
        ],
        "lighting": [
            "gold imperial window light, polished stone reflections",
            "cool archive blue glow, austere shadows",
            "starfield observatory light, clean white rim",
            "holographic probability light across face",
        ],
        "palettes": [
            "imperial blue and gold palette, mathematical grandeur",
            "archive white and pale cyan palette, scholar clarity",
            "black glass and golden equation palette, Seldon Plan mood",
            "cold star silver and deep navy palette, outer reach",
        ],
        "cinematic": [
            "prestige empire sci-fi framing, colossal architecture, calm face",
            "psychohistory chamber shot, equations as foreground, readable pose",
            "archive prophecy portrait, restrained color, intellectual tension",
        ],
        "avoid": ["lightsabers", "cyberpunk street gangs", "wizard castles"],
    },
    {
        "id": "battlestar_galactica",
        "label": "Battlestar Galactica colonial fleet survival",
        "source": "Battlestar Galactica",
        "weight": 0.72,
        "signature_terms": ["Galactica", "Colonial Fleet", "Cylon", "Viper", "Raptor", "Caprica"],
        "roles": [
            "Colonial Fleet Viper pilot",
            "Galactica deck officer",
            "Cylon infiltrator in human disguise",
            "Caprica resistance fighter",
            "Raptor recon navigator",
            "Twelve Colonies refugee leader",
            "fleet priestess of Kobol",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Viper pilot flight suit, orange panels, helmet at hip",
            "Colonial Fleet officer uniform, grey-blue jacket, dog tags",
            "deck crew work suit, tool harness, scuffed boots",
            "Caprica resistance coat, practical straps, worn gloves",
            "Cylon-inspired sleek red-black dress, chrome accent",
            "Kobol priestess robe, simple cloth, symbolic necklace",
        ],
        "environments": [
            "Galactica hangar deck, Viper fighters, yellow work lights",
            "Battlestar CIC, tactical table, dim blue displays",
            "Caprica ruined city street, smoke, broken glass",
            "Cylon basestar chamber, red light, biomechanical walls",
            "refugee fleet corridor, crowded bunks, soft lamps",
            "Kobol temple ruins, rain, ancient stone",
        ],
        "props": [
            "Viper pilot helmet, scratched visor, squadron markings",
            "Colonial sidearm, compact practical frame",
            "dog tags, tiny engraved detail",
            "Raptor flight chart, paper and digital notes",
            "Cylon data spine, red glowing strip",
            "Kobol scripture book, worn leather cover",
        ],
        "factions": [
            "Colonial Fleet identity, military flight gear, survival discipline",
            "Galactica crew identity, worn uniforms, practical shipboard life",
            "Cylon identity, red scanning light, synthetic mystery",
            "Caprica resistance identity, civilian coats, improvised weapons",
            "Kobol faith identity, ancient symbols, pilgrimage mood",
        ],
        "ships": [
            "Viper fighter parked behind subject",
            "Raptor shuttle bay silhouette",
            "Battlestar Galactica hull outside window",
            "Cylon Raider red-eye silhouette in space",
        ],
        "architecture": [
            "Battlestar ribbed metal corridors, worn paint, military labels",
            "CIC tactical room, blue displays, old monitors",
            "Cylon organic-metal chamber, red light, curved walls",
            "Kobol stone temple, rain and moss",
        ],
        "technology": [
            "analog shipboard displays, tactical maps, hard switches",
            "Cylon red scanner line, restrained glow",
            "flight deck launch rails, hydraulic machinery",
        ],
        "lighting": [
            "dim blue shipboard light, military shadows",
            "red Cylon scanner glow, glossy black contrast",
            "hangar work lights, smoke and metal reflections",
            "rainy Caprica daylight, grey survival mood",
        ],
        "palettes": [
            "navy grey and orange flight suit palette",
            "red Cylon and black chrome palette",
            "shipboard blue and worn steel palette",
            "rain grey and olive resistance palette",
        ],
        "cinematic": [
            "military survival sci-fi key art, fighter bay depth",
            "shipboard drama framing, practical gear, tired confidence",
            "synthetic infiltrator portrait, red scanner light, ambiguity",
        ],
        "avoid": ["Federation optimism", "Jedi mysticism", "fantasy castles"],
    },
    {
        "id": "dune",
        "label": "Dune Arrakis desert empire mysticism",
        "source": "Dune",
        "weight": 0.9,
        "signature_terms": ["Arrakis", "Fremen", "Bene Gesserit", "Atreides", "Harkonnen", "spice melange"],
        "roles": [
            "Bene Gesserit sister",
            "Fremen desert warrior",
            "Atreides royal envoy",
            "Harkonnen court assassin",
            "Sardaukar battle priestess",
            "Spacing Guild oracle",
            "Arrakis spice smuggler",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Fremen stillsuit, wrapped desert scarf, blue eye emphasis",
            "Bene Gesserit black hooded gown, severe silhouette",
            "Atreides green-black court armor, signet ring, cloak",
            "Harkonnen black ceremonial armor, harsh shoulders",
            "Sardaukar white battle robe, red markings, plated gloves",
            "Spacing Guild veil and breathing apparatus, translucent fabric",
        ],
        "environments": [
            "Arrakis desert ridge, twin moons, spice haze",
            "sietch cavern interior, water seals, warm lamps",
            "Atreides palace hall, brutalist stone, desert windows",
            "Harkonnen industrial throne room, black oil reflections",
            "ornithopter landing pad, sandstorm horizon",
            "spice harvester field, huge tracks, wormsign in distance",
        ],
        "props": [
            "crysknife, pale curved blade, sacred handling",
            "ornithopter control map, brass and glass detail",
            "spice melange vial, amber dust glow",
            "Gom Jabbar needle box, tiny black case",
            "Atreides signet ring, green banner detail",
            "stillsuit water tube, functional design",
        ],
        "factions": [
            "Fremen identity, stillsuit, blue eyes, desert survival",
            "Bene Gesserit identity, black hooded discipline, hidden power",
            "House Atreides identity, green-black nobility, hawk symbol mood",
            "House Harkonnen identity, black industrial cruelty, pale menace",
            "Sardaukar identity, white combat ritual, imperial brutality",
            "Spacing Guild identity, veils, navigation mysticism, strange technology",
        ],
        "creatures": [
            "sandworm ridge breaking the dune line",
            "desert mouse silhouette near stillsuit boot",
            "ornithopter shadow crossing spice haze",
        ],
        "architecture": [
            "Arrakis brutalist palace stone, narrow sun shafts",
            "sietch carved rock chambers, water seals, woven rugs",
            "Harkonnen black industrial halls, oil sheen, huge scale",
            "imperial court geometry, gold banners, severe symmetry",
        ],
        "technology": [
            "ornithopter wing mechanics, dragonfly silhouette",
            "stillsuit water reclamation tubes, readable function",
            "spice navigation devices, amber holographic dust",
            "shield belt shimmer, subtle blue distortion",
        ],
        "lighting": [
            "harsh desert sun, high contrast, spice haze",
            "warm sietch lamplight, cave shadows",
            "black industrial underlight, Harkonnen menace",
            "gold imperial window light, austere symmetry",
        ],
        "palettes": [
            "sand gold and black stillsuit palette",
            "Atreides green and desert tan palette",
            "Harkonnen black and oil bronze palette",
            "spice amber and moon blue palette",
        ],
        "cinematic": [
            "epic desert empire framing, massive scale, readable stillsuit",
            "ritual sci-fi portrait, hooded silhouette, severe composition",
            "sandstorm key art, cloak motion, distant wormsign",
        ],
        "avoid": ["laser swords", "bright cyberpunk streets", "wizard castle classrooms"],
    },
    {
        "id": "mass_effect",
        "label": "Mass Effect Citadel spectre space RPG",
        "source": "Mass Effect",
        "weight": 0.88,
        "signature_terms": ["Citadel", "N7", "Spectre", "Systems Alliance", "Cerberus", "Mass Relay"],
        "roles": [
            "N7 commander heroine",
            "Citadel Spectre operative",
            "Systems Alliance pilot",
            "Cerberus defecting agent",
            "Asari-inspired biotic commando",
            "Quarian-inspired engineer",
            "Omega station information broker",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "N7 black armor, red-white stripe, readable chest plate",
            "Spectre formal tactical coat, polished shoulder plates",
            "Systems Alliance flight suit, harness, compact gloves",
            "Cerberus-style white-black armor, yellow lights",
            "Asari-inspired sleek biotic robe armor, blue glow",
            "Quarian-inspired hooded enviro-suit, patterned fabric, visor",
            "Omega club coat, red neon reflections, armored boots",
        ],
        "environments": [
            "Citadel Presidium balcony, curved glass, alien garden",
            "Normandy-like starship cabin, blue consoles, galaxy map",
            "Omega asteroid station bar, red neon, metal walkways",
            "Mass Relay space view, blue energy ring, starfield",
            "Systems Alliance hangar, shuttle ramp, clean military lights",
            "alien council chamber, tall windows, polished floors",
        ],
        "props": [
            "omni-tool hologram, orange interface around wrist",
            "M-8 Avenger-like sci-fi rifle, compact silhouette",
            "Spectre badge, small metallic emblem",
            "biotic amp module, blue energy glow",
            "data pad with galaxy map, clean blue UI",
            "helmet under arm, reflective visor",
        ],
        "factions": [
            "N7 identity, black armor, red-white stripe, elite commander mood",
            "Citadel Council identity, diplomatic polish, alien architecture",
            "Systems Alliance identity, navy-blue military pragmatism",
            "Cerberus identity, white-black armor, yellow warning lights",
            "Asari commando identity, elegant biotic blue energy",
            "Quarian migrant fleet identity, hooded enviro-suit, patterned cloth",
            "Geth technology mood, clean synthetic lights, geometric panels",
        ],
        "creatures": [
            "Asari-like alien silhouette in council background",
            "Turian-like armored diplomat silhouette",
            "Krogan-like heavy mercenary silhouette",
            "Geth-like synthetic drone shape, blue optic",
        ],
        "architecture": [
            "Citadel curved white architecture, clean glass, garden terraces",
            "starship CIC consoles, blue galaxy map, sleek panels",
            "Omega station metal walkways, red neon, patched walls",
            "diplomatic council chamber, high windows, polished stone",
        ],
        "technology": [
            "omni-tool wrist interface, orange holographic panels",
            "biotic blue energy field, clean contained glow",
            "galaxy map hologram, rotating star clusters",
            "mass effect field coils, blue-white light",
        ],
        "lighting": [
            "blue console glow and soft white starship light",
            "orange omni-tool light on hand, cool rim light",
            "red asteroid station neon, metallic shadow",
            "clean diplomatic daylight through curved glass",
        ],
        "palettes": [
            "N7 black red and white palette, elite sci-fi",
            "Citadel blue white and garden green palette",
            "Omega red and gunmetal palette, station noir",
            "biotic blue and silver palette, elegant power",
        ],
        "cinematic": [
            "space RPG key art, armor readable, galaxy backdrop",
            "diplomatic sci-fi portrait, curved architecture, clean lighting",
            "starship command composition, hologram foreground, focused gaze",
        ],
        "avoid": ["wizard robes", "wasteland diners", "gothic medieval armor"],
    },
    {
        "id": "halo",
        "label": "Halo ringworld supersoldier war",
        "source": "Halo",
        "weight": 0.84,
        "signature_terms": ["UNSC", "Spartan", "ODST", "Covenant", "Forerunner", "Halo ring"],
        "roles": [
            "UNSC Spartan supersoldier woman",
            "ODST drop trooper",
            "Forerunner ruin explorer",
            "Covenant war survivor",
            "AI companion handler",
            "UNSC Navy intelligence officer",
            "Reach battlefield scout",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Spartan-style green power armor, black undersuit, scratched plates",
            "ODST dark drop armor, visor raised, tactical straps",
            "UNSC officer jacket over armored bodysuit, utility belt",
            "Forerunner-tech explorer suit, white panels, cyan glyphs",
            "Covenant salvage cloak over combat suit, purple metal pieces",
            "Reach scout armor, worn green plates, amber visor",
        ],
        "environments": [
            "Halo ring horizon, curved world arc in sky, grassland battlefield",
            "UNSC frigate hangar, Warthog nearby, cold lights",
            "Forerunner ruin interior, glowing blue hardlight bridges",
            "Covenant cruiser corridor, purple metal, alien lights",
            "ODST rain-soaked city street, drop pods, smoke",
            "Reach battlefield ridge, burning sky, evac ships",
        ],
        "props": [
            "MA5 rifle-inspired sci-fi assault rifle, clean military silhouette",
            "energy sword, blue plasma blade, controlled glow",
            "plasma rifle, purple metal casing, blue highlights",
            "Cortana-like blue AI hologram, tiny figure in palm",
            "Warthog jeep silhouette, rugged tires, hangar background",
            "drop pod beacon, red flashing light",
            "hardlight shield module, hexagonal glow",
        ],
        "factions": [
            "UNSC identity, green armor, military stencils, practical hardware",
            "Spartan program identity, heavy armor, visor motif, calm strength",
            "ODST identity, black drop armor, orbital drop pod details",
            "Covenant identity, purple alien metal, plasma glow",
            "Forerunner identity, white geometric ruins, blue hardlight",
        ],
        "creatures": [
            "Elite-like alien warrior silhouette behind purple glass",
            "Grunt-like small alien silhouette near crates",
            "Flood-like infection tendrils kept subtle in background",
            "drone swarm over battlefield smoke",
        ],
        "architecture": [
            "Forerunner geometric white stone, blue hardlight lines",
            "UNSC military hangar, grey panels, vehicle bays",
            "Covenant curved purple metal corridor, alien lamps",
            "ringworld landscape with artificial horizon arc",
        ],
        "technology": [
            "blue hardlight bridge, clean geometric glow",
            "AI hologram projection, transparent blue figure",
            "military HUD visor, amber reflections",
            "plasma weapon coils, contained blue-purple light",
        ],
        "lighting": [
            "blue hardlight glow against grey armor",
            "rainy city combat light, orange fires, wet surfaces",
            "bright ringworld daylight, clean green landscape",
            "purple Covenant interior light, alien metal reflections",
        ],
        "palettes": [
            "olive green and amber visor palette, supersoldier mood",
            "Forerunner white and cyan palette, ancient sci-fi",
            "purple plasma and black metal palette, alien war",
            "rain blue and orange fire palette, urban battle",
        ],
        "cinematic": [
            "military sci-fi poster, armor readable, ringworld horizon",
            "first-person shooter key art, strong silhouette, weapon clean",
            "ancient alien ruin framing, hardlight depth, heroic scale",
        ],
        "avoid": ["magical castle robes", "wasteland diners", "vampire lounges"],
    },
    {
        "id": "warhammer_40k",
        "label": "Warhammer 40K grimdark hive cathedral war",
        "source": "Warhammer 40,000",
        "weight": 0.88,
        "signature_terms": ["Adepta Sororitas", "Inquisition", "Adeptus Mechanicus", "Astra Militarum", "hive city", "servo-skull"],
        "roles": [
            "Adepta Sororitas-inspired battle sister",
            "Inquisition interrogator",
            "Astra Militarum officer",
            "Adeptus Mechanicus tech-priestess",
            "Necromunda underhive bounty huntress",
            "hive city noble duelist",
            "Chaos cult infiltrator",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "black power armor corset silhouette, purity seals, red cloth",
            "red Mechanicus robe, brass cables, hood lowered",
            "Inquisition long coat, high collar, silver rosette",
            "Astra Militarum officer coat, medals, tactical belt",
            "underhive scavenger armor, respirator, patched cloak",
            "ornate gothic plate armor, fleur-de-lis motifs, candles",
        ],
        "environments": [
            "Imperial hive city cathedral street, skull statues, smoke",
            "gothic cathedral starship nave, stained glass, machinery",
            "underhive factory bridge, chains, steam, yellow lamps",
            "Mechanicus forge temple, red robes, cog altars",
            "Inquisition interrogation chamber, black stone, red candles",
            "battlefield trench shrine, broken banners, ash rain",
        ],
        "props": [
            "bolter-like heavy pistol, blocky silhouette, purity seal",
            "chainsword, serrated blade, red warning light",
            "lasgun, long rifle, worn metal casing",
            "servo-skull, floating lens, tiny cables",
            "Inquisition rosette, red enamel detail",
            "cogitator data slate, green screen, brass casing",
            "rosary of purity seals, parchment strips, wax stamps",
            "ornate power sword, blue energy edge",
        ],
        "factions": [
            "Adepta Sororitas identity, black armor, red cloth, purity seals",
            "Inquisition identity, rosette badge, black coat, gothic authority",
            "Adeptus Mechanicus identity, red robe, cog motifs, augmetic limbs",
            "Astra Militarum identity, officer coat, medals, battlefield practicality",
            "Space Marine chapter shrine mood, giant armor icons, banners",
            "Chaos cult identity, cracked symbols, red-black forbidden atmosphere",
            "Necromunda underhive gang identity, respirator, scrap armor, industrial grime",
        ],
        "creatures": [
            "servo-skull familiar with tiny lens",
            "cherub-like machine drone, candle glow",
            "tyranid-like alien claw shadow in smoke",
            "daemon silhouette behind cracked stained glass",
            "underhive mutant silhouette in steam",
        ],
        "architecture": [
            "gothic cathedral arches fused with machinery",
            "hive city vertical canyon, pipes, shrines, banners",
            "Mechanicus forge altar, cog wheels, red lamps",
            "black stone interrogation room, candles, iron doors",
        ],
        "technology": [
            "ancient machine interfaces, brass knobs, green screens",
            "cybernetic augmetics, visible cables, devotional ornaments",
            "plasma coils, blue glow, heavy industrial casing",
            "servo-skull optics, tiny lenses, parchment tags",
        ],
        "lighting": [
            "red candlelight and cathedral shadow, grim atmosphere",
            "forge orange glow, black armor reflections",
            "blue plasma rim light, smoke layers",
            "sickly green cogitator glow, dark stone contrast",
        ],
        "palettes": [
            "black red and antique gold palette, gothic authority",
            "brass red and smoke grey palette, Mechanicus mood",
            "bone white and crimson palette, ritual war",
            "gunmetal and blue plasma palette, grim sci-fi",
        ],
        "cinematic": [
            "grimdark cover art, towering gothic scale, readable armor",
            "cathedral sci-fi portrait, vertical arches, sacred machinery",
            "war banner composition, smoke depth, severe expression",
        ],
        "avoid": ["cute academy tone", "clean bright Starfleet optimism", "suburban motel mystery"],
    },
    {
        "id": "cyberpunk_2077",
        "label": "Cyberpunk 2077 Night City mercenary noir",
        "source": "Cyberpunk 2077",
        "weight": 0.9,
        "signature_terms": ["Night City", "Arasaka", "Militech", "Maelstrom", "Voodoo Boys", "Netrunner"],
        "roles": [
            "Night City netrunner woman",
            "Arasaka corporate assassin",
            "Militech combat tech operative",
            "Maelstrom chrome street mercenary",
            "Voodoo Boys data mystic",
            "Afterlife club fixer",
            "braindance editor",
            "cyberdoc apprentice",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "black synth-leather jacket, glowing seam trim, utility belt",
            "Arasaka formal combat dress, red-black corporate accents",
            "Militech armored vest over fitted bodysuit, matte plates",
            "netrunner suit, cable ports, translucent raincoat",
            "street merc jacket, chrome arm guard, thigh holster",
            "clubwear tech jacket, holographic sleeve panels, black stockings",
        ],
        "environments": [
            "Night City megabuilding balcony, giant ads, rain haze",
            "Arasaka tower lobby, black marble, red holograms",
            "Militech checkpoint street, armored drones, wet asphalt",
            "neon noodle alley, steam vents, stacked signs",
            "abandoned braindance studio, glowing monitors, cables",
            "cyberdoc clinic, chrome chair, surgical lamps",
        ],
        "props": [
            "cyberdeck, glowing cable ports, readable screen",
            "Mantis blade cyberarm, clean folded silhouette",
            "smart pistol, compact black frame, red sight",
            "monowire spool, faint blue line, controlled glow",
            "braindance wreath device, chrome headband",
            "data shard, transparent glowing memory chip",
        ],
        "factions": [
            "Arasaka corporate identity, black and red logo mood, polished menace",
            "Militech security identity, gunmetal armor, yellow warning accents",
            "Maelstrom gang identity, red optics, industrial metal details",
            "Voodoo Boys netrunner identity, ritual tech, green data glow",
            "Afterlife mercenary identity, black leather, neon bar mood",
        ],
        "architecture": [
            "brutalist megabuilding concrete, neon signs, dense vertical city",
            "black corporate tower glass, red holographic signage",
            "stacked apartment balconies, cables and vending machines",
            "cyber clinic chrome panels, surgical lamps, cable nests",
        ],
        "technology": [
            "neural interface cables, visible but clean",
            "holographic city map, layered blue-red data",
            "wetware implant tools, chrome and soft blue light",
            "advertising holograms, giant face screens, rain distortion",
        ],
        "lighting": [
            "magenta neon and yellow streetlamp reflections, rainy noir",
            "red corporate glow, black marble contrast",
            "green data light on face, deep city shadows",
            "warm noodle stand light against cold rain",
        ],
        "palettes": [
            "magenta yellow and black palette, rainy cyberpunk contrast",
            "red black and chrome palette, corporate danger",
            "acid green and deep violet palette, netrunner mood",
            "warm amber and cold blue palette, city noir",
        ],
        "cinematic": [
            "cyberpunk noir key visual, rain reflections, readable cyberware",
            "megacity vertical framing, giant ads behind subject",
            "tech thriller portrait, interface glow, hands visible",
        ],
        "avoid": ["medieval castles", "wizard school robes", "wasteland diner retrofuturism"],
    },
    {
        "id": "blade_runner",
        "label": "Blade Runner rainy replicant noir",
        "source": "Blade Runner",
        "weight": 0.72,
        "signature_terms": ["replicant", "Tyrell", "Los Angeles 2019", "Voight-Kampff", "spinner", "origami unicorn"],
        "roles": [
            "replicant noir lounge singer",
            "Tyrell corporate secretary",
            "blade runner investigator",
            "rainy street android runaway",
            "off-world advertisement model",
            "neon noodle stall witness",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "transparent raincoat over black dress, wet reflections",
            "structured noir trench coat, high collar, tall boots",
            "Tyrell gold corporate gown, owl brooch, severe elegance",
            "retro-future secretary blouse, pencil skirt, stockings",
            "neon lounge dress, sequins, smoky makeup",
            "android street coat, silver collar, worn gloves",
        ],
        "environments": [
            "rainy Los Angeles 2019 street, giant geisha billboard, steam",
            "Tyrell pyramid office, golden light, owl silhouette",
            "Voight-Kampff interrogation room, blinds shadows, black table",
            "neon noodle market, umbrellas, crowded signs",
            "abandoned apartment, broken piano, city lights outside",
            "spinner landing pad, rain haze, red warning lights",
        ],
        "props": [
            "Voight-Kampff scanner, analog lens, tiny red light",
            "origami unicorn, small white paper detail",
            "replicant memory photo, worn corners",
            "blade runner blaster, heavy black frame",
            "Tyrell owl brooch, gold reflection",
            "neon cigarette holder, smoky silhouette",
        ],
        "factions": [
            "Tyrell Corporation identity, gold luxury, cold artificial power",
            "blade runner identity, trench coat, badge, interrogation tools",
            "replicant identity, elegant artificial humanity, haunted gaze",
            "off-world colony advert mood, neon fantasy, rain decay",
        ],
        "architecture": [
            "Tyrell pyramid interior, monumental gold windows",
            "rainy market streets, neon signs, steam pipes",
            "brutalist apartment block, wet concrete, giant billboards",
            "interrogation room blinds, table reflections, black walls",
        ],
        "technology": [
            "Voight-Kampff lenses, analog mechanical iris",
            "spinner vehicle lights, rain-smeared glass",
            "giant animated billboard faces, neon reflections",
            "replicant memory archive, printed photos and scanlines",
        ],
        "lighting": [
            "gold Tyrell sunset through monumental windows",
            "rainy cyan-magenta street neon, deep black shadows",
            "Venetian blinds noir light across face",
            "orange smoke haze, wet glass reflections",
        ],
        "palettes": [
            "gold black and smoke palette, Tyrell luxury",
            "cyan magenta and rain black palette, street noir",
            "amber neon and dark brown palette, retro-future decay",
            "white paper and blue rain palette, melancholic detail",
        ],
        "cinematic": [
            "neo-noir replicant portrait, rain reflections, haunted face",
            "interrogation chamber framing, scanner foreground, still tension",
            "rainy future city shot, billboard scale, clear silhouette",
        ],
        "avoid": ["Night City gang logic", "Jedi mysticism", "fantasy magic"],
    },
    {
        "id": "ghost_in_the_shell",
        "label": "Ghost in the Shell cybernetic police philosophy",
        "source": "Ghost in the Shell",
        "weight": 0.7,
        "signature_terms": ["Section 9", "cyberbrain", "thermoptic camouflage", "Puppet Master", "Kusanagi-style", "Tachikoma"],
        "roles": [
            "Section 9 tactical cyborg investigator",
            "cyberbrain crime analyst",
            "thermoptic infiltration specialist",
            "Puppet Master case witness",
            "cybernetic harbor sniper",
            "Tachikoma mechanic",
        ],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": [
            "Section 9 tactical coat, smart fabric panels, earpiece",
            "matte bodysuit under cropped jacket, subtle cyber seams",
            "thermoptic cloak shimmer, transparent edge distortion",
            "formal cyber-police blazer, shoulder holster, gloves",
            "harbor raincoat, black boots, data visor",
            "mechanic coverall, tool belt, blue robot oil stains",
        ],
        "environments": [
            "Section 9 operations room, glass screens, city map",
            "rainy Japanese harbor, cranes, neon water reflections",
            "cyberbrain dive chamber, cables, blue liquid light",
            "rooftop sniper nest, city haze, antenna forest",
            "underground hacker den, monitors, green code",
            "corporate lobby, clean glass, invisible threat",
        ],
        "props": [
            "cyberbrain cable ports, clean neck detail",
            "compact police pistol, black frame, controlled pose",
            "Tachikoma-like blue robot companion, round optics",
            "thermoptic cloak device, small wrist control",
            "data-glove interface, translucent blue UI",
            "cyborg maintenance tool kit, chrome instruments",
        ],
        "factions": [
            "Public Security Section 9 identity, tactical law enforcement gear",
            "Puppet Master mystery mood, ghost in the machine symbolism",
            "corporate cybercrime identity, clean glass, hidden corruption",
            "cybernetic black market mood, cables, artificial bodies",
        ],
        "droids": [
            "Tachikoma-like blue spider tank, friendly optics",
            "small surveillance drone, silent rotor, blue sensor",
            "robotic maintenance arm, chrome joints",
        ],
        "architecture": [
            "near-future Japanese harbor, cranes, rain, towers",
            "Section 9 glass command room, transparent displays",
            "corporate atrium, clean panels, surveillance cameras",
            "cyberbrain lab, cables, blue tanks, sterile white walls",
        ],
        "technology": [
            "cyberbrain network visualization, blue data threads",
            "thermoptic camouflage shimmer, subtle body outline",
            "full-body prosthetic shell details, elegant mechanical joints",
            "AR data windows, clean police interface",
        ],
        "lighting": [
            "rainy harbor blue light, reflective black water",
            "sterile lab cyan glow, clean body highlights",
            "green code underlight, hacker den shadows",
            "soft corporate daylight, glass reflections",
        ],
        "palettes": [
            "cyan grey and black palette, cyber police mood",
            "rain blue and neon green palette, hacker atmosphere",
            "white glass and pale blue palette, synthetic body clarity",
            "harbor orange and steel palette, urban melancholy",
        ],
        "cinematic": [
            "philosophical cybercrime key visual, clean interface, calm gaze",
            "near-future police thriller framing, rain, readable cyberware",
            "cyberbrain dive portrait, cables and blue light, serene mood",
        ],
        "avoid": ["Night City street gang overkill", "wasteland rust", "wizard castles"],
    },
]


MORE_SPECS = [
    {
        "id": "resident_evil",
        "label": "Resident Evil biohazard mansion outbreak",
        "source": "Resident Evil",
        "weight": 0.86,
        "signature_terms": ["S.T.A.R.S.", "Umbrella", "Raccoon City", "Spencer Mansion", "T-virus", "Tyrant"],
        "roles": ["S.T.A.R.S. special agent", "Umbrella lab survivor", "Raccoon City police heroine", "Spencer Mansion investigator", "quarantine medic", "anti-biohazard commando"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["blue tactical police uniform, shoulder holster, gloves", "black tactical vest, radio cable, practical boots", "Umbrella lab coat over dark dress, red biohazard patch", "civilian survivor jacket, bandaged arm, utility pouch", "red leather jacket, combat belt, thigh holster", "quarantine suit half-removed, respirator at neck"],
        "environments": ["Spencer Mansion main hall, grand staircase, broken chandelier", "Raccoon City police station corridor, rain through windows", "Umbrella underground lab, glass tanks, red warning lights", "hospital quarantine ward, plastic curtains, emergency lamps", "abandoned subway shelter, old posters, flickering lights", "save room, typewriter desk, warm lamp, dark corners"],
        "props": ["S.T.A.R.S. badge, small readable detail", "Beretta-style handgun, flashlight grip, practical stance", "green herb pouch, survival inventory detail", "Umbrella keycard, red-white logo mood", "T-virus sample vial, blue-green liquid", "first aid spray can, red medical label"],
        "factions": ["S.T.A.R.S. identity, tactical police gear, badge detail", "Umbrella Corporation identity, red-white biohazard branding, sterile menace", "Raccoon City Police Department mood, blue uniform, station architecture", "BSAA-inspired anti-biohazard identity, field gear, practical patches"],
        "creatures": ["Tyrant-like huge shadow behind lab glass", "Licker-like crawling silhouette in ceiling shadow", "zombie crowd blurred behind barricade", "mutated dog silhouette at corridor end"],
        "architecture": ["gothic mansion wood paneling, red carpet, grand staircase", "police station stone arches, bulletin boards, broken glass", "sterile underground lab, glass tubes, warning stripes", "quarantine hospital curtains, tiled walls, emergency signage"],
        "technology": ["retro lab terminals, green CRT text, warning beacons", "biocontainment chambers, glass condensation, tube lights", "industrial medical equipment, cables and monitors"],
        "lighting": ["flashlight cone in dark corridor, tense shadows", "red lab alarm lights, sterile glass reflections", "save room warm lamp, deep surrounding darkness", "rainy police station blue light, wet stone reflections"],
        "palettes": ["red warning light and cold steel palette", "police blue and wet black palette", "sterile white and biohazard green palette", "mansion burgundy and dark oak palette"],
        "cinematic": ["survival horror key visual, flashlight beam, readable equipment", "mansion horror framing, doorway depth, practical weapon", "lab outbreak thriller composition, glass tanks, red alarms"],
        "avoid": ["wizard robes", "space opera mysticism", "bright magical school mood"],
    },
    {
        "id": "the_last_of_us",
        "label": "The Last of Us overgrown survival drama",
        "source": "The Last of Us",
        "weight": 0.68,
        "signature_terms": ["Fireflies", "FEDRA", "Clicker", "Cordyceps", "Boston QZ", "Jackson"],
        "roles": ["Fireflies field medic", "FEDRA quarantine deserter", "Jackson patrol scout", "Cordyceps outbreak survivor", "ruined city smuggler", "winter lodge defender"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["worn denim jacket, backpack straps, muddy boots", "Fireflies patch on green jacket, field bandages", "FEDRA tactical jacket, cracked armor plates", "winter parka, scarf, rifle sling", "patched flannel shirt, practical jeans, hiking boots", "rain poncho over survival gear, flashlight strap"],
        "environments": ["overgrown Boston street, vines over cars, soft sunlight", "FEDRA quarantine gate, concrete walls, warning signs", "Jackson settlement fence, snow, warm cabin lights", "abandoned museum hall, spores in sunbeams", "flooded subway tunnel, moss, flashlight beam", "ruined university lab, broken glass, ivy"],
        "props": ["shiv knife, taped handle, practical grip", "revolver with worn wooden grip", "gas mask hanging at hip, fogged lenses", "Fireflies dog tag, small engraved detail", "field medkit, dirty bandage roll", "guitar case, scratched wood, strap over shoulder"],
        "factions": ["Fireflies identity, resistance patch, field medic gear", "FEDRA identity, militarized quarantine armor, warning labels", "Jackson survivor community mood, winter practical clothing", "smuggler identity, hidden weapons, worn backpack"],
        "creatures": ["Clicker-like infected silhouette in fungal hallway", "bloater-like huge shadow behind spores", "runner infected crowd blurred in distance"],
        "architecture": ["overgrown city blocks, vines, abandoned cars", "quarantine zone concrete, floodlights, chain link", "wooden mountain settlement, snow, warm lamps", "ruined university corridors, ivy and broken windows"],
        "technology": ["old radio, battery pack, taped wires", "FEDRA checkpoint floodlights, warning speakers", "field generator, extension cables, practical lamps"],
        "lighting": ["gold sunbeams through spores, warm ruin light", "cold flashlight beam, green overgrowth shadows", "winter blue daylight, warm cabin windows", "rainy grey city light, wet moss reflections"],
        "palettes": ["moss green and faded denim palette", "rust orange and overgrown concrete palette", "winter blue and warm cabin amber palette", "dirty olive and quarantine yellow palette"],
        "cinematic": ["grounded survival drama framing, backpack readable, emotional stillness", "overgrown apocalypse key visual, nature reclaiming the city", "tense stealth shot, flashlight and spores, clear silhouette"],
        "avoid": ["retro Fallout branding", "cyberpunk neon", "wizard school motifs"],
    },
    {
        "id": "dead_space",
        "label": "Dead Space derelict engineer horror",
        "source": "Dead Space",
        "weight": 0.64,
        "signature_terms": ["USG Ishimura", "Unitology", "Marker", "RIG suit", "plasma cutter", "necromorph"],
        "roles": ["USG Ishimura engineer", "Unitology cult survivor", "RIG suit repair specialist", "space medical bay investigator", "mining deck security officer", "Marker signal researcher"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["RIG engineering suit, spine health lights, heavy gloves", "mining deck armor, bronze plates, helmet at side", "Unitology black robe over utility suit, red marker pendant", "medical bay jumpsuit, clean straps, bloodless warning tags", "security armor, visor raised, cold sweat", "vacuum suit undersuit, magnetic boots, tool belt"],
        "environments": ["USG Ishimura engineering deck, orange hazard lights, pipes", "zero-g medical bay, floating tools, cold metal walls", "Unitology shrine room, Marker symbols, red candles", "mining deck tram station, sparks, heavy machinery", "hydroponics bay, dead plants, green emergency light", "airlock corridor, frost, warning labels"],
        "props": ["plasma cutter tool, orange light, industrial grip", "RIG helmet, scratched gold visor", "kinesis module, blue hand glow", "stasis module, circular blue charge", "Marker fragment, black-red carved shape", "audio log recorder, tiny waveform screen"],
        "factions": ["CEC engineering identity, industrial suit, tool practicality", "Unitology identity, Marker symbols, ritual dread", "Ishimura security identity, heavy armor, emergency lights"],
        "creatures": ["necromorph-like claw silhouette behind frosted glass", "infector-like shadow near ceiling vent", "lurker-like shape in zero-g distance"],
        "architecture": ["industrial spaceship corridors, ribbed metal, warning stripes", "Ishimura mining deck machinery, orange lamps, conveyor rails", "medical bay glass partitions, floating instruments", "Unitology shrine alcoves, black stone and red light"],
        "technology": ["RIG spine health display, blue lights", "plasma cutter mining tool, bright orange beam", "kinesis field, small blue distortion", "stasis field effect, frozen sparks"],
        "lighting": ["orange hazard lights, deep industrial shadows", "cold blue medical light, floating dust", "red Marker ritual glow, black metal contrast", "flickering emergency strobes, smoke layers"],
        "palettes": ["bronze orange and dark steel palette", "cold medical blue and black palette", "red Marker and industrial grey palette", "vacuum white frost and hazard yellow palette"],
        "cinematic": ["space horror key visual, tool weapon readable, corridor dread", "derelict ship framing, warning lights, heavy suit silhouette", "zero-g medical horror, floating objects, clean face focus"],
        "avoid": ["clean Starfleet optimism", "fantasy castles", "bright anime adventure"],
    },
    {
        "id": "silent_hill",
        "label": "Silent Hill fog town psychological horror",
        "source": "Silent Hill",
        "weight": 0.68,
        "signature_terms": ["Silent Hill", "Otherworld", "Pyramid Head", "Brookhaven Hospital", "Alchemilla Hospital", "siren"],
        "roles": ["fog town lost visitor", "Brookhaven nurse survivor", "Otherworld ritual witness", "Alchemilla hospital investigator", "lakeside grief mourner", "rusted church penitent"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["worn cardigan over black dress, muddy shoes", "bloodless nurse uniform with cracked badge, practical stockings", "raincoat over dark skirt, flashlight strap", "rust-stained coat, bandaged wrist, boots", "church mourner dress, old pendant, gloves", "schoolteacher coat avoided, adult formal blouse and skirt"],
        "environments": ["Silent Hill foggy street, ash fall, dead storefronts", "Brookhaven Hospital corridor, peeling paint, flickering lights", "Otherworld rust chamber, chain link walls, red siren glow", "Alchemilla Hospital room, old bed, green fluorescent haze", "lakeside pier, thick fog, distant town lights", "abandoned church, red stained glass, ash dust"],
        "props": ["flashlight beam, fog visible in cone", "portable radio, static waves, cracked casing", "rusted key, tag label, small detail", "old photograph, torn edge, hidden meaning", "map marked in red pen, folded paper", "small music box, tarnished metal"],
        "factions": ["Order cult identity, red symbols, church secrecy", "Otherworld identity, rust, chain link, siren light", "fog world identity, ash fall, isolation, muted clothing"],
        "creatures": ["Pyramid Head-like distant executioner silhouette", "nurse creature silhouette behind frosted glass", "mannequin-like horror shape in red shadow"],
        "architecture": ["foggy resort town street, dead signs, wet asphalt", "hospital tile corridor, peeling paint, green lights", "Otherworld chain-link architecture, rust plates, hanging wires", "old church nave, red glass, broken pews"],
        "technology": ["static radio, visible signal lines", "broken hospital monitors, green flicker", "siren warning light, red rotating beam"],
        "lighting": ["flat foggy daylight, ash in air", "sickly hospital fluorescent, green tint", "red siren glow, rust shadows", "flashlight cone, black corners"],
        "palettes": ["ash grey and rust red palette", "hospital green and dirty white palette", "fog white and wet black palette", "brown rust and dark crimson palette"],
        "cinematic": ["psychological horror portrait, fog depth, readable prop", "Otherworld transformation framing, rust textures, controlled chaos", "hospital corridor key visual, flashlight and empty doors"],
        "avoid": ["action shooter glam", "cyberpunk neon city", "wizard academy warmth"],
    },
    {
        "id": "supernatural",
        "label": "Supernatural Winchester road hunter horror",
        "source": "Supernatural",
        "weight": 0.78,
        "signature_terms": ["Winchester", "Men of Letters", "devil's trap", "angel blade", "Crossroads demon", "EMF meter"],
        "roles": ["Winchester-style road hunter", "Men of Letters archivist", "Crossroads demon dealmaker", "angel-marked investigator", "demonologist in motel room", "hunter bar informant"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["black leather jacket, fitted jeans, silver necklace", "trench coat over dark dress, boots, occult pendant", "flannel shirt tied at waist, tactical belt, thigh holster", "motel glamour dress, leather jacket, salt-stained boots", "black lace top with hunter coat, practical pants", "old diner waitress dress with hidden weapons"],
        "environments": ["cheap motel room, occult symbols on wall, neon through blinds", "Men of Letters bunker archive, green lamps, old files", "rainy graveyard, old headstones, flashlight beam", "roadside diner at midnight, red booths, empty windows", "dark forest road, car headlights, fog", "abandoned church basement, salt circle, cracked floor"],
        "props": ["sawed-off shotgun, engraved demon trap charm", "angel blade-like silver dagger, bright edge highlight", "John Winchester-style occult journal, handwritten symbols", "EMF meter, blinking red lights", "salt canister, white salt line on floor", "anti-possession tattoo motif, black symbol detail"],
        "factions": ["Winchester hunter network identity, old car keys, leather journal", "Men of Letters identity, bunker archives, sigil-covered files", "Angel faction identity, trench coat, gold warding symbols", "Demon faction identity, black eyes motif, crossroads red light", "Leviathan-style corporate monster mood, black suit, cold grin"],
        "creatures": ["black-eyed possessed figure blurred in background", "hellhound claw marks on door", "ghost silhouette in fogged window", "wraith-like ghost distortion in mirror", "wendigo-like tall shadow in forest"],
        "architecture": ["cheap motel wallpaper, old lamps, patterned carpet", "Men of Letters bunker shelves, green lamps, brass files", "rural church woodwork, cracked stained glass", "graveyard iron fence, old stone mausoleum"],
        "magic": ["devil's trap circle, red chalk on wood floor", "salt circle protection, clear white line, candle points", "angel warding symbols, faint gold light", "exorcism sigils, black ink symbols, controlled glow"],
        "lighting": ["neon motel light through blinds, rain shadows", "flashlight cone in fog, cool blue darkness", "warm diner lamps against black windows", "candle circle glow, dark basement contrast"],
        "palettes": ["motel neon red and sickly green palette", "rain blue and warm tungsten palette", "graveyard grey and cold moon palette", "black leather and silver charm palette"],
        "cinematic": ["monster-of-the-week TV framing, practical props, tense mood", "occult road trip noir, rain reflections, flashlight edge light", "motel horror composition, blinds shadows, readable face"],
        "avoid": ["space opera starships", "magical academy castle", "high fantasy armor"],
    },
    {
        "id": "constantine",
        "label": "Constantine Hellblazer occult noir",
        "source": "Constantine",
        "weight": 0.68,
        "signature_terms": ["Hellblazer", "Constantine", "House of Mystery", "First of the Fallen", "Nergal", "Newcastle"],
        "roles": ["Hellblazer occult fixer", "Constantine-inspired trench coat exorcist", "House of Mystery archivist", "Newcastle survivor occultist", "demon debt collector", "angelic informant in a smoky bar"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["tan trench coat over black dress, loosened tie, boots", "smoky club coat, occult pin, dark stockings", "exorcist formal blouse, rolled sleeves, silver ring", "House of Mystery velvet robe coat, old keys at belt", "punk occult jacket, ripped hem, charm bracelets", "angelic informant suit dress, pale scarf, gold pin"],
        "environments": ["London occult alley, rain, old brick, neon pub sign", "House of Mystery library, impossible doors, candle stacks", "Newcastle basement ritual room, chalk marks, broken mirror", "Hellblazer smoky bar, red lamps, occult patrons", "church backroom, cigarettes, holy water, old files", "subway platform, demonic graffiti, green light"],
        "props": ["holy lighter, small flame, brass detail", "occult playing cards, sigil backs, worn edges", "exorcism cigarette case, scratched silver", "demon contract parchment, red wax seal", "House of Mystery keyring, impossible keys", "angel feather in glass vial, gold glow"],
        "factions": ["Hellblazer street occult identity, trench coat, cynical charm", "House of Mystery identity, impossible rooms, old books", "First of the Fallen hell faction mood, red contracts, black smoke", "Nergal demon debt mood, infected gold glow", "angelic bureaucracy mood, pale gold and cold judgement"],
        "creatures": ["demon silhouette in cigarette smoke", "angel wing shadow on wet brick", "imp-like face in old mirror", "hell portal glow behind door crack"],
        "architecture": ["London brick alleys, wet pavement, pub signs", "House of Mystery impossible staircase, book walls, candles", "old church vestry, peeling paint, holy icons", "subway tile corridor, green fluorescent light"],
        "magic": ["exorcism circle, chalk sigils, cigarette smoke", "demon contract magic, red wax, black letters", "angelic warding light, gold symbols, restrained glow", "portal doorway to hell, orange light kept background"],
        "lighting": ["rainy sodium streetlight, black coat shadows", "candle library glow, deep brown smoke", "red hell backlight, silhouette edge", "green subway fluorescent, noir tension"],
        "palettes": ["tan trench coat and dirty gold palette", "smoke grey and hell red palette", "candle amber and old book brown palette", "London rain blue and sodium orange palette"],
        "cinematic": ["occult noir portrait, cigarette smoke, sigils readable", "urban exorcist key visual, trench coat, wet street reflections", "hell contract scene, red light, practical magic"],
        "avoid": ["Winchester motel specifics unless fusion", "space war armor", "bright academy fantasy"],
    },
    {
        "id": "the_x_files",
        "label": "The X-Files FBI paranormal conspiracy",
        "source": "The X-Files",
        "weight": 0.66,
        "signature_terms": ["FBI basement office", "Mulder", "Scully", "Syndicate", "black oil", "Cigarette Smoking Man"],
        "roles": ["FBI paranormal investigator", "Scully-inspired forensic doctor", "Mulder-inspired conspiracy profiler", "Syndicate whistleblower", "alien abduction witness", "black oil case analyst"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["FBI black suit, white blouse, badge at belt", "forensic coat over dark skirt, blue evidence gloves", "trench coat over formal suit, flashlight in hand", "witness raincoat, hospital bracelet, tired eyes", "Syndicate formal black coat, cigarette smoke, red file", "field jacket, jeans, evidence satchel"],
        "environments": ["FBI basement office, I Want to Believe poster, file cabinets", "rainy forest abduction site, flashlight beams, fog", "government archive corridor, fluorescent lights, classified boxes", "desert black site fence, searchlights, night sky", "motel case room, photos pinned on wall", "autopsy room, steel table, cold blue light"],
        "props": ["FBI badge, clear tiny detail", "X-File folder, red classified stamp", "flashlight, sharp cone through fog", "black oil vial, glossy dark liquid", "alien implant chip, tiny metallic shard", "cassette recorder with witness tape"],
        "factions": ["FBI identity, formal suit, badge, restrained professionalism", "Syndicate conspiracy identity, black files, cigarette smoke", "alien colonist mystery mood, cold light, hidden technology", "lone gunmen hacker mood, cluttered equipment, monitors"],
        "creatures": ["grey alien silhouette behind frosted glass", "Flukeman-like sewer shadow, kept distant", "black oil ripple under skin suggested through vial only"],
        "architecture": ["FBI basement office, low ceiling, file cabinets", "government archive shelves, fluorescent lights", "desert black site concrete, fences, searchlights", "small-town motel room, investigation board, blinds"],
        "technology": ["classified tape recorder, analog waveform", "alien implant scanner, green medical display", "government surveillance monitors, grainy screens"],
        "lighting": ["flashlight beams through forest fog", "cold autopsy room blue, steel reflections", "fluorescent government hallway, sterile tension", "motel tungsten lamp against rainy window"],
        "palettes": ["FBI black suit and file-folder beige palette", "forest green and flashlight white palette", "cold autopsy blue and steel palette", "desert night black and searchlight yellow palette"],
        "cinematic": ["paranormal procedural framing, evidence readable, restrained tension", "conspiracy thriller portrait, file folders and flashlight", "alien mystery key visual, cold light, hidden threat"],
        "avoid": ["demon road hunter props", "wizard school robes", "mecha war logic"],
    },
    {
        "id": "buffy_the_vampire_slayer",
        "label": "Buffy the Vampire Slayer Sunnydale hellmouth",
        "source": "Buffy the Vampire Slayer",
        "weight": 0.64,
        "signature_terms": ["Sunnydale", "Hellmouth", "Watcher", "Slayer", "The Bronze", "Magic Box"],
        "roles": ["Sunnydale Slayer heroine", "Watcher-trained occult researcher", "Magic Box spell clerk", "The Bronze vampire hunter", "Initiative escapee", "Hellmouth guardian"],
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": ["stylish leather jacket over dress, stake tucked at belt", "Watcher library blouse, plaid skirt, boots", "Magic Box velvet top, occult jewelry, black stockings", "club outfit with practical jacket, tall boots", "Initiative tactical jacket, black pants, radio cable", "cemetery patrol coat, scarf, silver necklace"],
        "environments": ["Sunnydale cemetery, moonlit headstones, fresh dirt", "The Bronze nightclub, purple lights, brick walls", "Magic Box shop, shelves of herbs, candles, occult books", "Watcher library, wooden tables, old volumes", "Hellmouth basement portal, red glow, cracked floor", "Initiative underground corridor, white lab lights, metal doors"],
        "props": ["wooden stake, clear silhouette, polished grip", "Watcher diary, old leather and red ribbon", "crossbow, compact frame, bolts visible", "Magic Box spell ingredients, jars and labels", "Slayer scythe-like red blade, dramatic but readable", "holy water bottle, tiny cross charm"],
        "factions": ["Slayer identity, confident stance, stake and practical fashion", "Watcher Council identity, old books, formal restraint", "Scooby Gang mood, research table, friendship-coded props", "Initiative identity, sterile underground labs, tactical gear", "Hellmouth demon cult mood, red portal symbols"],
        "creatures": ["vampire silhouette with fangs in cemetery fog", "demon shadow behind club curtain", "hellhound-like claw marks near portal"],
        "architecture": ["Sunnydale cemetery iron gates, old crypts, moonlight", "The Bronze brick club interior, stage lights, crowd shadows", "Magic Box wooden shelves, jars, candle tables", "Watcher library balcony, old books and ladders"],
        "magic": ["spell circle on shop floor, candles and herbs", "Hellmouth portal glow, red cracks, controlled intensity", "Watcher protective sigils, chalk and old ink", "vampire dust effect, subtle ash particles"],
        "lighting": ["purple nightclub light, brick shadows", "cemetery moonlight, fog and blue edges", "warm Magic Box candlelight, herbal glass reflections", "red Hellmouth underlight, dramatic contrast"],
        "palettes": ["purple club and black leather palette", "cemetery blue and warm stake wood palette", "Magic Box amber and deep green palette", "Hellmouth red and charcoal palette"],
        "cinematic": ["supernatural action TV framing, stake readable, confident pose", "cemetery patrol key visual, moonlight and crypt depth", "occult shop portrait, herbs and candles, clear face focus"],
        "avoid": ["Winchester motel props unless fusion", "sci-fi starship corridors", "high fantasy castles"],
    },
]


SPECS += MORE_SPECS


COMPACT_SPECS = [
    ("lord_of_the_rings", "The Lord of the Rings Middle-earth ring quest", "The Lord of the Rings", ["Rivendell", "Rohan", "Gondor", "Moria", "Mordor", "Lothlorien"], ["Rivendell elven ranger noblewoman", "Rohan shieldmaiden queen", "Gondor royal exile princess", "Moria-forged armor lady", "Lothlorien river guardian", "Dunedain ranger huntress"], ["Lothlorien elven green cloak, leather corset armor, leaf clasp", "Rohan silver chainmail dress, fur shoulder mantle, sword belt", "Gondor white tower robe gown, embroidered hem, silver circlet", "black ranger armor, cloak hood lowered, practical straps"], ["Rivendell forest ruins, mossy stones, sunbeams through trees", "Minas Tirith white tower balcony, mountain wind, banners below", "Moria dwarf hall forge, golden fire, carved stone columns", "Lothlorien elven river city, arched bridges, silver leaves"], ["Anduril-inspired engraved longsword, clean blade reflection", "Lothlorien leaf-carved bow, silver string, quiver visible", "One Ring-like gold ring on chain, tiny gold highlight", "mithril-like chainmail texture, silver fine links"], ["Rivendell elven court identity, leaf ornaments, silver embroidery", "Rohan horse-lord identity, fur mantle, green-gold banner mood", "Gondor white tree identity, ivory cloth, silver symbols", "Mordor dark army mood, black metal, red ash glow"]),
    ("the_witcher", "The Witcher continent monster contract fantasy", "The Witcher", ["Kaer Morhen", "Aretuza", "Nilfgaard", "Skellige", "Temeria", "Toussaint"], ["Kaer Morhen-trained monster huntress", "Aretuza sorceress", "Nilfgaardian spy noblewoman", "Skellige shieldmaiden", "Temerian battlefield medic", "vampire court informant"], ["Witcher school leather armor, silver studs, potion belt", "Aretuza sorceress gown, black velvet, silver pendant", "Nilfgaardian black plate armor, gold sun motif, cloak", "Skellige fur mantle, chainmail dress, braided hair"], ["Kaer Morhen mountain keep, snow, wolf banners", "Aretuza academy tower, sea cliffs, moonlit windows", "Novigrad back alley, wet cobblestones, tavern lanterns", "Toussaint vampire manor, red roses, moonlit balcony"], ["silver monster-slayer sword, wolf medallion charm", "Witcher potion vials, colored glass, belt loops", "contract notice parchment, wax seal, monster sketch", "vampire hunting stake, silver cap, clean silhouette"], ["School of the Wolf identity, wolf medallion, practical leather", "Aretuza sorceress identity, elegant magic, academy polish", "Nilfgaard identity, black armor, gold sun banners", "Skellige identity, fur mantle, sea wind, carved runes"]),
    ("dragon_age", "Dragon Age Thedas political dark fantasy", "Dragon Age", ["Thedas", "Grey Wardens", "Inquisition", "Kirkwall", "Orlais", "Tevinter"], ["Grey Warden commander", "Inquisition spymaster", "Orlesian masked noblewoman", "Tevinter mage aristocrat", "Dalish elf keeper", "Kirkwall rogue duelist"], ["Grey Warden blue armor, griffon insignia, weathered cape", "Inquisition green-black coat, eye emblem, leather straps", "Orlesian masquerade gown, gold mask, feather trim", "Tevinter black robe armor, red-gold geometry"], ["Skyhold war room, banners, snowy mountains", "Kirkwall stone alley, chains, harsh light", "Orlais palace ballroom, masks, gold mirrors", "Tevinter magisterium hall, black marble, red magic"], ["Grey Warden griffon shield, steel rim", "Inquisition dagger, green hilt, spy detail", "lyrium vial, blue glow, belt pouch", "Orlesian mask, gold filigree, hand-held"], ["Grey Wardens identity, griffon heraldry, worn duty", "Inquisition identity, eye symbol, organized power", "Orlais court identity, masks, velvet, intrigue", "Tevinter magister identity, red-gold arrogance"]),
    ("elden_ring", "Elden Ring Lands Between shattered grace", "Elden Ring", ["Lands Between", "Erdtree", "Tarnished", "Raya Lucaria", "Caelid", "Volcano Manor"], ["Tarnished noble knight", "Raya Lucaria sorceress", "Golden Order paladin", "Volcano Manor assassin", "Caelid wanderer", "Carian princess knight"], ["Tarnished travel armor, ragged cloak, leather straps", "Raya Lucaria blue sorcerer robe, glintstone crown accent", "Golden Order white-gold armor dress, radiant trim", "Carian knight armor, silver plates, blue cape"], ["Lands Between cliff, Erdtree glowing in distance, golden haze", "Raya Lucaria academy library, blue crystals, moonlit books", "Caelid red swamp plain, scarlet sky, ruined towers", "Volcano Manor candlelit hall, red carpets, serpent statues"], ["Site of Grace golden spark, small guiding light", "glintstone staff, blue crystal headpiece", "rune-etched greatsword, worn hilt, heavy blade", "Erdtree medallion, gold leaf detail"], ["Tarnished identity, worn armor, grace light, exile mood", "Golden Order identity, white-gold symbols, radiant authority", "Raya Lucaria identity, blue glintstone, academy sorcery", "Volcano Manor identity, red-black aristocracy, serpent motifs"]),
    ("dark_souls", "Dark Souls Lordran dying fire fantasy", "Dark Souls", ["Lordran", "Firelink Shrine", "Anor Londo", "Bonfire", "Ashen One", "Catarina"], ["Firelink shrine keeper", "Anor Londo silver knight lady", "Catarina wandering knight", "abyss watcher huntress", "painted world exile", "bonfire pilgrim"], ["ashen travel armor, ragged cloak, ember cracks", "silver knight armor dress, plume, polished gauntlets", "Catarina-inspired round armor silhouette, worn cloth", "black abyss hunter coat, wolf emblem, tall boots"], ["Firelink Shrine ruins, bonfire glow, ash drifting", "Anor Londo cathedral steps, golden sunset", "painted world snow bridge, white fog", "catacomb corridor, skull candles, black stone"], ["coiled sword fragment, ember glow", "Estus flask, warm orange glass", "black knight sword, charred blade", "white soapstone mark, glowing runes"], ["Firelink pilgrim identity, ash cloth, ember faith", "Anor Londo silver knight identity, golden cathedral mood", "Abyss Watchers identity, wolf crest, black coat", "Catarina knight identity, rounded armor, humble courage"]),
    ("bloodborne", "Bloodborne Yharnam gothic hunter nightmare", "Bloodborne", ["Yharnam", "Hunter's Dream", "Cainhurst", "Old Blood", "Healing Church", "Byrgenwerth"], ["Yharnam hunter lady", "Cainhurst vileblood noblewoman", "Healing Church investigator", "Byrgenwerth scholar", "Hunter's Dream doll-like guide", "nightmare frontier survivor"], ["long hunter coat, high collar, layered belts", "Cainhurst white noble dress, silver armor pieces", "church hunter robe coat, black gloves, silver pendant", "Victorian blouse, leather corset, tall boots"], ["Yharnam gothic street, wet cobblestones, tall lamps", "Hunter's Dream garden, moonlit flowers, workshop", "Cainhurst snow castle hall, red carpet, silver light", "Healing Church cathedral, candles, towering arches"], ["trick weapon saw blade, folded silhouette", "hunter pistol, antique silver, gothic grip", "blood vial charm, red glass, leather strap", "messenger lantern, small pale glow"], ["Hunter identity, long coats, trick weapons, moonlit dread", "Healing Church identity, cathedral authority, old blood ritual", "Cainhurst Vileblood identity, snow castle, red nobility", "Byrgenwerth scholar mood, forbidden knowledge, lake fog"]),
    ("castlevania", "Castlevania vampire castle gothic action", "Castlevania", ["Dracula's Castle", "Belmont", "Alucard", "Wallachia", "Vampire Killer", "Carmilla"], ["Belmont vampire hunter", "Alucard-inspired dhampir noblewoman", "Carmilla court vampire", "Wallachian witch scholar", "castle chapel swordswoman", "night creature commander"], ["Belmont leather hunter armor, long coat, whip belt", "white dhampir coat dress, gold trim, black stockings", "red-black vampire court gown, jeweled choker", "gothic battle nun armor, silver cross motifs"], ["Dracula's Castle throne room, red windows, black stone", "castle clock tower, gears, moonlight", "Wallachian village at night, burning torches", "chapel hall, stained glass, candle rows"], ["Vampire Killer-inspired whip, coiled leather", "holy water flask, blue glass", "silver longsword, ornate guard", "crimson spellbook, bat clasp"], ["Belmont clan identity, leather armor, sacred weapons", "Dracula's court identity, black-red nobility, bat motifs", "Carmilla faction mood, vampire diplomacy, crimson elegance", "Wallachian rebel identity, torches, rough cloaks"]),
    ("the_legend_of_zelda", "The Legend of Zelda Hyrule open-air adventure", "The Legend of Zelda", ["Hyrule", "Sheikah", "Gerudo", "Zora", "Rito", "Triforce"], ["Hyrule wanderer princess", "Sheikah shrine scout", "Gerudo desert warrior queen", "Zora river guardian", "Rito sky messenger", "ancient tech researcher"], ["Hylian tunic dress, leather belt, travel boots", "Sheikah stealth bodysuit, blue glowing symbols, scarf", "Gerudo desert silks, gold ornaments, practical sandals", "Zora ceremonial robe, pearl trim, water-blue fabric"], ["Hyrule field at sunrise, ruins, wild grass, distant castle", "Sheikah shrine interior, blue ancient tech lines, stone platforms", "Gerudo desert bazaar, colorful tents, warm sunset", "Zora domain waterfall city, luminous blue water, stone arches"], ["Master Sword-inspired blue hilt blade, clean heroic glow", "Hylian Shield-inspired blue shield, gold emblem motif", "Sheikah Slate-like tablet, blue ancient interface", "Triforce pendant, gold triangle charm"], ["Hylian royal identity, blue cloth, gold triangle motif", "Sheikah identity, eye symbol mood, blue ancient tech", "Gerudo identity, desert gold, red fabric, warrior confidence", "Zora identity, water-blue elegance, pearl and fin motifs"]),
    ("pokemon", "Pokemon regional creature trainer adventure", "Pokemon", ["Pokemon Center", "Pokeball", "Pokedex", "Team Rocket", "gym badge", "Elite Four"], ["Pokemon trainer heroine", "Team Rocket stylish rival", "Professor lab assistant", "electric gym leader", "ghost-type trainer", "Champion challenger"], ["trainer jacket, fingerless gloves, shorts over black tights", "gym leader performance outfit, colored badge pins, sneakers", "Team Rocket-inspired black uniform, red accent, tall boots", "ghost-type gothic dress, ribbon choker, striped stockings"], ["Pokemon Center plaza, red roof, evening lamps", "regional gym arena, crowd lights, battle platform", "Professor lab, Pokeball shelves, starter posters", "haunted tower, purple candles, old wooden stairs"], ["Pokeball in hand, clean red-white sphere", "Pokedex device, small blue screen", "gym badge case, shiny badges, readable detail", "trainer backpack, potion bottle, map case"], ["Pokemon trainer identity, cap, backpack, Pokeball belt", "Team Rocket identity, black uniform, red emblem mood", "gym leader identity, badge motifs, arena spotlight", "Elite Four identity, dramatic cloak, polished arena presence"]),
    ("final_fantasy_vii", "Final Fantasy VII Midgar mako cyber fantasy", "Final Fantasy VII", ["Midgar", "Shinra", "SOLDIER", "Avalanche", "Mako", "Materia"], ["Avalanche eco-rebel", "Shinra executive agent", "SOLDIER-inspired swordswoman", "Midgar slum florist mage", "Turks-style investigator", "mako reactor saboteur"], ["black tactical skirt suit, red ribbon, gloves", "SOLDIER-style sleeveless armor, giant sword harness", "Shinra corporate coat, sharp shoulders, badge", "flower seller dress with combat boots, ribbon detail"], ["Midgar plate underside, green mako glow, pipes", "Sector 5 church, flowers, broken roof sunlight", "Shinra tower lobby, polished floors, blue screens", "mako reactor catwalk, green light, steam"], ["Materia orb bracelet, colored glass glow", "Buster Sword-inspired giant blade, readable silhouette", "Shinra ID badge, tiny logo mood", "Avalanche satchel, explosive warning tags"], ["Avalanche identity, eco-rebel gear, worn straps", "Shinra Electric Power identity, corporate polish, mako glow", "SOLDIER identity, elite armor, enormous blade", "Turks identity, black suits, sharp professionalism"]),
    ("nier_automata", "NieR Automata android ruins melancholy", "NieR Automata", ["YoRHa", "2B", "9S", "A2", "machine lifeforms", "Bunker"], ["YoRHa battle android", "scanner android archivist", "resistance camp operator", "A2-inspired deserter", "machine village observer", "Bunker command envoy"], ["black YoRHa dress, blindfold visor, white hair", "scanner coat, shorts over dark tights, utility pouch", "resistance camp cloak, worn straps, boots", "white tactical bodysuit, black skirt panel, gloves"], ["overgrown city ruins, white flowers, broken towers", "desert apartment complex, sand and machines", "amusement park ruins, faded lights, clown signs", "Bunker white command room, black space outside"], ["Virtuous Contract-like katana, clean black-white hilt", "Pod companion drone, small floating cube", "black visor blindfold, lace edge detail", "machine lifeform core, glowing yellow eye"], ["YoRHa identity, black-white uniforms, android elegance", "Resistance identity, patched camp gear, human memory", "Machine lifeform identity, yellow eyes, simple machine shapes kept background", "Bunker command identity, white minimal geometry"]),
]


def compact_spec(module_id, label, source, terms, roles, outfits, environments, props, factions):
    flavor = f"{label} {source}".lower()
    uses_magic = any(
        key in flavor
        for key in (
            "fantasy",
            "witch",
            "magic",
            "souls",
            "bloodborne",
            "castlevania",
            "zelda",
            "pokemon",
            "final fantasy",
            "dishonored",
            "demon",
            "occult",
            "vampire",
            "myth",
        )
    )
    uses_tech = any(
        key in flavor
        for key in (
            "sci-fi",
            "cyber",
            "space",
            "metal gear",
            "metro",
            "mad max",
            "alien",
            "predator",
            "bioshock",
            "half-life",
            "portal",
            "nier",
            "final fantasy vii",
            "pokemon",
            "gundam",
            "evangelion",
            "matrix",
            "stargate",
            "expanse",
            "doctor who",
            "starcraft",
        )
    )
    data = {
        "id": module_id,
        "label": label,
        "source": source,
        "signature_terms": list(terms),
        "roles": list(roles),
        "role_details": COMMON_ROLE_DETAILS,
        "outfits": list(outfits),
        "environments": list(environments),
        "props": list(props),
        "factions": list(factions),
        "architecture": [
            f"{terms[0]} architecture, setting-specific structure, readable background",
            f"{terms[1]} visual language, props and walls support the world",
            f"{terms[2]} landmark details, no generic random backdrop",
        ],
        "lighting": [
            f"{terms[0]} mood lighting, cinematic and coherent",
            f"{terms[1]} accent light, controlled contrast",
            f"{terms[2]} atmospheric rim light, clean silhouette",
            "balanced face light, background depth",
        ],
        "palettes": [
            f"{terms[0]} inspired palette, varied but coherent",
            f"{terms[1]} accent palette, strong focal colors",
            f"{terms[2]} environmental palette, no repeated cyan default",
            "balanced cinematic palette, skin tones preserved",
        ],
        "cinematic": [
            f"{label} key visual, world terms visible, readable outfit",
            f"{source} inspired composition, specific props and architecture",
            "cinematic portrait framing, clear face focus, no world collision",
        ],
        "avoid": ["random franchise collision", "unrelated generic equipment", "unrelated architecture"],
    }
    if uses_tech:
        data["technology"] = [
            f"{terms[0]} equipment language, functional readable details",
            f"{terms[1]} interface or craft details, restrained glow",
            f"{terms[2]} artifact detail, small but recognizable",
        ]
    if uses_magic:
        data["magic"] = [
            f"{terms[0]} supernatural logic, controlled effect size",
            f"{terms[1]} symbolic power detail, readable hand pose",
            f"{terms[2]} ritual or energy motif, face not obscured",
        ]
    return data


SPECS += [compact_spec(*item) for item in COMPACT_SPECS]


EXTRA_COMPACT_SPECS = [
    ("metal_gear_solid", "Metal Gear Solid tactical espionage action", "Metal Gear Solid", ["FOXHOUND", "Shadow Moses", "Outer Heaven", "Metal Gear", "codec", "Cypher"], ["FOXHOUND infiltrator", "Shadow Moses tactical spy", "Outer Heaven defector", "cyborg ninja observer", "Diamond Dogs sniper", "codec intelligence handler"], ["sneaking suit, harness, tactical gloves", "black bodysuit with armor panels, thigh holster", "winter infiltration jacket, stealth hood, boots", "military dress coat, patches, gloves"], ["Shadow Moses snow base, searchlights, hangars", "Outer Heaven jungle compound, rain, fences", "Metal Gear hangar, massive railgun silhouette", "codec command room, green screens, dim lamps"], ["SOCOM pistol, suppressor, readable grip", "cardboard box disguise prop, subtle background joke", "codec earpiece, tiny light", "stealth camo module, faint shimmer"], ["FOXHOUND identity, tactical stealth gear, codec mood", "Outer Heaven identity, military patches, rogue soldier atmosphere", "Diamond Dogs identity, worn field gear, private army markings", "Patriots conspiracy mood, clean files, hidden control"]),
    ("metro", "Metro post-nuclear tunnel survival", "Metro", ["Moscow Metro", "Spartan Rangers", "D6", "Hansa", "Red Line", "Dark Ones"], ["Spartan Ranger scout", "Moscow Metro station medic", "Hansa tunnel guard", "Red Line deserter", "D6 bunker explorer", "surface gas mask scavenger"], ["patched ranger armor, gas mask at neck, ammo pouches", "metro station coat, scarf, practical boots", "tunnel guard armor, helmet lamp, canvas straps", "surface winter suit, cracked visor, heavy gloves"], ["Moscow Metro platform settlement, lanterns, bunks", "D6 bunker corridor, blast doors, green lights", "surface Moscow ruins, snow, radiation haze", "dark tunnel checkpoint, red lamps, rails"], ["gas mask with cracked lens, readable straps", "pneumatic rifle, brass pressure gauge", "metro ticket charm, small paper tag", "military flashlight, chest harness"], ["Spartan Rangers identity, gas masks, rugged armor", "Hansa identity, checkpoint order, trade station lamps", "Red Line identity, red banners, tunnel authority", "D6 military bunker identity, sealed doors, old tech"]),
    ("mad_max", "Mad Max wasteland road war", "Mad Max", ["Wasteland", "War Rig", "Immortan", "Citadel", "V8", "Bullet Farm"], ["War Rig road warrior", "Citadel rebel driver", "Bullet Farm sharpshooter", "desert tanker mechanic", "V8 cult escapee", "wasteland biker queen"], ["dusty leather harness, canvas wraps, heavy boots", "white desert cloth over armor pieces, goggles", "mechanic tank top, tool belt, scarf, knee pads", "black road armor, shoulder pads, fingerless gloves"], ["desert highway convoy, dust wall, spiked vehicles", "Citadel cliff fortress, water pipes, sun glare", "Bullet Farm yard, rusted ammo crates, fires", "night dune camp, engines, blue moon"], ["sawed-off shotgun, leather sling", "steering wheel talisman, chrome skull detail", "gasoline can, warning paint", "flare gun, red smoke"], ["Citadel rebel identity, desert cloth, survival fury", "War Boys cult mood, chrome ritual, V8 symbols", "Bullet Farm identity, ammo belts, rusty weapons", "road warrior identity, leather, dust, engines"]),
    ("alien", "Alien Weyland-Yutani industrial xenomorph horror", "Alien", ["Weyland-Yutani", "Nostromo", "LV-426", "xenomorph", "M56 smartgun", "synthetic"], ["Weyland-Yutani corporate survivor", "Nostromo warrant officer", "Colonial Marines technician", "LV-426 colony engineer", "synthetic science officer", "dropship crew chief"], ["blue-grey flight jumpsuit, patches, rolled sleeves", "Colonial Marines armor vest, shoulder lamp, boots", "corporate black blazer, Weyland-Yutani badge mood", "industrial engineer harness, tool belt, gloves"], ["Nostromo corridor, wet chains, yellow lights", "LV-426 colony hallway, rain, emergency strobes", "Sulaco dropship bay, military crates, blue light", "Weyland-Yutani lab, glass tanks, cold white glow"], ["motion tracker, green radar screen", "M56 smartgun-like rig, heavy harness", "flamethrower, orange pilot light", "synthetic milk-white tool case"], ["Weyland-Yutani identity, corporate greed, sterile menace", "Colonial Marines identity, practical armor, patches", "Nostromo crew identity, industrial worker gear, tired realism", "synthetic identity, clean uniform, ambiguous calm"]),
    ("predator", "Predator jungle hunt thermal alien warrior", "Predator", ["Yautja", "jungle hunt", "thermal vision", "plasma caster", "Predator mask", "trophy wall"], ["jungle special forces scout", "Yautja-tech survivor", "trophy hunter archaeologist", "thermal tracking expert", "rainforest commando", "alien ritual witness"], ["jungle tactical vest, mud streaks, bandana", "torn field shirt, ammo straps, boots", "Yautja-tech cloak fragments, bone trophies", "thermal visor harness, camo pants, gloves"], ["Central American jungle, rain, heat haze", "Yautja trophy chamber, bones, alien metal", "muddy riverbank, laser dots through leaves", "abandoned guerrilla camp, smoke, vines"], ["plasma caster shoulder device, blue targeting dots", "Predator mask held at side, metal dreadlock beads", "thermal scanner tablet, red-yellow display", "jungle machete, worn grip"], ["Yautja hunter identity, trophy tech, honor ritual mood", "special forces identity, jungle gear, survival tension", "alien hunt identity, thermal vision, red laser dots", "trophy wall identity, bone ornaments, dark metal"]),
    ("bioshock", "BioShock Rapture art deco undersea dystopia", "BioShock", ["Rapture", "Andrew Ryan", "Big Daddy", "ADAM", "Plasmid", "Ryan Industries"], ["Rapture lounge singer", "plasmid scientist", "art deco smuggler", "Big Daddy repair engineer", "Atlas resistance messenger", "Ryan Industries executive"], ["art deco evening dress, pearl necklace, gloves", "lab coat over satin dress, ADAM vial belt", "diving engineer suit pieces, brass helmet nearby", "smuggler trench coat, stockings, pistol holster"], ["Rapture glass tunnel, ocean outside, neon signs", "Kashmir restaurant ruin, art deco lights, water leaks", "Ryan Industries office, brass and marble, propaganda posters", "medical pavilion, flickering signs, tiled floor"], ["Plasmid syringe, blue-red liquid", "ADAM vial, glowing red glass", "wrench, brass handle, readable tool", "old radio, Atlas voice mood"], ["Ryan Industries identity, art deco capitalism, brass luxury", "Atlas resistance identity, smuggler gear, hidden messages", "Big Daddy engineering identity, brass diving armor mood", "Rapture citizen identity, glamour decayed by water"]),
    ("dishonored", "Dishonored Dunwall whale-oil occult plague", "Dishonored", ["Dunwall", "Karnaca", "Outsider", "whale oil", "Abbey", "Clockwork Soldier"], ["Dunwall masked assassin", "Karnaca aristocrat spy", "Abbey overseer defector", "whale-oil engineer", "Outsider-marked witch", "Empress court bodyguard"], ["dark assassin coat, folding mask at hip", "Karnaca silk dress, leather corset, boots", "Abbey grey coat, silver charm, gloves", "engineer apron over blouse, whale-oil canisters"], ["Dunwall rooftop, plague posters, whale-oil lamps", "Karnaca balcony, warm sea light, tiled walls", "Boyle masquerade hall, masks, chandeliers", "Clockwork Mansion room, shifting walls, brass machinery"], ["folding assassin blade, clear wrist mechanism", "Outsider bone charm, carved ivory", "whale-oil tank, blue glow", "clockwork soldier mask, brass detail"], ["Loyalist conspiracy identity, masks, rooftop stealth", "Abbey of the Everyman identity, grey uniforms, zealotry", "Outsider occult identity, black eyes motif avoided, void symbols", "Karnaca aristocracy identity, silk and sunlit stone"]),
    ("half_life", "Half-Life Black Mesa Combine resistance", "Half-Life", ["Black Mesa", "City 17", "Combine", "HEV suit", "Alyx", "Gravity Gun"], ["Black Mesa scientist survivor", "City 17 resistance fighter", "Combine civil protection defector", "HEV suit explorer", "Alyx-inspired hacker mechanic", "Vortigaunt ally witness"], ["orange HEV-inspired suit pieces, black undersuit", "resistance jacket, messenger bag, fingerless gloves", "Combine-style grey tactical coat, visor raised", "lab coat over practical clothes, ID badge"], ["Black Mesa test chamber, orange hazard lights", "City 17 plaza, Combine tower, concrete", "Ravenholm street, traps, dark roofs", "resistance lab, cables, monitors, gravity tool bench"], ["Gravity Gun-like orange device, readable prongs", "crowbar, red metal, iconic prop", "Black Mesa ID badge, small detail", "Combine scanner drone, blue eye"], ["Black Mesa identity, research lab, hazard suits", "City 17 resistance identity, patched jackets, urban rebellion", "Combine identity, grey armor, surveillance tech", "Lambda resistance identity, orange symbol mood"]),
    ("portal", "Portal Aperture test chamber sci-fi puzzle", "Portal", ["Aperture Science", "GLaDOS", "test chamber", "portal gun", "Companion Cube", "Turret"], ["Aperture test subject", "GLaDOS facility technician", "portal puzzle runner", "companion cube courier", "turret maintenance engineer", "old Aperture researcher"], ["orange test jumpsuit, white tank layer, long-fall boots", "white lab coat, Aperture badge, black gloves", "facility technician suit, utility belt, knee pads", "retro Aperture dress, blue-orange accents"], ["Aperture test chamber, white panels, glass observation room", "old Aperture underground lab, yellowed signs, pipes", "turret production line, red lasers, clean floor", "relaxation vault, sterile walls, portal glow"], ["portal gun, clean white shell, blue-orange glow", "Companion Cube, heart logo, scuffed edges", "turret shell, red eye, small scale", "Aperture clipboard, test notes"], ["Aperture Science identity, clean panels, test signage", "GLaDOS facility identity, sterile menace, camera eyes", "old Aperture identity, retro signs, yellow tile, cave echoes", "test subject identity, orange jumpsuit, puzzle survival"]),
]


SPECS += [compact_spec(*item) for item in EXTRA_COMPACT_SPECS]


WIDE_LENSES = [
    ("core", "core identity", "iconic lead", "signature outfit", "primary location", "signature prop"),
    ("factions", "faction conflict", "faction agent", "faction uniform", "conflict zone", "faction artifact"),
    ("landmarks", "landmark setpiece", "scene lead", "setpiece outfit", "landmark scene", "setpiece object"),
]


def build_wide_spec(row, lens):
    module_id, source, terms, vibe = row
    lens_id, lens_label, role_kind, outfit_kind, env_kind, prop_kind = lens
    focus = list(terms)
    label = f"{source} {lens_label} {vibe}"
    data = {
        "id": f"{module_id}_{lens_id}",
        "label": label,
        "source": source,
        "weight": 0.42,
        "signature_terms": focus,
        "roles": [
            f"{source} {role_kind}, {focus[0]} identity, mature woman design",
            f"{focus[1]} specialist, confident expression, readable silhouette",
            f"{focus[2]} operative, cinematic posture, clear face focus",
            f"{focus[3]} wanderer, world-specific styling, hands readable",
            f"{focus[4]} envoy, calm authority, detailed costume logic",
            f"{focus[5]} rogue, dramatic presence, setting-specific details",
        ],
        "outfits": [
            f"{source} inspired {outfit_kind}, {focus[0]} motifs, practical boots",
            f"{focus[1]} styled coat, layered fabric, emblem details",
            f"{focus[2]} field outfit, readable straps, gloves, utility belt",
            f"{focus[3]} ceremonial look, jewelry and trim matching the world",
            f"{focus[4]} travel gear, worn materials, coherent silhouette",
            f"{focus[5]} elite uniform, polished accents, no generic costume clash",
        ],
        "environments": [
            f"{source} {env_kind}, {focus[0]} setting, cinematic depth",
            f"{focus[1]} corridor or street, architecture specific to {source}",
            f"{focus[2]} stronghold, banners or signage visible",
            f"{focus[3]} ruins or command room, props support the world",
            f"{focus[4]} exterior vista, atmosphere and landscape match",
            f"{focus[5]} hidden chamber, readable set dressing",
        ],
        "props": [
            f"{focus[0]} {prop_kind}, held clearly, readable silhouette",
            f"{focus[1]} emblem or badge, small but visible",
            f"{focus[2]} weapon or tool, functional design, no random crossover",
            f"{focus[3]} artifact, glowing detail kept controlled",
            f"{focus[4]} map, token, or device, world-specific markings",
            f"{focus[5]} relic, trophy, or interface, clean focal detail",
        ],
        "factions": [
            f"{focus[0]} identity, costume and props reinforce {source}",
            f"{focus[1]} faction mood, colors and symbols stay coherent",
            f"{focus[2]} organization logic, equipment fits the world",
            f"{focus[3]} rival identity, set dressing supports conflict",
            f"{focus[4]} cultural styling, architecture and clothing match",
            f"{focus[5]} hidden faction clue, subtle but recognizable",
        ],
        "creatures": [
            f"{source} setting-specific creature, entity, vehicle, or companion silhouette tied to {focus[0]}",
            f"{focus[1]} background threat or ally, subtle and readable",
            f"{focus[2]} symbolic entity detail, kept behind the main character",
        ],
        "architecture": [
            f"{focus[0]} architecture, recognizable silhouette and materials",
            f"{focus[1]} set design, doors, walls, signage, and props match",
            f"{focus[2]} landmark geometry, no unrelated backdrop",
            f"{source} visual identity in the background, readable but not cluttered",
        ],
        "lighting_mood": [
            f"{source} cinematic lighting, {focus[0]} mood, clean face light",
            f"{focus[1]} accent light, controlled contrast",
            f"{focus[2]} atmosphere, depth layers, readable silhouette",
            f"{vibe} mood lighting, setting-specific color logic",
        ],
        "color_palettes": [
            f"{focus[0]} inspired palette, varied and coherent",
            f"{focus[1]} accent palette, strong focal colors",
            f"{focus[2]} environmental palette, avoids repeated cyan default",
            f"{source} color identity, balanced skin tones, cinematic finish",
        ],
        "cinematic_language": [
            f"{source} key visual, {lens_label}, world terms visible",
            f"{vibe} composition, specific props and architecture",
            f"cinematic portrait framing, clear face focus, no world collision",
        ],
        "prompt_modifiers": [
            f"world details stay {source} themed",
            f"{', '.join(focus[:6])} remain dominant and recognizable",
            "generic pools may add pose, camera, expression, framing, and mild atmosphere only",
            "do not mix in unrelated franchise world logic unless fusion mode is active",
        ],
    }
    flavor = f"{source} {vibe} {' '.join(focus)}".lower()
    tech_keys = (
        "sci-fi",
        "cyber",
        "space",
        "robot",
        "mecha",
        "machine",
        "station",
        "surveillance",
        "hacker",
        "simulation",
        "post-apocalyptic",
        "military",
        "spy",
        "tech",
        "future",
        "nanosuit",
        "android",
        "digital",
        "cyborg",
        "orbital",
    )
    magic_keys = (
        "fantasy",
        "magic",
        "occult",
        "supernatural",
        "vampire",
        "gothic",
        "myth",
        "curse",
        "witch",
        "demon",
        "spirit",
        "cosmic",
        "fairy",
        "alchemy",
        "dragon",
        "underworld",
    )
    if any(key in flavor for key in tech_keys):
        data["technology"] = [
            f"{focus[0]} equipment language, functional readable details",
            f"{focus[1]} interface, insignia, or mechanism, restrained glow",
            f"{focus[2]} tool design, materials match {source}",
        ]
    if any(key in flavor for key in magic_keys):
        data["magic_system"] = [
            f"{focus[0]} power logic, controlled effect size",
            f"{focus[1]} symbol or ritual motif, readable hand pose",
            f"{focus[2]} energy or curse detail, face not obscured",
        ]
    return data


WIDE_FRANCHISE_ROWS = [
    ("stargate", "Stargate", ["Stargate", "SG-1", "Goa'uld", "Jaffa", "Atlantis", "Wraith"], "ancient portal military sci-fi"),
    ("the_expanse", "The Expanse", ["Rocinante", "OPA", "Belter", "Mars Congressional Republic", "Protomolecule", "Ceres Station"], "hard sci-fi political survival"),
    ("doctor_who", "Doctor Who", ["TARDIS", "Time Lord", "Dalek", "Cyberman", "Gallifrey", "Sonic Screwdriver"], "time travel cosmic adventure"),
    ("firefly", "Firefly", ["Serenity", "Browncoats", "Alliance", "Reavers", "Ariel", "Persephone"], "space western frontier"),
    ("farscape", "Farscape", ["Moya", "Peacekeepers", "Scarrans", "Leviathan ship", "Hynerian court", "wormhole tech"], "alien fugitive space opera"),
    ("babylon_5", "Babylon 5", ["Babylon 5 station", "Minbari", "Narn", "Centauri", "Vorlon", "Shadow War"], "diplomatic station space opera"),
    ("andor", "Andor", ["Ferrix", "ISB", "Mon Mothma network", "Aldhani", "Narkina 5", "Luthen gallery"], "rebel spy thriller"),
    ("the_mandalorian", "The Mandalorian", ["Mandalore", "Beskar", "Darksaber", "Nevarro", "Mudhorn signet", "Armorer forge"], "bounty hunter frontier space opera"),
    ("rogue_one", "Rogue One", ["Scarif", "Death Star plans", "Jedha", "Rebel intelligence", "Krennic security", "Kyber temple"], "doomed rebellion war story"),
    ("clone_wars", "Clone Wars", ["Republic cruiser", "Separatist droids", "Mandalore siege", "Coruscant underworld", "Jedi Temple", "Kamino"], "animated galactic war"),
    ("the_matrix", "The Matrix", ["Matrix code", "Nebuchadnezzar", "Agents", "Zion", "red pill", "sentinel machines"], "simulation cyber rebellion"),
    ("terminator", "Terminator", ["Skynet", "T-800", "Resistance", "Judgment Day", "Cyberdyne", "time displacement"], "machine apocalypse action"),
    ("robocop", "RoboCop", ["OCP", "Detroit Metro West", "ED-209", "Prime Directives", "Old Detroit", "cyborg officer"], "corporate cyber police dystopia"),
    ("tron", "TRON", ["Grid", "CLU", "light cycle", "Identity Disc", "ENCOM", "Recognizers"], "digital neon arena adventure"),
    ("total_recall", "Total Recall", ["Rekall", "Mars colony", "Kuato", "Cohaagen", "mutant resistance", "memory implant"], "memory conspiracy sci-fi"),
    ("minority_report", "Minority Report", ["PreCrime", "precog vision", "spider scanners", "Washington future", "halo device", "predictive crime"], "predictive surveillance noir"),
    ("westworld", "Westworld", ["Delos", "host awakening", "Mesa Hub", "Westworld park", "Rehoboam", "black hat"], "android western mystery"),
    ("black_mirror", "Black Mirror", ["Nosedive rating", "San Junipero", "USS Callister", "White Bear", "cookie tech", "memory grain"], "near-future social tech horror"),
    ("altered_carbon", "Altered Carbon", ["stacks", "sleeves", "Meths", "Bay City", "Envoy", "Raven Hotel"], "body-swapping cyber noir"),
    ("severance", "Severance", ["Lumon", "MDR office", "severed floor", "waffle party", "Eagan shrine", "Perpetuity Wing"], "corporate liminal psychological sci-fi"),
    ("dark", "Dark", ["Winden", "Sic Mundus", "time cave", "Triquetra", "Noah", "apocalypse loop"], "time loop mystery"),
    ("twin_peaks", "Twin Peaks", ["Black Lodge", "Red Room", "Blue Rose", "Great Northern", "Laura Palmer case", "Owl Cave"], "surreal small-town mystery"),
    ("true_detective", "True Detective", ["Carcosa", "Yellow King", "Louisiana bayou", "Lone Star case", "Rust Cohle board", "occult crime scene"], "ritual crime noir"),
    ("hannibal", "Hannibal", ["Baltimore State Hospital", "Will Graham visions", "Lecter dinner", "Ravenstag", "FBI profiler", "Florence chapel"], "baroque forensic thriller"),
    ("peaky_blinders", "Peaky Blinders", ["Birmingham", "Shelby Company", "Garrison pub", "Small Heath", "racecourse deal", "flat cap razor"], "gangland period noir"),
    ("sherlock", "Sherlock", ["Baker Street", "Moriarty network", "Mind Palace", "Scotland Yard", "221B", "deduction board"], "modern detective mystery"),
    ("the_sandman", "The Sandman", ["Dreaming", "Morpheus", "Corinthian", "Endless", "Lucienne library", "ruby dreamstone"], "mythic dream fantasy"),
    ("good_omens", "Good Omens", ["Aziraphale bookshop", "Crowley Bentley", "Ineffable Plan", "Heaven office", "Hell bureaucracy", "flaming sword"], "angel demon comedy fantasy"),
    ("american_gods", "American Gods", ["House on the Rock", "Mr Wednesday", "New Gods", "Old Gods", "Lakeside", "storm coin"], "mythic roadside Americana"),
    ("lovecraft_country", "Lovecraft Country", ["Ardham Lodge", "Sons of Adam", "Book of Names", "shoggoth", "Chicago magic", "ancestral spell"], "occult historical horror"),
    ("the_walking_dead", "The Walking Dead", ["Alexandria", "Hilltop", "Saviors", "Whisperers", "Commonwealth", "walkers"], "survivor community apocalypse"),
    ("game_of_thrones", "Game of Thrones", ["Winterfell", "King's Landing", "Targaryen", "Stark", "Lannister", "Iron Throne"], "political medieval fantasy"),
    ("house_of_the_dragon", "House of the Dragon", ["Dragonstone", "King's Landing", "Targaryen court", "Hightower faction", "Black Council", "dragonpit"], "dragon dynasty court intrigue"),
    ("wheel_of_time", "The Wheel of Time", ["Aes Sedai", "White Tower", "Ajah", "Two Rivers", "Seanchan", "One Power"], "prophecy magic epic fantasy"),
    ("shadow_and_bone", "Shadow and Bone", ["Grisha", "Ravka", "Shadow Fold", "Ketterdam", "Crow Club", "Small Science"], "tsarpunk magic heist fantasy"),
    ("rings_of_power", "Rings of Power", ["Numenor", "Lindon", "Eregion", "Khazad-dum", "Mordor", "Southlands"], "second age high fantasy"),
    ("mistborn", "Mistborn", ["Luthadel", "Allomancy", "Steel Inquisitor", "Mistborn cloak", "Lord Ruler", "metal vials"], "metal magic rebellion fantasy"),
    ("stormlight_archive", "Stormlight Archive", ["Roshar", "Knights Radiant", "Shardblade", "Stormlight", "Alethi warcamp", "Urithiru"], "storm epic fantasy"),
    ("malazan", "Malazan Book of the Fallen", ["Malazan Empire", "Bridgeburners", "Warrens", "Tiste Andii", "Moon's Spawn", "Deck of Dragons"], "military epic dark fantasy"),
    ("discworld", "Discworld", ["Ankh-Morpork", "Unseen University", "Night Watch", "Witches of Lancre", "Death's domain", "Assassins Guild"], "satirical fantasy city"),
    ("earthsea", "Earthsea", ["Roke", "true names", "Archipelago", "Atuan tombs", "dragon speech", "Gont"], "island wizard myth fantasy"),
    ("the_dark_tower", "The Dark Tower", ["Gilead", "Mid-World", "gunslinger", "Ka-tet", "Crimson King", "rose field"], "weird western dark fantasy"),
    ("conan", "Conan", ["Cimmeria", "Aquilonia", "Stygia", "Tower of the Elephant", "Set cult", "Hyborian Age"], "sword and sorcery pulp"),
    ("red_sonja", "Red Sonja", ["Hyrkania", "Zamora", "Kulan Gath", "she-devil sword", "mercenary queen", "blood oath"], "sword and sorcery heroine"),
    ("elric", "Elric of Melnibone", ["Melnibone", "Stormbringer", "Chaos Lords", "Dreaming City", "White Wolf", "Tanelorn"], "decadent dark fantasy"),
    ("warhammer_fantasy", "Warhammer Fantasy", ["Empire of Man", "Witch Hunters", "Chaos Warriors", "Kislev", "Lustria", "Skaven undercity"], "grim fantasy war"),
    ("magic_the_gathering", "Magic The Gathering", ["Ravnica", "Innistrad", "Zendikar", "Phyrexia", "Planeswalker", "Eldrazi"], "multiverse planeswalker fantasy"),
    ("dungeons_and_dragons", "Dungeons and Dragons", ["Forgotten Realms", "Waterdeep", "Baldur's Gate", "Underdark", "Dragonlance", "Beholder"], "tabletop heroic fantasy"),
    ("forgotten_realms", "Forgotten Realms", ["Waterdeep", "Baldur's Gate", "Neverwinter", "Underdark", "Zhentarim", "Harpers"], "classic fantasy city intrigue"),
    ("ravenloft", "Ravenloft", ["Barovia", "Castle Ravenloft", "Strahd", "Vistani", "Mists", "Amber Temple"], "gothic vampire domain"),
    ("planescape", "Planescape", ["Sigil", "Lady of Pain", "Factions", "Outlands", "portal keys", "Lower Planes"], "planar city fantasy"),
    ("eberron", "Eberron", ["Sharn", "Dragonmarked Houses", "Warforged", "Lightning Rail", "Mournland", "Khorvaire"], "magepunk noir fantasy"),
    ("pathfinder", "Pathfinder", ["Golarion", "Absalom", "Pathfinder Society", "Cheliax", "Numeria", "Runelords"], "adventure guild fantasy"),
    ("shadowrun", "Shadowrun", ["Seattle sprawl", "megacorp", "Awakened magic", "Matrix decker", "street samurai", "dragon CEO"], "cyberpunk urban fantasy"),
    ("cyberpunk_red", "Cyberpunk RED", ["Night City", "Edgerunners", "Trauma Team", "Nomad packs", "Netrunner", "Rockerboy"], "tabletop cyberpunk chaos"),
    ("vampire_masquerade", "Vampire: The Masquerade", ["Camarilla", "Anarchs", "Sabbat", "Toreador", "Nosferatu", "Elysium"], "vampire political gothic"),
    ("world_of_darkness", "World of Darkness", ["Mage Ascension", "Werewolf Apocalypse", "Changeling Dreaming", "Wraith Oblivion", "Technocracy", "Umbra"], "urban supernatural conspiracy"),
    ("call_of_cthulhu", "Call of Cthulhu", ["Miskatonic University", "Arkham", "Necronomicon", "Deep Ones", "Elder Signs", "R'lyeh"], "cosmic investigation horror"),
    ("delta_green", "Delta Green", ["Delta Green cell", "MAJESTIC", "Night Floors", "King in Yellow", "unnatural threat", "burner identity"], "government cosmic horror"),
    ("scp_foundation", "SCP Foundation", ["SCP Foundation", "Site-19", "MTF squad", "Euclid anomaly", "containment breach", "Class-D files"], "anomaly containment horror"),
    ("control", "Control", ["Federal Bureau of Control", "Oldest House", "Hiss", "Service Weapon", "Astral Plane", "Objects of Power"], "paranatural brutalist mystery"),
    ("alan_wake", "Alan Wake", ["Bright Falls", "Dark Place", "Taken", "Clicker", "Cauldron Lake", "Writer's Room"], "writerly shadow horror"),
    ("quantum_break", "Quantum Break", ["Monarch Solutions", "time fracture", "chronon field", "End of Time", "Riverport", "time stutter"], "time fracture action sci-fi"),
    ("death_stranding", "Death Stranding", ["Bridges", "BTs", "Chiral Network", "Timefall", "Porter suit", "BB pod"], "lonely post-collapse courier sci-fi"),
    ("horizon_zero_dawn", "Horizon Zero Dawn", ["Nora", "Carja", "Aloy-style hunter", "Focus device", "Tallneck", "Thunderjaw"], "machine wilderness tribal sci-fi"),
    ("ghost_of_tsushima", "Ghost of Tsushima", ["Tsushima", "Sakai clan", "Mongol invasion", "Ghost stance", "Kurosawa wind", "Golden Temple"], "samurai island war drama"),
    ("sekiro", "Sekiro", ["Ashina", "Wolf prosthetic", "Divine Heir", "Senpou Temple", "Fountainhead Palace", "Shinobi arts"], "shinobi mythic action"),
    ("monster_hunter", "Monster Hunter", ["Hunter's Guild", "Rathalos", "Rathian", "Zinogre", "Palico", "Ancient Forest"], "monster hunt expedition fantasy"),
    ("armored_core", "Armored Core", ["Armored Core", "Raven", "Rubicon", "Coral", "Arquebus", "Balam"], "mecha mercenary war"),
    ("titanfall", "Titanfall", ["Frontier Militia", "IMC", "Titan chassis", "Pilot jump kit", "BT-7274", "Angel City"], "mech pilot frontier sci-fi"),
    ("destiny", "Destiny", ["Guardians", "Traveler", "Ghost shell", "Vanguard", "Hive", "Awoken Reef"], "space magic looter myth"),
    ("overwatch", "Overwatch", ["Overwatch", "Talon", "Omnic Crisis", "Numbani", "King's Row", "Watchpoint Gibraltar"], "hero shooter global sci-fi"),
    ("valorant", "Valorant", ["Radiants", "Kingdom Corporation", "Spike", "Protocol", "Ascent", "Bind"], "tactical radiant near-future"),
    ("league_of_legends", "League of Legends", ["Runeterra", "Piltover", "Zaun", "Noxus", "Demacia", "Ionia"], "champion fantasy conflict"),
    ("arcane", "Arcane", ["Piltover", "Zaun", "Hextech", "Chembarons", "Undercity", "Council chamber"], "hextech class-war fantasy"),
    ("starcraft", "StarCraft", ["Terran Dominion", "Zerg Swarm", "Protoss", "Koprulu sector", "Ghost operative", "Xel'Naga"], "military sci-fi alien war"),
    ("warcraft", "Warcraft", ["Stormwind", "Orgrimmar", "Lordaeron", "Night Elves", "Burning Legion", "Kirin Tor"], "high fantasy faction war"),
    ("diablo", "Diablo", ["Sanctuary", "Horadrim", "Tristram", "High Heavens", "Burning Hells", "Nephalem"], "dark gothic loot fantasy"),
    ("doom", "DOOM", ["UAC", "Mars base", "Hell portal", "Argent energy", "Praetor suit", "BFG"], "demonic industrial shooter"),
    ("quake", "Quake", ["Slipgate", "Strogg", "Shub-Niggurath", "Rune portals", "Elder World", "gothic arena"], "gothic arena sci-fi horror"),
    ("wolfenstein", "Wolfenstein", ["Kreisau Circle", "Deathshead tech", "Nazi war machine", "Da'at Yichud", "Venus base", "Panzerhund"], "alternate history resistance action"),
    ("borderlands", "Borderlands", ["Pandora", "Vault Hunters", "Hyperion", "Crimson Raiders", "Eridian Vault", "Maliwan"], "loot wasteland neon chaos"),
    ("stalker", "S.T.A.L.K.E.R.", ["Zone", "Monolith", "Strelok", "anomaly field", "artifact detector", "Pripyat"], "radioactive exclusion zone survival"),
    ("crysis", "Crysis", ["Nanosuit", "CELL", "Ceph", "Lingshan Islands", "New York quarantine", "Tactical visor"], "nanosuit alien war"),
    ("far_cry", "Far Cry", ["Rook Islands", "Kyrat", "Hope County", "Eden's Gate", "Yara", "guerrilla camp"], "wildland militia survival"),
    ("watch_dogs", "Watch Dogs", ["ctOS", "DedSec", "Blume Corporation", "Chicago hack", "San Francisco hackerspace", "profiler UI"], "hacktivist surveillance thriller"),
    ("mirrors_edge", "Mirror's Edge", ["City of Glass", "Runners", "KrugerSec", "Cascadia", "red route marker", "Faith-style parkour"], "clean parkour dystopia"),
    ("deus_ex", "Deus Ex", ["UNATCO", "Majestic 12", "Illuminati", "Sarif Industries", "augmentation", "Panchaea"], "conspiracy cyberpunk RPG"),
    ("system_shock", "System Shock", ["Citadel Station", "SHODAN", "TriOptimum", "cyberspace deck", "mutant crew", "engineering bay"], "rogue AI space station horror"),
    ("prey", "Prey", ["Talos I", "Typhon", "TranStar", "Neuromod", "Mimic", "GLOO cannon"], "space station mimic horror"),
    ("thief", "Thief", ["The City", "Hammerites", "Pagans", "Keepers", "Mechanists", "Builder cathedral"], "stealth gothic city fantasy"),
    ("assassins_creed", "Assassin's Creed", ["Assassins", "Templars", "Animus", "Isu artifact", "hidden blade", "Eagle Vision"], "historical conspiracy stealth"),
    ("tomb_raider", "Tomb Raider", ["Croft Manor", "Trinity", "Yamatai", "Siberian tomb", "Atlantean ruins", "dual pistols"], "archaeological survival adventure"),
    ("uncharted", "Uncharted", ["El Dorado", "Shambhala", "Avery's treasure", "Sic Parvis Magna", "Naughty Dog ruins", "grappling hook"], "pulp treasure hunt adventure"),
    ("god_of_war", "God of War", ["Nine Realms", "Valkyries", "Blades of Chaos", "Leviathan Axe", "Jotunheim", "Olympus"], "mythic action epic"),
    ("hades", "Hades", ["House of Hades", "Olympus boons", "Elysium", "Tartarus", "Styx", "Infernal Arms"], "underworld mythic roguelike"),
    ("darkest_dungeon", "Darkest Dungeon", ["Hamlet", "Ancestor", "Crimson Court", "Warrens", "Weald", "stress affliction"], "gothic dungeon despair"),
    ("hollow_knight", "Hollow Knight", ["Hallownest", "Dream Nail", "Radiance", "Greenpath", "City of Tears", "Mantis Lords"], "melancholic insect kingdom fantasy"),
    ("devil_may_cry", "Devil May Cry", ["Devil May Cry office", "Dante style", "Vergil katana", "Red Queen", "Qliphoth", "demon hunter"], "stylish demon action"),
    ("bayonetta", "Bayonetta", ["Umbra Witches", "Lumen Sages", "Infernal Demons", "Paradiso", "Witch Time", "Scarborough Fair"], "baroque witch action"),
    ("mortal_kombat", "Mortal Kombat", ["Outworld", "Earthrealm", "Netherrealm", "Lin Kuei", "Shirai Ryu", "Elder Gods"], "martial tournament fantasy"),
    ("street_fighter", "Street Fighter", ["World Warrior", "Shadaloo", "Metro City", "Satsui no Hado", "Interpol agent", "arcade arena"], "global martial arts action"),
    ("tekken", "Tekken", ["Mishima Zaibatsu", "G Corporation", "King of Iron Fist", "Devil Gene", "Zaibatsu tower", "arena lights"], "corporate fighting saga"),
    ("soulcalibur", "Soulcalibur", ["Soul Edge", "Soul Calibur", "Astral Chaos", "Holy Roman ruins", "cursed blade", "weapon master"], "weapon fighter dark fantasy"),
    ("final_fantasy_viii", "Final Fantasy VIII", ["Balamb Garden", "SeeD", "Gunblade", "Sorceress", "Lunatic Pandora", "Triple Triad"], "military academy fantasy sci-fi"),
    ("final_fantasy_ix", "Final Fantasy IX", ["Alexandria", "Lindblum", "Black Mage Village", "Mist Continent", "Tantalus", "Trance"], "storybook crystal fantasy"),
    ("final_fantasy_x", "Final Fantasy X", ["Spira", "Yevon", "Summoner pilgrimage", "Blitzball", "Zanarkand", "Aeons"], "tropical pilgrimage fantasy"),
    ("final_fantasy_xiv", "Final Fantasy XIV", ["Eorzea", "Scions", "Garlean Empire", "Crystal Tower", "Ishgard", "Allagan tech"], "MMO epic fantasy"),
    ("final_fantasy_xvi", "Final Fantasy XVI", ["Valisthea", "Dominants", "Eikons", "Rosaria", "Sanbreque", "Mothercrystals"], "dark crystal war fantasy"),
    ("akira", "Akira", ["Neo-Tokyo", "capsule biker gang", "Espers", "military lab", "Olympic stadium", "psychic explosion"], "cyberpunk psychic catastrophe"),
    ("cowboy_bebop", "Cowboy Bebop", ["Bebop ship", "Red Dragon syndicate", "Mars casino", "Woolong bounty", "Swordfish II", "Ganymede"], "jazz space bounty noir"),
    ("evangelion", "Neon Genesis Evangelion", ["NERV", "Evangelion unit", "Angel attack", "Tokyo-3", "AT Field", "Geofront"], "apocalyptic mecha psychology"),
    ("gundam", "Gundam", ["Mobile Suit", "Earth Federation", "Zeon", "Newtype", "Colony drop", "White Base"], "real robot space war"),
    ("macross", "Macross", ["SDF-1", "Valkyrie fighter", "Zentradi", "Minmay concert", "Protoculture", "Macross City"], "idol fighter space opera"),
    ("code_geass", "Code Geass", ["Britannia", "Black Knights", "Geass", "Knightmare Frame", "Area 11", "Ashford estate"], "mecha rebellion chess drama"),
    ("psycho_pass", "Psycho-Pass", ["Sibyl System", "Dominator", "Public Safety Bureau", "Crime Coefficient", "latent criminal", "MWPSB"], "surveillance police dystopia"),
    ("ergo_proxy", "Ergo Proxy", ["Romdo", "AutoReiv", "Proxy", "Cogito virus", "Mosk", "wasteland dome"], "philosophical android noir"),
    ("serial_experiments_lain", "Serial Experiments Lain", ["Wired", "NAVI computer", "Knights", "Protocol 7", "cyber hallucination", "power lines"], "surreal internet ghost story"),
    ("attack_on_titan", "Attack on Titan", ["Survey Corps", "Walls Maria Rose Sina", "Titan threat", "ODM gear", "Marley", "Paths"], "vertical action war fantasy"),
    ("fullmetal_alchemist", "Fullmetal Alchemist", ["Amestris", "State Alchemist", "Homunculi", "Philosopher's Stone", "Central Command", "transmutation circle"], "alchemy military fantasy"),
    ("naruto", "Naruto", ["Hidden Leaf", "Akatsuki", "Sharingan", "chakra", "Hokage", "ANBU"], "shinobi village fantasy"),
    ("bleach", "Bleach", ["Soul Society", "Shinigami", "Zanpakuto", "Hueco Mundo", "Quincy", "Bankai"], "spirit swordsman supernatural action"),
    ("one_piece", "One Piece", ["Grand Line", "Straw Hat pirates", "World Government", "Devil Fruit", "Marineford", "Wano"], "pirate adventure fantasy"),
    ("demon_slayer", "Demon Slayer", ["Demon Slayer Corps", "Nichirin blade", "Hashira", "Muzan", "Infinity Castle", "Breathing Style"], "taisho demon hunting fantasy"),
    ("jujutsu_kaisen", "Jujutsu Kaisen", ["Jujutsu sorcerer", "cursed energy", "Sukuna", "Shibuya incident", "Domain Expansion", "Zenin clan"], "curse exorcist action"),
    ("chainsaw_man", "Chainsaw Man", ["Public Safety", "Devil Hunter", "Makima office", "Gun Devil", "chainsaw devil", "Tokyo alleys"], "devil hunter urban horror"),
    ("berserk", "Berserk", ["Band of the Hawk", "Brand of Sacrifice", "Eclipse", "God Hand", "Midland", "Dragon Slayer"], "brutal dark fantasy"),
    ("claymore", "Claymore", ["Claymore organization", "Yoma", "Awakened Being", "Teresa legend", "Pieta battle", "silver eyes"], "monster hunter dark fantasy"),
    ("trigun", "Trigun", ["No Man's Land", "Plant technology", "July city", "Gung-Ho Guns", "sandsteamer", "double dollar bounty"], "desert gunslinger sci-fi"),
    ("hellsing", "Hellsing", ["Hellsing Organization", "Millennium", "Vampire police", "Integra manor", "Alucard seal", "London siege"], "vampire gun gothic"),
    ("vampire_hunter_d", "Vampire Hunter D", ["Nobility", "Frontier villages", "Dunpeal", "sacred sword", "cyber gothic castles", "Left Hand"], "post-apocalyptic vampire gothic"),
    ("tokyo_ghoul", "Tokyo Ghoul", ["CCG", "Anteiku", "Kagune", "Aogiri Tree", "Tokyo wards", "quinque weapon"], "urban ghoul tragedy"),
    ("parasyte", "Parasyte", ["parasite organism", "Migi-like morph", "government task force", "body horror duel", "alien cells", "city rooftop"], "body horror alien thriller"),
    ("alita", "Battle Angel Alita", ["Iron City", "Motorball", "Zalem", "Panzer Kunst", "cyborg body", "Hunter-Warrior"], "cyborg martial sci-fi"),
    ("pacific_rim", "Pacific Rim", ["Jaeger", "Kaiju", "PPDC", "drift compatibility", "Shatterdome", "breach portal"], "giant robot monster war"),
    ("godzilla", "Godzilla", ["Monarch", "Godzilla", "King Ghidorah", "Mothra", "kaiju warning", "hollow earth"], "kaiju disaster myth"),
    ("jurassic_park", "Jurassic Park", ["InGen", "Isla Nublar", "raptor paddock", "T-Rex enclosure", "amber DNA", "visitor center"], "dinosaur theme park thriller"),
    ("avatar_pandora", "Avatar", ["Pandora", "Na'vi", "RDA", "Hallelujah Mountains", "Eywa", "AMP suit"], "alien rainforest epic"),
    ("the_mummy", "The Mummy", ["Hamunaptra", "Medjai", "Book of the Dead", "Imhotep curse", "scarab swarm", "Egyptian ruins"], "pulp Egyptian occult adventure"),
    ("indiana_jones", "Indiana Jones", ["Ark of the Covenant", "Holy Grail", "Temple of Doom", "Crystal Skull", "Marshall College", "ancient map"], "pulp archaeology adventure"),
    ("hellraiser", "Hellraiser", ["Lament Configuration", "Cenobites", "Leviathan maze", "Hell Priest", "chains", "flesh puzzle"], "sadomasochistic cosmic horror"),
    ("halloween", "Halloween", ["Haddonfield", "Shape mask", "Smith's Grove", "October leaves", "kitchen knife", "suburban street"], "slasher suburb dread"),
    ("nightmare_on_elm_street", "Nightmare on Elm Street", ["Elm Street", "dream killer", "boiler room", "clawed glove", "red-green sweater", "nightmare logic"], "dream slasher horror"),
    ("scream", "Scream", ["Woodsboro", "Ghostface", "Stab franchise", "phone call", "suburban party", "meta slasher"], "self-aware slasher noir"),
    ("saw", "Saw", ["Jigsaw", "Nerve Gas House", "reverse bear trap", "tape recorder", "industrial bathroom", "moral test"], "industrial trap thriller"),
    ("the_ring", "The Ring", ["cursed videotape", "Sadako", "well", "static TV", "seven days", "wet hair ghost"], "video curse ghost horror"),
    ("the_grudge", "The Grudge", ["Ju-on curse", "Kayako house", "Toshio shadow", "tatami room", "croaking sound", "white ghost"], "vengeful house curse horror"),
    ("the_conjuring", "The Conjuring", ["Warren case files", "Annabelle room", "Perron farmhouse", "demonic possession", "music box", "exorcism kit"], "haunted case-file horror"),
    ("insidious", "Insidious", ["The Further", "red door", "astral projection", "Lipstick-Face Demon", "gas mask seance", "dark realm"], "astral haunting horror"),
    ("hereditary", "Hereditary", ["Paimon cult", "miniature house", "treehouse ritual", "family seance", "attic shrine", "blue candle"], "domestic occult horror"),
    ("midsommar", "Midsommar", ["Harga commune", "flower crown", "midsummer ritual", "yellow temple", "runic tapestry", "daylight horror"], "folk horror daylight ritual"),
    ("the_witch", "The VVitch", ["New England farm", "Black Phillip", "coven woods", "Puritan dress", "witch mark", "dark sermon"], "colonial folk horror"),
    ("suspiria", "Suspiria", ["Tanz Academy", "Three Mothers", "red dance studio", "witch coven", "stained glass", "Berlin ballet"], "surreal witch dance horror"),
    ("crimson_peak", "Crimson Peak", ["Allerdale Hall", "red clay", "Sharpe family", "ghost bride", "gothic staircase", "snowy manor"], "romantic gothic ghost story"),
    ("pans_labyrinth", "Pan's Labyrinth", ["Faun", "Pale Man", "labyrinth gate", "mandrake root", "Spanish forest", "underworld princess"], "dark fairy tale war"),
    ("dracula", "Dracula", ["Castle Dracula", "Transylvania", "Carfax Abbey", "vampire brides", "Renfield", "blood moon"], "classic vampire gothic"),
    ("frankenstein", "Frankenstein", ["Victor Frankenstein", "galvanic lab", "Creature", "Arctic pursuit", "Promethean science", "lightning apparatus"], "gothic science tragedy"),
    ("van_helsing", "Van Helsing", ["Transylvania hunt", "Vatican arsenal", "Dracula brides", "monster hunter coat", "werewolf serum", "castle laboratory"], "monster hunter gothic action"),
    ("pirates_caribbean", "Pirates of the Caribbean", ["Black Pearl", "Port Royal", "Davy Jones", "Flying Dutchman", "Aztec gold", "Tortuga"], "cursed pirate adventure"),
    ("john_wick", "John Wick", ["Continental Hotel", "High Table", "gold coins", "adjudicator", "bulletproof suit", "neon club"], "assassin underworld action"),
    ("james_bond", "James Bond", ["MI6", "Q Branch", "Aston Martin", "SPECTRE", "casino royale", "00 agent"], "spy glamour thriller"),
    ("mission_impossible", "Mission Impossible", ["IMF", "Ethan-style mask tech", "NOC list", "vault heist", "self-destruct message", "Langley"], "impossible spy heist"),
    ("kingsman", "Kingsman", ["Kingsman tailor shop", "Statesman", "Church fight", "umbrella shield", "Manners maketh man", "spy gadgets"], "tailored spy action"),
    ("sin_city", "Sin City", ["Basin City", "Old Town", "Marv alleys", "Yellow Bastard", "Kadie's Bar", "black-white noir"], "graphic crime noir"),
    ("blade", "Blade", ["Daywalker", "vampire nightclub", "House of Erebus", "serum injector", "silver stakes", "blood god ritual"], "vampire martial cyber gothic"),
    ("underworld", "Underworld", ["Vampire coven", "Lycan war", "Death Dealer", "Corvinus bloodline", "Viktor mansion", "silver nitrate rounds"], "blue-black vampire action"),
    ("the_crow", "The Crow", ["Devil's Night", "crow familiar", "rooftop revenge", "gothic makeup", "Top Dollar gang", "rainy Detroit"], "goth revenge urban fantasy"),
    ("transformers", "Transformers", ["Autobots", "Decepticons", "Cybertron", "AllSpark", "Energon", "Optimus convoy"], "robot war blockbuster"),
    ("starship_troopers", "Starship Troopers", ["Mobile Infantry", "Arachnids", "Klendathu", "Federal Service", "bug war", "drop armor"], "satirical military bug war"),
    ("district_9", "District 9", ["MNU", "District 9 camp", "Prawn aliens", "alien exosuit", "black fluid", "Johannesburg"], "alien refugee sci-fi"),
    ("elysium", "Elysium", ["Elysium station", "exoskeleton rig", "Med-Bay", "Earth slums", "Delacourt security", "data heist"], "class-war orbital sci-fi"),
    ("edge_of_tomorrow", "Edge of Tomorrow", ["Mimics", "time loop battle", "Jacket exosuit", "Louvre assault", "Omega", "United Defense Force"], "time-loop alien war"),
    ("snowpiercer", "Snowpiercer", ["Snowpiercer train", "Tail section", "Engine room", "Wilford order", "frozen earth", "class cars"], "train-bound class apocalypse"),
]


def parse_wide_rows(text):
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        module_id, source, terms, vibe = [part.strip() for part in line.split("|", 3)]
        rows.append((module_id, source, [term.strip() for term in terms.split(";")], vibe))
    return rows


BULK_FRANCHISE_ROWS_TEXT = """
elder_scrolls|The Elder Scrolls|Tamriel;Skyrim;Morrowind;Oblivion;Daedric Prince;Imperial City|open-world high fantasy RPG
skyrim|Skyrim|Whiterun;College of Winterhold;Dark Brotherhood;Thieves Guild;Dragonborn;Daedric artifact|nordic dragon fantasy
morrowind|Morrowind|Vvardenfell;House Telvanni;Vivec City;Ashlanders;Red Mountain;Silt Strider|alien volcanic fantasy
oblivion|Oblivion|Cyrodiil;Kvatch;Arcane University;Mythic Dawn;Oblivion Gate;Shivering Isles|imperial daedric fantasy
starfield|Starfield|Constellation;United Colonies;Freestar Collective;Neon city;Crimson Fleet;Artifact temple|NASA-punk exploration sci-fi
outer_worlds|The Outer Worlds|Halcyon;Spacer's Choice;Groundbreaker;Byzantium;Auntie Cleo;Board colony|corporate colony satire sci-fi
dragon_quest|Dragon Quest|Erdrick legacy;Slime companion;castle town;Luminary;Yggdrasil;Zenithian gear|classic heroic JRPG fantasy
chrono_trigger|Chrono Trigger|Millennial Fair;Epoch time machine;Kingdom of Guardia;Magus castle;Lav o s threat;Zeal kingdom|time travel JRPG adventure
xenoblade|Xenoblade Chronicles|Monado;Bionis;Mechonis;Alrest;Aegis core;Colony 9|titan world JRPG fantasy
fire_emblem|Fire Emblem|Garreg Mach;Crest bearer;Pegasus knight;House leader;Emblem ring;war council|tactical royal fantasy
persona|Persona|Velvet Room;Phantom Thieves;Shadow world;arcana card;metaverse palace;Evoker|urban occult psychology RPG
shin_megami_tensei|Shin Megami Tensei|Tokyo apocalypse;Demon summoner;Law faction;Chaos faction;Magatsuhi;Cathedral of Shadows|demon negotiation post-apocalypse
yakuza|Yakuza Like a Dragon|Kamurocho;Tojo Clan;Omi Alliance;Millennium Tower;Dragon tattoo;clan office|neon crime drama
red_dead_redemption|Red Dead Redemption|Van der Linde gang;Blackwater;Saint Denis;frontier camp;Pinkerton pursuit;dead eye duel|western outlaw tragedy
grand_theft_auto|Grand Theft Auto|Los Santos;Vice City;Liberty City;heist crew;FIB raid;street racer|satirical crime sandbox
la_noire|L.A. Noire|Los Angeles police;case notebook;interrogation room;Hollywoodland;traffic desk;noir alley|period detective noir
max_payne|Max Payne|Valkyr drug;New York snow;bullet time;noir monologue;Aesir Corporation;hotel shootout|neo-noir revenge action
hitman|Hitman|ICA;47 barcode;safehouse;disguise kit;silent assassin;contract briefing|assassin sandbox thriller
splinter_cell|Splinter Cell|Third Echelon;goggles glow;NSA black ops;Paladin aircraft;shadow infiltration;Lambert briefing|stealth espionage thriller
rainbow_six|Rainbow Six|Rainbow team;breach charge;hostage rescue;night vision;counter-terror unit;operators roster|tactical counter-terror action
ghost_recon|Ghost Recon|Ghost squad;Aurora island;Wolves faction;optical camo;drone recon;wildlands cartel|special forces tactical action
the_division|The Division|SHD agents;Dark Zone;ISAC watch;Cleaners faction;JTF checkpoint;New York outbreak|urban collapse tactical RPG
arma|Arma|Altis;NATO task force;CSAT;mil-sim radio;forward operating base;recon patrol|realistic military sandbox
battlefield|Battlefield|Conquest flag;war-torn city;armored column;frontline squad;destructible building;fighter jet pass|large-scale war action
call_of_duty|Call of Duty|Task Force 141;Warzone drop;Gulag;Modern Warfare;Zombies mystery box;Black Ops safehouse|cinematic military action
medal_of_honor|Medal of Honor|OSS mission;Normandy landing;Pacific theater;Tier One operator;war diary;field command|war drama action
gears_of_war|Gears of War|COG armor;Locust Horde;Lancer chainsaw;Ephyra ruins;Emergence hole;Jacinto|chunky cover-shooter sci-fi
xcom|XCOM|XCOM base;Sectoid;ADVENT;Skyranger;psionic operative;alien autopsy|alien invasion tactics
command_and_conquer|Command and Conquer|GDI;Brotherhood of Nod;Tiberium;Kane temple;Mammoth tank;Ion Cannon|tiberium war RTS
red_alert|Command and Conquer Red Alert|Allied command;Soviet war machine;Chronosphere;Tesla coil;Yuri faction;Kirov airship|alternate history RTS
homeworld|Homeworld|Kharak;Kushan fleet;Mothership;Bentusi;Vaygr;hyperspace core|fleet exile space opera
eve_online|EVE Online|New Eden;Amarr Empire;Gallente Federation;Caldari State;Minmatar Republic;capsuleer ship|space economy sandbox
elite_dangerous|Elite Dangerous|Pilots Federation;Thargoids;Coriolis station;Sidewinder cockpit;guardian ruins;supercruise|realistic space sim
no_mans_sky|No Man's Sky|Atlas;Anomaly station;Sentinel drones;Traveller glyphs;multi-tool;exotic planet|procedural cosmic exploration
stellaris|Stellaris|galactic council;fallen empire;precursor relic;crisis fleet;ringworld segment;science ship|grand strategy space opera
rimworld|RimWorld|crashlanded colony;ancient danger;mechanoids;royalty permit;tribal raid;rim settlement|colony survival sci-fi
factorio|Factorio|factory bus;biters;rocket silo;inserter line;oil refinery;logistic robots|industrial automation survival
satisfactory|Satisfactory|FICSIT;space elevator;factory platform;alien planet;conveyor tower;pioneer suit|bright factory exploration
subnautica|Subnautica|4546B;Aurora wreck;Seamoth;Leviathan class;Precursor facility;kelp forest|underwater alien survival
abzu|ABZU|ocean temple;diver suit;great white companion;coral sanctuary;ancient mural;sunken machine|meditative ocean fantasy
stray|Stray|Walled City 99;B-12 drone;Zurks;Companions;neon alley;control room|robot city exploration
outer_wilds|Outer Wilds|Hearthian explorer;Nomai ruins;timber hearth;quantum moon;Ash Twin project;eye signal|time-loop space archaeology
kerbal_space_program|Kerbal Space Program|Kerbal Space Center;Mun lander;rocket staging;mission control;green astronaut;orbital maneuver|playful space engineering
frostpunk|Frostpunk|Generator city;Londoners;Faith Keepers;Order guard;coal thumper;frozen wasteland|frozen survival city-builder
this_war_of_mine|This War of Mine|Pogoren shelter;scavenging night;sniper junction;radio news;ruined apartment;survivor stove|civilian war survival
papers_please|Papers Please|Arstotzka checkpoint;entry permit;border inspector;Ministry seal;gray booth;detained line|bureaucratic dystopia
disco_elysium|Disco Elysium|Revachol;R.C.M. badge;Whirling-in-Rags;Inland Empire;Thought Cabinet;Dolores Dei|philosophical detective RPG
kentucky_route_zero|Kentucky Route Zero|Route Zero;Equus Oils;Bureau of Reclaimed Spaces;Echo River;TV horse farm;bluegrass ghosts|magical realist road mystery
life_is_strange|Life is Strange|Arcadia Bay;Blackwell campus;butterfly photo;storm vision;Polaroid wall;Two Whales diner|time-rewind small town drama
detroit_become_human|Detroit Become Human|CyberLife;Jericho;android LED;deviant revolution;Detroit tower;RK series|android civil rights sci-fi
heavy_rain|Heavy Rain|Origami Killer;rainy motel;FBI ARI glasses;warehouse trial;police precinct;paper crane|rain-soaked crime thriller
beyond_two_souls|Beyond Two Souls|Aiden entity;CIA training;infraworld rift;Navajo desert;psychic link;containment lab|psychic paranormal drama
until_dawn|Until Dawn|Blackwood Mountain;Washington Lodge;wendigo mine;totem clue;butterfly effect;winter cabin|interactive slasher mountain horror
the_quarry|The Quarry|Hackett's Quarry;summer camp lodge;werewolf curse;campfire trail;boathouse;moonlit woods|summer-camp monster horror
dead_by_daylight|Dead by Daylight|Entity realm;hook sacrifice;generator repair;fog trial;killer shack;survivor flashlight|asymmetric horror arena
phasmophobia|Phasmophobia|ghost investigation van;EMF reader;spirit box;haunted farmhouse;salt evidence;sanity monitor|co-op ghost hunting horror
outlast|Outlast|Mount Massive Asylum;night vision camera;Murkoff files;Variant ward;blood corridor;security room|found-footage asylum horror
amnesia|Amnesia|Brennenburg Castle;dark descent;sanity drain;lantern oil;orb chamber;shadow pursuit|gothic memory horror
soma|SOMA|PATHOS-II;WAU;ARK project;deep sea station;structure gel;scan copy|existential underwater sci-fi horror
fatal_frame|Fatal Frame|Camera Obscura;Himuro Mansion;crimson butterfly;spirit photograph;ritual mask;haunted village|Japanese ghost photography horror
clock_tower|Clock Tower|Barrows mansion;Scissorman;panic meter;gothic corridors;clock tower hall;survivor hiding spot|stalker mansion horror
siren|Siren|Hanuda village;Shibito;red water;sightjack;ritual siren;abandoned school avoided|Japanese village curse horror
the_evil_within|The Evil Within|STEM system;Beacon hospital;Keeper safehead;Union town;Mobius lab;mental horror|surreal survival horror
five_nights_freddys|Five Nights at Freddy's|Freddy Fazbear's;security office;animatronic stage;power monitor;purple guy lore;backroom camera|animatronic night horror
bendy|Bendy and the Ink Machine|Joey Drew Studios;ink machine;Bendy cutout;rubber hose demon;animation desk;ink river|cartoon studio horror
hello_neighbor|Hello Neighbor|Raven Brooks;Neighbor basement;suburban house;keycard puzzle;creaky stairs;hidden room|suburban stealth mystery
limbo|Limbo|black forest;saw trap;spider silhouette;monochrome fog;industrial gears;lonely platform|monochrome nightmare puzzle
inside_game|Inside|red-shirt escapee;corporate facility;mind control device;flooded lab;masked workers;the Huddle|wordless dystopian puzzle
gris|GRIS|watercolor ruins;grief statue;red dress;singing power;wind temple;constellation bridge|emotional surreal platform fantasy
journey|Journey|red cloak traveler;desert ruins;cloth creature;mountain beacon;sand surfing;ancient glyphs|wordless desert pilgrimage
sky_children_light|Sky Children of the Light|Sky kingdom;candle spirits;winged cape;Eden storm;constellation gate;cloud realm|gentle cloud pilgrimage fantasy
flower_game|Flower|petal stream;wind path;city bloom;grass field;dreamscape sky;restored color|abstract nature restoration
monument_valley|Monument Valley|impossible geometry;Crow People;Ida princess;rotating tower;Escher stairs;sacred geometry|optical illusion puzzle fantasy
fez|Fez|2D-3D village;golden cube;glyph language;rotating world;ancient telescope;bit city|retro dimensional puzzle
celeste|Celeste|Celeste Mountain;mirror self;strawberry path;crystal heart;windy summit;old hotel|mountain self-discovery platformer
ori|Ori|Nibel forest;Spirit Tree;Kuro owl;Gumon ruins;glowing spirit;water tree|luminous forest spirit fantasy
cuphead|Cuphead|Inkwell Isles;Devil casino;rubber hose boss;run-and-gun stage;Elder Kettle;contract scroll|vintage cartoon boss fantasy
undertale|Undertale|Underground;Determination;Royal Guard;CORE facility;Ruins door;SOUL heart|quirky monster underground RPG
deltarune|Deltarune|Dark World;Castle Town;Delta Rune;Cyber World;card kingdom;fountain seal|surreal monster RPG
omori|OMORI|Headspace;white space;dream picnic;black lightbulb;neighbor's room;deep well|psychological dream RPG
earthbound|EarthBound|Eagleland;PSI power;Onett;Saturn Valley;Giygas;meteorite hill|suburban psychic JRPG
mother3|Mother 3|Nowhere Islands;Pigmask Army;Needle sites;chimera lab;Tazmily village;dragon awakening|pastoral psychic tragedy
undertow_bioshock_infinite|BioShock Infinite|Columbia;Vox Populi;Songbird;Sky-Line;Lutece device;Handyman|floating-city quantum dystopia
thief_modern|Thief 2014|Baron's Watch;The City;Primal Stone;Clock Tower hideout;gloom plague;master thief|shadowy steampunk stealth
kingdom_hearts|Kingdom Hearts|Keyblade;Heartless;Organization XIII;Destiny Islands;Traverse Town;Scala ad Caelum|crossover heart fantasy
fable|Fable|Albion;Heroes Guild;Bowerstone;Balverine;Spire;Guild Seal|storybook moral fantasy
dragons_dogma|Dragon's Dogma|Gransys;Arisen;Pawn legion;Everfall;Bitterblack Isle;Dragon's bargain|monster quest dark fantasy
kingdom_come|Kingdom Come Deliverance|Bohemia;Rattay;Skalitz;Sir Radzig;medieval codex;blacksmith son|grounded medieval drama
mount_and_blade|Mount and Blade|Calradia;Swadian knights;Vaegir border;Khergit steppe;Bannerlord clan;siege camp|sandbox medieval war
total_war_warhammer|Total War Warhammer|Karl Franz;High Elves;Lizardmen;Chaos invasion;Skaven undercity;vortex campaign|mass battle fantasy strategy
civilization|Civilization|world wonder;great person;settler banner;district plaza;tech tree;cultural victory|historical grand strategy
crusader_kings|Crusader Kings|dynasty court;succession crisis;intrigue scheme;holy war;royal marriage;feudal council|medieval dynasty sandbox
europa_universalis|Europa Universalis|merchant republic;colonial charter;imperial diet;trade node;royal court;war map|early-modern grand strategy
hearts_of_iron|Hearts of Iron|war room;frontline map;factory queue;resistance cell;naval invasion;radar station|global war strategy
age_of_empires|Age of Empires|town center;castle age;relic monk;siege workshop;wonder build;scout cavalry|historical RTS
age_of_mythology|Age of Mythology|Atlantean oracle;Norse god power;Egyptian monument;Greek myth unit;Titan gate;favor altar|mythic RTS
heroes_might_magic|Heroes of Might and Magic|Erathia;Necropolis town;Castle hero;artifact map;mage guild;dragon utopia|turn-based high fantasy
dark_crystal|The Dark Crystal|Thra;Gelfling clan;Skeksis castle;Mystics valley;Crystal of Truth;Podling village|puppet dark fantasy
labyrinth|Labyrinth|Goblin City;Jareth ballroom;Escher stairs;crystal orb;bog of eternal stench;maze gate|whimsical dark fantasy
willow|Willow|Tir Asleen;Nelwyn village;Daikini warrior;Madmartigan sword;Bavmorda castle;Elora prophecy|classic quest fantasy
legend_movie|Legend|Darkness lord;unicorn forest;Lili gown;goblin kitchen;sunlit glade;black castle|mythic fairy tale fantasy
princess_bride|The Princess Bride|Florin;Dread Pirate Roberts;Fire Swamp;Cliffs of Insanity;Miracle Max;R.O.U.S. tracks|storybook swashbuckling romance
stardust|Stardust|Stormhold;fallen star;witch queen;sky pirate ship;Wall village;glass dagger|romantic fairy tale adventure
golden_compass|His Dark Materials|Oxford;Alethiometer;Magisterium;daemon companion;Svalbard bears;Dust|parallel-world theological fantasy
narnia|The Chronicles of Narnia|Narnia;Cair Paravel;White Witch;Aslan banner;wardrobe portal;lamp-post snow|portal kingdom fantasy
percy_jackson|Percy Jackson|Camp Half-Blood;Olympian cabins;Riptide sword;Lotus Casino;Underworld gate;quest prophecy|modern myth adventure
artemis_fowl|Artemis Fowl|Fowl Manor;LEPRecon;Haven City;fairy technology;time stop dome;gold ransom|fairy heist techno-fantasy
mortal_engines|Mortal Engines|traction city;London engine;anti-traction league;Stalker soldier;airhaven;old-tech museum|city-eating steampunk dystopia
maze_runner|The Maze Runner|Glade;Maze walls;WCKD lab;Griever;Scorch trials;memory vial|dystopian trial survival
hunger_games|The Hunger Games|Panem;Capitol fashion;District 12;arena cornucopia;Mockingjay pin;Peacekeepers|dystopian rebellion spectacle
divergent|Divergent|Dauntless faction;Erudite lab;Abnegation grey;faction test;Chicago wall;simulation serum|faction dystopian action
the_100|The 100|Ark station;Grounders;Mount Weather;Polis;Nightblood;A.L.I.E.|post-apocalyptic clan sci-fi
lost|Lost|Dharma Initiative;Swan station;smoke monster;Others camp;Oceanic 815;island hatch|mystery island sci-fi
fringe|Fringe|Fringe Division;alternate universe;Massive Dynamic;Observer;Cortexiphan;amber quarantine|weird science procedural
person_of_interest|Person of Interest|The Machine;Samaritan;numbers case;subway hideout;Finch library;surveillance grid|AI surveillance thriller
mr_robot|Mr. Robot|fsociety mask;E Corp;Steel Mountain;Dark Army;subway hack;laptop terminal|hacktivist psychological thriller
orphan_black|Orphan Black|Leda clones;Dyad Institute;Neolution;Clone Club;Proletheans;genetic patent|clone conspiracy thriller
the_boys|The Boys|Vought;The Seven;Compound V;supe collateral;Vought Tower;underground vigilantes|corporate superhero satire
invincible|Invincible|Global Defense Agency;Viltrumite;Guardians HQ;alien coalition;hero academy avoided;blood moon city|brutal superhero coming-of-age
watchmen|Watchmen|Minutemen;Watchmen smiley;Karnak base;Rorschach journal;Veidt tower;Dr Manhattan glow|deconstructed superhero noir
batman|Batman|Gotham City;Bat-Signal;Wayne Manor;Arkham Asylum;Rogues Gallery;utility belt|gothic urban vigilante
superman|Superman|Metropolis;Daily Planet;Kryptonian crystal;Fortress of Solitude;LexCorp;House of El|hopeful superhero myth
wonder_woman|Wonder Woman|Themyscira;Amazon armor;lasso of truth;Olympian temple;Ares war;invisible jet|mythic superhero fantasy
green_lantern|Green Lantern|Oa;Green Lantern Corps;power ring;Sector 2814;Manhunters;emotional spectrum|cosmic superhero corps
flash|The Flash|Central City;Speed Force;STAR Labs;Rogues;time remnant;red lightning|speedster science adventure
arrow|Arrow|Star City;Queen Consolidated;League of Assassins;island survival;green hood;trick arrows|urban archer vigilante
gotham|Gotham|GCPD;Arkham inmates;Penguin club;Falcone crime;Gotham docks;Wayne case|crime city origin noir
spider_man|Spider-Man|New York skyline;Daily Bugle;Oscorp;spider-sense;web shooters;Sinister Six|urban web-slinger superhero
x_men|X-Men|Xavier Institute;Brotherhood;Cerebro;Sentinels;mutant registry;Danger Room|mutant civil rights superhero
fantastic_four|Fantastic Four|Baxter Building;Negative Zone;Latveria;Doctor Doom;cosmic rays;unstable molecules|science family superhero
guardians_galaxy|Guardians of the Galaxy|Knowhere;Milano ship;Nova Corps;Ravagers;Infinity Stone;cosmic outlaw|space outlaw superhero
doctor_strange|Doctor Strange|Sanctum Sanctorum;Kamar-Taj;Sling Ring;Dark Dimension;Eye of Agamotto;mirror dimension|mystic superhero sorcery
black_panther|Black Panther|Wakanda;Dora Milaje;Vibranium;Golden City;Panther habit;ancestral plane|afrofuturist royal superhero
moon_knight|Moon Knight|Khonshu;Crescent darts;DuAt;Egyptian tomb;white suit;midnight mission|mythic vigilante thriller
lokiverse|Loki|TVA;Time Variance Authority;Miss Minutes;Sacred Timeline;Citadel at End;variant file|bureaucratic time fantasy
wandavision|WandaVision|Westview;Hex field;SWORD;scarlet magic;retro sitcom set;Agatha basement|surreal suburban witch fantasy
blade_runner_2049|Blade Runner 2049|K Wallace;LAPD baseline;memory archive;Las Vegas ruins;replicant bones;Ana Stelline lab|melancholic replicant noir
mad_men|Mad Men|Sterling Cooper;Madison Avenue;pitch room;1960s office;ad campaign board;smoke-filled lounge|period advertising drama
boardwalk_empire|Boardwalk Empire|Atlantic City;Nucky organization;Prohibition speakeasy;Commodore estate;bootleg convoy;Boardwalk lights|prohibition crime drama
deadwood|Deadwood|Deadwood camp;Gem Saloon;gold claim;frontier mud;lawman's badge;opium den|frontier western drama
yellowstone|Yellowstone|Dutton ranch;Broken Rock;livestock brand;Montana valley;bunkhouse;market equities|modern ranch dynasty drama
westworld_movie|Westworld film|Delos park;gunslinger android;saloon loop;Romanworld;Medievalworld;malfunction code|theme-park android western
vikings|Vikings|Kattegat;Ragnar clan;shieldmaiden;longship raid;Uppsala temple;Great Heathen Army|norse saga drama
the_last_kingdom|The Last Kingdom|Uhtred oath;Bebbanburg;Wessex court;Dane camp;shield wall;Alfred's papers|saxon viking historical epic
rome|Rome|Aventine;Julius Caesar;Legion XIII;Forum politics;Cleopatra court;Roman villa|ancient political drama
spartacus|Spartacus|Capua ludus;gladiator arena;House of Batiatus;rebel camp;Roman villa;arena sand|gladiator rebellion drama
black_sails|Black Sails|Nassau;Walrus ship;pirate council;Spanish gold;New Providence;tavern map|pirate political drama
the_terror|The Terror|HMS Erebus;HMS Terror;Arctic ice;Tuunbaq;Royal Navy camp;frozen ship|polar expedition horror
chernobyl|Chernobyl|Pripyat;reactor four;liquidators;dosimeter;control room;exclusion zone|nuclear disaster drama
dark_city|Dark City|Strangers;midnight tuning;Shell Beach;memory syringe;noir city;clockwork sky|expressionist memory sci-fi
the_fifth_element|The Fifth Element|Fhloston Paradise;Mondoshawan stones;Zorg Industries;Leeloo-style straps;NYC flying traffic;diva opera|colorful space opera
valerian|Valerian|Alpha station;Mule planet;Shingouz brokers;space bazaar;converter creature;pearl city|comic space adventure
jupiter_ascending|Jupiter Ascending|Abrasax dynasty;sky boots;Orous court;harvest planet;splice guards;space royalty|baroque space monarchy
cloud_atlas|Cloud Atlas|Neo Seoul;Somni archive;Cloud Atlas sextet;far-future valley;corporate fabricants;ship journal|reincarnation sci-fi mosaic
inception|Inception|dream heist;totem spinner;folding city;limbo shore;hotel corridor;architect model|layered dream thriller
tenet|Tenet|inversion turnstile;temporal pincer;freeport vault;algorithm piece;red-blue room;opera siege|time-inversion spy sci-fi
interstellar|Interstellar|Endurance ship;wormhole near Saturn;Miller's planet;TARS robot;Cooper Station;tesseract library|cosmic exploration drama
arrival|Arrival|Heptapod;Shell ship;nonlinear language;Montana site;ink circle glyph;linguist tent|first-contact linguistic sci-fi
contact|Contact|Vega signal;Machine ring;Arecibo dish;Hadden pod;starfield beach;SETI lab|first-contact scientific wonder
close_encounters|Close Encounters|Devils Tower;five-tone signal;mothership lights;mashed mountain;landing site;UFO convoy|UFO awe mystery
et|E.T.|Elliott house;moon bicycle;Speak and Spell;botanical revival;government tents;forest farewell|gentle alien suburb fantasy
men_in_black|Men in Black|MIB headquarters;neuralyzer;Noisy Cricket;alien pawn shop;worm guys;black suit agents|alien bureaucracy comedy sci-fi
ghostbusters|Ghostbusters|firehouse HQ;proton pack;PKE meter;Ecto-1;Stay Puft;Gozer temple|paranormal comedy action
beetlejuice|Beetlejuice|Neitherworld;Handbook for Recently Deceased;sandworm desert;Deetz house;striped suit;waiting room|surreal ghost comedy
addams_family|The Addams Family|Addams mansion;Morticia greenhouse;Thing hand;Wednesday crossbow avoided;gothic family hall;moonlit graveyard|macabre family gothic
munsters|The Munsters|Mockingbird Lane;Munster mansion;Drag-U-La;Herman lab;Lily parlor;Grandpa's dungeon|retro monster sitcom gothic
dark_shadows|Dark Shadows|Collinwood Manor;Barnabas Collins;Widow's Hill;Angelique curse;Blue Whale tavern;vampire cane|soap-opera vampire gothic
sleepy_hollow|Sleepy Hollow|Headless Horseman;Ichabod investigation;Tree of the Dead;Hessian rider;covered bridge;colonial church|colonial gothic mystery
penny_dreadful|Penny Dreadful|London demimonde;Vanessa Ives;Dorian portrait;Frankenstein lab;Grand Guignol;witch coven|victorian monster gothic
the_magicians|The Magicians|Brakebills;Fillory;Neitherlands;Library order;hedge witch;spell discipline|mature magical academy fantasy
charmed|Charmed|Halliwells;Book of Shadows;Power of Three;P3 club;Whitelighter orb;demon vanquish|urban witch family fantasy
witcher_books|Witcher Saga|Cintra;Ciri prophecy;Lodge of Sorceresses;Thanedd coup;Northern Kingdoms;Nilfgaardian court|political monster fantasy
name_of_the_wind|The Kingkiller Chronicle|University;Archives;Eolian stage;Ademre;the Chandrian;Naming magic|lyrical academy fantasy
gentleman_bastards|Gentleman Bastards|Camorr;Gentleman Bastards;Elderglass towers;Capa Barsavi;Sinspire;Thorn of Camorr|fantasy con artist heist
first_law|The First Law|Union court;Inquisition;Northmen;Magi;Gurkhul;Circle of the World|grimdark political fantasy
black_company|The Black Company|Annals;Lady's Tower;Taken;Company standard;Taglios;Shadowmasters|mercenary dark fantasy
powder_mage|Powder Mage|Adro;powder trance;Privileged sorcery;Field Marshal;Kresimir cult;flintlock rifle|gunpowder revolution fantasy
lightbringer|Lightbringer|Chromeria;Prism;luxin drafting;Blackguard;satrapy court;colored lenses|color magic political fantasy
broken_earth|The Broken Earth|Stillness;orogene;Fulcrum;stone eater;fifth season;obelisk network|seismic apocalypse fantasy
memory_sorrow_thorn|Memory Sorrow Thorn|Hayholt;Sithi;Storm King;Bright-Nail;Erkynland;Aldheorte forest|classic epic fantasy
shannara|Shannara|Four Lands;Druid Keep;Ellcrys tree;Sword of Shannara;Federation army;Elven court|post-apocalyptic elf fantasy
belgariad|The Belgariad|Riva;Aldur's Orb;Mallorea;Sendaria;Prophecy of Light;Polgara tower|classic prophecy fantasy
riftwar|Riftwar Cycle|Midkemia;Kelewan;Tsurani;Crydee;magician Pug;rift gate|portal war fantasy
dragonlance|Dragonlance|Krynn;Solamnic Knights;Dragon Highlords;Towers of High Sorcery;dragonlance spear;Qualinesti|classic dragon war fantasy
wheel_of_time_books|Wheel of Time Books|Tar Valon;Aes Sedai;Aiel Waste;Forsaken;Dragon Banner;Waygate|prophecy weaving epic fantasy
red_rising|Red Rising|Society colors;Gold Peerless Scarred;Mars Institute;Razor blade;Sons of Ares;Iron Rain|class war space opera
the_expanse_books|The Expanse Books|Rocinante;OPA;Laconia;protomolecule gate;Medina Station;Belter tattoos|hard sci-fi political saga
foundation_books|Foundation Books|Trantor;Terminus;Second Foundation;psychohistory;Hari Seldon vault;Empire fall|mathematical galactic history
dune_books|Dune Books|Arrakis;Fremen sietch;Bene Gesserit;spice melange;sandworm;Golden Path|desert messiah space epic
hyperion|Hyperion Cantos|Time Tombs;Shrike;Hegemony;Ousters;WorldWeb;farcasters|literary space pilgrimage
ender_game|Ender's Game|Battle School avoided;Command fleet;Formics;ansible;Ender strategy;Eros command|military strategy sci-fi
old_mans_war|Old Man's War|Colonial Defense Forces;CDF soldiers;BrainPal;skip drive;Consu;colony world|military space opera
the_culture|The Culture|Culture Minds;GSV ship;Special Circumstances;Orbitals;drone companion;knife missile|post-scarcity space opera
revelation_space|Revelation Space|Conjoiners;Ultras;Inhibitors;Yellowstone;Nostalgia for Infinity;melding plague|gothic hard sci-fi
neuromancer|Neuromancer|Chiba City;matrix cowboy;Wintermute;Tessier-Ashpool;razorgirl;Sprawl|foundational cyberpunk noir
snow_crash|Snow Crash|Metaverse;Deliverator;Raven biker;Raft city;L. Bob Rife;katana courier|satirical cyberpunk adventure
ready_player_one|Ready Player One|OASIS;Halliday quest;IOI Sixers;DeLorean avatar;Anorak castle;Easter egg key|VR nostalgia adventure
altered_carbon_books|Altered Carbon Books|Takeshi Kovacs;Envoy corps;stack immortality;Harlan's World;needlecast;Meth palace|sleeve-swapping cyber noir
blade_runner_book|Do Androids Dream of Electric Sheep|empathy box;Mercerism;electric animals;Voigt-Kampff;San Francisco decay;andies|android existential noir
roadside_picnic|Roadside Picnic|Harmont Zone;stalker pouch;golden sphere;anomaly field;Institute perimeter;Roadside artifact|alien visitation zone mystery
solaris|Solaris|Solaris ocean;Kelvin station;neutrino visitor;library room;planetary consciousness;research deck|psychological first-contact sci-fi
annihilation|Annihilation|Area X;Southern Reach;shimmer border;biologist journal;lighthouse tower;mutated marsh|ecological cosmic horror
southern_reach|Southern Reach Trilogy|Area X;Control office;seance and science;topographical anomaly;forgotten coast;biologist expedition|bureaucratic eco-horror
the_left_hand_darkness|The Left Hand of Darkness|Gethen;Ekumen envoy;Karhide;Orgoreyn;ice journey;ansible report|anthropological ice planet sci-fi
earthsea_books|Earthsea Books|Roke;true names;Gont;Atuan tombs;dragon speech;Archipelago|island wizard myth fantasy
discworld_books|Discworld Books|Ankh-Morpork;Unseen University;Night Watch;Witches of Lancre;Death's domain;Assassins Guild|satirical fantasy multiverse
good_omens_book|Good Omens Book|Aziraphale bookshop;Crowley Bentley;Ineffable Plan;Them village;Four Horsepersons;flaming sword|apocalyptic comedy fantasy
american_gods_book|American Gods Book|House on the Rock;Old Gods;New Gods;Lakeside;storm coin;roadside motel|mythic Americana fantasy
the_stand|The Stand|Captain Trips;Mother Abagail;Flagg;Boulder Free Zone;Las Vegas empire;superflu road|post-plague mythic horror
it_stephen_king|It|Derry;Pennywise;Losers Club adult return;Neibolt Street;deadlights;storm drain|cosmic small-town horror
dark_tower_books|Dark Tower Books|Gilead;gunslinger;Ka-tet;Mid-World;Crimson King;rose field|weird western multiverse
mistborn_era2|Mistborn Era Two|Elendel;Twinborn lawkeeper;metal vial;Pathian earring;Set conspiracy;roughs town|industrial allomancy western
the_locked_tomb|The Locked Tomb|Ninth House;necromancer cavalier;Lyctor lab;bone construct;Canaan House;Emperor's tomb|gothic necromantic space fantasy
gideon_the_ninth|Gideon the Ninth|Ninth House skull paint;Canaan House trials;cavalier sword;necromantic keys;bone wards;Lyctor mystery|gothic necromancer cavalier mystery
"""


WIDE_FRANCHISE_ROWS += parse_wide_rows(BULK_FRANCHISE_ROWS_TEXT)


SPECS += [build_wide_spec(row, lens) for row in WIDE_FRANCHISE_ROWS for lens in WIDE_LENSES]


MODULE_CATALOG = [make_specific_module(spec) for spec in SPECS]


def get_modules():
    return [dict(item) for item in MODULE_CATALOG]
