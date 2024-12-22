import os
from utils import save_csv_file
from codebase.data_augmentation import DataAugmentation
from codebase.dataset_management import DatasetManagement
from codebase.knowledge_graph import KnowledgeGraphBuilder


if __name__ == "__main__":
    base_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_file, "Dataset")
    # Folders to check
    folder_name = os.path.join(dataset_path, "Processed_Rice_Leaf_Disease_Images")
    folder_list = [f"{folder_name}/Bacterialblight",
                   f"{folder_name}/Blast",
                   f"{folder_name}/Brownspot",
                   f"{folder_name}/Tungro",
                   f"{folder_name}/Healthy"]
    dataset_management = DatasetManagement(dataset_path)
    dataset_management.count_images(folder_list)

    input_folder = folder_name
    output_folder = os.path.join(dataset_path, "Processed_Rice_Leaf_Disease_Images")
    # Move images from source to destination
    # source_dir = f"{dataset_path}1/RiceLeafs/train/Healthy"
    # source_dir = f"{dataset_path}1/RiceLeafs/validation/Healthy"
    # destination_dir = f"{dataset_path}Rice Leaf Disease Images/Healthy"
    # dataset_management.move_images(source_dir, destination_dir)

    data_augmentation = DataAugmentation()
    # Process all images, resizing only those that need resizing
    # data_augmentation.process_images(input_folder, output_folder, target_size=(300, 300))

    # source_dir = folder_name
    # split_dataset = os.path.join(dataset_path, "Split_Rice_Leaf_Disease_Dataset")
    # train_dir = os.path.join(split_dataset, "train")
    # validate_dir = os.path.join(split_dataset, "validate")
    # test_dir = os.path.join(split_dataset, "test")
    #
    # dataset_management.set_train_val_test_path(train_dir, validate_dir, test_dir)
    # dataset_management.creating_train_val_test()
    # dataset_management.split_dataset(source_dir)

    # Initialize Knowledge Graph Builder and build the graph
    input_folder_for_kg = output_folder
    kg_builder = KnowledgeGraphBuilder()
    kg_builder.remove_all_data_from_graph()
    kg_builder.create_nodes_and_relationships(input_folder_for_kg)
    image_text_pairs_df = kg_builder.create_image_text_pairs()

    csv_file_path = os.path.join(dataset_path, "image_text_pairs.csv")
    save_csv_file(image_text_pairs_df, csv_file_path)