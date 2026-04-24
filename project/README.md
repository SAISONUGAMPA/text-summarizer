# Text Summarizer Web App

A Flask-based web application that summarizes text and web articles using natural language processing.

## Features

- **Text Summarization**: Paste your own text to get a concise summary
- **URL Summarization**: Enter a URL to fetch and summarize article content
- **Real-time Processing**: Fast summarization using NLTK
- **Responsive UI**: Works on desktop and mobile devices

## Technologies Used

- **Backend**: Flask (Python web framework)
- **NLP**: NLTK (Natural Language Toolkit)
- **Web Scraping**: BeautifulSoup4
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SAISONUGAMPA/text-summarizer.git
cd text-summarizer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. The app will automatically open in your browser at:
   - **Local**: http://127.0.0.1:5000
   - **Network**: http://<your-ip>:5000 (accessible from other devices on the same WiFi)

3. Stop the server with `CTRL+C`

## Usage

### Text Summary
1. Go to the "Text Summary" tab
2. Paste your text (at least 10 characters)
3. Click "Summarize Text"
4. Get a concise summary in 1-2 seconds

### URL Summary
1. Go to the "URL Summary" tab
2. Enter a URL (with or without https://)
3. Click "Summarize URL"
4. The app fetches the article and provides a summary with the title

## Project Structure

```
.
├── app.py                 # Main Flask application
├── textSummarizer.py      # Text summarization logic
├── urlTextReader.py       # URL content extraction
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── templates/
    └── index.html        # Web interface
```

## API Endpoints

### POST /api/summarize-text
Summarizes plain text.

**Request:**
```json
{
  "text": "Your text here..."
}
```

**Response:**
```json
{
  "summary": "Summarized text..."
}
```

### POST /api/summarize-url
Fetches and summarizes content from a URL.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "title": "Article Title",
  "summary": "Summarized content..."
}
```

## Deployment

### Deploy on Render
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Connect your GitHub repository
4. Deploy as a Web Service
5. Set environment: Python 3.9+
6. Build command: `pip install -r requirements.txt`
7. Start command: `gunicorn app:app`

### Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Railway auto-detects Flask and deploys

## Error Handling

- Minimum 10 characters required for text summarization
- URL must be valid and accessible
- Network timeouts are set to 10 seconds for URL fetching

## License

This project is open source and available under the MIT License.

## Author

SAISONUGAMPA

---

Happy Summarizing! 📝
