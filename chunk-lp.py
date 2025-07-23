import os
from bs4 import BeautifulSoup

def save_chunk(element):
    class_attr = element.get("class", [])
    if len(class_attr) < 2:
        return

    # Always use the second class as the chunk identifier
    chunk_class = class_attr[1]
    if chunk_class.startswith("lp-"):
        chunk_name = chunk_class.replace("lp-", "")
        folder = "chunks-landing-page"
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"{chunk_name}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(element))
        print(f"✅ Saved: {filename}")

# === Load original HTML ===
with open("./pages/landing-page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

body = soup.body
if not body:
    print("❌ No <body> tag found.")
    exit()

# === Extract sections and footer ===
for element in body.find_all(["section", "footer"]):
    save_chunk(element)
