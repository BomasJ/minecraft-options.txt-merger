import os

# Define input paths
MAIN_OPTIONS_FILE = os.path.join("options_main", "options.txt")
OTHER_OPTIONS_DIR = "options_other"  # Directory with other option files
OUTPUT_FILE = "options.txt"

def merge_keybinds(main_keybinds, other_keybinds):
    """Merge two sets of keybinds, ensuring no replacement if the key exists in main_keybinds."""
    if not isinstance(main_keybinds, list) or not isinstance(other_keybinds, list):
        raise ValueError("Both main_keybinds and other_keybinds should be lists.")

    merged = {bind.split(":")[0]: bind for bind in main_keybinds}  # Use the key before the first ":"

    # Now, add keybinds from `other_keybinds` only if they don't already exist in `merged`
    for bind in other_keybinds:
        key = bind.split(":", 1)[0]  # Get the key (before the ":")
        if key not in merged:
            merged[key] = bind

    return list(merged.values())

def load_options_and_keybinds(file_path):
    """Load options, keybinds, and resourcePacks from a file."""
    options = []
    keybinds = []
    resource_packs = None  # Track the resourcePacks line
    if not os.path.exists(file_path):
        return options, keybinds, resource_packs

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("key_"):  # Keybinds
                keybinds.append(line)
            elif line.startswith("resourcePacks:"):  # get resource pack line
                resource_packs = line
                options.append(line)
            else:
                options.append(line)

    return options, keybinds, resource_packs


def merge_resource_packs(*packs):
    """Merge and format multiple resourcePacks, ensuring no duplicates, sorting, and handling empty values."""
    # Combine all resource packs, split by commas, remove empty values, and merge them into a set for uniqueness
    merged_packs = set()

    for pack in packs:
        if pack:  # Only process non-empty resource packs
            # Clean up and add resource packs to the set (remove "resourcePacks:" part if needed)
            pack_list = pack.replace("resourcePacks:[", "").replace("]", "").split(",")
            merged_packs.update([p.strip() for p in pack_list if p.strip()])

    # Sort the merged resource packs
    sorted_packs = sorted(merged_packs)

    # Return the final formatted resourcePacks line if there are any merged packs
    if sorted_packs:
        return f"[{','.join(sorted_packs)}]"
    return None  # If no resource packs are present


# Load options, keybinds, and resourcePacks from the main options file
main_options, main_keybinds, main_resource_packs = load_options_and_keybinds(MAIN_OPTIONS_FILE)

# Initialize the list to collect all keybinds and resource packs from other files
all_other_keybinds = []
all_other_resource_packs = []

# Loop through files in the options_other directory
for filename in os.listdir(OTHER_OPTIONS_DIR):
    if filename.endswith(".txt"):  # Process only .txt files
        other_options_file = os.path.join(OTHER_OPTIONS_DIR, filename)
        _, other_keybinds, other_resource_packs = load_options_and_keybinds(other_options_file)

        # Collect keybinds and resource packs from other files
        all_other_keybinds.extend(other_keybinds)
        if other_resource_packs:
            all_other_resource_packs.append(other_resource_packs.strip())

# Merge the keybinds from main and all other options
merged_keybinds = merge_keybinds(main_keybinds, all_other_keybinds)

# Merge resource packs if they exist in both the main and other options
merged_resource_packs = merge_resource_packs(main_resource_packs, *all_other_resource_packs)

# Output the options, merged keybinds, and merged resource packs to options.txt
with open(OUTPUT_FILE, "w") as file:
    resource_written = False
    incompatible_written = False
    for line in main_options:
        if line.startswith("resourcePacks:") and not resource_written:
                file.write("resourcePacks:" + merged_resource_packs + "\n")
                resource_written = True
        elif line.startswith("incompatibleResourcePacks:") and not incompatible_written:
                file.write("incompatibleResourcePacks:" + merged_resource_packs + "\n")
                incompatible_written = True
        else:
            file.write(line + "\n")

    # If main options.txt didn't have a resourcePacks line, add the merged resource packs
    if not resource_written and merged_resource_packs:
        file.write(merged_resource_packs + "\n")

    # Write the merged keybinds
    for keybind in merged_keybinds:
        file.write(keybind + "\n")

print(f"Merged options, keybinds, and resource packs saved to {OUTPUT_FILE}")
