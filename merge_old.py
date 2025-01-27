import os

# Define input and output paths
MAIN_OPTIONS_FILE = os.path.join("options_main", "options.txt")
OTHER_OPTIONS_FILE = os.path.join("options_other", "options.txt")
OUTPUT_FILE = "options.txt"

# Priority keybinds to be placed at the top
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

def load_options(file_path):
    """Load options from a file and split into options and keybinds."""
    options = []
    keybinds = []
    if not os.path.exists(file_path):
        return options, keybinds

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("key_"):
                keybinds.append(line)
            else:
                options.append(line)

    return options, keybinds


def categorize_keybind(keybind):
    """Extract the category of a keybind."""
    keybind = keybind.split(":", 1)[0]  # Remove everything after `:`

    # Define prefixes to remove and clean up
    prefixes_to_remove = [
        "key_key.", "key_keybind.", "key_keybinds.", "key_mod.",
        "key_info.", "key_gui.", "key_keys."
    ]

    # Remove specific prefixes
    for prefix in prefixes_to_remove:
        if keybind.startswith(prefix):
            keybind = keybind[len(prefix):]
            break  # Only one prefix can apply

    # Handle "key_" prefix to extract the category (e.g., "key_create" => "create")
    if keybind.startswith("key_"):
        keybind = keybind[len("key_"):]

    # Handle known prefixes and split
    if keybind.startswith("key_key.") or keybind.startswith("key_keybind.") or keybind.startswith(
            "key_keybinds.") or keybind.startswith("key_mod."):
        parts = keybind.split(".", 2)
        category = parts[1] if len(parts) > 1 else "unknown"
    elif keybind.startswith("key_info.") or keybind.startswith("key_gui."):
        parts = keybind.split(".", 2)
        category = parts[1] if len(parts) > 1 else "unknown"
    else:
        category = keybind.split(".")[0]

    # Return the category, removing '_key' if present
    return category.replace("_key", "")

def merge_keybinds(main_keybinds, other_keybinds):
    """Merge keybinds, ensuring duplicates are handled and new categories are appended."""
    merged = {bind.split(":")[0]: bind for bind in main_keybinds}
    categories = {categorize_keybind(bind): [] for bind in main_keybinds}

    for bind in other_keybinds:
        key, value = bind.split(":", 1)
        category = categorize_keybind(bind)

        if key in merged:
            if "key.keyboard.unknown" in merged[key]:
                merged[key] = bind  # Replace unknown bindings
        else:
            merged[key] = bind
            if category in categories:
                categories[category].append(bind)
            else:
                categories[category] = [bind]

    return merged, categories

def write_output(options, keybinds, categories):
    """Write the merged options and keybinds to the output file."""
    with open(OUTPUT_FILE, "w") as file:
        for option in options:
            file.write(option + "\n")

        file.write("\n")  # Blank line between options and keybinds

        # Write priority keybinds
        for key_prefix in PRIORITY_KEYBINDS:
            for full_key, bind in list(keybinds.items()):
                if full_key.startswith(key_prefix):
                    file.write(bind + "\n")
                    del keybinds[full_key]

        # Write categorized keybinds
        for category, binds in categories.items():
            for bind in binds:
                if bind in keybinds.values():
                    file.write(bind + "\n")

        # Write uncategorized keybinds
        for bind in keybinds.values():
            file.write(bind + "\n")

        # Debugging information
        print("\nCategories: " + ", ".join(categories.keys()) + "\n")

# Load options and keybinds from both files
main_options, main_keybinds = load_options(MAIN_OPTIONS_FILE)
_, other_keybinds = load_options(OTHER_OPTIONS_FILE)

# Merge keybinds
merged_keybinds, categories = merge_keybinds(main_keybinds, other_keybinds)

# Write the output
write_output(main_options, merged_keybinds, categories)
