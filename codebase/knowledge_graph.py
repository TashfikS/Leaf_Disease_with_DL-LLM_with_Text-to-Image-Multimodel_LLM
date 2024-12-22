from py2neo import Graph, Node, Relationship
import os
import pandas as pd
from utils import get_image_path

# Connect to Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))


class KnowledgeGraphBuilder:
    def __init__(self):
        pass

    def create_nodes_and_relationships(self, input_folder):
        """
        Creates nodes and relationships in the Neo4j database
        for each image in the folder structure, avoiding duplicates.
        """
        # Loop through disease folders (Bacterialblight, Blast, etc.)
        for folder_name in os.listdir(input_folder):
            folder_path = os.path.join(input_folder, folder_name)
            if os.path.isdir(folder_path):  # Only process directories

                    # Use MERGE to avoid creating duplicate Disease nodes
                    disease_node = Node("Disease", name=folder_name)
                    graph.merge(disease_node, "Disease", "name")

                    # Process each image in the subfolder
                    for file_name in os.listdir(folder_path):
                        image_rel_path = os.path.join(folder_name, file_name)  # Use relative path

                        # Use MERGE to avoid creating duplicate Image nodes
                        image_node = Node("Image", path=image_rel_path)
                        graph.merge(image_node, "Image", "path")

                        # Create relationship between Image and Disease
                        has_disease = Relationship(image_node, "HAS_DISEASE", disease_node)
                        graph.create(has_disease)

                        # Define symptoms and treatments manually or use a predefined list
                        symptoms = self.get_symptoms_for_disease(folder_name)
                        treatments = self.get_treatment_for_disease(folder_name)

                        for symptom in symptoms:
                            # Use MERGE to avoid creating duplicate Symptom nodes
                            symptom_node = Node("Symptom", name=symptom)
                            graph.merge(symptom_node, "Symptom", "name")

                            # Create relationships between Disease and Symptom
                            has_symptom = Relationship(disease_node, "HAS_SYMPTOM", symptom_node)
                            graph.create(has_symptom)

                            # Create relationships between Image and Symptom
                            image_has_symptom = Relationship(image_node, "HAS_SYMPTOM", symptom_node)
                            graph.create(image_has_symptom)

                        for treatment in treatments:
                            # Use MERGE to avoid creating duplicate Treatment nodes
                            treatment_node = Node("Treatment", name=treatment)
                            graph.merge(treatment_node, "Treatment", "name")

                            # Create relationships between Disease and Treatment
                            has_treatment = Relationship(disease_node, "HAS_TREATMENT", treatment_node)
                            graph.create(has_treatment)

    def get_symptoms_for_disease(self, disease):
        # Example symptoms for each disease, you can update these
        symptoms = {
            "Bacterialblight": ["yellow spots", "necrosis"],
            "Blast": ["grey spots", "wilting"],
            "Brownspot": ["small brown spots", "yellow edges"],
            "Tungro": ["yellowing", "stunted growth"]
        }
        return symptoms.get(disease, [])

    def get_treatment_for_disease(self, disease):
        # Example treatments for each disease
        treatments = {
            "Bacterialblight": ["Use antibiotics", "Remove infected leaves"],
            "Blast": ["Fungicide application", "Remove infected plants"],
            "Brownspot": ["Improve drainage", "Use fungicides"],
            "Tungro": ["Use resistant varieties", "Use insecticides"]
        }
        return treatments.get(disease, [])

    def create_image_text_pairs(self):
        """
        Extracts image-text pairs from the Neo4j graph and stores them in a DataFrame.
        """
        image_text_pairs = []

        # Query Neo4j to get image paths and their corresponding disease, symptoms, and treatments
        query = """
        MATCH (img:Image)-[:HAS_DISEASE]->(d:Disease)-[:HAS_SYMPTOM]->(s:Symptom), (d)-[:HAS_TREATMENT]->(t:Treatment)
        RETURN img.path AS image, d.name AS disease, collect(s.name) AS symptoms, collect(t.name) AS treatments
        """

        result = graph.run(query)

        # Process results into image-text pairs
        for record in result:
            image_rel_path = record['image']
            disease = record['disease']
            symptoms = ", ".join(record['symptoms'])
            treatments = ", ".join(record['treatments'])

            # Construct the full image path dynamically for Kaggle
            image_path = get_image_path(image_rel_path)

            # Form the description (text)
            text = f"This image shows {disease} with symptoms: {symptoms}. The treatment includes: {treatments}."

            # Append the pair to the list
            image_text_pairs.append({"image_path": image_path, "text": text})

        # Convert to DataFrame
        df = pd.DataFrame(image_text_pairs)
        return df

    def remove_all_data_from_graph(self):
        """
        Removes all nodes and relationships from the Neo4j graph.
        """
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        graph.run(query)
        print("All nodes and relationships removed from the graph.")
