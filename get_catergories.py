PRIORITY_KEYBINDS = [
    "key_key.attack",
    "key_key.use",
    "key_key.forward",
    "key_key.left",
    "key_key.back",
    "key_key.right",
    "key_key.jump",
    "key_key.sneak",
    "key_key.sprint",
    "key_key.drop",
    "key_key.inventory",
    "key_key.chat",
    "key_key.playerlist",
    "key_key.pickItem",
    "key_key.command",
    "key_key.socialInteractions",
    "key_key.screenshot",
    "key_key.togglePerspective",
    "key_key.smoothCamera",
    "key_key.fullscreen",
    "key_key.spectatorOutlines",
    "key_key.swapOffhand",
    "key_key.saveToolbarActivator",
    "key_key.loadToolbarActivator",
    "key_key.advancements",
    "key_key.hotbar.1",
    "key_key.hotbar.2",
    "key_key.hotbar.3",
    "key_key.hotbar.4",
    "key_key.hotbar.5",
    "key_key.hotbar.6",
    "key_key.hotbar.7",
    "key_key.hotbar.8",
    "key_key.hotbar.9",
]

def categorize_keybind(keybind):
    """Extract the category of a keybind."""
    keybind = keybind.split(":", 1)[0]  # Remove everything after `:`

    # Define prefixes to remove and clean up
    prefixes_to_remove = [
        "key_key.", "key_keybind.", "key_keybinds.", "key_mod.",
        "key_info.", "key_gui.", "key_keys.", "key_Options Gui:"
    ]

    # Remove specific prefixes
    for prefix in prefixes_to_remove:
        if keybind.startswith(prefix):
            keybind = keybind[len(prefix):]
            break  # Only one prefix can apply

    # Extract the category by splitting the keybind string
    if keybind.startswith("key_"):
        keybind = keybind[len("key_"):]  # Remove the "key_" prefix
    elif ":key." in keybind:
        keybind = keybind.split(":key.", 1)[-1]  # Extract after ":key."

    # Get the category, which is the first part before any dots (e.g., "attack" from "key_key.attack")
    category = keybind.split(".")[0]

    # Return the cleaned category (remove '_key' if present)
    return category.replace("_key", "")  # Remove '_key' suffix if present

def list_categories(keybinds):
    """Generate a list of unique categories from the keybinds."""
    categories = set()
    for keybind in keybinds:
        # Only consider valid keybinds that contain "key_" or ":key." and are not in the priority prefixes
        if ("key_" in keybind or ":key." in keybind):
            # Exclude keybinds that match any of the PRIORITY_KEYBINDS_PREFIXES
            if not any(keybind.startswith(prefix) for prefix in PRIORITY_KEYBINDS):
                category = categorize_keybind(keybind)
                categories.add(category)
    return sorted(categories)  # Sort the categories alphabetically

# Read the merged keybinds from file
with open("options.txt", "r") as file:
    keybinds = [line.strip() for line in file.readlines()]

# Generate the list of categories, excluding PRIORITY_KEYBINDS
categories = list_categories(keybinds)

# Output the categories
with open("categories.txt", "w") as file:
    for category in categories:
        file.write(category + "\n")

print("Categories saved to categories.txt")
