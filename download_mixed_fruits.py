import os
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO

# Folder to save images
save_dir = "mixed_fruits"
os.makedirs(save_dir, exist_ok=True)

# Search query
query = "mixed fruits"
max_images = 200

# Keep track of seen URLs to avoid duplicates
seen_urls = set()
image_count = 0

with DDGS() as ddgs:
    results = ddgs.images(query, max_results=max_images)
    for result in results:
        url = result["image"]
        if url in seen_urls:
            continue
        seen_urls.add(url)

        try:
            # Download image
            response = requests.get(url, timeout=10)

            # Verify image using PIL
            img = Image.open(BytesIO(response.content))
            img.verify()  # Throws error if image is invalid

            # Decide extension
            ext = url.split('.')[-1].split('?')[0].lower()
            if len(ext) > 5 or '/' in ext:
                ext = 'jpg'

            # Save image
            image_count += 1
            filename = os.path.join(save_dir, f"mixed_fruits_{image_count}.{ext}")
            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"[{image_count}] Downloaded: {filename}")

            if image_count >= max_images:
                break

        except Exception as e:
            print(f"❌ Failed to download or verify image from {url}: {e}")

print(f"\n✅ Finished. {image_count} valid images saved to '{save_dir}'.")
