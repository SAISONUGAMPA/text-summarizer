import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from string import punctuation

# Download NLTK resources (Run once)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


class TextSummarizer:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.stopWords = set(stopwords.words("english") + list(punctuation))
        self.text = ""
        self.sentences = []

    def input_text(self):
        while True:
            self.text = input("Enter the text to summarize:\n")
            if len(self.text) > 10:
                break
            else:
                print("Please enter text of at least 10 characters.")

    def tokenize_sentence(self):
        return word_tokenize(self.text)

    def cal_freq(self, words):
        freqTable = {}

        for word in words:
            word = word.lower()

            if word in self.stopWords:
                continue

            word = self.stemmer.stem(word)

            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        return freqTable

    def compute_sentence(self, freqTable):
        self.sentences = sent_tokenize(self.text)
        sentenceValue = {}

        for sentence in self.sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        return sentenceValue

    def sumAvg(self, sentenceValue):
        if len(sentenceValue) == 0:
            return 0

        sumValues = sum(sentenceValue.values())
        # Use median instead of mean for more robust threshold
        sorted_values = sorted(sentenceValue.values())
        n = len(sorted_values)
        if n % 2 == 0:
            median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            median = sorted_values[n//2]

        return median

    def print_summary(self, sentenceValue, average):
        if not sentenceValue:
            return "No summary available."
        
        summary = []
        sentence_lengths = {}

        # Calculate sentence lengths for length normalization
        for sentence in self.sentences:
            word_count = len(word_tokenize(sentence))
            sentence_lengths[sentence] = word_count

        # Score all sentences
        for sentence in self.sentences:
            if sentence in sentenceValue:
                score = sentenceValue[sentence]
                word_count = sentence_lengths.get(sentence, 0)

                # Skip very short sentences (less than 2 words)
                if word_count < 2:
                    continue

                # Normalize score by sentence length to avoid bias toward long sentences
                normalized_score = score / (word_count ** 0.5)
                summary.append((normalized_score, sentence))

        if not summary:
            return "No suitable sentences for summary."

        # Sort by normalized score and take top sentences
        summary.sort(key=lambda x: x[0], reverse=True)

        # Limit to at most 30% of original sentence count, minimum 1
        max_sentences = max(1, len(self.sentences) // 3)
        selected = [sent for _, sent in summary[:max_sentences]]

        # Restore original order for coherent output
        selected.sort(key=lambda s: self.sentences.index(s))

        return ' '.join(selected)


# Main Program
if __name__ == "__main__":
    ts = TextSummarizer()

    ts.input_text()

    words = ts.tokenize_sentence()
    freqTable = ts.cal_freq(words)
    sentenceValue = ts.compute_sentence(freqTable)
    avg = ts.sumAvg(sentenceValue)
    summary = ts.print_summary(sentenceValue, avg)

    print("\n" + "=" * 60)
    print("FINAL SUMMARY:\n")
    print(summary)
    print("=" * 60)