import os
import cv2
import numpy as np
from collections import Counter
from rich.console import Console
from rich.table import Table
from color_utils import ColorUtils

class ImageProcessor:
    def __init__(self, image_dir='images'):
        self.image_dir = image_dir
        
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def preprocess_subimage(self, image_data):
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    def process_subimage(self, ch, method, properties, body):
        try:
            image_id = properties.headers.get('image_id', 'N/A')
            image = self.preprocess_subimage(body)
            print(f"Processing subimage ID: {image_id}")
            
            # Save the processed image
            image_filename = f"{image_id}.png"
            image_path = os.path.join(self.image_dir, image_filename)
            cv2.imwrite(image_path, image)

            pixels = image.reshape((-1, 3))
            colors_luminosity_count = Counter()

            for pixel in pixels:
                result_color = ColorUtils().classify_color(tuple(pixel))
                key = f"{result_color['Nearest Color']} - {result_color['Luminosity']}" if result_color['Luminosity'] != 'N/A' else result_color['Nearest Color']
                colors_luminosity_count[key] += 1

            self.print_color_statistics(image_id, colors_luminosity_count)

        except Exception as e:
            print(f"Error during image processing: {e}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def print_color_statistics(self, image_id, colors_luminosity_count):
        sorted_table = sorted(colors_luminosity_count.items(), key=lambda x: x[1], reverse=True)

        console = Console()
        console.print(f"[bold]Subimage ID: {image_id}[/bold]")

        table = Table(title="Color Statistics")
        table.add_column("Color", justify="center", style="cyan", no_wrap=True)
        table.add_column("Pixel Count", justify="center", style="magenta", no_wrap=True)

        for entry in sorted_table:
            table.add_row(str(entry[0]), str(entry[1]))

        console.print(table)
