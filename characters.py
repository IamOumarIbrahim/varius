# Database of 50 selectable characters with their stats and custom pixel color themes.

CHARACTERS_DB = [
  {
    "name": "Ariana Grande",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 85, "move_speed": 1.25, "armor": 1, "magnet_range": 3.5 },
    "starting_weapon": "High Note Sonic Wave",
    "unique_ability": {
      "name": "Positions Shift",
      "description": "Every 12 seconds, switches between three stances: Combat (+20% damage), Agile (+30% speed), and Magnet (+100% item pickup radius)."
    },
    "crafting_bonus": "+20% discount when purchasing materials or accessories from NPCs.",
    "theme": {
      "hair": (90, 60, 40),      # High ponytail brown
      "skin": (240, 190, 150),
      "shirt": (230, 200, 210),   # Pink top
      "pants": (80, 80, 90),
      "eyes": (60, 40, 20),
      "has_ponytail": True
    }
  },
  {
    "name": "Sabrina Carpenter",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 90, "move_speed": 1.2, "armor": 2, "magnet_range": 3.0 },
    "starting_weapon": "Espresso Shot",
    "unique_ability": {
      "name": "Nonsense Outro",
      "description": "Killing a boss triggers a fast-paced lyrical explosion that disorients all surrounding enemies, making them attack each other for 6 seconds."
    },
    "crafting_bonus": "Allows alchemy stations and cooking pots to instantly double food or potion outputs 15% of the time.",
    "theme": {
      "hair": (245, 220, 120),    # Blonde bangs
      "skin": (255, 210, 180),
      "shirt": (60, 60, 80),      # Dark blue corset
      "pants": (230, 230, 240),   # White skirt
      "eyes": (50, 120, 200)
    }
  },
  {
    "name": "Damon Salvatore",
    "origin": "The Vampire Diaries",
    "stats": { "max_health": 140, "move_speed": 1.35, "armor": 4, "magnet_range": 1.5 },
    "starting_weapon": "Vampiric Claws",
    "unique_ability": {
      "name": "Crow Metamorphosis",
      "description": "When health drops below 30%, turns into an invincible crow for 4 seconds, restoring 2% HP per second and ignoring all terrain blocks."
    },
    "crafting_bonus": "Gains a +15% damage and mining speed boost during the in-game night cycle.",
    "theme": {
      "hair": (30, 25, 25),       # Jet black messy
      "skin": (245, 230, 220),    # Pale vampire skin
      "shirt": (20, 20, 20),      # Black leather jacket
      "pants": (40, 40, 45),      # Dark jeans
      "eyes": (80, 130, 240)      # Piercing blue eyes
    }
  },
  {
    "name": "Rory Gilmore",
    "origin": "Gilmore Girls",
    "stats": { "max_health": 95, "move_speed": 1.05, "armor": 2, "magnet_range": 4.0 },
    "starting_weapon": "Heavy Ivy League Textbook",
    "unique_ability": {
      "name": "Procrastination Panic",
      "description": "Whenever more than 25 enemies are on screen, attacks fire 50% faster as stress levels spike."
    },
    "crafting_bonus": "Unlocks recipe blueprints one tier early and increases book/scroll crafting speed by 50%.",
    "theme": {
      "hair": (100, 60, 30),      # Brunette bob
      "skin": (255, 220, 190),
      "shirt": (200, 190, 170),   # Chilton knit sweater
      "pants": (50, 50, 80),      # Blue skirt
      "eyes": (60, 140, 200)
    }
  },
  {
    "name": "Taylor Swift",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 95, "move_speed": 1.15, "armor": 2, "magnet_range": 4.5 },
    "starting_weapon": "Spangled Guitar Strike",
    "unique_ability": {
      "name": "Eras Tour",
      "description": "Every 60 seconds, shifts the biome background tune, granting massive passive bonuses depending on the active 'Era' (e.g., Red grants fire trails, Reputation grants shadow armor)."
    },
    "crafting_bonus": "Increases the selling price of all handmade items and weapons to merchants by 25%.",
    "theme": {
      "hair": (230, 200, 100),    # Blonde with bangs
      "skin": (255, 220, 190),
      "shirt": (180, 40, 180),    # Sparkly purple
      "pants": (240, 100, 180),   # Pink boots
      "eyes": (40, 120, 220)
    }
  },
  {
    "name": "Wednesday Addams",
    "origin": "Wednesday / Addams Family",
    "stats": { "max_health": 105, "move_speed": 1.1, "armor": 3, "magnet_range": 1.8 },
    "starting_weapon": "Thing (Severed Hand)",
    "unique_ability": {
      "name": "Cello Requiem",
      "description": "Periodically summons dark shockwaves that slow down enemy movement speed by 35% and deals shadow damage over time."
    },
    "crafting_bonus": "Harvests rare monster drops and dark crafting materials at double the normal drop rate.",
    "theme": {
      "hair": (15, 15, 20),       # Black braids
      "skin": (245, 245, 245),    # Pale white skin
      "shirt": (20, 20, 20),      # Black uniform
      "pants": (20, 20, 20),      # Black skirt
      "eyes": (20, 20, 25),
      "has_braids": True
    }
  },
  {
    "name": "Walter White",
    "origin": "Breaking Bad",
    "stats": { "max_health": 100, "move_speed": 0.95, "armor": 2, "magnet_range": 2.0 },
    "starting_weapon": "Fulminated Mercury",
    "unique_ability": {
      "name": "Say My Name",
      "description": "Consuming potions provides temporary complete immunity to debuffs and doubles weapon chemical splash damage radii for 8 seconds."
    },
    "crafting_bonus": "Crafts potions, bombs, and chemical weapons without ever using up the water bottle/glass container resource.",
    "theme": {
      "hair": (120, 80, 40),      # Bald / brown goatee
      "skin": (245, 210, 175),
      "shirt": (210, 195, 145),   # Yellow hazmat shirt
      "pants": (180, 170, 120),   # Khakis
      "eyes": (60, 120, 180),
      "is_bald": True,
      "has_goatee": True
    }
  },
  {
    "name": "Michael Scott",
    "origin": "The Office",
    "stats": { "max_health": 110, "move_speed": 1.1, "armor": 1, "magnet_range": 2.2 },
    "starting_weapon": "Dundie Award Projectile",
    "unique_ability": { "name": "Threat Level Midnight", "description": "Accidentally fires a chaotic barrage of bullets in all directions when taking hit damage greater than 20 HP." },
    "crafting_bonus": "Reduces copper, silver, and gold resource costs by 10% through 'aggressive corporate management'.",
    "theme": {
      "hair": (50, 45, 45),       # Dark slicked-back
      "skin": (250, 215, 180),
      "shirt": (45, 55, 90),      # Navy suit jacket
      "pants": (45, 55, 90),      # Navy pants
      "eyes": (60, 40, 20)
    }
  },
  {
    "name": "Homelander",
    "origin": "The Boys",
    "stats": { "max_health": 160, "move_speed": 1.4, "armor": 6, "magnet_range": 1.2 },
    "starting_weapon": "Laser Eyes",
    "unique_ability": {
      "name": "Fragile Ego",
      "description": "Damage scales up to +100% the higher his current health is, but drops significantly if he takes consecutive hits."
    },
    "crafting_bonus": "Instantly melts raw iron and lead ores directly in his inventory without needing a forge or anvil.",
    "theme": {
      "hair": (230, 210, 120),    # Blonde combed
      "skin": (255, 220, 185),
      "shirt": (35, 60, 140),     # Bright blue suit
      "pants": (35, 60, 140),
      "eyes": (255, 0, 0),        # Red laser eyes glowing
      "has_cape": True,
      "cape_color": (200, 30, 30)
    }
  },
  {
    "name": "Harry Potter",
    "origin": "Wizarding World",
    "stats": { "max_health": 90, "move_speed": 1.15, "armor": 2, "magnet_range": 2.8 },
    "starting_weapon": "Holly Wand (Expelliarmus)",
    "unique_ability": {
      "name": "Invisibility Cloak",
      "description": "Standing completely still for 2.5 seconds renders the player invisible, stopping enemy aggro and boosting health regeneration."
    },
    "crafting_bonus": "Grants all crafted staves, robes, and magical equipment a guaranteed positive random modifier/enchantment.",
    "theme": {
      "hair": (35, 30, 30),       # Messy black
      "skin": (255, 220, 185),
      "shirt": (20, 20, 20),      # Black wizard robe
      "pants": (70, 70, 70),      # Dark grey
      "eyes": (50, 180, 50),      # Bright green eyes
      "has_scar": True
    }
  },
  {
    "name": "Katniss Everdeen",
    "origin": "The Hunger Games",
    "stats": { "max_health": 115, "move_speed": 1.25, "armor": 3, "magnet_range": 1.7 },
    "starting_weapon": "Mockingjay Bow",
    "unique_ability": {
      "name": "Tracker Jacker Nest",
      "description": "Ranged arrow critical strikes have a 20% chance to drop a wasp nest, sending homing tracker jackers to poison surrounding enemy units."
    },
    "crafting_bonus": "Can craft all bow variants, wood platforms, and basic hunting arrows utilizing half the standard wood material costs.",
    "theme": {
      "hair": (70, 45, 25),       # Dark braid
      "skin": (240, 200, 160),
      "shirt": (30, 30, 30),      # Dark hunting jacket
      "pants": (80, 65, 45),      # Brown trousers
      "eyes": (80, 90, 100),
      "has_braids": True
    }
  },
  {
    "name": "Barbie",
    "origin": "Barbie",
    "stats": { "max_health": 100, "move_speed": 1.2, "armor": 4, "magnet_range": 3.0 },
    "starting_weapon": "Fashion Purse Slap",
    "unique_ability": {
      "name": "You Can Be Anything",
      "description": "At the start of every game level, choose one passive role bonus: Doctor (+Regen), Astronaut (+Jump Height), or Engineer (+Mining Speed)."
    },
    "crafting_bonus": "Can change the aesthetic, dye colors, or appearance of any armor piece without consuming crafting dyes.",
    "theme": {
      "hair": (255, 230, 110),    # Bright blonde
      "skin": (255, 210, 180),
      "shirt": (255, 80, 180),    # Neon pink top
      "pants": (255, 80, 180),    # Pink skirt
      "eyes": (60, 130, 220)
    }
  },
  {
    "name": "Billie Eilish",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 105, "move_speed": 1.1, "armor": 3, "magnet_range": 2.5 },
    "starting_weapon": "Bad Guy Bassline",
    "unique_ability": {
      "name": "Ocean Eyes",
      "description": "Freezes all enemies within a wide visible ring for 3.5 seconds whenever a major horde threshold arrives."
    },
    "crafting_bonus": "Can synthesize custom stealth gear and shadow clothing utilizing bioluminescent materials.",
    "theme": {
      "hair": (50, 200, 80),      # Neon green roots & black hair
      "skin": (245, 235, 225),
      "shirt": (40, 40, 40),      # Oversized black tee
      "pants": (40, 40, 40),
      "eyes": (100, 180, 220)
    }
  },
  {
    "name": "Geralt of Rivia",
    "origin": "The Witcher",
    "stats": { "max_health": 150, "move_speed": 1.2, "armor": 6, "magnet_range": 1.4 },
    "starting_weapon": "Silver Sword",
    "unique_ability": {
      "name": "Igni Sign",
      "description": "Deploys a frontal cone of fire every 8 seconds that burns away light enemy units and ignites combustible world tiles."
    },
    "crafting_bonus": "Identifies the exact stats and hidden loot drops of monsters simply by approaching them.",
    "theme": {
      "hair": (220, 220, 220),    # Long white hair
      "skin": (230, 220, 210),    # Pale, scarred
      "shirt": (40, 40, 40),      # Black studded leather
      "pants": (30, 30, 30),
      "eyes": (240, 180, 30),     # Yellow cat eyes
      "has_scar": True
    }
  },
  {
    "name": "Lara Croft",
    "origin": "Tomb Raider",
    "stats": { "max_health": 120, "move_speed": 1.3, "armor": 4, "magnet_range": 2.2 },
    "starting_weapon": "Dual Pistols",
    "unique_ability": {
      "name": "Relic Hunter",
      "description": "Reveals hidden treasure chests and buried underground structures directly on the player mini-map radar view."
    },
    "crafting_bonus": "+30% mining speed when using pickaxes on standard subterranean stones, sandstone, and granite blocks.",
    "theme": {
      "hair": (90, 50, 25),       # Brown braid
      "skin": (245, 205, 160),
      "shirt": (40, 120, 130),    # Turquoise tank top
      "pants": (90, 80, 60),      # Brown shorts
      "eyes": (80, 60, 40),
      "has_ponytail": True
    }
  },
  {
    "name": "Kratos",
    "origin": "God of War",
    "stats": { "max_health": 180, "move_speed": 1.0, "armor": 8, "magnet_range": 1.1 },
    "starting_weapon": "Blades of Chaos",
    "unique_ability": {
      "name": "Spartan Rage",
      "description": "Taking heavy cumulative damage fills a rage meter. When activated, grants temporary invincibility and massive melee shockwaves."
    },
    "crafting_bonus": "Upgrades physical weapons at anvils using fewer rare metal ingots than other characters.",
    "theme": {
      "hair": (160, 160, 160),    # Bald / red tattoo on head
      "skin": (240, 235, 235),    # Ash white skin
      "shirt": (120, 60, 40),     # Leather shoulder strap
      "pants": (80, 40, 30),      # Red/bronze skirt kilt
      "eyes": (220, 50, 50),
      "is_bald": True,
      "has_tattoo": True
    }
  },
  {
    "name": "Sonic the Hedgehog",
    "origin": "Sonic the Hedgehog",
    "stats": { "max_health": 90, "move_speed": 1.8, "armor": 2, "magnet_range": 2.6 },
    "starting_weapon": "Spin Dash",
    "unique_ability": {
      "name": "Super Sonic Ring Shield",
      "description": "Collecting 100 gold coins creates a golden ring barrier that completely negates the next incoming attack instance."
    },
    "crafting_bonus": "+40% standard exploration and running speed when traveling across flat grass or asphalt blocks.",
    "theme": {
      "hair": (30, 80, 220),      # Blue quills
      "skin": (255, 210, 160),    # Peach snout / belly
      "shirt": (30, 80, 220),     # Blue torso
      "pants": (220, 30, 30),     # Red sneakers shoes
      "eyes": (40, 180, 40),
      "is_sonic": True
    }
  },
  {
    "name": "Pikachu",
    "origin": "Pokémon",
    "stats": { "max_health": 85, "move_speed": 1.4, "armor": 1, "magnet_range": 2.0 },
    "starting_weapon": "Thunderbolt",
    "unique_ability": {
      "name": "Volt Tackle",
      "description": "Dashing forward transforms Pikachu into an electrical surge that chains lightning strikes between up to 10 separate monsters."
    },
    "crafting_bonus": "Acts as a mobile power source, letting automated base defenses or electronic crafting wire networks run without fuel.",
    "theme": {
      "hair": (255, 220, 50),     # Yellow body
      "skin": (255, 220, 50),     # Yellow face
      "shirt": (255, 220, 50),    # Yellow belly
      "pants": (255, 220, 50),
      "eyes": (20, 20, 20),
      "is_pikachu": True
    }
  },
  {
    "name": "Spider-Man",
    "origin": "Marvel Comics",
    "stats": { "max_health": 125, "move_speed": 1.45, "armor": 4, "magnet_range": 2.0 },
    "starting_weapon": "Web Shooter Slam",
    "unique_ability": {
      "name": "Spidey Sense",
      "description": "Grants a permanent passive 25% chance to dodge any incoming physical attack or projectile trap perfectly."
    },
    "crafting_bonus": "Can craft strong vertical grappling hooks and climbing ropes with simple fiber materials.",
    "theme": {
      "hair": (200, 30, 30),      # Red mask
      "skin": (200, 30, 30),
      "shirt": (200, 30, 30),     # Red/blue suit
      "pants": (30, 60, 180),     # Blue legs
      "eyes": (255, 255, 255),    # White big mask eyes
      "is_masked": True
    }
  },
  {
    "name": "Batman",
    "origin": "DC Comics",
    "stats": { "max_health": 140, "move_speed": 1.2, "armor": 7, "magnet_range": 1.6 },
    "starting_weapon": "Batarang",
    "unique_ability": {
      "name": "The Dark Knight",
      "description": "Attacking unsuspecting enemies from above or out of darkness deals 3x critical sneak attack damage."
    },
    "crafting_bonus": "Allows engineering items, radar trackers, and utility gadgets to be built without needing complex blueprints.",
    "theme": {
      "hair": (20, 20, 25),       # Black cowl
      "skin": (245, 215, 180),    # Mouth visible
      "shirt": (60, 60, 65),      # Grey suit
      "pants": (30, 30, 35),      # Dark grey pants
      "eyes": (255, 255, 255),    # Glowing slit eyes
      "has_cape": True,
      "cape_color": (15, 15, 20)
    }
  },
  {
    "name": "Deadpool",
    "origin": "Marvel Universe",
    "stats": { "max_health": 110, "move_speed": 1.25, "armor": 3, "magnet_range": 1.5 },
    "starting_weapon": "Dual Katanas",
    "unique_ability": {
      "name": "Fourth Wall Break",
      "description": "Passively regenerates 3% of maximum health every single second, regardless of current combat status or active enemy debuffs."
    },
    "crafting_bonus": "Has a quirky chance to randomly mutate a weapon into a completely different, higher-tier variant while crafting.",
    "theme": {
      "hair": (180, 20, 20),      # Red mask
      "skin": (180, 20, 20),
      "shirt": (180, 20, 20),     # Red suit with black straps
      "pants": (20, 20, 20),      # Black straps
      "eyes": (255, 255, 255),    # White mask slits
      "is_masked": True
    }
  },
  {
    "name": "Wolverine",
    "origin": "X-Men",
    "stats": { "max_health": 165, "move_speed": 1.15, "armor": 6, "magnet_range": 1.0 },
    "starting_weapon": "Adamantium Claws",
    "unique_ability": {
      "name": "Berserker Slash",
      "description": "Melee strikes slice clean through solid terrain blocks up to 2 tiles deep, quickly creating pathways while evading waves."
    },
    "crafting_bonus": "Can mine hard volcanic obsidian or hellstone blocks using basic standard digging tools.",
    "theme": {
      "hair": (255, 215, 0),      # Yellow cowl with black wings
      "skin": (250, 210, 180),
      "shirt": (255, 215, 0),     # Yellow suit
      "pants": (30, 70, 180),     # Blue pants
      "eyes": (255, 255, 255),
      "has_cowl_wings": True
    }
  },
  {
    "name": "SpongeBob SquarePants",
    "origin": "SpongeBob SquarePants",
    "stats": { "max_health": 100, "move_speed": 1.05, "armor": 5, "magnet_range": 2.5 },
    "starting_weapon": "Bubble Wand",
    "unique_ability": {
      "name": "Absorbent Body",
      "description": "Blunt physical attacks from enemies are automatically cushioned, reducing overall damage intake by a flat 40%."
    },
    "crafting_bonus": "Can breathe completely underwater without an oxygen meter and swims at maximum base velocity.",
    "theme": {
      "hair": (255, 230, 40),     # Yellow sponge body
      "skin": (255, 230, 40),
      "shirt": (255, 255, 255),   # White shirt + red tie
      "pants": (120, 80, 40),      # Brown square pants
      "eyes": (80, 180, 255),
      "is_spongebob": True
    }
  },
  {
    "name": "Rick Sanchez",
    "origin": "Rick and Morty",
    "stats": { "max_health": 95, "move_speed": 1.15, "armor": 3, "magnet_range": 2.4 },
    "starting_weapon": "Portal Gun Blast",
    "unique_ability": {
      "name": "Dimension Hop",
      "description": "When completely surrounded by a dense horde, portals open to drop a random environmental obstacle onto the battlefield."
    },
    "crafting_bonus": "+35% speed when constructing electronics, machinery wiring networks, or laser defense traps.",
    "theme": {
      "hair": (160, 210, 230),    # Spiky blue hair
      "skin": (230, 210, 190),
      "shirt": (120, 180, 210),   # Blue shirt + lab coat
      "pants": (100, 70, 50),     # Brown pants
      "eyes": (20, 20, 20)
    }
  },
  {
    "name": "Bella Swan",
    "origin": "Twilight",
    "stats": { "max_health": 90, "move_speed": 1.0, "armor": 2, "magnet_range": 2.0 },
    "starting_weapon": "Clumsy Trip Tripping",
    "unique_ability": {
      "name": "Mental Shield",
      "description": "Completely immune to status debuffs like confusion, slowness, or curse fields projected by magical monster types."
    },
    "crafting_bonus": "Attracts supernatural protective companion units to fight alongside her with 20% higher stat values.",
    "theme": {
      "hair": (80, 50, 30),       # Brown straight hair
      "skin": (250, 215, 185),
      "shirt": (60, 90, 70),      # Green jacket
      "pants": (40, 50, 70),      # Blue jeans
      "eyes": (90, 70, 50)
    }
  },
  {
    "name": "Edward Cullen",
    "origin": "Twilight",
    "stats": { "max_health": 135, "move_speed": 1.6, "armor": 5, "magnet_range": 1.5 },
    "starting_weapon": "Marble Punch",
    "unique_ability": {
      "name": "Diamond Skin",
      "description": "When standing out in bright outdoor desert or snow sunlight biomes, deflects 25% of incoming missile projectiles back at enemies."
    },
    "crafting_bonus": "Can cross spiked floors or floor hazards without triggering physical traps or terrain damage.",
    "theme": {
      "hair": (110, 80, 50),      # Bronze styled hair
      "skin": (245, 245, 250),    # Pale marble skin
      "shirt": (45, 45, 55),      # Grey pea coat
      "pants": (25, 25, 30),      # Dark pants
      "eyes": (200, 160, 50),     # Amber eyes
      "sparkles_outdoor": True
    }
  },
  {
    "name": "Jon Snow",
    "origin": "Game of Thrones",
    "stats": { "max_health": 130, "move_speed": 1.1, "armor": 5, "magnet_range": 1.3 },
    "starting_weapon": "Longclaw (Valyrian Steel)",
    "unique_ability": {
      "name": "Direwolf Pack",
      "description": "Summons Ghost the direwolf to seek out and bite moving targets, slowing them to a crawl while dealing heavy tearing damage."
    },
    "crafting_bonus": "Completely immune to cold/freezing slow effects when traversing sub-zero frost and ice biomes.",
    "theme": {
      "hair": (25, 20, 20),       # Dark curly hair
      "skin": (245, 215, 185),
      "shirt": (15, 15, 15),      # Night's Watch heavy fur coat
      "pants": (25, 25, 25),      # Black leather pants
      "eyes": (40, 30, 20),
      "has_fur": True
    }
  },
  {
    "name": "Daenerys Targaryen",
    "origin": "Game of Thrones",
    "stats": { "max_health": 100, "move_speed": 1.15, "armor": 2, "magnet_range": 2.0 },
    "starting_weapon": "Dragon Flame Breath",
    "unique_ability": {
      "name": "Dracarys",
      "description": "Every 20 seconds, a dragon shadows the field, bathing a giant vertical column of tiles in extreme purifying fire."
    },
    "crafting_bonus": "Completely unaffected by environmental lava tiles or underworld fire burn debuffs.",
    "theme": {
      "hair": (245, 245, 245),    # Silver/white braided hair
      "skin": (255, 215, 180),
      "shirt": (40, 100, 150),    # Blue dress
      "pants": (230, 230, 240),
      "eyes": (130, 80, 180)      # Violet eyes
    }
  },
  {
    "name": "Travis Scott",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 110, "move_speed": 1.25, "armor": 3, "magnet_range": 3.0 },
    "starting_weapon": "Astroworld Soundwave",
    "unique_ability": {
      "name": "Sicko Mode",
      "description": "Entering a killing streak of 100 drops a giant meteor planet speaker onto the map, shattering scenery blocks and crushing ground monsters."
    },
    "crafting_bonus": "Speeds up block placement and structural assembly times by 30% when building arenas.",
    "theme": {
      "hair": (30, 30, 30),       # Dark braids
      "skin": (135, 80, 45),      # Dark skin
      "shirt": (95, 60, 40),      # Brown Cactus Jack tee
      "pants": (50, 50, 50),
      "eyes": (30, 30, 30)
    }
  },
  {
    "name": "The Weeknd",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 100, "move_speed": 1.2, "armor": 4, "magnet_range": 2.7 },
    "starting_weapon": "Blinding Lights Laser",
    "unique_ability": {
      "name": "After Hours Night walk",
      "description": "Emits a persistent neon aura in deep caves that illuminates dark map foggy zones while draining health from shadowed enemies."
    },
    "crafting_bonus": "Can see structural block outline grids and hidden wires through solid stone walls.",
    "theme": {
      "hair": (30, 25, 25),       # Afro styled hair
      "skin": (120, 75, 40),
      "shirt": (200, 30, 30),     # Signature red suit coat
      "pants": (20, 20, 20),      # Black tie/pants
      "eyes": (40, 30, 20)
    }
  },
  {
    "name": "Luke Skywalker",
    "origin": "Star Wars",
    "stats": { "max_health": 115, "move_speed": 1.25, "armor": 4, "magnet_range": 2.5 },
    "starting_weapon": "Lightsaber Strike",
    "unique_ability": {
      "name": "Force Pull Vortex",
      "description": "Activating the ability physically yanks all loose drops, resources, and lightweight enemies in a massive circle directly to him."
    },
    "crafting_bonus": "Can dismantle mechanical structures and scrap assemblies to recover 100% of the base material resources.",
    "theme": {
      "hair": (160, 120, 60),     # Dirty blonde
      "skin": (255, 220, 185),
      "shirt": (240, 235, 210),   # Tatoiine beige tunic
      "pants": (200, 190, 160),
      "eyes": (40, 100, 200),
      "has_lightsaber": True,
      "saber_color": (30, 220, 50) # Green lightsaber
    }
  },
  {
    "name": "Darth Vader",
    "origin": "Star Wars",
    "stats": { "max_health": 170, "move_speed": 0.9, "armor": 9, "magnet_range": 1.8 },
    "starting_weapon": "Sith Saber Throw",
    "unique_ability": {
      "name": "Force Choke Hold",
      "description": "Lifts the strongest visible enemy miniboss into the air, rendering them completely helpless while dealing continuous crushing damage."
    },
    "crafting_bonus": "Forges red glowing lights and heavy cybernetic alloy items with 25% higher armor output properties.",
    "theme": {
      "hair": (15, 15, 20),       # Black helmet
      "skin": (15, 15, 20),       # Black helmet face
      "shirt": (25, 25, 30),      # Chest plate controls
      "pants": (25, 25, 30),
      "eyes": (220, 30, 30),      # Glowing red lenses
      "has_cape": True,
      "cape_color": (10, 10, 15),
      "has_lightsaber": True,
      "saber_color": (255, 30, 30) # Red lightsaber
    }
  },
  {
    "name": "Elsa",
    "origin": "Frozen",
    "stats": { "max_health": 95, "move_speed": 1.15, "armor": 3, "magnet_range": 2.2 },
    "starting_weapon": "Ice Shard Flurry",
    "unique_ability": {
      "name": "Let It Go Storm",
      "description": "Creates a sprawling blizzard circle that turns normal ground water pools into solid ice blocks, slipping enemies and providing clear platforms."
    },
    "crafting_bonus": "Can freely shape and construct functional defensive walls and castles out of standard snow and ice blocks.",
    "theme": {
      "hair": (230, 240, 250),    # Ice blonde braid
      "skin": (255, 225, 200),
      "shirt": (120, 220, 240),   # Light blue gown
      "pants": (160, 240, 255),
      "eyes": (60, 160, 240),
      "has_ponytail": True
    }
  },
  {
    "name": "Naruto Uzumaki",
    "origin": "Naruto",
    "stats": { "max_health": 130, "move_speed": 1.35, "armor": 4, "magnet_range": 1.9 },
    "starting_weapon": "Rasengan Sphere",
    "unique_ability": {
      "name": "Shadow Clone Horde",
      "description": "Summons 5 mirror decoy clones that mimic the starting weapon projectile direction before dissipating after 5 seconds."
    },
    "crafting_bonus": "Reduces stamina and food consumption bars significantly, allowing prolonged running, jumping, and wall-climbing.",
    "theme": {
      "hair": (240, 220, 40),     # Spiky yellow hair
      "skin": (250, 215, 180),
      "shirt": (230, 100, 30),    # Orange/black jumpsuit
      "pants": (230, 100, 30),
      "eyes": (60, 120, 240),
      "has_headband": True
    }
  },
  {
    "name": "Gojo Satoru",
    "origin": "Jujutsu Kaisen",
    "stats": { "max_health": 120, "move_speed": 1.3, "armor": 10, "magnet_range": 2.5 },
    "starting_weapon": "Divergent Fist",
    "unique_ability": {
      "name": "Infinity Barrier",
      "description": "Creates a space barrier where slow-moving projectiles automatically halt and vanish before making physical contact with his model."
    },
    "crafting_bonus": "Can instantly bypass dungeon door locks or block access restrictions without needing specific keys.",
    "theme": {
      "hair": (245, 245, 245),    # Spiky white hair
      "skin": (255, 220, 185),
      "shirt": (30, 30, 45),      # Black high-collar coat
      "pants": (30, 30, 45),
      "eyes": (20, 20, 25),       # Blindfolded black wrap
      "has_blindfold": True
    }
  },
  {
    "name": "Indiana Jones",
    "origin": "Indiana Jones",
    "stats": { "max_health": 120, "move_speed": 1.15, "armor": 3, "magnet_range": 2.3 },
    "starting_weapon": "Archeologist Whip",
    "unique_ability": {
      "name": "Trap Disarm Sense",
      "description": "Dungeon dart traps, pressure plates, and explosives outline brightly in a red caution hue and do not trigger if walked on."
    },
    "crafting_bonus": "Extracts double the precious gemstones (diamonds, rubies, emeralds) when mining mineral nodes.",
    "theme": {
      "hair": (100, 70, 40),      # Fedora hat brown
      "skin": (245, 210, 180),
      "shirt": (210, 200, 180),   # Tan shirt + satchel strap
      "pants": (90, 70, 50),      # Brown trousers
      "eyes": (60, 40, 20),
      "has_fedora": True
    }
  },
  {
    "name": "Jack Sparrow",
    "origin": "Pirates of the Caribbean",
    "stats": { "max_health": 110, "move_speed": 1.2, "armor": 3, "magnet_range": 2.8 },
    "starting_weapon": "Flintlock & Cutlass",
    "unique_ability": {
      "name": "Rum Stumble Dodge",
      "description": "Moves in an unpredictable, swaying path line that automatically confuses enemy targeting tracking scripts."
    },
    "crafting_bonus": "Can spot shipwreck locations and deep-sea treasure chests at extreme distances on oceanic maps.",
    "theme": {
      "hair": (60, 40, 30),       # Dreadlocks + red bandana
      "skin": (230, 195, 160),
      "shirt": (160, 150, 140),   # Pirate coat
      "pants": (40, 35, 30),
      "eyes": (20, 20, 20),
      "has_bandana": True
    }
  },
  {
    "name": "Neo",
    "origin": "The Matrix",
    "stats": { "max_health": 115, "move_speed": 1.4, "armor": 4, "magnet_range": 2.0 },
    "starting_weapon": "Code Punch Combo",
    "unique_ability": {
      "name": "Bullet Time Matrix",
      "description": "Manually trigger a 4-second global time slowdown, allowing precise positioning adjustments amidst dense bullets."
    },
    "crafting_bonus": "Rewrites crafting properties to guarantee that engineered accessories yield high stat rolls.",
    "theme": {
      "hair": (25, 25, 25),       # Black slick short
      "skin": (245, 220, 190),
      "shirt": (15, 15, 20),      # Black trench coat
      "pants": (15, 15, 20),
      "eyes": (10, 10, 15),       # Sunglasses
      "has_sunglasses": True
    }
  },
  {
    "name": "Patrick Star",
    "origin": "SpongeBob SquarePants",
    "stats": { "max_health": 190, "move_speed": 0.75, "armor": 7, "magnet_range": 1.5 },
    "starting_weapon": "Rocky Star Throw",
    "unique_ability": {
      "name": "Is This Krusty Krab?",
      "description": "Sits down blankly, gaining complete damage invulnerability for 3 seconds while releasing a concussive shockwave yell."
    },
    "crafting_bonus": "Can crush solid stone structures into smooth sand blocks using standard basic hammers.",
    "theme": {
      "hair": (255, 160, 160),    # Pink starfish body
      "skin": (255, 160, 160),
      "shirt": (150, 230, 80),    # Lime green shorts with purple flowers
      "pants": (150, 230, 80),
      "eyes": (20, 20, 20),
      "is_starfish": True
    }
  },
  {
    "name": "Ted Lasso",
    "origin": "Ted Lasso",
    "stats": { "max_health": 125, "move_speed": 1.1, "armor": 3, "magnet_range": 3.0 },
    "starting_weapon": "Soccer Ball Volley",
    "unique_ability": {
      "name": "Believe Banner",
      "description": "Plants a persistent banner team zone that increases companion health bars and weapon firing rates by 20% inside the circle."
    },
    "crafting_bonus": "NPC merchants offer rare hidden storage items and friendly dialogue perks early.",
    "theme": {
      "hair": (100, 75, 45),      # Brown side-parted / moustache
      "skin": (250, 215, 180),
      "shirt": (35, 60, 110),     # AFC Richmond blue sweater
      "pants": (60, 60, 65),      # Chino pants
      "eyes": (40, 30, 20),
      "has_mustache": True
    }
  },
  {
    "name": "Barbie Ken",
    "origin": "Barbie Movie",
    "stats": { "max_health": 110, "move_speed": 1.2, "armor": 4, "magnet_range": 2.0 },
    "starting_weapon": "Beach Mojo Sparring",
    "unique_ability": {
      "name": "Beach Off Confrontation",
      "description": "Challenges the highest tier onscreen threat to a duel, increasing direct weapon strike damage to them by 50%."
    },
    "crafting_bonus": "Can construct structural wood framing assemblies and bridges using 30% less timber raw materials.",
    "theme": {
      "hair": (245, 230, 130),    # Bleached blonde
      "skin": (245, 205, 160),    # Tan skin
      "shirt": (255, 140, 40),    # Orange beach shirt
      "pants": (80, 200, 240),    # Light blue shorts
      "eyes": (60, 140, 210)
    }
  },
  {
    "name": "Beth Harmon",
    "origin": "The Queen's Gambit",
    "stats": { "max_health": 90, "move_speed": 1.1, "armor": 2, "magnet_range": 3.2 },
    "starting_weapon": "Chess Knight Striker",
    "unique_ability": {
      "name": "Grandmaster Vision",
      "description": "Projects a grid overlay pattern onto the ground screen. Enemies walking along matching diagonal lines take immediate vulnerability spikes."
    },
    "crafting_bonus": "Doubles research parsing speeds and processing rates at automated laboratory stations.",
    "theme": {
      "hair": (220, 100, 40),     # Auburn hair bob
      "skin": (255, 225, 205),
      "shirt": (230, 230, 230),   # Black/white checkered top
      "pants": (40, 40, 40),
      "eyes": (100, 75, 45)
    }
  },
  {
    "name": "Joel Miller",
    "origin": "The Last of Us",
    "stats": { "max_health": 145, "move_speed": 1.1, "armor": 5, "magnet_range": 1.6 },
    "starting_weapon": "Custom Pump Shotgun",
    "unique_ability": {
      "name": "Listen Mode Soundwaves",
      "description": "Crouching down outlines zombie clickers, hidden traps, and buried items through solid cave wall blocks."
    },
    "crafting_bonus": "Can repair broken weapons or reinforce structural wood barricades using scrap items directly.",
    "theme": {
      "hair": (70, 60, 55),       # Grey-brown hair & full beard
      "skin": (240, 200, 165),
      "shirt": (110, 100, 60),    # Olive dirty shirt
      "pants": (50, 55, 75),      # Jeans
      "eyes": (60, 50, 45),
      "has_goatee": True # Represents full beard
    }
  },
  {
    "name": "Luffy",
    "origin": "One Piece",
    "stats": { "max_health": 150, "move_speed": 1.3, "armor": 4, "magnet_range": 2.5 },
    "starting_weapon": "Gum-Gum Pistol Punch",
    "unique_ability": {
      "name": "Gear Third Giant Fist",
      "description": "Inflates arms to execute a heavy ground hammer punch, completely destroying an entire screen area of block tiles and light targets."
    },
    "crafting_bonus": "Consuming standard meat or cookery food dishes returns three times the normal health recovery points.",
    "theme": {
      "hair": (25, 20, 20),       # Straw hat yellow + black hair
      "skin": (250, 210, 175),
      "shirt": (220, 30, 30),     # Open red shirt
      "pants": (40, 80, 180),     # Blue shorts + sash
      "eyes": (20, 20, 20),
      "has_straw_hat": True
    }
  },
  {
    "name": "Cloud Strife",
    "origin": "Final Fantasy VII",
    "stats": { "max_health": 140, "move_speed": 1.2, "armor": 5, "magnet_range": 1.8 },
    "starting_weapon": "Buster Sword Slash",
    "unique_ability": {
      "name": "Limit Break Cross-Slash",
      "description": "When the energy meter fills completely, unlocks an omni-directional sword combo that pierces block barriers and armor parameters."
    },
    "crafting_bonus": "Can fuse glowing materia crystal stones into basic standard equipment slots to add magical elemental properties.",
    "theme": {
      "hair": (245, 225, 60),     # Spiky anime blonde
      "skin": (250, 215, 185),
      "shirt": (45, 45, 60),      # SOLDIER dark blue vest
      "pants": (45, 45, 60),
      "eyes": (60, 200, 255),     # Glowing Mako eyes
      "has_buster_sword": True
    }
  },
  {
    "name": "Link",
    "origin": "The Legend of Zelda",
    "stats": { "max_health": 120, "move_speed": 1.2, "armor": 5, "magnet_range": 2.2 },
    "starting_weapon": "Master Sword Beam",
    "unique_ability": {
      "name": "Spin Attack Cyclone",
      "description": "Charging the primary attack key button executes a full radius blade spin, deflecting incoming projectiles away."
    },
    "crafting_bonus": "Can craft throwing bombs and custom clay pots that yield items when smashed.",
    "theme": {
      "hair": (230, 200, 80),     # Blonde + green cap
      "skin": (250, 215, 180),
      "shirt": (50, 150, 50),     # Green tunic
      "pants": (235, 225, 200),   # White trousers
      "eyes": (60, 140, 220),
      "has_green_cap": True
    }
  },
  {
    "name": "Billie Butcher",
    "origin": "The Boys",
    "stats": { "max_health": 135, "move_speed": 1.15, "armor": 4, "magnet_range": 1.5 },
    "starting_weapon": "Crowbar Smash Combo",
    "unique_ability": {
      "name": "Temp V Power injection",
      "description": "Consuming a special compound chemical grants laser vision and super speed mechanics for a brief 10-second period."
    },
    "crafting_bonus": "Deals an extra flat +25% damage modifier when attacking high-tier superpower boss targets.",
    "theme": {
      "hair": (35, 30, 30),       # Dark curly hair & beard
      "skin": (245, 210, 180),
      "shirt": (20, 35, 30),      # Dark floral shirt + black coat
      "pants": (25, 25, 25),
      "eyes": (255, 220, 50),     # Yellow laser glow option
      "has_goatee": True
    }
  },
  {
    "name": "Harley Quinn",
    "origin": "DC Comics",
    "stats": { "max_health": 110, "move_speed": 1.35, "armor": 3, "magnet_range": 2.2 },
    "starting_weapon": "Oversized Mallet Smash",
    "unique_ability": {
      "name": "Pop Gun Confetti Boom",
      "description": "Fires random rolling explosive joke jacks that detonate into brightly colored status confusion clouds."
    },
    "crafting_bonus": "Crafts explosive chemical powder combinations and landmine traps using half standard charcoal costs.",
    "theme": {
      "hair": (255, 255, 255),    # White pigtails (pink/blue tips)
      "skin": (255, 240, 240),    # Pale white skin
      "shirt": (200, 30, 50),     # Red/black crop top
      "pants": (30, 30, 40),      # Shorts
      "eyes": (40, 150, 240),
      "has_pigtails_split": True
    }
  },
  {
    "name": "Joker",
    "origin": "DC Comics",
    "stats": { "max_health": 105, "move_speed": 1.2, "armor": 3, "magnet_range": 2.0 },
    "starting_weapon": "Razor Playing Cards",
    "unique_ability": {
      "name": "Laughing Gas Cloud",
      "description": "Deploys a toxic gas field matrix that forces affected enemy units to walk in random directions while losing health points."
    },
    "crafting_bonus": "Can rig standard chests and background urn container boxes into deadly perimeter defense traps.",
    "theme": {
      "hair": (30, 180, 50),      # Green slicked back
      "skin": (255, 255, 255),    # White face paint
      "shirt": (120, 40, 150),    # Purple suit jacket
      "pants": (120, 40, 150),
      "eyes": (20, 20, 20),
      "has_red_smile": True
    }
  },
  {
    "name": "Lady Gaga",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 105, "move_speed": 1.15, "armor": 4, "magnet_range": 3.2 },
    "starting_weapon": "Disco Stick Laserbeam",
    "unique_ability": {
      "name": "Bad Romance Hypnosis",
      "description": "Renders up to 8 surrounding monsters friendly, causing them to group up and shield her model from incoming projectiles."
    },
    "crafting_bonus": "Allows tailor weaving loom stations to craft premium high-defense armor out of simple cloth or leather strips.",
    "theme": {
      "hair": (250, 250, 250),    # Bleach silver wig
      "skin": (255, 215, 180),
      "shirt": (40, 40, 40),      # Shiny black metallic outfit
      "pants": (40, 40, 40),
      "eyes": (120, 50, 200)
    }
  },
  {
    "name": "Chappell Roan",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 90, "move_speed": 1.2, "armor": 2, "magnet_range": 3.3 },
    "starting_weapon": "Pink Pony Club Sparkler",
    "unique_ability": {
      "name": "Femininomenon",
      "description": "Every 15 seconds, triggers a neon dance floor radius that causes all minor enemies to stop moving and dance, taking continuous damage for 4 seconds."
    },
    "crafting_bonus": "Crafts glowing vanity items, light sources, and torches without consuming any coal or gel.",
    "theme": {
      "hair": (220, 50, 20),      # Curly red
      "skin": (255, 245, 245),    # Pale white
      "shirt": (240, 100, 180),   # Glitter pink
      "pants": (50, 100, 200),    # Denim shorts
      "eyes": (80, 50, 30),
      "has_ponytail": True
    }
  },
  {
    "name": "Olivia Rodrigo",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 95, "move_speed": 1.3, "armor": 2, "magnet_range": 2.8 },
    "starting_weapon": "Driver's License Impact",
    "unique_ability": {
      "name": "Bad Idea Right?",
      "description": "Dashing forward leaves a trail of spilled automotive oil that trips enemies, slowing them by 50% and making them highly susceptible to fire damage."
    },
    "crafting_bonus": "+25% movement speed boost when traveling along custom-built sky rails or minecart tracks.",
    "theme": {
      "hair": (45, 30, 20),       # Dark brown long
      "skin": (245, 205, 165),
      "shirt": (150, 80, 220),    # Purple crop top
      "pants": (30, 30, 30),      # Black pants
      "eyes": (40, 25, 15)
    }
  },
  {
    "name": "Lorelai Gilmore",
    "origin": "Gilmore Girls",
    "stats": { "max_health": 100, "move_speed": 1.4, "armor": 1, "magnet_range": 3.0 },
    "starting_weapon": "Scalding Coffee Splat",
    "unique_ability": {
      "name": "Fast-Talking Filibuster",
      "description": "Stuns all surrounding enemies with a rapid-fire wall of text dialogue, leaving them completely frozen in place for 3 seconds."
    },
    "crafting_bonus": "Consuming caffeine or cooking pot food items gives a 2x longer stat duration buff.",
    "theme": {
      "hair": (50, 35, 25),       # Dark brown wavy
      "skin": (255, 220, 190),
      "shirt": (40, 100, 200),    # Blue coat
      "pants": (25, 25, 25),      # Black trousers
      "eyes": (80, 150, 250)
    }
  },
  {
    "name": "Steve Harrington",
    "origin": "Stranger Things",
    "stats": { "max_health": 130, "move_speed": 1.15, "armor": 5, "magnet_range": 1.8 },
    "starting_weapon": "Nail-Spiked Bat",
    "unique_ability": {
      "name": "Babysitter Protocol",
      "description": "Grants any active companion units or summoned pets a +30% boost to their maximum health and armor values while nearby."
    },
    "crafting_bonus": "Can craft complex wooden barricades and iron trapdoors directly out of the inventory without an anvil.",
    "theme": {
      "hair": (100, 65, 35),      # Volume brown coiffure
      "skin": (255, 220, 190),
      "shirt": (80, 90, 110),     # Gray member's jacket
      "pants": (60, 90, 150),     # Blue jeans
      "eyes": (70, 50, 30)
    }
  },
  {
    "name": "The Mandalorian",
    "origin": "Star Wars",
    "stats": { "max_health": 140, "move_speed": 1.2, "armor": 8, "magnet_range": 1.5 },
    "starting_weapon": "Whistling Birds Missiles",
    "unique_ability": {
      "name": "Beskar Shielding",
      "description": "Passively blocks a flat 5 damage from every incoming attack. Fully deflects environmental spike trap hits."
    },
    "crafting_bonus": "Reduces the amount of raw platinum, titanium, and titanium alloy bars needed to craft high-tier armor sets by 20%.",
    "theme": {
      "hair": (50, 50, 50),
      "skin": (85, 90, 95),       # Helmet silver-gray
      "shirt": (120, 125, 130),   # Beskar chest
      "pants": (60, 50, 45),
      "eyes": (15, 15, 15),       # Dark visor
      "is_bald": True,
      "has_cape": True,
      "cape_color": (70, 70, 70)
    }
  },
  {
    "name": "Tony Stark",
    "origin": "Marvel Universe",
    "stats": { "max_health": 100, "move_speed": 1.25, "armor": 4, "magnet_range": 2.5 },
    "starting_weapon": "Repulsor Hand Blast",
    "unique_ability": {
      "name": "House Party Protocol",
      "description": "When health drops below 20%, automatically spawns two automated drone turrets that follow the player and laser down hordes for 10 seconds."
    },
    "crafting_bonus": "Unlocks a permanent 15% discount on all metal bar costs when building heavy machinery, wiring tech, or automated traps.",
    "theme": {
      "hair": (40, 30, 20),       # Dark brown styled hair
      "skin": (255, 220, 190),
      "shirt": (180, 30, 40),     # Red armor chest
      "pants": (180, 30, 40),
      "eyes": (0, 200, 255),      # Glowing blue repulsor eyes
      "has_goatee": True
    }
  },
  {
    "name": "Paul Atreides",
    "origin": "Dune",
    "stats": { "max_health": 110, "move_speed": 1.2, "armor": 3, "magnet_range": 2.2 },
    "starting_weapon": "Crysknife Slash",
    "unique_ability": {
      "name": "The Voice",
      "description": "Commands all onscreen enemies to move backwards away from the player model for 4 seconds, clearing immediate breathing room."
    },
    "crafting_bonus": "Gains a massive +40% mining speed efficiency and movement bonus specifically within desert and sand biomes.",
    "theme": {
      "hair": (20, 20, 25),       # Black curly hair
      "skin": (235, 195, 160),    # Desert tan
      "shirt": (25, 25, 30),      # Black stillsuit
      "pants": (25, 25, 30),
      "eyes": (20, 100, 255),     # Blue-in-blue eyes
      "has_cape": True,
      "cape_color": (40, 40, 45)
    }
  },
  {
    "name": "Enid Sinclair",
    "origin": "Wednesday",
    "stats": { "max_health": 115, "move_speed": 1.3, "armor": 3, "magnet_range": 2.0 },
    "starting_weapon": "Rainbow Acrylic Claws",
    "unique_ability": {
      "name": "Blood Moon Wolf-Out",
      "description": "Temporarily mutates into a powerful werewolf for 8 seconds, gaining massive life-steal healing properties on every physical claw strike."
    },
    "crafting_bonus": "Can synthesize bright neon cosmetic dyes, colored wool blocks, and decorative tile accents at zero resource cost.",
    "theme": {
      "hair": (245, 230, 150),    # Blonde with colorful tips
      "skin": (255, 225, 210),
      "shirt": (240, 110, 180),   # Striped pink sweater
      "pants": (80, 120, 200),
      "eyes": (80, 160, 240),
      "has_braids": True
    }
  },
  {
    "name": "Percy Jackson",
    "origin": "Percy Jackson & the Olympians",
    "stats": { "max_health": 120, "move_speed": 1.2, "armor": 4, "magnet_range": 2.0 },
    "starting_weapon": "Anaklusmos (Riptide Sword)",
    "unique_ability": {
      "name": "Hydrokinetic Surge",
      "description": "Standing inside water pools or honey tiles increases health regeneration by 500% and forms a protective water shield."
    },
    "crafting_bonus": "Completely removes the risk of drowning; allows the player to move at full sprinting speeds while completely submerged underwater.",
    "theme": {
      "hair": (30, 30, 35),       # Messy black
      "skin": (245, 210, 175),
      "shirt": (255, 110, 30),    # Orange camp shirt
      "pants": (50, 80, 180),
      "eyes": (40, 180, 150)      # Sea-green eyes
    }
  },
  {
    "name": "Sailor Moon",
    "origin": "Sailor Moon",
    "stats": { "max_health": 90, "move_speed": 1.15, "armor": 2, "magnet_range": 3.5 },
    "starting_weapon": "Moon Tiara Magic",
    "unique_ability": {
      "name": "Cosmic Healing Escalation",
      "description": "Emits a brilliant silver light across the screen that instantly purifies corrupted, cursed, or toxic debuffs from the player and maps."
    },
    "crafting_bonus": "Allows standard fallen stars and mana crystals to drop at a 30% higher frequency during clear night cycles.",
    "theme": {
      "hair": (255, 220, 40),     # Bright gold twin tails
      "skin": (255, 215, 185),
      "shirt": (245, 245, 250),   # White sailor fuku
      "pants": (40, 70, 220),     # Blue skirt
      "eyes": (50, 130, 250),
      "has_ponytail": True
    }
  },
  {
    "name": "Goku",
    "origin": "Dragon Ball",
    "stats": { "max_health": 150, "move_speed": 1.3, "armor": 4, "magnet_range": 1.7 },
    "starting_weapon": "Ki Blast Volley",
    "unique_ability": {
      "name": "Kamehameha Wave",
      "description": "Charges up a massive energy beam that completely vaporizes any solid world blocks and enemies in a straight line across the horizon."
    },
    "crafting_bonus": "Can smash raw obsidian, hellstone, or hard meteorite nodes using basic iron pickaxes or bare hands.",
    "theme": {
      "hair": (20, 20, 20),       # Spiky black hair
      "skin": (245, 205, 170),
      "shirt": (255, 100, 0),     # Orange gi
      "pants": (255, 100, 0),
      "eyes": (30, 30, 30)
    }
  },
  {
    "name": "Roronoa Zoro",
    "origin": "One Piece",
    "stats": { "max_health": 135, "move_speed": 1.2, "armor": 5, "magnet_range": 1.2 },
    "starting_weapon": "Three-Sword Style Onogiri",
    "unique_ability": {
      "name": "1080 Pound Hoof",
      "description": "A massive sweeping sword wind slice that instantly chops down all background trees, giant mushrooms, and foliage tiles while killing enemies."
    },
    "crafting_bonus": "Wood harvested from trees is automatically doubled in yield per trunk chopped.",
    "theme": {
      "hair": (40, 180, 80),      # Green cropped
      "skin": (235, 190, 150),
      "shirt": (30, 80, 45),      # Green coat
      "pants": (20, 20, 20),
      "eyes": (30, 30, 30),
      "has_blindfold": True       # Eye scar/closed eye
    }
  },
  {
    "name": "Weird Barbie",
    "origin": "Barbie Movie",
    "stats": { "max_health": 105, "move_speed": 1.1, "armor": 3, "magnet_range": 2.6 },
    "starting_weapon": "Contortionist Kick",
    "unique_ability": {
      "name": "Permanent Splits Dodge",
      "description": "Possesses a unique erratic hit-box that automatically allows her to slide under flying projectiles and arrow traps without taking damage."
    },
    "crafting_bonus": "Can brew completely experimental potions at alchemy labs that combine two random potion effects together into one bottle.",
    "theme": {
      "hair": (230, 100, 200),    # Chopped pink
      "skin": (255, 210, 180),
      "shirt": (240, 80, 160),    # Wacky pink dress
      "pants": (150, 220, 50),    # Green/yellow tights
      "eyes": (80, 120, 220)
    }
  },
  {
    "name": "Kendrick Lamar",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 110, "move_speed": 1.25, "armor": 3, "magnet_range": 2.4 },
    "starting_weapon": "Euphoria Diss Track",
    "unique_ability": {
      "name": "Not Like Us Booby-Trap",
      "description": "Stamps a massive soundwave emblem onto the ground tile. When a boss walks over it, it detonates for 500% critical armor-piercing damage."
    },
    "crafting_bonus": "Deals an additional flat +20% damage bonus against any elite enemy unit or level mini-boss.",
    "theme": {
      "hair": (20, 20, 20),       # Black braids
      "skin": (110, 80, 55),      # Dark brown
      "shirt": (120, 120, 130),   # Gray hoodie
      "pants": (30, 30, 30),
      "eyes": (30, 25, 20)
    }
  },
  {
    "name": "Maddy Perez",
    "origin": "Euphoria",
    "stats": { "max_health": 95, "move_speed": 1.2, "armor": 3, "magnet_range": 2.9 },
    "starting_weapon": "Rhinestone Nail Swipe",
    "unique_ability": {
      "name": "Pure Intimidation glare",
      "description": "Looking directly at a horde causes the front row of enemies to cower, reducing their base attack damage properties by 40% for 5 seconds."
    },
    "crafting_bonus": "Provides a massive armor buff defense rating to any equipped clothing or vanity items that normally offer 0 armor values.",
    "theme": {
      "hair": (25, 20, 20),       # Dark slicked
      "skin": (230, 185, 145),
      "shirt": (80, 180, 240),    # Blue rhinestone top
      "pants": (25, 25, 25),
      "eyes": (30, 20, 15)
    }
  },
  {
    "name": "Donkey",
    "origin": "Shrek",
    "stats": { "max_health": 125, "move_speed": 1.35, "armor": 3, "magnet_range": 2.2 },
    "starting_weapon": "Hind-Leg Hoof Kick",
    "unique_ability": {
      "name": "Dragon Wife Air-Strike",
      "description": "Summons a friendly ruby dragon to soar overhead, raining explosive fireballs onto dense clusters of ground enemies for 6 seconds."
    },
    "crafting_bonus": "Baking or cooking at campfires always outputs a unique 'Waffle' food item that provides max health regeneration variables.",
    "theme": {
      "hair": (100, 100, 100),
      "skin": (150, 150, 150),    # Gray donkey coat
      "shirt": (180, 180, 180),
      "pants": (150, 150, 150),
      "eyes": (90, 60, 30),
      "is_bald": True
    }
  },
  {
    "name": "Gollum",
    "origin": "Lord of the Rings",
    "stats": { "max_health": 80, "move_speed": 1.4, "armor": 1, "magnet_range": 4.0 },
    "starting_weapon": "Raw Fish Chomp",
    "unique_ability": {
      "name": "My Precious Stealth",
      "description": "Crouching down downscales enemy aggro distance to near zero, allowing easy crawling through dangerous high-level dungeon corridors."
    },
    "crafting_bonus": "Increases the overall find rate of raw gold ores, platinum nuggets, and rare metal rings inside storage vases by 50%.",
    "theme": {
      "hair": (80, 80, 80),       # Thin gray strands
      "skin": (180, 190, 185),    # Pale gray skin
      "shirt": (180, 190, 185),
      "pants": (90, 85, 75),      # Loincloth
      "eyes": (120, 200, 255),    # Large pale eyes
      "is_bald": True
    }
  },
  {
    "name": "Max Mayfield",
    "origin": "Stranger Things",
    "stats": { "max_health": 100, "move_speed": 1.5, "armor": 2, "magnet_range": 2.5 },
    "starting_weapon": "Skateboard Wheel Grind",
    "unique_ability": {
      "name": "Running Up That Hill",
      "description": "Putting on red headphones provides absolute temporary immunity to magical curses, slow traps, or psychic attacks for 10 seconds."
    },
    "crafting_bonus": "Can quickly vault over vertical wall block obstacles up to 3 tiles high without needing to slow down or break them.",
    "theme": {
      "hair": (220, 90, 30),      # Ginger red
      "skin": (255, 220, 190),
      "shirt": (230, 180, 50),    # Yellow jacket
      "pants": (70, 100, 180),
      "eyes": (70, 150, 240)
    }
  },
  {
    "name": "Kim Kardashian",
    "origin": "Pop Culture",
    "stats": { "max_health": 100, "move_speed": 1.1, "armor": 4, "magnet_range": 5.0 },
    "starting_weapon": "Camera Flash Blind",
    "unique_ability": {
      "name": "Break the Internet",
      "description": "Triggers a massive flash-bulb explosion on screen that completely stuns all targets and pulls all dropped items directly into inventory."
    },
    "crafting_bonus": "Expands global player inventory storage capacity by an extra 20 full slots via luxury leather backpack mechanics.",
    "theme": {
      "hair": (20, 20, 20),       # Long dark hair
      "skin": (235, 190, 155),    # Tan skin
      "shirt": (220, 180, 160),   # Nude top
      "pants": (220, 180, 160),
      "eyes": (70, 45, 30)
    }
  },
  {
    "name": "Dua Lipa",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 95, "move_speed": 1.3, "armor": 2, "magnet_range": 3.2 },
    "starting_weapon": "Levitating Laser Disco",
    "unique_ability": {
      "name": "Radical Optimism Wave",
      "description": "Every 14 seconds, projects a expanding neon grid across the floor tiles. Any enemies stepped on the grid get bounced backwards and irradiated with rainbow damage."
    },
    "crafting_bonus": "Allows crafting tables to build glowing glass and neon furniture blocks using 50% fewer standard sand blocks.",
    "theme": {
      "hair": (150, 20, 50),      # Cherry red hair
      "skin": (230, 185, 145),    # Olive skin
      "shirt": (200, 200, 220),   # Silver glitter top
      "pants": (30, 30, 30),
      "eyes": (70, 45, 30)
    }
  },
  {
    "name": "Carmy Berzatto",
    "origin": "The Bear",
    "stats": { "max_health": 110, "move_speed": 1.25, "armor": 3, "magnet_range": 2.0 },
    "starting_weapon": "Chef's Chopping Knife",
    "unique_ability": {
      "name": "Yes Chef! Panic Mode",
      "description": "When the screen contains more than 30 enemy targets, his attack speed doubles and his movement becomes erratic for 6 seconds as kitchen ticket stress spikes."
    },
    "crafting_bonus": "Cooking stations, kitchens, and alembic setups craft food items and recovery dishes instantly with double the stat recovery value.",
    "theme": {
      "hair": (110, 80, 50),      # Curly dark hair
      "skin": (245, 215, 185),    # Pale chef skin
      "shirt": (30, 60, 150),     # Blue apron / white shirt
      "pants": (25, 25, 25),
      "eyes": (70, 120, 240)
    }
  },
  {
    "name": "Paris Geller",
    "origin": "Gilmore Girls",
    "stats": { "max_health": 90, "move_speed": 1.1, "armor": 1, "magnet_range": 3.8 },
    "starting_weapon": "Spiteful Debate Podiums",
    "unique_ability": {
      "name": "Neurotic Filibuster",
      "description": "Launches an uninterrupted verbal barrage that stuns and fractures elite monsters or boss types, lowering their armor rating by a flat 50%."
    },
    "crafting_bonus": "Speeds up tech-tree progression research and blueprint parsing speeds by a massive 40% when interacting with historical bookshelves.",
    "theme": {
      "hair": (235, 210, 110),    # Blonde bob
      "skin": (255, 220, 190),
      "shirt": (40, 70, 130),     # Blue uniform vest
      "pants": (100, 75, 50),     # Brown skirt
      "eyes": (60, 130, 70)
    }
  },
  {
    "name": "Elena Gilbert",
    "origin": "The Vampire Diaries",
    "stats": { "max_health": 100, "move_speed": 1.15, "armor": 2, "magnet_range": 2.5 },
    "starting_weapon": "Doppelganger Mirror Strike",
    "unique_ability": {
      "name": "Petrova Bloodline Curse",
      "description": "Taking fatal damage has a 50% chance to immediately resurrect her at 30% health, triggering a localized shadow explosion that clears nearby horde units."
    },
    "crafting_bonus": "Doubles the collection yield when harvesting rare flora, alchemy flowers, and mystical wood blocks in forest biomes.",
    "theme": {
      "hair": (85, 55, 35),       # Straight brown hair
      "skin": (255, 220, 190),
      "shirt": (160, 40, 50),     # Red knit top
      "pants": (50, 70, 140),     # Blue jeans
      "eyes": (70, 45, 30)
    }
  },
  {
    "name": "Drake",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 105, "move_speed": 1.15, "armor": 3, "magnet_range": 4.0 },
    "starting_weapon": "OVO Owl Sonic Ring",
    "unique_ability": {
      "name": "Certified Lover Boy Charm",
      "description": "Periodically forces up to 5 non-boss ground enemies to completely change their allegiance, walking into the horde to act as meat shields."
    },
    "crafting_bonus": "Increases the overall coin and gold-brick drop values from underground chests and smashed ceramic pottery by 30%.",
    "theme": {
      "hair": (20, 20, 20),       # Fade buzzcut
      "skin": (180, 140, 105),    # Light brown skin
      "shirt": (245, 200, 40),    # Yellow OVO hoodie
      "pants": (30, 30, 30),
      "eyes": (40, 30, 20)
    }
  },
  {
    "name": "Saitama",
    "origin": "One Punch Man",
    "stats": { "max_health": 200, "move_speed": 1.5, "armor": 5, "magnet_range": 1.0 },
    "starting_weapon": "Normal Punch",
    "unique_ability": {
      "name": "Consecutive Normal Punches",
      "description": "Every 25 seconds, unleashes a short-range physical fury that completely obliterates any enemies and instantly mines a 5-block deep tunnel through any hard world tiles."
    },
    "crafting_bonus": "Can mine raw iron, obsidian, or hard dungeon bricks using completely bare fists without requiring a pickaxe tool.",
    "theme": {
      "hair": (50, 50, 50),
      "skin": (255, 220, 190),
      "shirt": (255, 210, 20),    # Yellow hero suit
      "pants": (220, 40, 40),     # Red boots
      "eyes": (20, 20, 20),
      "is_bald": True,
      "has_cape": True,
      "cape_color": (240, 240, 240)
    }
  },
  {
    "name": "Arthur Morgan",
    "origin": "Red Dead Redemption 2",
    "stats": { "max_health": 140, "move_speed": 1.1, "armor": 5, "magnet_range": 1.9 },
    "starting_weapon": "Cattleman Revolver",
    "unique_ability": {
      "name": "Dead Eye Targeting",
      "description": "Slows down enemy movement speed by 60% for 3 seconds while locking onto and shooting the 6 closest targets with critical damage bullets."
    },
    "crafting_bonus": "Crafting base campfires, wood fences, ropes, and survival scaffolding costs 50% fewer timber raw resources.",
    "theme": {
      "hair": (90, 65, 45),       # Messy brown hair
      "skin": (235, 185, 140),    # Weathered skin
      "shirt": (70, 110, 160),    # Blue cowboy shirt
      "pants": (45, 45, 45),
      "eyes": (60, 110, 100),
      "has_fedora": True          # Stetson cowboy hat
    }
  },
  {
    "name": "Wanda Maximoff",
    "origin": "Marvel Universe",
    "stats": { "max_health": 95, "move_speed": 1.2, "armor": 2, "magnet_range": 2.8 },
    "starting_weapon": "Chaos Magic Hex Bolts",
    "unique_ability": {
      "name": "Reality Distortion Hex",
      "description": "Turns a cluster of 10 incoming enemies into passive, breakable environmental objects like stone pillars, wood blocks, or copper ore clusters."
    },
    "crafting_bonus": "Can use alchemy transmuting grids to change low-tier dirt or stone blocks directly into basic copper or iron metal ores.",
    "theme": {
      "hair": (195, 65, 30),      # Copper red hair
      "skin": (255, 220, 190),
      "shirt": (170, 30, 40),     # Scarlet corset
      "pants": (25, 25, 25),
      "eyes": (255, 50, 50),      # Red glowing eyes
      "has_cape": True,
      "cape_color": (160, 20, 30)
    }
  },
  {
    "name": "Steve",
    "origin": "Minecraft",
    "stats": { "max_health": 120, "move_speed": 1.1, "armor": 4, "magnet_range": 2.4 },
    "starting_weapon": "Diamond Pickaxe Swipe",
    "unique_ability": {
      "name": "Panic Block Placement",
      "description": "When attacked, immediately places a 3x3 protective dirt wall grid around his current coordinates to safely block out incoming monster projectiles."
    },
    "crafting_bonus": "Increases the maximum item stack capacity constraint inside the global backpack inventory storage from 99 up to 999 items.",
    "theme": {
      "hair": (80, 50, 25),       # Blocky brown hair
      "skin": (220, 160, 120),    # Tan skin
      "shirt": (0, 190, 200),     # Cyan t-shirt
      "pants": (50, 60, 160),     # Blue pants
      "eyes": (120, 80, 200)
    }
  },
  {
    "name": "Lana Del Rey",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 85, "move_speed": 1.05, "armor": 3, "magnet_range": 3.6 },
    "starting_weapon": "Summertime Sadness Fog",
    "unique_ability": {
      "name": "Vintage Melancholy Aura",
      "description": "Projects a persistent sepia aura ring that slows enemy projectiles and ticks continuous ice/frost damage onto standard ground monster sprites."
    },
    "crafting_bonus": "Can use calligraphy and desk stations to craft mystical paper scrolls that act as permanent music-box ambient background buffs.",
    "theme": {
      "hair": (115, 70, 45),      # Auburn brown waves
      "skin": (255, 235, 225),    # Pale skin
      "shirt": (240, 240, 250),   # White ribbon dress
      "pants": (240, 240, 250),
      "eyes": (65, 40, 25)
    }
  },
  {
    "name": "Zagreus",
    "origin": "Hades",
    "stats": { "max_health": 130, "move_speed": 1.4, "armor": 4, "magnet_range": 2.1 },
    "starting_weapon": "Stygian Blade Slash",
    "unique_ability": {
      "name": "Olympian Dash Boon",
      "description": "Dashing forward leaves a trail of divine deflected sparks that reflect incoming arrows and ignite surface tiles with secondary lightning damage."
    },
    "crafting_bonus": "Upon experiencing a player death screen, retains 20% of harvested world gems and hard gold coins inside the permanent stash.",
    "theme": {
      "hair": (20, 20, 20),       # Spiky black hair (laurel)
      "skin": (245, 245, 245),    # Underworld pale
      "shirt": (200, 30, 40),     # Toga and shoulder guard
      "pants": (180, 30, 30),
      "eyes": (220, 40, 40),      # Flaming red eyes
      "has_green_cap": True       # Representing the laurel wreath
    }
  },
  {
    "name": "Rihanna",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 100, "move_speed": 1.2, "armor": 4, "magnet_range": 4.2 },
    "starting_weapon": "Diamond Shine Laser",
    "unique_ability": {
      "name": "Shine Bright Shockwave",
      "description": "Triggers a blinding crystalline explosion that illuminates dark subterranean fog systems completely while turning common enemies to stone formats."
    },
    "crafting_bonus": "Extracts raw crystals, diamonds, and precious gems at a 35% higher drop rate when structural mining in deep underground biomes.",
    "theme": {
      "hair": (20, 20, 20),       # Sleek black ponytail
      "skin": (185, 140, 100),    # Warm caramel
      "shirt": (230, 40, 50),     # Red puffer outfit
      "pants": (230, 40, 50),
      "eyes": (60, 140, 90),
      "has_ponytail": True
    }
  },
  {
    "name": "Thanos",
    "origin": "Marvel Universe",
    "stats": { "max_health": 190, "move_speed": 0.85, "armor": 10, "magnet_range": 1.5 },
    "starting_weapon": "Titan Double-Blade",
    "unique_ability": {
      "name": "Perfect Balance Snap",
      "description": "Instantly deletes exactly 50% of the active onscreen enemy targets, but costs 25% of his current health value to deploy the cosmic strain."
    },
    "crafting_bonus": "Increases the upgrade quality limits of heavy armors and weapons at standard anvils past their default base level caps.",
    "theme": {
      "hair": (50, 50, 50),
      "skin": (150, 110, 180),    # Titan purple
      "shirt": (210, 165, 30),    # Gold armor plates
      "pants": (210, 165, 30),
      "eyes": (30, 30, 30),
      "is_bald": True
    }
  },
  {
    "name": "Travis Kelce",
    "origin": "Pop Culture / Sports",
    "stats": { "max_health": 150, "move_speed": 1.3, "armor": 6, "magnet_range": 1.8 },
    "starting_weapon": "Football Spiral Pass",
    "unique_ability": {
      "name": "Red Zone Cleaving Rush",
      "description": "Charges forward in an unstoppable straight line, physics-knocking enemies to the side of the screen and busting through weak wooden blocks."
    },
    "crafting_bonus": "Gains a 25% jump height modifier and stamina acceleration bonus when stepping along green grass or leaf block environments.",
    "theme": {
      "hair": (110, 85, 60),      # Buzzcut and beard
      "skin": (255, 220, 190),
      "shirt": (200, 30, 40),     # Red jersey #87
      "pants": (240, 240, 240),
      "eyes": (60, 110, 200),
      "has_goatee": True
    }
  },
  {
    "name": "Bill Cipher",
    "origin": "Gravity Falls",
    "stats": { "max_health": 80, "move_speed": 1.25, "armor": 5, "magnet_range": 3.0 },
    "starting_weapon": "Weirdmageddon Eye Beam",
    "unique_ability": {
      "name": "Madness Bubble Shift",
      "description": "Fires a chaotic bubble that randomizes the target mechanics of enemies inside it, changing their gravity orientation so they float to the roof."
    },
    "crafting_bonus": "Causes storage chests to occasionally spawn completely glitched, high-tier loot patterns instead of common tier materials.",
    "theme": {
      "hair": (20, 20, 20),
      "skin": (255, 225, 0),      # Yellow triangle
      "shirt": (20, 20, 20),      # Bow tie
      "pants": (255, 225, 0),
      "eyes": (255, 255, 255),    # Eye of Providence
      "is_bald": True,
      "has_fedora": True          # Top hat
    }
  },
  {
    "name": "Charli XCX",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 90, "move_speed": 1.4, "armor": 2, "magnet_range": 3.4 },
    "starting_weapon": "Brat Green Laser Wall",
    "unique_ability": {
      "name": "360 Party Crash",
      "description": "Every 12 seconds, triggers a hyperpop bass drop that gives a massive 50% movement speed burst and leaves a toxic neon trail that melts enemy armor values."
    },
    "crafting_bonus": "Transforms regular wire and basic gems into glowing neon club light tiles at zero cost.",
    "theme": {
      "hair": (25, 20, 20),       # Messy dark hair
      "skin": (255, 215, 185),
      "shirt": (143, 219, 0),     # BRAT neon green
      "pants": (25, 25, 25),
      "eyes": (50, 30, 20)
    }
  },
  {
    "name": "Eminem",
    "origin": "Pop Culture / Music",
    "stats": { "max_health": 115, "move_speed": 1.25, "armor": 4, "magnet_range": 2.2 },
    "starting_weapon": "Rap God Mic Blast",
    "unique_ability": {
      "name": "Mom's Spaghetti Drop",
      "description": "Killing 75 enemies spawns a unique skillet item on the floor. Collecting it restores 40 HP and fully resets all active weapon cooldown parameters."
    },
    "crafting_bonus": "Crafts sonic traps, speakers, and soundwave defenses using 30% fewer metal components.",
    "theme": {
      "hair": (240, 230, 160),    # Bleach blonde crop
      "skin": (255, 220, 190),
      "shirt": (100, 100, 110),   # Gray hoodie
      "pants": (100, 100, 110),
      "eyes": (100, 130, 160)
    }
  },
  {
    "name": "Kris Jenner",
    "origin": "Pop Culture / Reality TV",
    "stats": { "max_health": 100, "move_speed": 1.1, "armor": 3, "magnet_range": 4.5 },
    "starting_weapon": "Corporate Contract Slap",
    "unique_ability": {
      "name": "The Momager Shield",
      "description": "Summons a rotating barrier of 3 heavy security guards that completely block out enemy projectiles. Guard count refreshes every 20 seconds."
    },
    "crafting_bonus": "Gains a permanent '10% Manager Cut'—returns 15% of all raw resources spent when building at any workstation.",
    "theme": {
      "hair": (20, 20, 20),       # Pixie cut
      "skin": (240, 195, 160),
      "shirt": (30, 30, 30),      # Black manager suit
      "pants": (30, 30, 30),
      "eyes": (60, 40, 30)
    }
  },
  {
    "name": "Squidward Tentacles",
    "origin": "SpongeBob SquarePants",
    "stats": { "max_health": 95, "move_speed": 1.0, "armor": 2, "magnet_range": 2.6 },
    "starting_weapon": "Off-Key Clarinet Blast",
    "unique_ability": {
      "name": "Artistic Meltdown",
      "description": "Unleashes an agonizing sonic shockwave that fractures elite monsters and instantly breaks down surrounding background tiles into raw items."
    },
    "crafting_bonus": "Can refine basic stone blocks into pristine, decorative marble structures without using a heavy furnace.",
    "theme": {
      "hair": (40, 40, 40),
      "skin": (140, 200, 190),    # Turquoise skin
      "shirt": (130, 85, 45),     # Brown collar shirt
      "pants": (140, 200, 190),
      "eyes": (230, 220, 60),     # Red pupil / yellow eyes
      "is_bald": True
    }
  },
  {
    "name": "Ryomen Sukuna",
    "origin": "Jujutsu Kaisen",
    "stats": { "max_health": 140, "move_speed": 1.3, "armor": 6, "magnet_range": 1.8 },
    "starting_weapon": "Cleave & Dismantle",
    "unique_ability": {
      "name": "Malevolent Shrine",
      "description": "Deploys a giant domain network for 5 seconds that automatically slices everything on screen, shredding block walls and enemies into raw materials."
    },
    "crafting_bonus": "Weapons upgraded at anvils gain a permanent +5% chance to trigger life-steal mechanics on critical strikes.",
    "theme": {
      "hair": (230, 140, 180),    # Pink spiky
      "skin": (245, 210, 180),    # Tattoos skin
      "shirt": (240, 235, 230),   # Light yukata robe
      "pants": (35, 35, 40),
      "eyes": (220, 30, 30)
    }
  },
  {
    "name": "Rhaenyra Targaryen",
    "origin": "House of the Dragon",
    "stats": { "max_health": 110, "move_speed": 1.15, "armor": 4, "magnet_range": 2.1 },
    "starting_weapon": "Syrax Fireball Flare",
    "unique_ability": {
      "name": "Dracarys Carpet-Bomb",
      "description": "Summons a golden dragon shadow to cross the viewport, bathing the ground plane in high-intensity flames that melt raw iron, lead, and copper tiles."
    },
    "crafting_bonus": "All forged swords, blades, and axes gain a permanent flat +15% armor penetration property.",
    "theme": {
      "hair": (245, 245, 250),    # Silver-gold Targaryen hair
      "skin": (255, 220, 195),
      "shirt": (140, 25, 35),     # Crimson/black gown
      "pants": (200, 160, 40),
      "eyes": (110, 100, 220),
      "has_braids": True
    }
  },
  {
    "name": "Leon S. Kennedy",
    "origin": "Resident Evil",
    "stats": { "max_health": 130, "move_speed": 1.2, "armor": 5, "magnet_range": 2.0 },
    "starting_weapon": "Tactical Laser Pistol",
    "unique_ability": {
      "name": "Roundhouse Kick Counter",
      "description": "Successfully dodging an incoming attack triggers a sweeping kick that knocks back immediate waves and shatters background furniture crates."
    },
    "crafting_bonus": "Can synthesize generic wild plants and mushrooms into elite maximum-tier health recovery potions.",
    "theme": {
      "hair": (210, 185, 120),    # Curtain blonde
      "skin": (255, 220, 190),
      "shirt": (100, 65, 40),     # Leather jacket
      "pants": (50, 50, 55),
      "eyes": (80, 130, 220)
    }
  },
  {
    "name": "Elle Woods",
    "origin": "Legally Blonde",
    "stats": { "max_health": 100, "move_speed": 1.2, "armor": 3, "magnet_range": 3.6 },
    "starting_weapon": "Scented Resume Toss",
    "unique_ability": {
      "name": "Bend and Snap Stun",
      "description": "Executes a flawless maneuver that charms and freezes all screen threats in place for 4 seconds while pulling loose loot items directly to her feet."
    },
    "crafting_bonus": "Can coat any basic armor piece in hot pink styling, granting a permanent +5% passive dodge rate modifier.",
    "theme": {
      "hair": (250, 220, 100),    # Long blonde hair
      "skin": (255, 215, 195),
      "shirt": (245, 75, 175),    # Hot pink outfit
      "pants": (245, 75, 175),
      "eyes": (70, 140, 230),
      "has_ponytail": True
    }
  },
  {
    "name": "Moo Deng",
    "origin": "Internet Memes / Pop Culture",
    "stats": { "max_health": 160, "move_speed": 1.35, "armor": 8, "magnet_range": 1.5 },
    "starting_weapon": "Sassy Pygmy Chomp",
    "unique_ability": {
      "name": "Water Spray Slippage",
      "description": "Bounces around erratically when taking hit damage, spraying water pools that slip enemies and immediately extinguish environmental lava or fire hazards."
    },
    "crafting_bonus": "Mines mud and clay tiles at 2x speed; standing on mud blocks grants a massive health regeneration boost.",
    "theme": {
      "hair": (50, 50, 50),
      "skin": (160, 140, 135),    # Grey pygmy hippo coat
      "shirt": (215, 180, 180),   # Rosy underbelly
      "pants": (160, 140, 135),
      "eyes": (30, 30, 30),
      "is_bald": True
    }
  },
  {
    "name": "Miles Morales",
    "origin": "Spider-Man: Across the Spider-Verse",
    "stats": { "max_health": 120, "move_speed": 1.45, "armor": 3, "magnet_range": 2.4 },
    "starting_weapon": "Venom Strike Spark",
    "unique_ability": {
      "name": "Bio-Electric Camouflage",
      "description": "Turns completely invisible for 3 seconds when heavily surrounded, charging a bio-electric dive that craters terrain blocks and paralyzes targets."
    },
    "crafting_bonus": "Can spray neon graffiti tags onto solid stone walls to permanently illuminate dark cave systems and map grids.",
    "theme": {
      "hair": (15, 15, 15),
      "skin": (70, 50, 35),
      "shirt": (25, 25, 25),      # Black/red spider suit
      "pants": (25, 25, 25),
      "eyes": (250, 250, 250)     # White spider mask lenses
    }
  }
]

