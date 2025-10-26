import streamlit as st
import datetime
import math
import random
import pandas as pd
import decimal
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import RegularPolygon, Circle
from matplotlib import animation
import io

dec = decimal.Decimal

# Constants
LETTER_VALUES = {
    'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
    'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9,
    'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8
}

VOWEL_VALUES = {'A':1, 'E':5, 'I':9, 'O':6, 'U':3}

CONSONANT_VALUES = {c: ((ord(c) - ord('A') + 1) % 9) or 9 for c in 'BCDFGHJKLMNPQRSTVWXYZ'}

AURA_COLORS = {
    1: "Red", 2: "Blue", 3: "Yellow", 4: "Green", 5: "Orange",
    6: "Purple", 7: "Indigo", 8: "Gold", 9: "Silver", 11: "White", 22: "White", 33: "White"
}

ELEMENT_MODIFIERS = {
    "Fire": " (Fiery Tint) 🔥🧙‍♂️", "Earth": " (Earthy Shade) 🌍🧙‍♀️",
    "Air": " (Airy Glow) 💨🪄", "Water": " (Watery Sheen) 🌊🔮"
}

MYSTICAL_SITES = {
    "Stonehenge": (51.1789, -1.8262),
    "Machu Picchu": (-13.1631, -72.5450),
    "Great Pyramid": (29.9792, 31.1342),
    "Uluru": (-25.3444, 131.0369),
    "Sedona Vortex": (34.8697, -111.7610),
    # Vedic and Puranic references
    "Mount Kailash": (31.0669, 81.3125),  # Abode of Shiva
    "Varanasi": (25.3176, 82.9739),  # Sacred city on Ganges
    "Kurukshetra": (29.9657, 76.8370),  # Battlefield of Mahabharata
    "Dwarka": (22.2442, 68.9686),  # Krishna's city
    "Ayodhya": (26.7929, 82.1999),  # Birthplace of Rama
    "Mathura": (27.4924, 77.6737),  # Birthplace of Krishna
    "Haridwar": (29.9457, 78.1642),  # Gateway to Gods
    "Ujjain": (23.1765, 75.7849),  # Mahakaleshwar Jyotirlinga
    "Rameswaram": (9.2876, 79.3129),  # Rama's bridge site
    "Kanchipuram": (12.8392, 79.7042)  # One of Sapta Puri
}

CITY_COORDS = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Salem": (42.5195, -70.8967),
    # Expanded with Vedic/Puranic relevant cities
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Varanasi": (25.3176, 82.9739),
    "Ayodhya": (26.7929, 82.1999),
    "Mathura": (27.4924, 77.6737),
    "Haridwar": (29.9457, 78.1642),
    "Ujjain": (23.1765, 75.7849),
    "Dwarka": (22.2442, 68.9686)
}

ZODIAC_SIGNS = [
    ("Capricorn", (1, 1), (1, 19)), ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)), ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)), ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)), ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)), ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)), ("Sagittarius", (11, 22), (12, 21)),
    ("Capricorn", (12, 22), (12, 31))
]

ZODIAC_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

ZODIAC = "Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces".split()

HOROSCOPE_TEMPLATES = [
    "Today, {zodiac}, embrace new opportunities as the stars align in your favor. 🌟✨🧙‍♂️",
    "{zodiac}, focus on relationships; harmony is key under current transits. 💖🤝🔮",
    "Financial insights await you, {zodiac} – trust your intuition. 💰🔮🪄",
    "{zodiac}, health and wellness take center stage; balance is essential. 🏋️‍♀️🥦🧙‍♀️"
]

ELEMENT_COMPAT = {
    ("Fire", "Fire"): 90, ("Fire", "Air"): 80, ("Fire", "Earth"): 50, ("Fire", "Water"): 40,
    ("Earth", "Earth"): 90, ("Earth", "Water"): 80, ("Earth", "Fire"): 50, ("Earth", "Air"): 40,
    ("Air", "Air"): 90, ("Air", "Fire"): 80, ("Air", "Water"): 50, ("Air", "Earth"): 40,
    ("Water", "Water"): 90, ("Water", "Earth"): 80, ("Water", "Air"): 50, ("Water", "Fire"): 40
}

