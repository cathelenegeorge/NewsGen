import pandas as pd
import streamlit as st

def load_data(csv_path):
    """Loads the structured news dataset."""
    try:
        df = pd.read_csv(csv_path)
        st.write("✅ Data loaded successfully")
        st.write(df.head(3))  # Print sample data
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: File '{csv_path}' not found.")
        return None

def generate_news_articles(df, category=None):
    """Generates all relevant news articles based on category."""
    if category and category != "All":
        df = df[df['Category'].str.lower() == category.lower()]

    if df.empty:
        return ["⚠️ No articles found for this category."]
    
    articles = []
    for _, article in df.iterrows():
        articles.append({
            "headline": article['Headline'],
            "source": article['Newspaper Name'],
            "date": article['Published Date'],
            "content": article['Content'],
            "summary": article['Human Summary']
        })
    
    return articles

# Streamlit App
st.title("NewsGen🍁✨")

data_file = "newsdataset.csv"  # Update with actual data file name
df = load_data(data_file)

if df is not None:
    category = st.selectbox("Select News Category:", ["All"] + list(df['Category'].unique()))
    if st.button("Generate News Article"):
        articles = generate_news_articles(df, category)
        for article in articles:
            if isinstance(article, str):
                st.warning(article)
            else:
                st.subheader(article["headline"])
                st.write(f"📰 Source: {article['source']}")
                st.write(f"📅 Date: {article['date']}")
                st.write(article["content"])
                st.success(f"Summary: {article['summary']}")
                st.markdown("---")
