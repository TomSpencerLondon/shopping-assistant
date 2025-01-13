import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize Elasticsearch client
es = Elasticsearch(
    os.getenv('ELASTICSEARCH_HOST'),
    basic_auth=(os.getenv('ELASTICSEARCH_USERNAME'), os.getenv('ELASTICSEARCH_PASSWORD'))
)

# Define the shop inventory
def create_inventory():
    inventory = [
        {"name": "Chicken Breast", "category": "Meat", "description": "Boneless chicken breast, perfect for curries.", "price": 5.99},
        {"name": "Coconut Milk", "category": "Canned Goods", "description": "Rich and creamy coconut milk for cooking.", "price": 2.49},
        {"name": "Garlic", "category": "Produce", "description": "Fresh garlic bulbs for seasoning.", "price": 0.99},
        {"name": "Onion", "category": "Produce", "description": "Yellow onions for cooking and seasoning.", "price": 0.79},
        {"name": "Ginger", "category": "Produce", "description": "Fresh ginger root for flavor.", "price": 1.49},
        {"name": "Turmeric Powder", "category": "Spices", "description": "Ground turmeric for adding color and flavor.", "price": 3.99},
        {"name": "Curry Powder", "category": "Spices", "description": "A blend of spices perfect for curries.", "price": 4.49},
        {"name": "Tomatoes", "category": "Produce", "description": "Fresh ripe tomatoes for sauces and curries.", "price": 2.99},
        {"name": "Basmati Rice", "category": "Grains", "description": "Long-grain basmati rice for serving with curry.", "price": 4.99},
    ]
    return pd.DataFrame(inventory)

# Generate embeddings for product descriptions
def get_embedding(text, model="text-embedding-ada-002"):
    try:
        text = text.replace("\n", " ")  # Normalize text
        response = client.embeddings.create(input=text, model=model)
        embedding = response.data[0].embedding
        if len(embedding) != 1536:
            raise ValueError("Embedding size mismatch.")
        return embedding
    except Exception as e:
        print(f"Error generating embedding for text '{text}': {e}")
        return None

# Split embeddings into smaller parts
def split_embedding(embedding, parts=2):
    chunk_size = len(embedding) // parts
    return [embedding[i * chunk_size:(i + 1) * chunk_size] for i in range(parts)]

# Index products into Elasticsearch
def index_inventory(inventory):
    inventory['vector'] = inventory['description'].apply(lambda x: get_embedding(x))
    inventory['vector_split'] = inventory['vector'].apply(lambda x: split_embedding(x) if x else None)
    inventory = inventory.dropna(subset=['vector_split'])  # Remove items with None embeddings
    actions = []
    for _, row in inventory.iterrows():
        doc = row.to_dict()
        split_vectors = doc.pop('vector_split')
        doc['vector_part_1'], doc['vector_part_2'] = split_vectors
        actions.append({"_index": "shop_inventory", "_source": doc})

    try:
        bulk(es, actions)
        print("Inventory indexed successfully.")
    except BulkIndexError as e:
        print("Bulk indexing failed.")
        for error in e.errors:
            print(error)

# Search for products based on a query
def search_products(query, top_k=5):
    query_vector = get_embedding(query)
    if query_vector is None:
        print("Failed to generate query vector.")
        return []
    query_parts = split_embedding(query_vector)
    try:
        response = es.search(
            index="shop_inventory",
            body={
                "size": top_k,
                "query": {
                    "function_score": {
                        "query": {"match_all": {}},
                        "script_score": {
                            "script": {
                                "source": """
                                    double score1 = cosineSimilarity(params.query_vector_part_1, 'vector_part_1');
                                    double score2 = cosineSimilarity(params.query_vector_part_2, 'vector_part_2');
                                    return score1 + score2;
                                """,
                                "params": {
                                    "query_vector_part_1": query_parts[0],
                                    "query_vector_part_2": query_parts[1]
                                }
                            }
                        }
                    }
                },
                "_source": ["name", "description", "price", "category"]
            }
        )
        return response['hits']['hits']
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def get_cooking_instructions(ingredients):
    try:
        ingredients_list = ', '.join(ingredient['_source']['name'] for ingredient in ingredients)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides detailed cooking instructions."
            },
            {
                "role": "user",
                "content": f"I have the following ingredients for a chicken curry: {ingredients_list}. Please provide step-by-step cooking instructions."
            }
        ]

        # Generate the completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            timeout=30
        )

        # Debug: Print the response object
        print("OpenAI API Response:", response)

        # Extract the message content from the response
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        else:
            print("Error: Unexpected response structure.")
            return "Sorry, I couldn't generate cooking instructions at the moment."
    except Exception as e:
        print(f"Error generating cooking instructions: {e}")
        return "Sorry, I couldn't generate cooking instructions at the moment."




# Main execution
if __name__ == "__main__":
    inventory = create_inventory()

    # Check if the index exists, create if not
    if not es.indices.exists(index="shop_inventory"):
        es.indices.create(
            index="shop_inventory",
            body={
                "mappings": {
                    "properties": {
                        "vector_part_1": {"type": "dense_vector", "dims": 768},
                        "vector_part_2": {"type": "dense_vector", "dims": 768},
                        "category": {"type": "keyword"},
                        "description": {"type": "text"},
                        "price": {"type": "float"},
                        "name": {"type": "text"}
                    }
                }
            }
        )

        index_inventory(inventory)

    # Perform a search for chicken curry ingredients
    user_query = "What ingredients should I buy to make a nice chicken curry?"
    search_results = search_products(user_query)

    # Print search results
    print("\nSearch Results:")
    for result in search_results:
        print(f"Name: {result['_source']['name']}")
        print(f"Price: ${result['_source']['price']}")
        print(f"Description: {result['_source']['description']}")
        print("-" * 50)

    # Generate cooking instructions
    if search_results:
        instructions = get_cooking_instructions(search_results)
        print("\nCooking Instructions:")
        print(instructions)
