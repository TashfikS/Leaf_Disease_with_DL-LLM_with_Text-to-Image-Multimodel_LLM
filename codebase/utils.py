import os

def get_image_path(image_rel_path):
    """
    Dynamically construct the full image path for training in Kaggle
    by prepending the base path.
    """
    base_path = "/kaggle/working/Processed_Rice_Leaf_Disease_Images"  # Base directory for Kaggle environment
    return os.path.join(base_path, image_rel_path)


def save_csv_file(df, path):
    # Save the image-text pairs DataFrame to a CSV file
    df.to_csv(path, index=False)
    print(f"CSV file saved to {path}")
