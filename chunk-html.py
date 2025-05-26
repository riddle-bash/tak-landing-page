import os
from bs4 import BeautifulSoup

def save_chunk(element):
    class_attr = element.get("class", [])
    if not class_attr:
        return

    for class_name in class_attr:
        if class_name.startswith("lp-"):
            chunk_name = class_name.replace("lp-", "")
            folder = "chunks"
            os.makedirs(folder, exist_ok=True)  # Create folder if needed
            filename = os.path.join(folder, f"{chunk_name}.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(element))
            print(f"✅ Saved: {filename}")
            break

# === Load original HTML ===
with open("landing-page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

body = soup.body
if not body:
    print("❌ No <body> tag found.")
    exit()

# === Extract sections and footer ===
for element in body.find_all(["section", "footer"]):
    save_chunk(element)
