import os

file_paths = [
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/y's/yohji yamamoto/pattern turtleneck top/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/vexed generation/joe hunter, adam thrope/front velcro pants/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/proving ground 4/hooman/memo/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/menichetti/reberto menichetti/joghurt/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/marithé + françois girbaud/françois girbaud, marithé girbaud/baby alpaca cardigan/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/issey miyake/issey miyake/mouth of truth/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/issey miyake/issey miyake/draped front top/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/giorgio armani le collezioni/giorgio armani/5 button jacket/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/allegri/martin margiela/puckered jacquard jacket/info.txt",
    "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma/archive/a-poc/dai fujiwara/a-poc inside t shirt/info.txt"
]

for info_path in file_paths:
    if not os.path.exists(info_path):
        print(f"File not found: {info_path}")
        continue

    with open(info_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Create YAML frontmatter
    yaml_content = "---"
    for line in lines:
        if ':' in line:
            yaml_content += line
    yaml_content += "---"

    # Write to index.md
    dir_path = os.path.dirname(info_path)
    md_path = os.path.join(dir_path, 'index.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    print(f"Created {md_path}")

    # Remove old info.txt
    os.remove(info_path)
    print(f"Removed {info_path}")
