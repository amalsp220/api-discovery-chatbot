import streamlit as st
import pandas as pd
import requests
import json

# Page config
st.set_page_config(
    page_title="API Discovery Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
.stApp {background-color: #0e1117;}
.api-card {padding: 20px; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 10px 0; color: white;}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 API Discovery Chatbot")
st.markdown("Discover and test 16,000+ free public APIs with intelligent search")

# Sample APIs data
sample_apis = [
    {"API": "OpenWeatherMap", "Description": "Weather data and forecasts", "Auth": "apiKey", "HTTPS": True, "CORS": "yes", "Category": "Weather", "Link": "https://openweathermap.org/api"},
    {"API": "NASA", "Description": "NASA data including imagery", "Auth": "apiKey", "HTTPS": True, "CORS": "yes", "Category": "Science", "Link": "https://api.nasa.gov"},
    {"API": "Random User", "Description": "Generate random user data", "Auth": "No", "HTTPS": True, "CORS": "yes", "Category": "Data", "Link": "https://randomuser.me"},
    {"API": "Cat Facts", "Description": "Daily cat facts", "Auth": "No", "HTTPS": True, "CORS": "yes", "Category": "Animals", "Link": "https://catfacts.com/api"},
    {"API": "Dog API", "Description": "Dog images", "Auth": "No", "HTTPS": True, "CORS": "yes", "Category": "Animals", "Link": "https://dog.ceo/dog-api"},
    {"API": "REST Countries", "Description": "Country information", "Auth": "No", "HTTPS": True, "CORS": "yes", "Category": "Geography", "Link": "https://restcountries.com"},
    {"API": "GitHub", "Description": "GitHub REST API", "Auth": "OAuth", "HTTPS": True, "CORS": "yes", "Category": "Development", "Link": "https://docs.github.com/en/rest"},
    {"API": "IP-API", "Description": "IP Geolocation", "Auth": "No", "HTTPS": True, "CORS": "yes", "Category": "Network", "Link": "https://ip-api.com"},
]

df = pd.DataFrame(sample_apis)

# Sidebar filters
st.sidebar.header("🎯 Filter APIs")

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

auth_types = ["All"] + sorted(df["Auth"].unique().tolist())
selected_auth = st.sidebar.selectbox("Auth Type", auth_types)

https_filter = st.sidebar.checkbox("HTTPS Only", value=True)
cors_filter = st.sidebar.checkbox("CORS Supported", value=False)

# Apply filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_auth != "All":
    filtered_df = filtered_df[filtered_df["Auth"] == selected_auth]

if https_filter:
    filtered_df = filtered_df[filtered_df["HTTPS"] == True]

if cors_filter:
    filtered_df = filtered_df[filtered_df["CORS"] == "yes"]

# Search
st.header("🔍 Search APIs")
search_query = st.text_input("Search by name or description", placeholder="e.g., weather, user data, animals...")

if search_query:
    mask = filtered_df["API"].str.contains(search_query, case=False, na=False) | filtered_df["Description"].str.contains(search_query, case=False, na=False)
    filtered_df = filtered_df[mask]

# Display results
st.subheader(f"📊 Found {len(filtered_df)} APIs")

for idx, row in filtered_df.iterrows():
    with st.expander(f"🚀 {row['API']} - {row['Category']}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Description:** {row['Description']}")
            st.markdown(f"**Category:** {row['Category']}")
            st.markdown(f"**Link:** [{row['Link']}]({row['Link']})")
        
        with col2:
            st.markdown(f"**Auth:** {row['Auth']}")
            st.markdown(f"**HTTPS:** {'✅' if row['HTTPS'] else '❌'}")
            st.markdown(f"**CORS:** {row['CORS']}")

# API Testing Playground
st.header("🧪 API Testing Playground")

api_url = st.text_input("Enter API URL to test", placeholder="https://api.example.com/endpoint")
method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])

if st.button("Test API"):
    if api_url:
        try:
            with st.spinner("Testing API..."):
                if method == "GET":
                    response = requests.get(api_url, timeout=5)
                elif method == "POST":
                    response = requests.post(api_url, timeout=5)
                elif method == "PUT":
                    response = requests.put(api_url, timeout=5)
                else:
                    response = requests.delete(api_url, timeout=5)
                
                st.success(f"✅ Status Code: {response.status_code}")
                st.json(response.json() if response.headers.get('content-type', '').startswith('application/json') else {"response": response.text[:500]})
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter an API URL")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Portfolio Project for AI Engineers")
