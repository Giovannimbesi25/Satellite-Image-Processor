import math

class ColorUtils:
    COLORS = {
        'Red': (255, 0, 0),
        'Green': (0, 255, 0),
        'Blue': (0, 0, 255),
        'Yellow': (255, 255, 0),
        'Cyan': (0, 255, 255),
        'Magenta': (255, 0, 255),
        'Black': (0, 0, 0),
        'White': (255, 255, 255),
    }

    DISTANCE_THRESHOLD = 127.5

    def calculate_distance(self, color1, color2):
        return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

    def calculate_luminosity(self, rgb):
        r, g, b = rgb
        return 0.299 * r + 0.587 * g + 0.114 * b

    def find_nearest_color(self, pixel):
        color_distances = [(name, self.calculate_distance(pixel, rgb)) for name, rgb in self.COLORS.items()]
        return min(color_distances, key=lambda x: x[1])[0]

    def classify_color(self, pixel):
        nearest_color = self.find_nearest_color(pixel)
        result = {'Nearest Color': nearest_color, 'Luminosity': 'N/A'}

        if nearest_color not in ['Black', 'White']:
            luminosity = self.calculate_luminosity(pixel)
            result['Luminosity'] = 'Light' if luminosity > ColorUtils.DISTANCE_THRESHOLD else 'Dark'

        return result
