import re

def rename_classes_in_css(css_content):
    def replacer(match):
        prefix = match.group(1)
        class_name = match.group(2)
        if not class_name.startswith("lp-"):
            return f"{prefix}.lp-{class_name}"
        return match.group(0)

    # Match either start of line or whitespace, followed by .class-name,
    # and make sure it’s followed by characters like space, comma, {, etc.
    return re.sub(r"(^|\s)\.([\w\-]+)(?=[\s,{.:#])", replacer, css_content)

def rename_classes_in_html(html_content, css_class_names):
    def replace_class_names(match):
        original = match.group(0)
        classes = match.group(1).split()
        new_classes = [
            f"lp-{cls}" if cls in css_class_names and not cls.startswith("lp-") else cls
            for cls in classes
        ]
        return f'class="{" ".join(new_classes)}"'

    return re.sub(r'class="([^"]+)"', replace_class_names, html_content)

# === Modify these paths if needed ===
css_file_path = "lp-styles.css"
html_file_path = "landing-page.html"

# === Read original CSS and HTML ===
with open(css_file_path, "r", encoding="utf-8") as f:
    css_content = f.read()

with open(html_file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# === Extract class names from CSS ===
css_class_names = set(re.findall(r"\.([\w\-]+)", css_content))

# === Transform contents ===
updated_css = rename_classes_in_css(css_content)
updated_html = rename_classes_in_html(html_content, css_class_names)

# === Optional: make backups
# with open(css_file_path + ".bak", "w", encoding="utf-8") as f: f.write(css_content)
# with open(html_file_path + ".bak", "w", encoding="utf-8") as f: f.write(html_content)

# === Write back to the same files ===
with open(css_file_path, "w", encoding="utf-8") as f:
    f.write(updated_css)

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(updated_html)

print("✅ Files updated in-place. You can now compare with Git.")
