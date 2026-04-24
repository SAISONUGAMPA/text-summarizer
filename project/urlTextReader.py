import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

nltk.download('punkt')
nltk.download('stopwords')


def get_article_text(url):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        page = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        title = soup.title.text if soup.title else "No Title"

        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])

        return title, text

    except Exception as e:
        print("Error fetching URL:", e)
        return None, None


def summarize_text(text, num_sentences=3):
    stopWords = set(stopwords.words("english") + list(punctuation))

    words = word_tokenize(text.lower())
    freqTable = {}

    for word in words:
        if word not in stopWords:
            freqTable[word] = freqTable.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentence_scores = {}

    for sentence in sentences:
        for word in freqTable:
            if word in sentence.lower():
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freqTable[word]

    summary_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:num_sentences]

    return summary_sentences


# MAIN PROGRAM
url = input("Enter article URL:\n")

title, text = get_article_text(url)

if text:
    print("\n" + "="*60)
    print("TITLE:", title)
    print("="*60)

    summary = summarize_text(text, 3)

    print("\nSUMMARY:\n")
    for s in summary:
        print("-", s)