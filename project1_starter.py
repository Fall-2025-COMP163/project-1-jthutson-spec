"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Tj Hutson
Date: 10/30/2025

AI Usage:
- AI helped generate initial function scaffolding and file I/O examples.
- I reviewed and understand each line and can explain the logic.
"""

def create_character(name, character_class):
    """
    Creates a new character dictionary with calculated stats.
    Returns: dict with keys:
    name, class, level, strength, magic, health, gold
    """
    # All new characters start at level 1
    level = 1

    # Get stats based on class + level
    strength, magic, health = calculate_stats(character_class, level)

    # Build the character dictionary
    character = {
        "name": name,
        "class": character_class,
        "level": level,
        "strength": strength,
        "magic": magic,
        "health": health,
        "gold": 100,  # starter gold
    }

    return character


def calculate_stats(character_class, level):
    """
    Calculates base stats based on class and level.
    You can adjust these formulas however you want,
    but keep the class identities.
    Returns: (strength, magic, health)
    """

    # Normalize the class name to handle 'warrior' vs 'Warrior'
    cls = character_class.lower()

    if cls == "warrior":
        # High strength, low magic, high health
        base_str = 12
        base_mag = 2
        base_hp = 120
        # Scale by level
        strength = base_str + (level * 3)
        magic = base_mag + (level * 1)
        health = base_hp + (level * 10)

    elif cls == "mage":
        # Low strength, high magic, medium health
        base_str = 4
        base_mag = 14
        base_hp = 90
        strength = base_str + (level * 1)
        magic = base_mag + (level * 4)
        health = base_hp + (level * 6)

    elif cls == "rogue":
        # Medium strength, medium magic, low health
        base_str = 8
        base_mag = 8
        base_hp = 80
        strength = base_str + (level * 2)
        magic = base_mag + (level * 2)
        health = base_hp + (level * 5)

    elif cls == "cleric":
        # Medium strength, high magic, high health
        base_str = 7
        base_mag = 12
        base_hp = 110
        strength = base_str + (level * 2)
        magic = base_mag + (level * 3)
        health = base_hp + (level * 8)

    else:
        # Fallback if class is unknown
        # (this prevents crashing in tests)
        base_str = 5
        base_mag = 5
        base_hp = 80
        strength = base_str + (level * 1)
        magic = base_mag + (level * 1)
        health = base_hp + (level * 5)

    return (strength, magic, health)


def save_character(character, filename):
    """
    Saves character to text file in the exact format required.

    Character Name: [name]
    Class: [class]
    Level: [level]
    Strength: [strength]
    Magic: [magic]
    Health: [health]
    Gold: [gold]

    Returns True if successful, False if error.
    """
    try:
        with open(filename, "w") as f:
            f.write(f"Character Name: {character['name']}\n")
            f.write(f"Class: {character['class']}\n")
            f.write(f"Level: {character['level']}\n")
            f.write(f"Strength: {character['strength']}\n")
            f.write(f"Magic: {character['magic']}\n")
            f.write(f"Health: {character['health']}\n")
            f.write(f"Gold: {character['gold']}\n")
        return True
    except OSError:
        # If anything goes wrong with the file (permissions, path, etc.)
        return False


def load_character(filename):
    """
    Loads character from a text file that was saved
    with save_character().
    Returns: character dict, or None if file not found / bad format.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None

    # We'll store parsed values here
    character = {}

    # Each line is like: "Character Name: Aria"
    # So we split on ": " and take the second part
    for line in lines:
        line = line.strip()
        if line.startswith("Character Name:"):
            character["name"] = line.split(": ", 1)[1]
        elif line.startswith("Class:"):
            character["class"] = line.split(": ", 1)[1]
        elif line.startswith("Level:"):
            character["level"] = int(line.split(": ", 1)[1])
        elif line.startswith("Strength:"):
            character["strength"] = int(line.split(": ", 1)[1])
        elif line.startswith("Magic:"):
            character["magic"] = int(line.split(": ", 1)[1])
        elif line.startswith("Health:"):
            character["health"] = int(line.split(": ", 1)[1])
        elif line.startswith("Gold:"):
            character["gold"] = int(line.split(": ", 1)[1])

    # Basic validation — make sure we actually got the keys
    required_keys = ["name", "class", "level", "strength", "magic", "health", "gold"]
    for key in required_keys:
        if key not in character:
            return None

    return character


def display_character(character):
    """
    Prints a formatted character sheet to the console.
    """
    print("=== CHARACTER SHEET ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"Strength: {character['strength']}")
    print(f"Magic: {character['magic']}")
    print(f"Health: {character['health']}")
    print(f"Gold: {character['gold']}")


def level_up(character):
    """
    Increases character level by 1 and recalculates stats
    based on their class and new level.
    """
    # Increase level
    character["level"] += 1

    # Recalculate stats using the same class
    strength, magic, health = calculate_stats(character["class"], character["level"])

    # Update stats on the same dictionary
    character["strength"] = strength
    character["magic"] = magic
    character["health"] = health
    # Optionally give some gold on level up
    character["gold"] += 25


# Main program area (optional - for testing your functions)
if __name__ == "__main__":
    print("=== CHARACTER CREATOR ===")
    name = input("Enter character name: ")
    cclass = input("Enter character class (Warrior/Mage/Rogue/Cleric): ")

    char = create_character(name, cclass)
    display_character(char)

    # Test saving
    save_name = "my_character.txt"
    if save_character(char, save_name):
        print(f"Character saved to {save_name}")

    # Test loading
    loaded_char = load_character(save_name)
    if loaded_char:
        print("\nLoaded from file:")
        display_character(loaded_char)

    # Test level up
    print("\nLeveling up...")
    level_up(loaded_char)
    display_character(loaded_char)
