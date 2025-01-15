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

```bash
➜  Desktop docker run -p 9200:9200 \
-e "discovery.type=single-node" \
-e "ELASTIC_PASSWORD=mysecurepassword" \
-e "xpack.security.http.ssl.enabled=false" \
-e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
docker.elastic.co/elasticsearch/elasticsearch:8.5.0
```

You may need to delete data from the previous run if you encounter issues with the new run.

```bash
curl -u elastic:mysecurepassword -X DELETE "http://localhost:9200/shop_inventory"
```
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

### Output

```bash
/Users/tspencer/Desktop/shopping-assistant/venv/bin/python3.12 /Users/tspencer/Desktop/shopping-assistant/shopping_assistant.py 

Search Results:
Name: Curry Powder
Price: $4.49
Description: A blend of spices perfect for curries.
--------------------------------------------------
Name: Chicken Breast
Price: $5.99
Description: Boneless chicken breast, perfect for curries.
--------------------------------------------------
Name: Turmeric Powder
Price: $3.99
Description: Ground turmeric for adding color and flavor.
--------------------------------------------------
Name: Basmati Rice
Price: $4.99
Description: Long-grain basmati rice for serving with curry.
--------------------------------------------------
Name: Tomatoes
Price: $2.99
Description: Fresh ripe tomatoes for sauces and curries.
--------------------------------------------------
OpenAI API Response: ChatCompletion(id='chatcmpl-Aq4AicvoS36fbwcpdrnAIAAimPfFd', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Sure, here is a step-by-step method to guide you in making a delicious chicken curry:\n\nIngredients:\n- 500 grams of Chicken Breast\n- 2 tablespoons of Curry Powder\n- 1 teaspoon of Turmeric Powder\n- 2 cups of Basmati Rice\n- 4 medium Tomatoes\n\nInstructions:\n\n1. Prepare the chicken: Cut the chicken breast into 1-inch cubes. \n\n2. Marinate the chicken: Mix 1 tablespoon of curry powder, turmeric powder and a bit of salt as per your taste with the chicken bits. Let it marinate for about 30 minutes.\n\n3. Cook the Basmati Rice: Rinse the rice until water runs clear. Bring 4 cups of water to a boil in a saucepan, then add the rice. When the water returns to a boil, reduce the heat to low, cover the saucepan and let simmer for about 15-20 minutes or until the rice is tender and the water is absorbed.\n\n4. Prepare the sauce: While your rice is cooking, finely chop the tomatoes. Heat 2 tablespoons of oil in a pan over medium heat, then add the remaining curry powder to it. Stir and cook for a minute. Add the chopped tomatoes and cook until they break down into a sauce, this will take about 10-15 minutes.\n\n5. Cook the chicken: Add the marinated chicken to the tomato and curry sauce. Stir well to coat the chicken with the sauce. Cover the pan and simmer for about 20 minutes, or until the chicken is cooked through. Make sure you stir occasionally to prevent the curry from sticking to the pan.\n\n6. Check and adjust seasoning: Taste the chicken curry and adjust the seasoning if necessary. If you prefer a spicier curry, you can add more curry powder at this stage.\n\n7. Serve: Fluff the rice with a fork and serve the chicken curry over the cooked basmati rice.\n\nEnjoy your homemade chicken curry!', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))], created=1736972456, model='gpt-4-0613', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=401, prompt_tokens=58, total_tokens=459, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

Cooking Instructions:
Sure, here is a step-by-step method to guide you in making a delicious chicken curry:

Ingredients:
- 500 grams of Chicken Breast
- 2 tablespoons of Curry Powder
- 1 teaspoon of Turmeric Powder
- 2 cups of Basmati Rice
- 4 medium Tomatoes

Instructions:

1. Prepare the chicken: Cut the chicken breast into 1-inch cubes. 

2. Marinate the chicken: Mix 1 tablespoon of curry powder, turmeric powder and a bit of salt as per your taste with the chicken bits. Let it marinate for about 30 minutes.

3. Cook the Basmati Rice: Rinse the rice until water runs clear. Bring 4 cups of water to a boil in a saucepan, then add the rice. When the water returns to a boil, reduce the heat to low, cover the saucepan and let simmer for about 15-20 minutes or until the rice is tender and the water is absorbed.

4. Prepare the sauce: While your rice is cooking, finely chop the tomatoes. Heat 2 tablespoons of oil in a pan over medium heat, then add the remaining curry powder to it. Stir and cook for a minute. Add the chopped tomatoes and cook until they break down into a sauce, this will take about 10-15 minutes.

5. Cook the chicken: Add the marinated chicken to the tomato and curry sauce. Stir well to coat the chicken with the sauce. Cover the pan and simmer for about 20 minutes, or until the chicken is cooked through. Make sure you stir occasionally to prevent the curry from sticking to the pan.

6. Check and adjust seasoning: Taste the chicken curry and adjust the seasoning if necessary. If you prefer a spicier curry, you can add more curry powder at this stage.

7. Serve: Fluff the rice with a fork and serve the chicken curry over the cooked basmati rice.

Enjoy your homemade chicken curry!
```


## Future Enhancements
- Allow user input to dynamically add items to the inventory.
- Include support for multiple recipes and cuisines.
- Add a web interface for user interaction.
---