# from py2neo import Graph
#
# # Connect to Neo4j
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
#
# # Clear the database
# graph.run("MATCH (n) DETACH DELETE n")
# print("All data deleted!")


# import pandas as pd
#
# # Load the CSV file into a DataFrame
# file_path = '/media/tinux/Volume-1/Research/Leaf_Disease_with_DL+LLM_with_Text-to-Image+Multimodel_LLM/Dataset/image_text_pairs.csv'
# df = pd.read_csv(file_path)
#
# # Check for duplicate rows
# duplicates = df[df.duplicated()]
#
# # Print the duplicate rows
# if not duplicates.empty:
#     print("Duplicate rows found:")
#     print(duplicates)
# else:
#     print("No duplicate rows found.")


import pandas as pd

# Load the CSV file into a DataFrame
file_path = '/media/tinux/Volume-1/Research/Leaf_Disease_with_DL+LLM_with_Text-to-Image+Multimodel_LLM/Dataset/image_text_pairs.csv'
df = pd.read_csv(file_path)

# Check for unique image paths
unique_images = df['image_path'].nunique()
total_entries = len(df)

print(f"Total entries in CSV: {total_entries}")
print(f"Unique image paths: {unique_images}")