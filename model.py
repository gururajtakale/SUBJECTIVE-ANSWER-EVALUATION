import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
import re

# Sample student's answer and expected answers
test_cases = [
    ("A CSV (Comma-Separated Values) file is a plain text format used to store tabular data, with each line representing a record and fields separated by commas. It is commonly used for data storage, exchange.",
     "Machine learning (ML) is a branch of artificial intelligence (AI) and computer science that focuses on using data and algorithms to enable AI to imitate the way that humans learn, gradually improving its accuracy."),
    ("Machine learning is a subset of artificial intelligence.",
     "Machine learning is a method used for data analysis that automates analytical model building."),
    ("Machine learning is a branch of AI.",
     "Machine learning is a branch of artificial intelligence (AI) and computer science that focuses on using data and algorithms to enable AI to imitate the way that humans learn, gradually improving its accuracy."),
    ("Machine learning is a method used for data analysis that automates analytical model building.",
     "Machine learning is a branch of artificial intelligence (AI) and computer science that focuses on using data and algorithms to enable AI to imitate the way that humans learn, gradually improving its accuracy."),
    ("Machine learning is a method used for data analysis that automates analytical model building.",
     "Machine learning is a subset of artificial intelligence."),
    ("Machine learning is a method used for data analysis that automates analytical model building.",
     "It is commonly used for data storage, exchange.")
]

# Pre-processing
def preprocess(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters and punctuation
    sentences = sent_tokenize(text)  # Tokenization into sentences
    words = [word_tokenize(sentence) for sentence in sentences]  # Tokenization of words in each sentence
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    words = [[stemmer.stem(word) for word in sentence if word not in stop_words] for sentence in words]  # Removal of stop words and stemming
    return words

# Train Word2Vec model
def train_word2vec(text):
    model = Word2Vec(text, min_count=1)
    return model

# Sentence analysis
def analyze_sentences(student_answer, expected_answer):
    student_sentence_count = len(student_answer)
    expected_sentence_count = len(expected_answer)
    return student_sentence_count, expected_sentence_count

# Cosine similarity using Word2Vec embeddings
def compute_cosine_similarity(student_answer, expected_answer, model):
    student_vectors = [sum(model.wv[word] for word in sentence if word in model.wv.key_to_index) / len(sentence) for sentence in student_answer]
    expected_vectors = [sum(model.wv[word] for word in sentence if word in model.wv.key_to_index) / len(sentence) for sentence in expected_answer]
    similarities = [cosine_similarity([student_vectors[i]], [expected_vectors[i]])[0][0] for i in range(min(len(student_vectors), len(expected_vectors)))]
    overall_similarity = sum(similarities) / len(similarities) if similarities else 0
    return overall_similarity

# Sentiment analysis
def sentiment_analysis(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)
    return sentiment_score['compound']

# Grammar checking
def grammar_check(text):
    tool = language_tool_python.LanguageTool('en-US')
    grammar_errors = tool.check(text)
    return grammar_errors

# Final scoring and result generation
def generate_result(cosine_similarity_score, student_sentence_count, expected_sentence_count, student_sentiment_score, expected_sentiment_score, student_grammar_errors, expected_grammar_errors):
    similarity_score = cosine_similarity_score * min(student_sentence_count, expected_sentence_count)
    sentiment_difference = abs(student_sentiment_score - expected_sentiment_score)
    grammar_penalty = len(student_grammar_errors) - len(expected_grammar_errors)
    final_score = similarity_score - sentiment_difference - grammar_penalty
    scaled_score = final_score * 10 / max(similarity_score, 1e-6)  # Scale to 10
    return scaled_score

# Grade classification
def classify_grade(score):
    if score == 0:
        return 'F'
    elif 0 < score <= 5:
        return 'C'
    elif 5 < score <= 6.5:
        return 'B'
    else:
        return 'A'

# Evaluate each test case
for i, (student_answer, expected_answer) in enumerate(test_cases):
    print(f"Test Case {i+1}:")
    processed_student_answer = preprocess(student_answer)
    processed_expected_answer = preprocess(expected_answer)

    model = train_word2vec(processed_expected_answer + processed_student_answer)

    student_sentence_count, expected_sentence_count = analyze_sentences(processed_student_answer, processed_expected_answer)

    cosine_similarity_score = compute_cosine_similarity(processed_student_answer, processed_expected_answer, model)

    student_sentiment_score = sentiment_analysis(student_answer)
    expected_sentiment_score = sentiment_analysis(expected_answer)

    student_grammar_errors = grammar_check(student_answer)
    expected_grammar_errors = grammar_check(expected_answer)

    result = generate_result(cosine_similarity_score, student_sentence_count, expected_sentence_count, student_sentiment_score, expected_sentiment_score, student_grammar_errors, expected_grammar_errors)

    grade = classify_grade(result)
    print("Scaled Score:", result)
    print("Grade:", grade)
    print()
