import json

class Preferences:
    def __init__(self, prefs_path):
        self.prefs_path = prefs_path
        self.preferences = None
        self.load_preferences()

    def load_preferences(self):
        default_prefs = {
            "url": "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            "tile_size": 256,
            "channels": 3,
            "dir": "/home/giovanni/Scrivania/Magistrale/Anno_2023_2024/Tramontana/Progetto/satellite-imagery-downloader/src/images",
            "headers": {
                "cache-control": "max-age=0",
                "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            },
            "tl": "",
            "br": "",
            "zoom": ""
        }

        try:
            with open(self.prefs_path, 'r', encoding='utf-8') as f:
                self.preferences = json.loads(f.read())
        except FileNotFoundError:
            self.preferences = default_prefs
            with open(self.prefs_path, 'w', encoding='utf-8') as f:
                json.dump(default_prefs, f, indent=2)

    def update_preferences(self, new_prefs):
        self.preferences.update(new_prefs)
        with open(self.prefs_path, 'w', encoding='utf-8') as f:
            json.dump(self.preferences, f, indent=2)