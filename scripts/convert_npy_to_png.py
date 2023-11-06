import numpy as np
from PIL import Image
import os
import glob

# Sökvägen där `.npy`-filerna är sparade
npy_files_path = 'imgs/CT_scan_images/npy_img'
# Sökvägen där de konverterade bilderna kommer att sparas
save_images_path = 'imgs/CT_scan_images/png_img'

if not os.path.exists(save_images_path):
    os.makedirs(save_images_path)

# Hitta alla `.npy` filer
npy_files = glob.glob(os.path.join(npy_files_path, '*.npy'))
print(f"Found {len(npy_files)} npy files.")

for npy_file in npy_files:
    try:
        # Läs in `.npy` filen
        image_array = np.load(npy_file)

        # Konvertera från 0-1 skala till HU
        image_array_HU = image_array * 4096 - 1024

        # Klipp HU-värdena till vanliga CT skanning intervall, till exempel -1024 till 3072
        image_array_HU_clipped = np.clip(image_array_HU, -1024, 3072)

        # Skala om HU-värden till 0-255
        min_val = -1024
        max_val = 3072
        scaled_array = 255 * (image_array_HU_clipped - min_val) / (max_val - min_val)

        # Konvertera till en PIL-bild
        image = Image.fromarray(scaled_array.astype(np.uint8))

        # Skapa filnamn och spara bilden
        image_file_name = os.path.basename(npy_file).replace('.npy', '.png')
        image_save_path = os.path.join(save_images_path, image_file_name)
        image.save(image_save_path)
        print(f"Saved {image_save_path}")
    except Exception as e:
        print(f"Could not process {npy_file}: {e}")