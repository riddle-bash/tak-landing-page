import re

def update_img_src_paths(html_content, new_base_path):
    def replacer(match):
        original = match.group(1)
        filename = original.lstrip("/")  # remove leading slash if present

        # Skip if already starts with correct base path
        if filename.startswith(new_base_path):
            return f'src="{original}"'

        return f'src="{new_base_path}/{filename}"'

    # Match src="..." inside <img> tags
    return re.sub(r'src="([^"]+)"', replacer, html_content)

# === Config ===
html_file_path = "landing-page.html"
new_img_path = "../../images/landing-page"

# === Read HTML ===
with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# === Update paths ===
updated_html = update_img_src_paths(html_content, new_img_path)

# === Write back to the same file ===
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(updated_html)

print("✅ Image paths updated in index.html")