# Universe / Show Groups definition
NAME_TO_GROUP = {
    # Pop Music & Reality
    "Ariana Grande": "Pop Music & Reality", "Sabrina Carpenter": "Pop Music & Reality",
    "Taylor Swift": "Pop Music & Reality", "Billie Eilish": "Pop Music & Reality",
    "Travis Scott": "Pop Music & Reality", "The Weeknd": "Pop Music & Reality",
    "Lady Gaga": "Pop Music & Reality", "Chappell Roan": "Pop Music & Reality",
    "Olivia Rodrigo": "Pop Music & Reality", "Kendrick Lamar": "Pop Music & Reality",
    "Kim Kardashian": "Pop Music & Reality", "Dua Lipa": "Pop Music & Reality",
    "Drake": "Pop Music & Reality", "Lana Del Rey": "Pop Music & Reality",
    "Rihanna": "Pop Music & Reality", "Charli XCX": "Pop Music & Reality",
    "Eminem": "Pop Music & Reality", "Kris Jenner": "Pop Music & Reality",
    "Travis Kelce": "Pop Music & Reality",
    
    # Marvel Universe
    "Spider-Man": "Marvel Universe", "Deadpool": "Marvel Universe",
    "Wolverine": "Marvel Universe", "Tony Stark": "Marvel Universe",
    "Wanda Maximoff": "Marvel Universe", "Thanos": "Marvel Universe",
    "Miles Morales": "Marvel Universe",
    
    # DC Universe
    "Batman": "DC Universe", "Harley Quinn": "DC Universe", "Joker": "DC Universe",
    
    # Star Wars
    "Luke Skywalker": "Star Wars", "Darth Vader": "Star Wars", "The Mandalorian": "Star Wars",
    
    # Anime & Manga
    "Naruto Uzumaki": "Anime & Manga", "Gojo Satoru": "Anime & Manga",
    "Luffy": "Anime & Manga", "Roronoa Zoro": "Anime & Manga",
    "Sailor Moon": "Anime & Manga", "Goku": "Anime & Manga",
    "Ryomen Sukuna": "Anime & Manga", "Saitama": "Anime & Manga",
    
    # Vampires & Twilight
    "Damon Salvatore": "Vampires & Twilight", "Bella Swan": "Vampires & Twilight",
    "Edward Cullen": "Vampires & Twilight", "Elena Gilbert": "Vampires & Twilight",
    
    # Gilmore Girls
    "Rory Gilmore": "Gilmore Girls", "Lorelai Gilmore": "Gilmore Girls", "Paris Geller": "Gilmore Girls",
    
    # SpongeBob SquarePants
    "SpongeBob SquarePants": "SpongeBob SquarePants", "Patrick Star": "SpongeBob SquarePants",
    "Squidward Tentacles": "SpongeBob SquarePants",
    
    # Stranger Things & Wednesday
    "Wednesday Addams": "Stranger Things & Wednesday", "Enid Sinclair": "Stranger Things & Wednesday",
    "Steve Harrington": "Stranger Things & Wednesday", "Max Mayfield": "Stranger Things & Wednesday",
    
    # Gaming Legends
    "Geralt of Rivia": "Gaming Legends", "Lara Croft": "Gaming Legends",
    "Kratos": "Gaming Legends", "Sonic the Hedgehog": "Gaming Legends",
    "Pikachu": "Gaming Legends", "Joel Miller": "Gaming Legends",
    "Cloud Strife": "Gaming Legends", "Link": "Gaming Legends",
    "Zagreus": "Gaming Legends", "Arthur Morgan": "Gaming Legends",
    "Steve": "Gaming Legends", "Leon S. Kennedy": "Gaming Legends",
    
    # Cinematic & TV Worlds
    "Walter White": "Cinematic & TV Worlds", "Michael Scott": "Cinematic & TV Worlds",
    "Homelander": "Cinematic & TV Worlds", "Harry Potter": "Cinematic & TV Worlds",
    "Katniss Everdeen": "Cinematic & TV Worlds", "Barbie": "Cinematic & TV Worlds",
    "Barbie Ken": "Cinematic & TV Worlds", "Weird Barbie": "Cinematic & TV Worlds",
    "Paul Atreides": "Cinematic & TV Worlds", "Percy Jackson": "Cinematic & TV Worlds",
    "Maddy Perez": "Cinematic & TV Worlds", "Donkey": "Cinematic & TV Worlds",
    "Gollum": "Cinematic & TV Worlds", "Carmy Berzatto": "Cinematic & TV Worlds",
    "Bill Cipher": "Cinematic & TV Worlds", "Rhaenyra Targaryen": "Cinematic & TV Worlds",
    "Elle Woods": "Cinematic & TV Worlds", "Moo Deng": "Cinematic & TV Worlds",
    "Jon Snow": "Cinematic & TV Worlds", "Daenerys Targaryen": "Cinematic & TV Worlds",
    "Elsa": "Cinematic & TV Worlds", "Indiana Jones": "Cinematic & TV Worlds",
    "Jack Sparrow": "Cinematic & TV Worlds", "Neo": "Cinematic & TV Worlds",
    "Ted Lasso": "Cinematic & TV Worlds", "Beth Harmon": "Cinematic & TV Worlds",
    "Rick Sanchez": "Cinematic & TV Worlds", "Billie Butcher": "Cinematic & TV Worlds"
}

# Decorate characters with their groups
for char in CHARACTERS_DB:
    char["group"] = NAME_TO_GROUP.get(char["name"], "Other")



