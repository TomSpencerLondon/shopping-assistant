Here’s a detailed **README** for your shopping assistant project:

---

# Shopping Assistant

This Python-based Shopping Assistant helps users find ingredients for recipes and provides step-by-step cooking instructions using the power of Elasticsearch and OpenAI's GPT-4.

## Features
- Search for items in a virtual shop inventory using semantic search powered by vector embeddings.
- Get detailed step-by-step cooking instructions based on selected ingredients.
- Combines Elasticsearch for data storage and retrieval and OpenAI GPT-4 for generating instructions.

---

## Prerequisites
Before you can run this project, ensure you have the following installed and configured:
1. **Python 3.9+**
2. **Elasticsearch**
3. **Pipenv or virtualenv** for managing dependencies.
4. **OpenAI API key** (create an account at [OpenAI](https://platform.openai.com) to get your API key).
5. **.env file** for storing sensitive environment variables.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/shopping-assistant.git
   cd shopping-assistant
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project directory with the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ELASTICSEARCH_HOST=http://localhost:9200
   ELASTICSEARCH_USERNAME=your_es_username
   ELASTICSEARCH_PASSWORD=your_es_password
   ```

5. **Start Elasticsearch**
   Ensure Elasticsearch is running on your machine or accessible via the provided `ELASTICSEARCH_HOST`.

---

## Usage

### Running the Application
1. **Run the Script**
   ```bash
   python shopping_assistant.py
   ```

2. **Interact with the Assistant**
    - The application will:
        1. Index a predefined inventory into Elasticsearch.
        2. Search for items based on a user query (e.g., "ingredients for chicken curry").
        3. Generate detailed cooking instructions based on the search results using OpenAI's GPT-4.

3. **Example Output**
   ```
   Search Results:
   Name: Curry Powder
   Price: $4.49
   Description: A blend of spices perfect for curries.
   --------------------------------------------------
   Name: Chicken Breast
   Price: $5.99
   Description: Boneless chicken breast, perfect for curries.
   --------------------------------------------------

   Cooking Instructions:
   Sure, I'd be glad to help you create a delightful chicken curry with these ingredients. Here are your step-by-step instructions:
   ...
   ```

---

## File Structure
```plaintext
shopping-assistant/
├── shopping_assistant.py  # Main script
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not included in repo)
├── README.md              # Project documentation
└── venv/                  # Virtual environment (ignored in .gitignore)
```

---

## How It Works

1. **Inventory Setup**
    - An inventory of ingredients is created using `pandas` and stored as a DataFrame.

2. **Vector Embeddings**
    - Product descriptions are converted to vector embeddings using OpenAI's embedding API (`text-embedding-ada-002`).

3. **Elasticsearch Integration**
    - The inventory is indexed into Elasticsearch using the `dense_vector` field for semantic search.

4. **Semantic Search**
    - User queries are converted into embeddings, and a kNN search retrieves relevant inventory items.

5. **Cooking Instructions**
    - OpenAI GPT-4 generates step-by-step cooking instructions based on the selected ingredients.

---

## Troubleshooting

### Common Issues
1. **Elasticsearch Connection Errors**
    - Ensure Elasticsearch is running and the `ELASTICSEARCH_HOST` in `.env` is correct.

2. **OpenAI API Errors**
    - Verify your OpenAI API key is valid and you have enough quota.

3. **Dependencies Not Found**
    - Ensure `pip install -r requirements.txt` is run inside the virtual environment.

4. **Unexpected Output**
    - Use the debug logs (`print` statements in the code) to verify the structure of the response objects.

---

## Future Enhancements
- Allow user input to dynamically add items to the inventory.
- Include support for multiple recipes and cuisines.
- Add a web interface for user interaction.
---