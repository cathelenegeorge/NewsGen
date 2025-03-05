import pandas as pd
import streamlit as st

def load_data(csv_path):
    """Loads the structured news dataset."""
    try:
        df = pd.read_csv(csv_path)
        st.write("✅ Data loaded successfully")
        st.write(df.head(10))  # Print sample data
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: File '{csv_path}' not found.")
        return None

def generate_news_article(df, category=None):
    """Generates a random news article based on category."""
    if category and category != "All":
        df = df[df['Category'].str.lower() == category.lower()]

    if df.empty:
        return "⚠️ No articles found for this category."

    article = df.sample(n=1).iloc[0]

    generated_article = {
        "headline": article['Headline'],
        "source": article['Newspaper Name'],
        "date": article['Published Date'],
        "content": article['Content'],
        "summary": article['Human Summary']
    }

    return generated_article

# Streamlit App
st.title("📰 NewsGen🐞🐈")
st.write("Generate news articles from structured data.")

csv_path = "newsdataset.csv"
df = load_data(csv_path)

if df is not None:
    categories = ["All"] + sorted(df['Category'].dropna().unique().tolist())
    selected_category = st.selectbox("Select News Category", categories)

    if st.button("Generate News Article"):
        article = generate_news_article(df, selected_category)

        if isinstance(article, dict):
            st.subheader(article['headline'])
            st.write(f"*Published by {article['source']} on {article['date']}*")
            st.write(article['content'])
            st.markdown(f"**Summary:** {article['summary']}")
        else:
            st.warning(article)  # Show a warning if no article is found
