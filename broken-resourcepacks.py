import os

# Define input paths
MAIN_OPTIONS_FILE = os.path.join("options_main", "options.txt")
OTHER_OPTIONS_FILE = os.path.join("options_other", "options.txt")
OUTPUT_FILE = "options.txt"

def load_options(file_path):
    print(file_path)
    """Load options from a file and return the list of lines."""
    options = []
    resource_packs = None  # Track the resourcePacks line
    if not os.path.exists(file_path):
        return options, resource_packs

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("resourcePacks:"):  # Resource packs line
                resource_packs = line
                print(resource_packs)
            options.append(line)

    return options, resource_packs

def merge_resource_packs(main_packs, other_packs):
    """Merge and sort resourcePacks, ensuring no duplicates."""
    # Convert to list, combine, and remove duplicates
    merged_packs = sorted(set(main_packs.split(",") + other_packs.split(",")))
    # Sort and format them back to the correct string format
    return 'resourcePacks:[' + ', '.join(merged_packs) + ']'

# Load options and resourcePacks from both files
main_options, main_resource_packs = load_options(MAIN_OPTIONS_FILE)
other_options, other_resource_packs = load_options(OTHER_OPTIONS_FILE)

# If resourcePacks exists in both files, merge them
merge_resource_packs(main_resource_packs, other_resource_packs)
# if main_resource_packs and other_resource_packs:
#     merged_resource_packs = merge_resource_packs(main_resource_packs, other_resource_packs)
# elif main_resource_packs:
#     merged_resource_packs = main_resource_packs
# elif other_resource_packs:
#     merged_resource_packs = other_resource_packs
# else:
#     merged_resource_packs = None

# Write merged options to the output file
with open(OUTPUT_FILE, "w") as file:
    # Insert resourcePacks at the same position as in the main options file
    resource_written = False
    for line in main_options:
        if line.startswith("resourcePacks:") and not resource_written:
            if merged_resource_packs:
                file.write(merged_resource_packs + "\n")
                resource_written = True
        # Write other options unchanged
        if not line.startswith("resourcePacks:"):
            file.write(line + "\n")

    # If resourcePacks wasn't written (case where it's in `other_options` but not `main_options`):
    if not resource_written and merged_resource_packs:
        file.write(merged_resource_packs + "\n")

print(f"Merged options saved to {OUTPUT_FILE}")
