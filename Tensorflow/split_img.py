import json
from PIL import Image
import os
import re

base_dir = '/home/pw-wq/Deep_learning/images'
output_dir = '/home/pw-wq/Deep_learning/cropped_images/Sunomata' 
# os.makedirs(output_dir, exist_ok=True)

with open('annotation.json', 'r') as file:
    data = json.load(file)

image_dict = {image['id']: image['path'] for image in data['images']}
pattern = re.compile(r'.*Sunomata.*')

for image_id, path in image_dict.items():
    print(f"Checking path: {path}")

    if pattern.match(path): 
        full_path = os.path.join(base_dir, path.lstrip('/'))

        print(f"Full path constructed: {full_path}")

        try:
            if not os.path.isfile(full_path):
                print(f"Error: File not found at path {full_path}")
                continue

            img = Image.open(full_path)
            print(f"Loaded image: {full_path}")
            
            annotations_found = False
            for i, annotation in enumerate(data['annotations']):
                if annotation['image_id'] == image_id:
                    annotations_found = True
                    bbox = annotation['bbox']
                    
                    print(f"Cropping image with bbox: {bbox}")
                    
                    x_min, y_min, width, height = bbox
                    x_max = x_min + width
                    y_max = y_min + height
                    bbox_corrected = [x_min, y_min, x_max, y_max]
                    
                    cropped_img = img.crop(bbox_corrected)
                    
                    base_name = os.path.basename(path)
                    file_name_without_ext = os.path.splitext(base_name)[0]
                    cropped_img_name = f'{file_name_without_ext}_crop_{i}.png'

                    cropped_img_path = os.path.join(output_dir, cropped_img_name)
                    cropped_img.save(cropped_img_path)
                    
                    print(f"Cropped image saved: {cropped_img_path}")
        
        except FileNotFoundError:
            print(f"Error: File not found at path {full_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

print("Processing complete.")
