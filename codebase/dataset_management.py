import requests
import zipfile
import py7zr
import os
import glob
import kagglehub
import shutil
import random

class DatasetManagement:
    def __init__(self, base_file_path):
        self.test_dir = None
        self.validate_dir = None
        self.train_dir = None
        self.base_file_path = base_file_path

    def download_through_url(self, url, file_name="file.zip"):
        output_path = os.path.expanduser(f"~{self.base_file_path}{file_name}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"File downloaded successfully to {output_path}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")

    def download_from_kaggle(self, dataset_endpoint):
        # Download latest version
        path = kagglehub.dataset_download(dataset_endpoint)

        print("Path to dataset files:", path)

    def upzip(self, zip_file_name):
        path = os.path.join(self.base_file_path, zip_file_name)
        print(path)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self.base_file_path)
            print("Unzipped successfully")

    def upzip_7z(self, seven_zip_name):
        with py7zr.SevenZipFile(seven_zip_name, mode='r') as archive:
            archive.extractall(path=self.base_file_path)
            print("7z file extracted successfully.")

    def count_images(self, folders):
        total_images = 0
        # Count images in each folder
        for folder in folders:
            folder_path = os.path.join(self.base_file_path, folder)
            if os.path.exists(folder_path):
                # Count files with image extensions
                image_count = len(
                    [file for file in os.listdir(folder_path) if file.endswith(('.jpg', '.png', '.jpeg'))])
                print(f"{folder}: {image_count} images")
                total_images += image_count
            else:
                print(f"Folder not found: {folder_path}")
        print(f"Total images: {total_images}")

    def move_images(self, source_dir, destination_dir):
        # Create the Healthy directory if it does not exist
        os.makedirs(destination_dir, exist_ok=True)

        # Copy all images from source to destination
        for filename in os.listdir(source_dir):
            if filename.endswith(('.jpg', '.png', '.jpeg')):  # Check for image files
                src_file = os.path.join(source_dir, filename)
                dest_file = os.path.join(destination_dir, filename)
                shutil.copy(src_file, dest_file)

        # List copied files for verification
        os.listdir(destination_dir)

    def remove_zip_7z_csv(self):
        # Paths to .zip, .csv, and .7z files
        zip_files = glob.glob(os.path.join(self.base_file_path, "*.zip"))
        csv_files = glob.glob(os.path.join(self.base_file_path, "/*.csv"))
        seven_zip_files = glob.glob(os.path.join(self.base_file_path, "*.7z"))

        # Combine all files to remove
        files_to_remove = zip_files + csv_files + seven_zip_files

        # Remove each file
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

        # Verify the directory
        print("Remaining files:", os.listdir(self.base_file_path))

    def remove_files_of_a_dir(self, path):
        # Path to the directory you want to remove
        dir_path = path

        # Delete the directory and all its contents
        shutil.rmtree(dir_path)

        print(f"Directory '{dir_path}' and all its contents have been removed.")

    def set_train_val_test_path(self, train_dir, validate_dir, test_dir):
        self.train_dir = train_dir
        self.validate_dir = validate_dir
        self.test_dir = test_dir

    def creating_train_val_test(self):
        for folder in [self.train_dir, self.validate_dir, self.test_dir]:
            os.makedirs(folder, exist_ok=True)

    def split_dataset(self, source_dir, train_ratio=0.7, validate_ratio=0.15):
        for category in os.listdir(source_dir):
            category_path = os.path.join(source_dir, category)
            if os.path.isdir(category_path):
                # Create subdirectories for train, validate, and test within the category
                os.makedirs(os.path.join(self.train_dir, category), exist_ok=True)
                os.makedirs(os.path.join(self.validate_dir, category), exist_ok=True)
                os.makedirs(os.path.join(self.test_dir, category), exist_ok=True)

                # List all images in the current category
                images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]

                # Shuffle the images for randomness
                random.shuffle(images)

                # Calculate the split indices
                total_images = len(images)
                train_end = int(total_images * train_ratio)
                validate_end = int(total_images * (train_ratio + validate_ratio))

                # Split the images
                train_images = images[:train_end]
                validate_images = images[train_end:validate_end]
                test_images = images[validate_end:]

                # Move images to the respective directories
                for image in train_images:
                    shutil.copy(os.path.join(category_path, image), os.path.join(self.train_dir, category, image))
                for image in validate_images:
                    shutil.copy(os.path.join(category_path, image), os.path.join(self.validate_dir, category, image))
                for image in test_images:
                    shutil.copy(os.path.join(category_path, image), os.path.join(self.test_dir, category, image))

                print(f"Category '{category}' split into train, validate, and test sets.")

        print("Dataset split completed.")


