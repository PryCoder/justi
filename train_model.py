# train_model.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training data
comments = [
    "you are awesome",
    "I hate you",
    "great work!",
    "you are so stupid",
    "I love this app",
    "shut up",
    "this is amazing",
    "idiot",
    "you are a genius",
    "what the hell",
    "go to hell",
    "fantastic job"
]

labels = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]  # 0 = clean, 1 = vulgar

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(comments)

model = LogisticRegression()
model.fit(X, labels)

# Save model and vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model trained and saved as model.pkl")
