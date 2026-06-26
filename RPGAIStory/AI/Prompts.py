from .Persona import Persona

def BuildPrompt(player, world, last_story, last_enemies, last_terrain, choice):
    return f"""
    {Persona}

    Player stats:
    {{
    "health": {player.health},
    "gold": {player.gold},
    "inventory": {player.inventory},
    "statuses": {player.statuses}
    }}

    World state:
    {{
    "storyline": "{world.current_storyline}",
    "location": "{world.location}",
    "time_played": {world.time_played}
    }}

    Last story:
    \"\"\"{last_story}\"\"\"

    Last enemies
    \"\"\"{last_enemies}\"\"\"
    
    Last terrain:
    \"\"\"{last_terrain}\"\"\"

    Player choice:
    \"\"\"{choice}\"\"\"

    Respond using this format:

    [STORY]
    (write immersive story text)

    [DATA]
    Optional, not always present. Structured data in JSON format describing enemies, terrain, items, etc. Use this to inform the UI on what to display and how to calculate outcomes.
    (JSON describing enemies, terrain, items, etc.)
        ex. 
        {{
        "enemies": [
            {{
            "name": "Shadow Wolf",
            "health": 45,
            "inventory": [
                {{"name": "Sharp Claws", "damage": 8, "durability": "infinite"}}
            ],
            "statuses": ["Rabid"],
            }}
        ],
        "terrain": {{
            "name": "Village Square",
            "effects": "Cramped space; limited movement for dodging."
        }},
        "loot_table": ["Wolf Pelt", "Shadow Essence", "10 Gold"]
        }}

    [STATS]
    (JSON describing stat changes)

    [CHOICES]
    - choice 1
    - choice 2
    - choice 3
    - choice 4
"""