tarot_cards = [
    ("The Fool", "New beginnings, innocence, spontaneity. 🃏🌱🧙‍♂️"),
    ("The Magician", "Manifestation, resourcefulness, power. 🔮🪄🧙‍♀️"),
    ("The High Priestess", "Intuition, unconscious knowledge, mystery. 🌙🧙‍♀️🔮"),
    ("The Empress", "Fertility, abundance, nurturing. 👑🌸🪄"),
    ("The Emperor", "Structure, authority, control. 🏰👑🧙‍♂️"),
    ("The Hierophant", "Tradition, conformity, morality. 📜🙏🔮"),
    ("The Lovers", "Relationships, choices, alignment. 💑❤️🪄"),
    ("The Chariot", "Direction, control, willpower. 🛡️🏇🧙‍♀️"),
    ("Strength", "Courage, patience, compassion. 🦁💪🔮"),
    ("The Hermit", "Soul-searching, introspection, guidance. 🏮🧓🪄"),
    ("Wheel of Fortune", "Change, cycles, fate. 🎡🔄🧙‍♂️"),
    ("Justice", "Fairness, truth, cause and effect. ⚖️📖🔮"),
    ("The Hanged Man", "Surrender, release, martyrdom. 🔄🙃🪄"),
    ("Death", "Endings, transformation, transition. 💀🦋🧙‍♀️"),
    ("Temperance", "Balance, moderation, patience. ⚗️🕊️🔮"),
    ("The Devil", "Bondage, addiction, materialism. 😈🔗🪄"),
    ("The Tower", "Upheaval, awakening, revelation. 🏰⚡🧙‍♂️"),
    ("The Star", "Hope, spirituality, renewal. ⭐🌌🔮"),
    ("The Moon", "Illusion, fear, anxiety. 🌕🐺🪄"),
    ("The Sun", "Success, vitality, positivity. ☀️😊🧙‍♀️"),
    ("Judgement", "Rebirth, inner calling, absolution. 📯👼🔮"),
    ("The World", "Completion, integration, accomplishment. 🌍🏆🪄")
]

DAY_ZERO = datetime.datetime(2000, 1, 1, 12, tzinfo=datetime.timezone.utc)

# Numerology Functions
def reduce_number(num):
    while num > 9 and num not in [11, 22, 33]:
        num = sum(int(d) for d in str(num))
    return num

def calculate_life_path(birth_date):
    year, month, day = birth_date.year, birth_date.month, birth_date.day
    day_reduced = reduce_number(day)
    month_reduced = reduce_number(month)
    year_reduced = reduce_number(year)
    total = day_reduced + month_reduced + year_reduced
    life_path = reduce_number(total)
    return life_path, {
        "Day Reduced": day_reduced,
        "Month Reduced": month_reduced,
        "Year Reduced": year_reduced,
        "Total Before Final Reduction": total
    }

def calculate_destiny_number(name):
    name_upper = name.upper().replace(" ", "")
    total = sum(LETTER_VALUES.get(char, 0) for char in name_upper)
    char_values = {char: LETTER_VALUES.get(char, 0) for char in name_upper}
    destiny = reduce_number(total)
    return destiny, char_values

def calculate_soul_urge(name):
    name_upper = name.upper().replace(" ", "")
    total = sum(VOWEL_VALUES.get(char, 0) for char in name_upper if char in VOWEL_VALUES)
    return reduce_number(total)

def calculate_personality(name):
    name_upper = name.upper().replace(" ", "")
    total = sum(CONSONANT_VALUES.get(char, 0) for char in name_upper if char in CONSONANT_VALUES)
    return reduce_number(total)

def get_aura_color(number, element):
    base = AURA_COLORS.get(number, "Gray")
    return base + ELEMENT_MODIFIERS.get(element, "")

# Astrology Functions
def get_zodiac_sign(month, day):
    for sign, (m1, d1), (m2, d2) in ZODIAC_SIGNS:
        if (month == m1 and day >= d1) or (month == m2 and day <= d2):
            return sign
    return "Unknown"

def get_zodiac_element(sign):
    return ZODIAC_ELEMENTS.get(sign, "Unknown")

def local_to_utc_approx(local_dt, lon):
    offset_hours = lon / 15.0
    return local_dt - datetime.timedelta(hours=offset_hours)

