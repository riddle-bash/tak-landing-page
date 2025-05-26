import re
from bs4 import BeautifulSoup

def save_chunk(element, prefix="section"):
    class_attr = element.get("class", [])
    if not class_attr:
        return

    for class_name in class_attr:
        if class_name.startswith("lp-"):
            chunk_name = class_name.replace("lp-", "")
            filename = f"{chunk_name}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(element))
            print(f"✅ Saved: {filename}")
            break

# === Load original HTML ===
with open("index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

body = soup.body
if not body:
    print("❌ No <body> tag found.")
    exit()

# === Extract sections and footer ===
for element in body.find_all(["section", "footer"]):
    save_chunk(element)
