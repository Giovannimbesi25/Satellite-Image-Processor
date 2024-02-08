import os
import cv2
import time
import re
from datetime import datetime
from image_downloading import download_image
from preferences import Preferences
from rabbitmq_sender import RabbitMQSender

class SubImageProcessor:
    def __init__(self, prefs_path):
        self.prefs = Preferences(prefs_path)
        self.rabbitmq_sender = RabbitMQSender()

    def take_input(self, messages):
        inputs = []
        fields = ['Top-left coordinates', 'Bottom-right coordinates', 'Zoom level', 'Number of subimages']

        try:
            for i, message in enumerate(messages):
                inp = input(message)
                if inp.lower() == 'q':
                    return None
                elif inp.lower() == 'r':
                    return self.take_input(messages)
                elif not inp.strip():
                    print(f" [!] Campo '{fields[i]}' mancante. Per favore, riprova.")
                    return self.take_input(messages)
                inputs.append(inp)
        except KeyboardInterrupt:
            return None
        return inputs

    def parse_coordinates(self, coord_string):
        lat, lon = map(float, re.findall(r'[+-]?\d*\.\d+', coord_string))
        return lat, lon

    def generate_subimages(self, image, num_subimages=8):
        height, width, _ = image.shape
        subimage_height = height // num_subimages

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        for i in range(num_subimages):
            start_y = i * subimage_height
            end_y = (i + 1) * subimage_height

            subimage = image[start_y:end_y, :, :]

            if subimage is not None and subimage.size != 0:
                _, subimage_data = cv2.imencode('.png', subimage)
                subimage_data = subimage_data.tobytes()

                subimage_id = f"{timestamp}_subimage_{i}"

                self.rabbitmq_sender.send_image(subimage_id, subimage_data, is_subimage=True, index=i)
            else:
                print(f" [!] Skipping subimage {i} due to empty or None.")

    def run(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        prefs_path = os.path.join(file_dir, 'preferences.json')
        image_dir = os.path.join(file_dir, 'images')

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        while True:
            messages = ['Enter top-left corner coordinates (lat, lon): ',
                        'Enter bottom-right corner coordinates (lat, lon): ',
                        'Enter zoom level: ',
                        'Enter the number of subimages: ']
            inputs = self.take_input(messages)

            if inputs is None:
                break

            lat1, lon1 = self.parse_coordinates(inputs[0])
            lat2, lon2 = self.parse_coordinates(inputs[1])
            zoom, num_subimages = map(int, inputs[2:])

            channels = int(self.prefs.preferences['channels'])
            tile_size = int(self.prefs.preferences['tile_size'])

            img = download_image(lat1, lon1, lat2, lon2, zoom, self.prefs.preferences['url'],
                                  self.prefs.preferences['headers'], tile_size, channels)

            if img is not None and img.size != 0:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_filename = f"satellite_image_{timestamp}.png"
                image_path = os.path.join(image_dir, image_filename)
                
                # Save original image
                cv2.imwrite(image_path, img)
                
                _, image_data = cv2.imencode('.png', img)
                image_data = image_data.tobytes()

                self.generate_subimages(img, int(num_subimages))
            else:
                print(" [!] Skipping image due to empty or None.")