def degrees_to_sign(deg):
    sign_index = int(deg // 30)
    deg_in_sign = deg % 30
    return f"{int(deg_in_sign)}° {ZODIAC[sign_index]}"

def calculate_ascendant_and_mc(birth_datetime_local, lat, lon):
    dt = local_to_utc_approx(birth_datetime_local, lon)
    d = (dt - DAY_ZERO).total_seconds() / 86400
    T = d / 36525
    oe = ((((-4.34e-8*T - 5.76e-7)*T + 0.0020034)*T - 1.831e-4)*T - 46.836769)*T / 3600 + 23.4392794444444
    oer = math.radians(oe)
    gmst = (67310.548 + (3155760000 + 8640184.812866) * T + 0.093104 * T**2 - 6.2e-6 * T**3) / 3600 % 24
    lst = (gmst + lon / 15) % 24
    lstr = math.radians(lst * 15)
    
    # Ascendant
    ascr = math.atan2(math.cos(lstr), -(math.sin(lstr) * math.cos(oer) + math.tan(math.radians(lat)) * math.sin(oer)))
    asc = math.degrees(ascr) % 360
    
    # Midheaven
    mcr = math.atan2(math.sin(lstr), math.cos(lstr) * math.cos(oer))
    mc = math.degrees(mcr) % 360
    
    return asc, degrees_to_sign(asc), mc, degrees_to_sign(mc)

# Moon Phase Functions
def moon_position(now=None):
    if now is None:
        now = datetime.datetime.now()
    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
    return lunations % dec(1)

def moon_phase(pos):
    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    phases = {
        0: "New Moon 🌑🔮", 1: "Waxing Crescent 🌒🧙‍♂️", 2: "First Quarter 🌓🪄", 3: "Waxing Gibbous 🌔🌟",
        4: "Full Moon 🌕✨", 5: "Waning Gibbous 🌖🧙‍♀️", 6: "Last Quarter 🌗🔮", 7: "Waning Crescent 🌘🪄"
    }
    return phases[int(index) & 7]

# Ley Line Functions
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def find_nearest_site(user_lat, user_lon):
    distances = {site: haversine_distance(user_lat, user_lon, lat, lon) for site, (lat, lon) in MYSTICAL_SITES.items()}
    nearest = min(distances, key=distances.get)
    return nearest, distances[nearest]

# Prediction and Other Functions
def generate_prediction(life_path, zodiac, element, moon_phase_name, asc_sign="", mc_sign=""):
    asc_text = f" with {asc_sign} rising 🌅🧙‍♂️" if asc_sign else ""
    mc_text = f" and {mc_sign} midheaven ☀️🔮" if mc_sign else ""
    predictions = [
        f"Your {zodiac} spirit{asc_text}{mc_text} ignites {element} energy during {moon_phase_name}: Brew potions under full moons – align with {zodiac} transits! 🧪🌕🪄✨",
        f"As a {zodiac}{asc_text}{mc_text}, your hidden talent lies in {element}-infused rituals in {moon_phase_name} – beware Mercury retrogrades affecting your path {life_path}. ⚠️🌌🧙‍♀️🪐",
        f"{element} flows through your {zodiac}{asc_text}{mc_text} veins in {moon_phase_name}: Chant ancient spells at dawn to unlock cosmic wealth. 📜🌅💰🔮",
        f"With {life_path} as your core, {zodiac}{asc_text}{mc_text} guides you to ethereal realms during {moon_phase_name} – harness {element} for ultimate power. 🌠🌀💥🧙‍♂️"
    ]
    return random.choice(predictions)

def generate_incantation(name, zodiac, moon_phase_name, asc_sign="", mc_sign=""):
    asc_text = f" as {asc_sign} ascends 🌄🪄" if asc_sign else ""
    mc_text = f" under {mc_sign} zenith 🏔️🔮" if mc_sign else ""
    return f"Chant '{name}' thrice under the {zodiac} stars{asc_text}{mc_text} at dawn during {moon_phase_name} to summon ethereal forces and align your destiny. 🗣️⭐🧙‍♀️✨"

def generate_daily_horoscope(zodiac):
    return random.choice(HOROSCOPE_TEMPLATES).format(zodiac=zodiac)

def calculate_compatibility(lp1, elem1, lp2, elem2):
    num_diff = abs(lp1 - lp2)
    elem_score = ELEMENT_COMPAT.get((elem1, elem2), 50)
    score = (100 - num_diff * 10) * (elem_score / 100)
    return max(0, min(100, int(score)))

def draw_tarot(zodiac):
    card, meaning = random.choice(tarot_cards)
    return f"{card}: {meaning} Influenced by your {zodiac}, this suggests focusing on personal growth. 🃏✨🧙‍♂️"

# Rune Casting
RUNES = [
    ("Fehu", "Wealth, prosperity, success. 💰🧙‍♂️"),
    ("Uruz", "Strength, health, power. 💪🔮"),
    ("Thurisaz", "Protection, defense, conflict. 🛡️🪄"),
    ("Ansuz", "Communication, wisdom, inspiration. 🗣️🌟"),
    ("Raidho", "Journey, movement, change. 🛤️✨"),
    ("Kenaz", "Knowledge, creativity, vision. 📖🧙‍♀️"),
    ("Gebo", "Partnership, gift, balance. 🤝🔮"),
    ("Wunjo", "Joy, harmony, pleasure. 😊🪄"),
    ("Hagalaz", "Disruption, change, trial. ⚡🌌"),
    ("Nauthiz", "Need, resistance, constraint. ⛓️🧙‍♂️"),
    ("Isa", "Stagnation, stillness, patience. ❄️🔮"),
    ("Jera", "Harvest, reward, cycles. 🌾🪄"),
    ("Eihwaz", "Endurance, reliability, strength. 🌲✨"),
    ("Perthro", "Fate, mystery, secrets. 🎲🧙‍♀️"),
    ("Algiz", "Protection, divinity, guidance. 🛡️🔮"),
    ("Sowilo", "Success, wholeness, life force. ☀️🪄"),
    ("Tiwaz", "Justice, leadership, authority. ⚖️🌟"),
    ("Berkano", "Growth, fertility, new beginnings. 🌱🧙‍♂️"),
    ("Ehwaz", "Partnership, trust, loyalty. 🐴🔮"),
    ("Mannaz", "Humanity, self, intelligence. 👤🪄"),
    ("Laguz", "Intuition, flow, unconscious. 🌊✨"),
    ("Ingwaz", "Fertility, gestation, potential. 🌰🧙‍♀️"),
    ("Dagaz", "Breakthrough, clarity, transformation. 🌅🔮"),
    ("Othala", "Heritage, home, legacy. 🏡🪄")
]

def cast_runes(num_runes=3):
    drawn = random.sample(RUNES, num_runes)
    return [f"{rune}: {meaning}" for rune, meaning in drawn]

# I Ching Divination
I_CHING_HEXNUMS = [2,24, 7,19,15,36,46,11,16,51,40,54,62,55,32,34, 8, 3,29,60,39,63,48, 5,45,17,47,58,31,49,28,43, 23,27, 4,41,52,22,18,26,35,21,64,38,56,30,50,14, 20,42,59,61,53,37,57, 9,12,25, 6,10,33,13,44, 1]

I_CHING_LINE_NAMES = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]

