#!/bin/bash

# Function to generate JSON for directory tree with sizes
generate_json() {
    local dir=${1:-.}
    local indent=${2:-0}
    local prefix=$(printf '%*s' "$indent" '')

    echo "${prefix}\"$(basename "$dir")\": {"
    echo "${prefix}  \"absolute_path\": \"$(realpath "$dir")\","
    echo "${prefix}  \"directories\": ["

    local first=true
    find "$dir" -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' item; do
        if [ "$first" = true ]; then
            first=false
        else
            echo "${prefix}    ,"
        fi
        local size=$(du -sh "$item" 2>/dev/null | cut -f1)
        echo "${prefix}    [\"$(basename "$item")\", \"$size\"]"
    done

    echo "${prefix}  ],"
    echo "${prefix}  \"files\": ["

    first=true
    find "$dir" -mindepth 1 -maxdepth 1 -type f -print0 | while IFS= read -r -d '' item; do
        if [ "$first" = true ]; then
            first=false
        else
            echo "${prefix}    ,"
        fi
        local size=$(du -sh "$item" 2>/dev/null | cut -f1)
        echo "${prefix}    [\"$(basename "$item")\", \"$size\"]"
    done

    echo "${prefix}  ]"

    # Recursively call generate_json for each subdirectory
    find "$dir" -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' item; do
        echo "${prefix},"
        generate_json "$item" $((indent + 2))
    done

    echo "${prefix}}"
}

# Main script execution
output_file="directory_tree.json"
{
    echo "{"
    generate_json "$1"
    echo "}"
} > "$output_file"

echo "Directory tree with sizes has been saved to $output_file"
