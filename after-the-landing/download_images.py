#!/usr/bin/env python3
"""Download representative NASA images into the website's images/ folders."""
import json, time, ssl, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# On some macOS Python installations, the default certificate bundle is missing
# or outdated. certifi provides a maintained CA bundle for HTTPS verification.
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()
ASSETS = {
    "moon": {
        "apollo11.jpg": [
            "Apollo 11 Eagle lunar module descent stage Tranquility Base",
            "Apollo 11 lunar module on the Moon",
            "Apollo 11 lunar module descent stage NASA"
        ],
        "lunar-rover.jpg": ["Apollo lunar roving vehicle Moon NASA"],
        "alsep.jpg": ["Apollo lunar surface experiments package ALSEP NASA"],
        "retroreflector.jpg": [
            "Apollo 11 laser ranging retroreflector array",
            "Apollo lunar laser ranging retroreflector",
            "lunar retroreflector Apollo 14"
        ],
        "surveyor.jpg": ["Surveyor spacecraft lunar lander NASA"],
        "apollo-tools.jpg": ["Apollo astronaut tools equipment on lunar surface NASA"],
        "sivb-impact.jpg": [
            "Apollo 12 S-IVB impact Moon",
            "Apollo 13 S-IVB lunar impact",
            "Apollo seismometer S-IVB impact experiment Moon"
        ],
        "ranger-impact.jpg": [
            "Ranger 7 final image lunar surface",
            "Ranger 7 spacecraft Moon 1964",
            "Ranger 7 lunar photographs NASA"
        ]
    },
    "mars": {
        "pathfinder.jpg": ["Mars Pathfinder lander on Mars NASA"],
        "sojourner.jpg": ["Sojourner Mars rover NASA"],
        "spirit.jpg": ["Mars Exploration Rover Spirit NASA"],
        "opportunity.jpg": ["Mars rover Opportunity NASA"],
        "phoenix.jpg": ["Phoenix Mars lander NASA"],
        "insight.jpg": ["NASA InSight lander Mars surface"],
        "perseverance.jpg": ["Perseverance rover Mars NASA"],
        "landing-debris.jpg": [
            "Perseverance parachute backshell debris Mars",
            "Mars Perseverance landing parachute on surface",
            "Perseverance rover descent stage debris Jezero crater"
        ],
        "curiosity.jpg": ["Curiosity rover Mars NASA"],
        "viking.jpg": ["Viking 1 Mars lander NASA"]
    }
}

def request_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AfterTheLandingEducationalProject/1.0"})
    with urllib.request.urlopen(req, timeout=30, context=SSL_CONTEXT) as response:
        return json.loads(response.read().decode("utf-8"))

def _certifi_available():
    try:
        import certifi  # noqa: F401
        return True
    except ImportError:
        return False


def main():
    total = sum(len(v) for v in ASSETS.values())
    done = 0
    for world, files in ASSETS.items():
        folder = ROOT / "images" / world
        folder.mkdir(parents=True, exist_ok=True)
        for filename, query in files.items():
            done += 1
            target = folder / filename
            if target.exists() and target.stat().st_size > 10_000:
                print(f"[{done}/{total}] Already exists: {world}/{filename}")
                continue
            queries = query if isinstance(query, list) else [query]
            print(f"[{done}/{total}] Finding: {filename}")
            try:
                image_url = None
                for attempt, search_term in enumerate(queries, 1):
                    print(f"  Search {attempt}/{len(queries)}: {search_term}")
                    api = "https://images-api.nasa.gov/search?media_type=image&page_size=30&q=" + urllib.parse.quote(search_term)
                    data = request_json(api)
                    items = data.get("collection", {}).get("items", [])
                    for item in items[:30]:
                        links = item.get("links", [])
                        candidate = next(
                            (x.get("href") for x in links
                             if x.get("render") == "image" and x.get("href")),
                            None
                        )
                        if candidate:
                            image_url = candidate
                            break
                    if image_url:
                        break
                if not image_url:
                    print("  No NASA image result found for any search term; skipped.")
                    continue
                req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=45, context=SSL_CONTEXT) as response:
                    content = response.read()
                    content_type = response.headers.get("Content-Type", "").lower()
                if len(content) < 5000:
                    print("  Result was too small; skipped.")
                    continue
                # Accept common image formats based on either the HTTP type or file signature.
                image_signature = content.startswith((
                    b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n",
                    b"GIF87a", b"GIF89a", b"RIFF", b"BM"
                ))
                if not content_type.startswith("image/") and not image_signature:
                    print(f"  Not an image (Content-Type: {content_type or 'unknown'}); trying next search.")
                    continue
                target.write_bytes(content)
                print(f"  Saved {target.relative_to(ROOT)} ({len(content)//1024} KB)")
                time.sleep(0.25)
            except Exception as exc:
                print(f"  Could not download this image: {exc}")
    print("\nFinished. Any skipped image can be retried by running this script again.")
    if not _certifi_available():
        print("\nIf HTTPS certificate errors occurred, run:")
        print("  python3 -m pip install --user --upgrade certifi")
        print("Then run this script again.")
    print("Open index.html in a browser. Internet is needed for fonts; local images work offline.")

if __name__ == "__main__":
    main()
