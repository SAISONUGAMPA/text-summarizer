from flask import Flask, render_template, request, jsonify
import webbrowser
import os
import socket
from threading import Timer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from string import punctuation
import urllib.request
from bs4 import BeautifulSoup

# Download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

app = Flask(__name__)

class TextSummarizer:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.stopWords = set(stopwords.words("english") + list(punctuation))
        self.text = ""
        self.sentences = []

    def tokenize_sentence(self, text):
        return word_tokenize(text)

    def cal_freq(self, words):
        freqTable = {}
        for word in words:
            word = word.lower()
            if word in self.stopWords:
                continue
            word = self.stemmer.stem(word)
            freqTable[word] = freqTable.get(word, 0) + 1
        return freqTable

    def compute_sentence(self, text, freqTable):
        sentences = sent_tokenize(text)
        sentenceValue = {}
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq
        return sentences, sentenceValue

    def sumAvg(self, sentenceValue):
        if len(sentenceValue) == 0:
            return 0
        sorted_values = sorted(sentenceValue.values())
        n = len(sorted_values)
        if n % 2 == 0:
            median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            median = sorted_values[n//2]
        return median

    def summarize(self, text):
        words = self.tokenize_sentence(text)
        freqTable = self.cal_freq(words)
        sentences, sentenceValue = self.compute_sentence(text, freqTable)
        avg = self.sumAvg(sentenceValue)
        
        summary = []
        sentence_lengths = {}
        
        for sentence in sentences:
            word_count = len(word_tokenize(sentence))
            sentence_lengths[sentence] = word_count
        
        for sentence in sentences:
            if sentence in sentenceValue:
                score = sentenceValue[sentence]
                word_count = sentence_lengths.get(sentence, 0)
                if word_count < 2:
                    continue
                normalized_score = score / (word_count ** 0.5)
                summary.append((normalized_score, sentence))
        
        if not summary:
            return ""
        
        summary.sort(key=lambda x: x[0], reverse=True)
        max_sentences = max(1, len(sentences) // 3)
        selected = [sent for _, sent in summary[:max_sentences]]
        selected.sort(key=lambda s: sentences.index(s))
        
        return ' '.join(selected)


def get_article_text(url):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        page = urllib.request.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(page, "html.parser")
        title = soup.title.text if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return title, text
    except Exception as e:
        return None, str(e)


summarizer = TextSummarizer()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/summarize-text', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if len(text) < 10:
            return jsonify({'error': 'Please enter at least 10 characters'}), 400
        
        summary = summarizer.summarize(text)
        
        if not summary:
            return jsonify({'error': 'Could not generate summary'}), 400
        
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summarize-url', methods=['POST'])
def summarize_url():
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please enter a URL'}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        title, text = get_article_text(url)
        
        if text is None:
            return jsonify({'error': 'Could not fetch the URL. Please check the URL and try again.'}), 400
        
        if len(text) < 10:
            return jsonify({'error': 'The fetched content is too short to summarize'}), 400
        
        summary = summarizer.summarize(text)
        
        if not summary:
            return jsonify({'error': 'Could not generate summary from the content'}), 400
        
        return jsonify({'title': title, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def open_browser(url):
    webbrowser.open(url)


def get_local_ip():
    try:
        # Method 1: Try to get IP by connecting to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and ip != "127.0.0.1":
            return ip
    except Exception:
        pass
    
    try:
        # Method 2: Get hostname and resolve it
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if ip and ip != "127.0.0.1":
            return ip
    except Exception:
        pass
    
    try:
        # Method 3: Parse ipconfig output (Windows specific)
        import subprocess
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if 'IPv4 Address' in line:
                ip = line.split(':')[-1].strip()
                if ip and ip != "127.0.0.1":
                    return ip
    except Exception:
        pass
    
    # Fallback
    return "127.0.0.1"


if __name__ == '__main__':
    # Get local IP address
    local_ip = get_local_ip()
    app_url = f'http://{local_ip}:5000/'
    
    # Open browser after a short delay
    timer = Timer(1.5, open_browser, args=[app_url])
    timer.daemon = True
    timer.start()
    
    print("=" * 60)
    print("Starting Text Summarizer Web App...")
    print("=" * 60)
    print(f"\n🌐 ACCESS URL (Desktop & Phone):")
    print(f"  {app_url}")
    print(f"\n📱 Phone must be on the same WiFi network!")
    print("=" * 60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
