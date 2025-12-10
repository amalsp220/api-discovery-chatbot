# 🤖 API Discovery Chatbot


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://api-discovery-chatbot-5obhjpm58wcsgsjsqtvg6n.streamlit.app/)
**🚀 [Live Demo](https://api-discovery-chatbot-5obhjpm58wcsgsjsqtvg6n.streamlit.app/)**
An AI-powered chatbot built with Streamlit that helps developers discover and test 16,000+ free public APIs. Features semantic search, interactive API testing playground, and comprehensive API metadata.

## ✨ Features

- 🔍 **Semantic Search**: Find APIs using natural language queries  
- 🎯 **Smart Filters**: Filter by category, authentication type, HTTPS support, and CORS  
- 🧪 **API Testing Playground**: Test APIs directly in the browser  
- 📊 **Rich Metadata**: View API documentation, authentication requirements, and more  
- ⚡ **Fast & Responsive**: Built with efficient text search algorithms  
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.8
pip
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/amalsp220/api-discovery-chatbot.git
cd api-discovery-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

Create the following files in your project:

```
api-discovery-chatbot/
├── app.py                 # Main application
├── requirements.txt       # Dependencies  
├── README.md             # This file
└── data/
    └── public_apis.csv   # API dataset (optional)
```

## 💻 Code Files

### Create `app.py`

Create a file named `app.py` with the complete Streamlit application code. Visit the repository to see the full code.

Key features of the app:
- TF-IDF based semantic search
- Multi-filter support (category, auth, HTTPS, CORS)
- Interactive HTTP request testing
- Sample data generation if CSV not found

### Create `requirements.txt`

```txt
streamlit==1.29.0
pandas==2.1.4  
scikit-learn==1.3.2
requests==2.31.0
numpy==1.26.2
```

### Data Source

The app can work with:
1. **Auto-generated sample data** (built-in)
2. **Full dataset** from public-apis GitHub repository

To use the full dataset, parse the APIs from [public-apis/public-apis](https://github.com/public-apis/public-apis) and create a CSV with columns: API, Description, Category, Auth, HTTPS, CORS, Link.

## 🎯 Usage

1. **Search for APIs**: Enter natural language queries like "weather API with no authentication"
2. **Apply Filters**: Use sidebar filters to narrow down results
3. **View Details**: Expand any API card to see full documentation
4. **Test APIs**: Switch to Test tab to make live HTTP requests

## 💡 Example Queries

- "free weather API with JSON response"
- "cryptocurrency prices with no auth"
- "random user data generator"
- "machine learning image recognition"

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Search**: scikit-learn (TF-IDF)
- **Data**: Pandas
- **HTTP Client**: Requests

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Public APIs](https://github.com/public-apis/public-apis) - Comprehensive API list
- [Streamlit](https://streamlit.io/) - Amazing web framework
- [scikit-learn](https://scikit-learn.org/) - Machine learning library

## 📞 Contact

**Amal SP** - [@amalsp220](https://github.com/amalsp220)

Project Link: [https://github.com/amalsp220/api-discovery-chatbot](https://github.com/amalsp220/api-discovery-chatbot)

---

⭐ **Star this repo if you find it helpful!**

## 📚 Next Steps

To complete the project:

1. Create the `app.py` file with the complete Streamlit code
2. Create the `requirements.txt` file  
3. Optional: Add data extraction script to parse public-APIs
4. Run `streamlit run app.py` to test locally
5. Deploy to Streamlit Cloud, Heroku, or your preferred platform

For the complete `app.py` code, check the repository commits or create a new issue requesting the full code file.