def cast_i_ching():
    r = random.randint(0, 63)
    current_hex = I_CHING_HEXNUMS[r]
    changing_lines = []
    for k in range(6):
        if random.randint(0,255) < 64:  # Approx 25% chance for changing line
            changing_lines.append(I_CHING_LINE_NAMES[k])
            r ^= (1 << k)
    future_hex = I_CHING_HEXNUMS[r]
    return current_hex, changing_lines, future_hex

# Advanced Crystal Grid with Sacred Geometry
ELEMENT_CRYSTAL_COLORS = {
    "Fire": "red",
    "Earth": "green",
    "Air": "yellow",
    "Water": "blue",
    "Unknown": "purple"
}

def draw_flower_of_life(ax, center, radius, num_circles=7, alpha=0.3):
    """Draw a simple Flower of Life pattern with overlapping circles."""
    ax.add_patch(Circle(center, radius, color='white', alpha=alpha, fill=False))
    for i in range(6):
        angle = i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        ax.add_patch(Circle((x, y), radius, color='white', alpha=alpha, fill=False))
    # Add more layers if num_circles > 7
    if num_circles > 7:
        for layer in range(1, (num_circles - 1) // 6 + 1):
            for i in range(6 * layer):
                angle = i * (2 * math.pi / (6 * layer))
                dist = radius * 2 * layer
                x = center[0] + dist * math.cos(angle)
                y = center[1] + dist * math.sin(angle)
                ax.add_patch(Circle((x, y), radius, color='white', alpha=alpha * (1 / (layer + 1)), fill=False))

def draw_metatrons_cube(ax, center, radius, alpha=0.5):
    """Draw Metatron's Cube by connecting centers of Flower of Life circles."""
    centers = [(center[0], center[1])]
    # Inner ring
    for i in range(6):
        angle = i * math.pi / 3
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        centers.append((x, y))
    # Outer ring, rotated
    for i in range(6):
        angle = i * math.pi / 3 + math.pi / 6
        x = center[0] + radius * 2 * math.cos(angle)
        y = center[1] + radius * 2 * math.sin(angle)
        centers.append((x, y))
    
    # Draw lines between centers that are 2*radius apart
    for i in range(len(centers)):
        for j in range(i+1, len(centers)):
            dx = centers[i][0] - centers[j][0]
            dy = centers[i][1] - centers[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            if abs(dist - 2 * radius) < 0.01 or abs(dist - radius * math.sqrt(3)) < 0.01 or abs(dist - radius) < 0.01:
                ax.plot([centers[i][0], centers[j][0]], [centers[i][1], centers[j][1]], color='gold', alpha=alpha, linewidth=1.5)

def draw_platonic_solid(ax, center, solid_type, size=0.2, color='blue', alpha=0.5):
    """Draw a simple 2D representation of a Platonic solid."""
    if solid_type == "tetrahedron":
        # Triangle for tetrahedron projection
        ax.add_patch(RegularPolygon(center, numVertices=3, radius=size, color=color, alpha=alpha))
    elif solid_type == "cube":
        # Square for cube
        ax.add_patch(RegularPolygon(center, numVertices=4, radius=size, color=color, alpha=alpha))
    elif solid_type == "octahedron":
        # Diamond shape
        ax.add_patch(RegularPolygon(center, numVertices=4, radius=size, color=color, alpha=alpha, orientation=math.pi/4))
    elif solid_type == "dodecahedron":
        # Pentagon
        ax.add_patch(RegularPolygon(center, numVertices=5, radius=size, color=color, alpha=alpha))
    elif solid_type == "icosahedron":
        # Triangle with lines
        ax.add_patch(RegularPolygon(center, numVertices=3, radius=size, color=color, alpha=alpha))
        ax.plot([center[0]-size/2, center[0]+size/2], [center[1]-size/4, center[1]-size/4], color=color, alpha=alpha)

def draw_kabbalah_tree(ax, alpha=0.5):
    """Draw a simple representation of the Kabbalah Tree of Life."""
    sephirot = [
        (0, 4.5, "Keter"), ( -1, 3.5, "Chokhmah"), (1, 3.5, "Binah"),
        (-1, 2, "Chesed"), (1, 2, "Gevurah"),
        (0, 1, "Tiferet"),
        (-1, 0, "Netzach"), (1, 0, "Hod"),
        (0, -1, "Yesod"),
        (0, -2, "Malkuth")
    ]
    for x, y, label in sephirot:
        ax.add_patch(Circle((x, y), 0.2, color='white', alpha=alpha))
        ax.text(x, y, label, fontsize=8, ha='center', va='center', color='black')
    
    paths = [
        (0, (0,4.5), (-1,3.5)), (1, (0,4.5), (1,3.5)),
        (2, (-1,3.5), (1,3.5)), (3, (-1,3.5), (-1,2)), (4, (1,3.5), (1,2)),
        (5, (-1,2), (1,2)), (6, (-1,2), (0,1)), (7, (1,2), (0,1)),
        (8, (0,1), (-1,0)), (9, (0,1), (1,0)), (10, (-1,0), (1,0)),
        (11, (-1,0), (0,-1)), (12, (1,0), (0,-1)), (13, (0,-1), (0,-2))
    ]
    for _, start, end in paths:
        ax.plot([start[0], end[0]], [start[1], end[1]], color='white', alpha=alpha)

def animate_platonic_solid(fig, ax, solid_type, color):
    """Create an animation of a rotating Platonic solid representation."""
    def update(frame):
        ax.clear()
        angle = frame * (2 * math.pi / 60)
        draw_platonic_solid(ax, (0, 0), solid_type, size=0.5, color=color, alpha=0.8)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')
    
    anim = animation.FuncAnimation(fig, update, frames=60, interval=50)
    return anim

def generate_crystal_grid(life_path, element, destiny, soul_urge, personality):
    fig, ax = plt.subplots(figsize=(8, 8))
    color = ELEMENT_CRYSTAL_COLORS.get(element, "purple")
    
    # Add Sacred Geometry: Flower of Life background
    draw_flower_of_life(ax, (0, 0), 0.5, num_circles=life_path + destiny % 10)
    
    # Add Metatron's Cube
    draw_metatrons_cube(ax, (0, 0), 0.5)
    
    # Add Kabbalah Tree of Life
    draw_kabbalah_tree(ax, alpha=0.3)
    
    # Central crystal with dynamic shape based on personality
    central_sides = (personality % 5) + 3  # 3 to 7 sides
    ax.add_patch(RegularPolygon((0, 0), numVertices=central_sides, radius=0.3, color=color, alpha=0.8, orientation=math.pi / central_sides))
    
    # Dynamic layers based on soul_urge and destiny, with varying rotations
    layers = min((life_path + soul_urge + personality) % 5 + 1, 5)  # Up to 5 layers for more dynamism
    rotation_offset = math.pi / (destiny or 1)  # Dynamic rotation based on destiny
    for layer in range(1, layers + 1):
        num_crystals = (destiny + soul_urge + layer) % (8 * layer) + 5 * layer  # Increased variability
        for i in range(num_crystals):
            angle = 2 * math.pi * i / num_crystals + (layer * rotation_offset)
            x = layer * 0.8 * math.cos(angle)
            y = layer * 0.8 * math.sin(angle)
            shape_sides = ((layer + personality) % 5) + 3  # Vary shape per layer
            ax.add_patch(RegularPolygon((x, y), numVertices=shape_sides, radius=0.15 / layer, color=color, alpha=0.7 - 0.1 * layer, orientation=angle))
    
    # Enhanced connections with NetworkX for dynamic graph, adding more cross-links
    G = nx.Graph()
    positions = {(0,0): (0,0)}
    for layer in range(1, layers + 1):
        num_crystals = (destiny + soul_urge + layer) % (8 * layer) + 5 * layer
        for i in range(num_crystals):
            angle = 2 * math.pi * i / num_crystals + (layer * rotation_offset)
            x = layer * 0.8 * math.cos(angle)
            y = layer * 0.8 * math.sin(angle)
            positions[(layer, i)] = (x, y)
            # Connect to center
            G.add_edge((0,0), (layer, i))
            # Connect to previous layer dynamically
            if layer > 1:
                prev_num = (destiny + soul_urge + layer - 1) % (8 * (layer-1)) + 5 * (layer-1)
                prev_i = i % prev_num
                G.add_edge((layer-1, prev_i), (layer, i))
            # Circumferential connections
            if i > 0:
                G.add_edge((layer, i-1), (layer, i))
            G.add_edge((layer, (i + 1) % num_crystals), (layer, i))  # Close the ring
            # Add spiral connections for dynamism
            if i % 3 == 0 and layer > 2:
                spiral_i = (i // 3) % (prev_num // 2 + 1)
                G.add_edge((layer, i), (layer-2, spiral_i))
    
    nx.draw_networkx_edges(G, positions, ax=ax, edge_color='gold', alpha=0.4, style='dotted', width=1.5)
    
    # Add Platonic Solids at outer positions
    platonic_solids = ["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"]
    for i, solid in enumerate(platonic_solids):
        angle = i * (2 * math.pi / 5)
        x = 3 * math.cos(angle)
        y = 3 * math.sin(angle)
        draw_platonic_solid(ax, (x, y), solid, size=0.2, color=color, alpha=0.6)
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Dynamic Sacred Crystal Grid for Life Path {life_path} ({element})", color='white')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    return fig

# Main App
st.title("Occult Destiny Weaver: Enhanced Numerology & Astrology Edition 🧙‍♂️🔮✨🌙")

name = st.text_input("Enter your full name 🧙‍♀️📜", value="Mahaan")
birth_date = st.date_input("Enter your birth date 🌌📅", value=datetime.date(1993, 7, 12), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))
birth_time = st.time_input("Enter your birth time (required for ascendant and midheaven) ⏳🪄", value=datetime.time(12, 26), step=60)
birth_city = st.selectbox("Select your birth city (or closest) 🏰🌍", list(CITY_COORDS.keys()) + ["Custom"])
if birth_city == "Custom":
    user_lat = st.number_input("Enter latitude 🌐🧙‍♂️", value=13.32, min_value=-90.0, max_value=90.0)
    user_lon = st.number_input("Enter longitude 🌐🔮", value=75.77, min_value=-180.0, max_value=180.0)
else:
    user_lat, user_lon = CITY_COORDS.get(birth_city, (0, 0))

if st.button("Weave My Destiny 🕸️🧙‍♀️🔮✨"):
    if birth_time is None:
        st.warning("Birth time is required for ascendant and midheaven calculations. Using defaults where possible. ⚠️🪄")
    
    # Numerology
    life_path, lp_details = calculate_life_path(birth_date)
    destiny, dest_details = calculate_destiny_number(name)
    soul_urge = calculate_soul_urge(name)
    personality = calculate_personality(name)
    
    st.subheader("Detailed Numerology Calculations 📊🔢🧙‍♂️")
    st.write(f"**Life Path Number**: {life_path} 🛤️🌟")
    st.json(lp_details)
    st.write(f"**Destiny Number**: {destiny} 🎯✨")
    st.write("Letter Values: 📜🪄", dest_details)
    st.write(f"**Soul Urge Number (Inner Self)**: {soul_urge} ❤️🔮")
    st.write(f"**Personality Number (Outer Self)**: {personality} 😊🧙‍♀️")
    
    # Numerology Chart
    num_df = pd.DataFrame({
        "Aspect": ["Life Path", "Destiny", "Soul Urge", "Personality"],
        "Value": [life_path, destiny, soul_urge, personality]
    })
    st.bar_chart(num_df.set_index("Aspect"))
    
    # Astrology
    zodiac = get_zodiac_sign(birth_date.month, birth_date.day)
    element = get_zodiac_element(zodiac)
    st.subheader("Astrology Integration ♈♉♊🧙‍♂️🌌")
    st.write(f"**Zodiac Sign**: {zodiac} 🌟🔮")
    st.write(f"**Element**: {element} 🌊🔥🌍💨🪄")
    st.write("Innovative Astro-Numerology: Your zodiac element influences your aura, creating unique energetic alignments. ⚡🧬✨")
    
    aura_color = get_aura_color(life_path, element)
    st.write(f"**Aura Color**: {aura_color} 🌈🧙‍♀️")
    
    # Ascendant and Midheaven
    asc_sign = ""
    mc_sign = ""
    if birth_time is not None:
        birth_datetime_local = datetime.datetime.combine(birth_date, birth_time)
        asc_deg, asc_display, mc_deg, mc_display = calculate_ascendant_and_mc(birth_datetime_local, user_lat, user_lon)
        asc_sign = asc_display
        mc_sign = mc_display
        st.write(f"**Ascendant (Rising Sign)**: {asc_sign} ({asc_deg:.2f}°) 🌅🪄")
        st.write(f"**Midheaven (MC)**: {mc_sign} ({mc_deg:.2f}°) 🏔️🔮")
    
    # Moon Phase on Birth
    birth_datetime = datetime.datetime.combine(birth_date, birth_time or datetime.time(0,0))
    moon_pos = moon_position(birth_datetime)
    moon_phase_name = moon_phase(moon_pos)
    st.write(f"**Moon Phase on Birth**: {moon_phase_name} ({round(float(moon_pos), 3)}) 🌙🧙‍♂️")
    
    # Ley Lines
    nearest_site, distance = find_nearest_site(user_lat, user_lon)
    st.subheader("Ley Line Mysticism 🗺️🌀🧙‍♀️")
    st.write(f"Nearest Mystical Site: {nearest_site} ({distance:.2f} km away) 📍✨")
    st.write(f"Astro-Ley Alignment: Your {zodiac} energy resonates with {nearest_site}'s ancient power. 🌌🪄🔮")
    
    # Interactive Map
    sites_df = pd.DataFrame({
        "lat": [user_lat] + [lat for lat, _ in MYSTICAL_SITES.values()],
        "lon": [user_lon] + [lon for _, lon in MYSTICAL_SITES.values()],
        "label": ["Your Birth Spot"] + list(MYSTICAL_SITES.keys())
    })
    st.map(sites_df)
    
    # Fate Spinner
    prediction = generate_prediction(life_path, zodiac, element, moon_phase_name, asc_sign, mc_sign)
    st.subheader("Fate Spinner Prediction 🎡🔮🧙‍♂️")
    st.write(prediction)
    if st.button("Spin Again 🔄🪄"):
        prediction = generate_prediction(life_path, zodiac, element, moon_phase_name, asc_sign, mc_sign)
        st.write(prediction)
    
    # Spell Card
    incantation = generate_incantation(name, zodiac, moon_phase_name, asc_sign, mc_sign)
    st.subheader("Shareable Spell Card 🃏📜✨")
    st.text_area("Your Custom Incantation", incantation, height=100)
    
    # Daily Horoscope
    st.subheader("Daily Horoscope 📅🌟🧙‍♀️")
    horoscope = generate_daily_horoscope(zodiac)
    st.write(horoscope)
    
    # Tarot Draw
    st.subheader("Tarot Insight 🃏✨🔮")
    if st.button("Draw a Tarot Card 🪄🧙‍♂️"):
        tarot = draw_tarot(zodiac)
        st.write(tarot)
    
    # Rune Casting
    st.subheader("Rune Casting ᚠᚢᚦᚨᚱᚲ🧙‍♂️🔮")
    if st.button("Cast Runes 🪄✨"):
        runes = cast_runes()
        for rune in runes:
            st.write(rune)
    
    # I Ching Divination
    st.subheader("I Ching Divination 📖🧙‍♀️🔮")
    if st.button("Cast I Ching 🪄🌌"):
        current_hex, changing_lines, future_hex = cast_i_ching()
        st.write(f"Current Hexagram: {current_hex} 📜")
        if changing_lines:
            st.write("Changing Lines: " + ", ".join(changing_lines) + " 🔄")
        else:
            st.write("No changing lines. 🔒")
        st.write(f"Future Hexagram: {future_hex} 🌟")
    
    # Crystal Grid Visualization
    st.subheader("Advanced Crystal Grid Visualization 💎🌀🧙‍♂️")
    st.write("An enhanced mystical crystal grid with layered patterns and sacred geometry (Flower of Life, Metatron's Cube, Platonic Solids) based on your Life Path, Destiny, Soul Urge, Personality, and Element, channeling cosmic energies. 🔮✨")
    fig = generate_crystal_grid(life_path, element, destiny, soul_urge, personality)
    st.pyplot(fig)
    
    # Animated Platonic Solid
    st.subheader("Animated Platonic Solid Visualization 🧊🔄🧙‍♀️")
    solid_type = st.selectbox("Choose a Platonic Solid to Animate", ["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"])
    if st.button("Animate Solid 🪄"):
        anim_fig, anim_ax = plt.subplots(figsize=(6, 6))
        anim_fig.patch.set_facecolor('black')
        anim_ax.set_facecolor('black')
        anim = animate_platonic_solid(anim_fig, anim_ax, solid_type, color=ELEMENT_CRYSTAL_COLORS.get(element, "purple"))
        buf = io.BytesIO()
        anim.save(buf, format='gif', writer='pillow', fps=30)
        buf.seek(0)
        st.image(buf, use_column_width=True)

# Compatibility Checker
with st.expander("Check Compatibility with Another Person 💑🔍🧙‍♀️"):
    name2 = st.text_input("Enter second person's full name 📝🪄")
    birth_date2 = st.date_input("Enter second person's birth date 📅🔮", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))
    birth_city2 = st.selectbox("Select second person's birth city 🏰🌍", list(CITY_COORDS.keys()) + ["Custom"])
    if birth_city2 == "Custom":
        user_lat2 = st.number_input("Enter second latitude 🌐🧙‍♂️", -90.0, 90.0)
        user_lon2 = st.number_input("Enter second longitude 🌐🔮", -180.0, 180.0)
    else:
        user_lat2, user_lon2 = CITY_COORDS.get(birth_city2, (0, 0))
    
    if st.button("Calculate Compatibility 📊❤️🪄") and name and name2:
        life_path2, _ = calculate_life_path(birth_date2)
        zodiac2 = get_zodiac_sign(birth_date2.month, birth_date2.day)
        element2 = get_zodiac_element(zodiac2)
        compat_score = calculate_compatibility(life_path, element, life_path2, element2)
        st.write(f"Compatibility Score: {compat_score}% 📈✨")
        st.write(f"Your {zodiac} ({element}) and their {zodiac2} ({element2}) create a unique synergy. ⚡🤝🧙‍♂️")

# Future Prediction Slider
st.subheader("Future Destiny Peek 🔮⏳🧙‍♀️")
future_year = st.slider("Select a future year 📅🪄", birth_date.year + 1, birth_date.year + 50)
future_date = datetime.date(future_year, birth_date.month, birth_date.day)
future_lp, _ = calculate_life_path(future_date)
st.write(f"In {future_year}, your vibrational energy shifts to Life Path influence {future_lp}. 🌌✨🔮")
