from textblob import TextBlob

def preprocess_text(text):
    # Simple whitespace-based tokenization
    return text.lower().split()

def get_sentiment(text):
    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment(sentences, target_string):
    # Preprocess the sentences
    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]

    # Get sentiment of the target string
    sentiment = get_sentiment(target_string)

    print(f"Target String: '{target_string}'")
    print(f"Sentiment: {sentiment}")

    return sentiment

# Example list of strings (sentences)
sentences = [
    "I love this product!",
    "This movie is terrible.",
    "I am feeling good today.",
    "I'm not happy with the service.",
    "The weather is nice outside.",
    "This book is amazing!"
]

target_string = "I am really excited about this event"

analyze_sentiment(sentences, target_string)