import os
import cv2
import numpy as np


class DataAugmentation:
    def __init__(self):
        pass

    def normalize_image(self, image):
        """
        Normalize an image to have pixel values between 0 and 1.
        """
        return image / 255.0  # Scale pixel values to the range [0, 1]

    def process_images(self, input_folder, output_folder, target_size=(300, 300)):
        """
        Process all images in the given folder (including subfolders).
        Resize images larger than the target size and normalize all images.
        """
        os.makedirs(output_folder, exist_ok=True)

        for folder_name in os.listdir(input_folder):
            input_subfolder = os.path.join(input_folder, folder_name)
            output_subfolder = os.path.join(output_folder, folder_name)
            os.makedirs(output_subfolder, exist_ok=True)

            for file_name in os.listdir(input_subfolder):
                input_path = os.path.join(input_subfolder, file_name)
                output_path = os.path.join(output_subfolder, file_name)

                try:
                    # Read the image
                    img = cv2.imread(input_path)
                    if img is None:
                        print(f"Skipping invalid file: {input_path}")
                        continue

                    # Get current dimensions
                    height, width = img.shape[:2]

                    # Resize only if the image is larger than the target size
                    if height != target_size[1] or width != target_size[0]:
                        img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

                    # Normalize the image
                    img_normalized = self.normalize_image(img)

                    # Convert normalized image back to 8-bit for saving
                    img_normalized_uint8 = (img_normalized * 255).astype(np.uint8)

                    # Save the processed image
                    cv2.imwrite(output_path, img_normalized_uint8)

                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

