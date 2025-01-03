import streamlit as st
import requests
import pandas as pd

# Function to fetch data from a URL (API)
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Assuming the API returns JSON data
        return data['recipes']  # Access the recipes list from the JSON response
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Function to search for recipes based on name
def search_recipes(data, query):
    df = pd.DataFrame(data)
    query_results = df[df.apply(lambda row: row.astype(str).str.contains(query.strip(), case=False).any(), axis=1)]
    return query_results

# Function to display recipes in card styling
def display_recipes(results):
    for index, row in results.iterrows():
        st.markdown(f"""
        <div style="background-color:#222222;padding:15px;border-radius:10px;margin-bottom:15px;">
            <h2 style="color:#ffffff;">{row.get('name', 'No Name')}</h2>
            <img src="{row.get('image', '')}" alt="Recipe Image" style="width:100%;border-radius:10px;">
            <p style="color:#ffffff;">{row.get('description', 'No Description')}</p>
            <p style="color:#ffffff;"><strong>Ingredients:</strong> {row.get('ingredients', 'No Ingredients')}</p>
            <p style="color:#ffffff;"><strong>Instructions:</strong> {row.get('instructions', 'No Instructions')}</p>
        </div>
        """, unsafe_allow_html=True)

# Streamlit application with dark theme styling
def main():
    # Custom CSS for dark theme styling
    st.markdown("""
        <style>
        .main {
            background-color: #000000;
            color: #ffffff;
        }
        .title {
            font-size: 2em;
            color: #ffffff;
        }
        .header {
            font-size: 1.5em;
            color: #ffffff;
            margin-top: 20px;
        }
        .result-table {
            margin-top: 20px;
        }
        .stTextInput input {
            background-color: #333333;
            color: #ffffff;
        }
        .stButton button {
            background-color: #333333;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 class="title">Recipe Search Application</h1>', unsafe_allow_html=True)

    # URL of the API
    url = "https://dummyjson.com/recipes"

    # Fetch data from the URL
    data = fetch_data(url)

    if data:
        # Sidebar for user input
        with st.sidebar:
            st.markdown('<h2 class="header">Search Parameters</h2>', unsafe_allow_html=True)
            query = st.text_input("Enter recipe name to search:")
            search_button = st.button("Search")

        if search_button and query:
            results = search_recipes(data, query)
            if not results.empty:
                st.markdown(f'<h2 class="header">Found {len(results)} recipes matching your query:</h2>', unsafe_allow_html=True)
                display_recipes(results)
            else:
                st.markdown('<h2 class="header">No recipes found for your query.</h2>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()