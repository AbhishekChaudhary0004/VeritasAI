# 📰 Rumour Verification System

An AI-powered fake news detection and rumour verification web application built with **Streamlit**. Paste a claim, article, or URL — get an instant **FAKE / REAL verdict** with confidence score, backed by live news search.

---

## 🚀 Features

### 🗣️ Tab 1 — Heard a Rumour?
- Type any claim (WhatsApp forward, social media post, word of mouth)
- Automatically searches **NewsAPI** for related articles
- Combines claim + article content for a stronger ML prediction
- Returns **FAKE / REAL verdict** + confidence percentage
- Shows all related source articles with expandable previews
- Links to trusted Indian & international fact-checkers

### 📄 Tab 2 — Paste Article
- Paste the full text of any news article
- Instant **ML-based prediction** with verdict and progress bar

### 🌍 Tab 3 — Live News Feed
- Filter by **Country** (India, USA, UK) and **Category** (General, Tech, Science, Health, Business, Sports)
- Fetches top headlines via NewsAPI
- Shows **summary metrics**: Total / Real / Fake counts
- Every article card shows inline FAKE/REAL verdict + confidence

### 🔗 Tab 4 — Check URL
- Paste any news article link
- Uses **newspaper3k** to auto-extract title + body text
- Returns full prediction and verdict
- Gracefully handles blocked/paywalled URLs with helpful fallback tips

### ⚙️ Sidebar
- 🌐 **Language selector** — English / French
- 🔢 **Article count slider** — 3 to 10 articles per search
- ℹ️ **About** — Built by Abhishek Chaudhary, B.Tech CSIT, AKGEC Ghaziabad

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit |
| ML Model | scikit-learn (saved as `model.pkl`) |
| Text Vectorisation | TF-IDF (saved as `tfidf.pkl`) |
| News Data | NewsAPI (`newsapi-python`) |
| Article Extraction | newspaper3k |
| Language | Python 3.9+ |

---

## 📁 Project Structure

```
rumour-verification-system/
│
├── app.py              # Main Streamlit application
├── model.pkl           # Trained ML classifier (scikit-learn)
├── tfidf.pkl           # Fitted TF-IDF vectoriser
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

> ⚠️ `model.pkl` and `tfidf.pkl` **must be present** in the root directory for the app to run.

---

## 🧠 How the Prediction Works

1. Input text is vectorised using the saved **TF-IDF** transformer (`tfidf.pkl`)
2. The scikit-learn classifier predicts `1` = REAL or `0` = FAKE
3. Confidence is derived from the model's `decision_function` score:
   ```python
   confidence = min(abs(score) * 20, 100)
   ```
4. For Tab 1, related NewsAPI article content is **concatenated** with the claim before prediction for higher accuracy

---

## ✅ Built-in Fact-Checker Links

| Site | URL |
|---|---|
| Alt News | https://www.altnews.in |
| Boom Live | https://www.boomlive.in |
| Snopes | https://www.snopes.com |
| Vishvas News | https://www.vishvasnews.com |

---

## 📌 Known Limitations

- NewsAPI free tier: **100 requests/day**, country filter unavailable in developer mode
- Some URLs (paywalled or JS-rendered) cannot be extracted by `newspaper3k` — use Tab 2 as fallback
- Model accuracy depends on the dataset used to train `model.pkl`

---

## 👨‍💻 Author

**Abhishek Chaudhary**  
B.Tech CSIT | AKGEC Ghaziabad  
Built with ❤️ using Python & Streamlit
