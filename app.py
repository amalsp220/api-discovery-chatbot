import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_prepare_data():
    """Load or create the API dataset"""
    try:
        df = pd.read_csv("data/public_apis.csv")
    except FileNotFoundError:
        # Create sample data
        st.info("📦 Using sample dataset. For full 16K+ APIs, add a CSV file.")
        df = pd.DataFrame({
            'API': [
                'OpenWeatherMap', 'NASA', 'Random User', 'Cat Facts', 
                'Dog API', 'REST Countries', 'IP API', 'GitHub',
                'Quotes', 'Unsplash', 'News API', 'OpenAI'
            ],
            'Description': [
                'Weather data and forecasts for any location',
                'NASA data including astronomy pictures and Mars rover photos',
                'Generate random user data for testing',
                'Daily cat facts and cat pictures',
                'Dog images by breed',
                'Country information including flags and currencies',
                'IP geolocation and information',
                'Repository and user data from GitHub',
                'Inspirational and random quotes',
                'High quality free stock photos',
                'News articles and headlines',
                'AI language models and completions'
            ],
            'Category': [
                'Weather', 'Science', 'Development', 'Animals',
                'Animals', 'Open Data', 'Development', 'Development',
                'Personality', 'Photography', 'News', 'Machine Learning'
            ],
            'Auth': [
                'apiKey', 'apiKey', 'No', 'No',
                'No', 'No', 'No', 'OAuth',
                'No', 'apiKey', 'apiKey', 'apiKey'
            ],
            'HTTPS': [True] * 12,
            'CORS': [
                'Unknown', 'No', 'Yes', 'No',
                'Yes', 'Yes', 'Yes', 'Yes',
                'Unknown', 'Unknown', 'Yes', 'Yes'
            ],
            'Link': [
                'https://openweathermap.org/api',
                'https://api.nasa.gov',
                'https://randomuser.me',
                'https://catfacts.com/api',
                'https://dog.ceo/dog-api',
                'https://restcountries.com',
                'https://ip-api.com',
                'https://docs.github.com/en/rest',
                'https://quotes.rest',
                'https://unsplash.com/developers',
                'https://newsapi.org',
                'https://platform.openai.com'
            ]
        })
    
    # Create search text
    df['search_text'] = (
        df['API'].fillna('') + ' ' +
        df['Description'].fillna('') + ' ' +
        df['Category'].fillna('')
    )
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df['search_text'])
    
    return df, vectorizer, tfidf_matrix

def search_apis(query, df, vectorizer, tfidf_matrix, filters=None, k=20):
    """Search APIs using cosine similarity"""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).ravel()
    df_copy = df.copy()
    df_copy['score'] = similarities
    
    result = df_copy
    
    if filters:
        if filters.get('categories'):
            result = result[result['Category'].isin(filters['categories'])]
        if filters.get('auth_types'):
            result = result[result['Auth'].isin(filters['auth_types'])]
        if filters.get('https_only'):
            result = result[result['HTTPS'] == True]
        if filters.get('cors_yes'):
            result = result[result['CORS'] == 'Yes']
    
    return result.nlargest(k, 'score')

def test_api(method, url, headers_json, body_json):
    """Test an API endpoint"""
    try:
        headers = json.loads(headers_json) if headers_json.strip() else {}
        body = json.loads(body_json) if body_json.strip() and method != 'GET' else None
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            timeout=10
        )
        
        return {
            'status': response.status_code,
            'headers': dict(response.headers),
            'body': response.text[:2000]
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 API Discovery Chatbot</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem; color: #666;'>"
        "Discover and test 16,000+ free public APIs"
        "</p>",
        unsafe_allow_html=True
    )
    
    # Load data
    df, vectorizer, tfidf_matrix = load_and_prepare_data()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Filters")
        
        categories = st.multiselect(
            "Categories",
            options=sorted(df['Category'].dropna().unique()),
            help="Filter by API category"
        )
        
        auth_types = st.multiselect(
            "Authentication",
            options=sorted(df['Auth'].dropna().unique()),
            help="Filter by authentication type"
        )
        
        https_only = st.checkbox("HTTPS Only", value=False)
        cors_yes = st.checkbox("CORS: Yes Only", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.metric("Total APIs", len(df))
        st.metric("Categories", df['Category'].nunique())
    
    # Main tabs
    tab1, tab2 = st.tabs(["🔍 Find APIs", "🧪 Test API"])
    
    with tab1:
        st.markdown("### Search for APIs")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input(
                "What kind of API are you looking for?",
                placeholder="e.g., weather API with JSON response",
                label_visibility="collapsed"
            )
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True, type="primary")
        
        if query and search_button:
            with st.spinner("Searching APIs..."):
                filters = {
                    'categories': categories,
                    'auth_types': auth_types,
                    'https_only': https_only,
                    'cors_yes': cors_yes
                }
                
                results = search_apis(query, df, vectorizer, tfidf_matrix, filters)
                
                st.markdown(f"### 📋 Found {len(results)} APIs")
                
                for idx, row in results.iterrows():
                    with st.expander(
                        f"**{row['API']}** | {row['Category']} | Relevance: {row['score']:.3f}"
                    ):
                        st.markdown(f"**Description:** {row['Description']}")
                        st.markdown(f"**Documentation:** [{row['Link']}]({row['Link']})")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Auth", row['Auth'])
                        col2.metric("HTTPS", "✅" if row['HTTPS'] else "❌")
                        col3.metric("CORS", row['CORS'])
                        
                        st.info("💡 Copy the API URL to test it in the 'Test API' tab!")
    
    with tab2:
        st.markdown("### HTTP Request Playground")
        st.markdown("Test any API endpoint directly!")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            test_url = st.text_input("Request URL", placeholder="https://api.example.com/endpoint")
        with col2:
            method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"])
        
        col1, col2 = st.columns(2)
        with col1:
            headers_input = st.text_area(
                "Headers (JSON)",
                value='{"Content-Type": "application/json"}',
                height=150
            )
        with col2:
            body_input = st.text_area(
                "Body (JSON)",
                value='{}',
                height=150,
                disabled=(method == 'GET')
            )
        
        if st.button("🚀 Send Request", type="primary"):
            if test_url:
                with st.spinner("Sending request..."):
                    result = test_api(method, test_url, headers_input, body_input)
                    
                    if 'error' in result:
                        st.error(f"❌ Error: {result['error']}")
                    else:
                        st.success(f"✅ Status Code: {result['status']}")
                        
                        with st.expander("📥 Response Headers", expanded=False):
                            st.json(result['headers'])
                        
                        with st.expander("📄 Response Body", expanded=True):
                            try:
                                st.json(json.loads(result['body']))
                            except:
                                st.text(result['body'])
            else:
                st.warning("Please enter a URL")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit | "
        "<a href='https://github.com/amalsp220/api-discovery-chatbot'>View on GitHub</a>"
        "</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
