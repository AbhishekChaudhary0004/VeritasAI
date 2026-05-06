
import streamlit as st
import pickle
from newsapi import NewsApiClient
from newspaper import Article

@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    tfidf = pickle.load(open("tfidf.pkl", "rb"))
    return model, tfidf

@st.cache_resource
def load_api():
    return NewsApiClient(api_key="NEWSAPI_KEY")

model, tfidf = load_model()
newsapi      = load_api()

def predict(text):
    input_tfidf = tfidf.transform([text])
    prediction  = model.predict(input_tfidf)[0]
    score       = model.decision_function(input_tfidf)[0]
    confidence  = min(abs(score) * 20, 100)
    return int(prediction), round(confidence, 1)

def show_verdict(prediction, confidence):
    col1, col2 = st.columns([2, 1])
    with col1:
        if prediction == 1:
            st.success("REAL NEWS — This appears to be genuine.")
        else:
            st.error("LIKELY FAKE — This may be misleading.")
    with col2:
        st.metric("Confidence", f"{confidence}%")
        st.progress(int(confidence))

def show_factcheckers():
    st.divider()
    st.caption("Also verify on trusted fact-checkers:")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.link_button("Alt News",     "https://www.altnews.in")
    with c2: st.link_button("Boom Live",    "https://www.boomlive.in")
    with c3: st.link_button("Snopes",       "https://www.snopes.com")
    with c4: st.link_button("Vishvas News", "https://www.vishvasnews.com")

def search_news(query, language="en", num=5):
    try:
        results = newsapi.get_everything(
            q=query,
            language=language,
            sort_by="relevancy",
            page_size=num
        )
        return results.get("articles", [])
    except Exception as e:
        st.error(f"NewsAPI error: {e}")
        return []

def show_sources(articles):
    if not articles:
        return
    st.subheader(f"Related sources found ({len(articles)}):")
    for article in articles:
        title  = article.get("title",  "No title") or "No title"
        source = article["source"]["name"]
        desc   = article.get("description", "")    or ""
        url    = article.get("url", "#")
        with st.expander(f"{source} — {title[:65]}..."):
            st.write(desc)
            st.link_button("Read full article", url)

st.set_page_config(
    page_title="Rumour Checker",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Rumour Verification System")
st.caption("Heard something? Check if it is real or fake instantly.")

with st.sidebar:
    st.header("Settings")
    language = st.selectbox(
        "News language",
        ["en", "fr"],
        format_func=lambda x: "English" if x == "en" else "French"
    )
    num_articles = st.slider("Articles to search", 3, 10, 5)
    st.divider()
    st.subheader("About")
    st.write("""
    Verifies news using:
    - Machine Learning (NLP)
    - Live news search
    - Multiple trusted sources

    Built by Abhishek Chaudhary
    B.Tech CSIT | AKGEC Ghaziabad
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "Heard a Rumour?",
    "Paste Article",
    "Live News Feed",
    "Check URL"
])

with tab1:
    st.subheader("Type exactly what you heard")
    st.write("WhatsApp forward, friend told you, saw on social media — type it below.")
    claim = st.text_area(
        "What did you hear?",
        placeholder="e.g. Government giving free LPG / Modi banned crypto / Cure for cancer found",
        height=120,
        key="tab1_input"
    )
    with st.columns([1, 4])[0]:
        check = st.button("Check Now", type="primary", key="tab1_btn")
    if check:
        if claim.strip() == "":
            st.warning("Please type the news you heard.")
        else:
            with st.spinner("Searching news sources..."):
                articles = search_news(claim, language, num_articles)
            if not articles:
                st.warning("No related articles found online.")
                st.info("Predicting on claim text alone — less reliable.")
                prediction, confidence = predict(claim)
                show_verdict(prediction, confidence)
            else:
                combined = claim
                for a in articles:
                    combined += " " + (a.get("title","")       or "")
                    combined += " " + (a.get("content","")     or "")
                    combined += " " + (a.get("description","") or "")
                prediction, confidence = predict(combined)
                st.divider()
                st.subheader("Your claim:")
                st.info(f'"{claim}"')
                show_verdict(prediction, confidence)
                if prediction == 0 and confidence > 70:
                    st.warning("This claim has characteristics of misinformation. Please verify before sharing.")
                elif prediction == 1 and confidence > 70:
                    st.success("Multiple news sources support this claim.")
                else:
                    st.info("Low confidence — this topic needs more verification.")
                show_sources(articles)
            show_factcheckers()

with tab2:
    st.subheader("Paste a full article")
    st.write("Copy any news article text and paste it below.")
    article_text = st.text_area(
        "Paste article here",
        height=300,
        key="tab2_input",
        placeholder="Paste the full article text here..."
    )
    if st.button("Analyse Article", type="primary", key="tab2_btn"):
        if article_text.strip() == "":
            st.warning("Please paste an article first.")
        else:
            prediction, confidence = predict(article_text)
            show_verdict(prediction, confidence)
            show_factcheckers()

with tab3:
    st.subheader("Browse and analyse live news")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        country = st.selectbox(
            "Country",
            ["in", "us", "gb"],
            format_func=lambda x: {"in":"India","us":"USA","gb":"UK"}[x],
            key="tab3_country"
        )
    with col_b:
        category = st.selectbox(
            "Category",
            ["general","technology","science","health","business","sports"],
            key="tab3_cat"
        )
    with col_c:
        num_live = st.slider("Articles", 5, 15, 8, key="tab3_num")
    if st.button("Fetch Live News", type="primary", key="tab3_btn"):
        with st.spinner("Fetching latest news..."):
            try:
                headlines = newsapi.get_top_headlines(
                    language="en",
                    country=country,
                    category=category,
                    page_size=num_live
                )
                live_articles = headlines.get("articles", [])
            except Exception as e:
                st.error(f"Could not fetch news: {e}")
                live_articles = []
        if not live_articles:
            st.warning("No articles found. Try different filters.")
        else:
            st.success(f"Fetched {len(live_articles)} articles!")
            real_count, fake_count, results_list = 0, 0, []
            for article in live_articles:
                title   = article.get("title","")       or ""
                content = article.get("content","")     or ""
                desc    = article.get("description","") or ""
                source  = article["source"]["name"]
                url     = article.get("url","#")
                full    = title + " " + content + " " + desc
                if full.strip() == "":
                    continue
                pred, conf = predict(full)
                if pred == 1: real_count += 1
                else:         fake_count += 1
                results_list.append({
                    "title":title,"source":source,
                    "url":url,"desc":desc,
                    "pred":pred,"conf":conf
                })
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("Total",        len(results_list))
            with m2: st.metric("Appears Real", real_count)
            with m3: st.metric("Appears Fake", fake_count)
            st.divider()
            for r in results_list:
                icon = "✅" if r["pred"] == 1 else "🚨"
                with st.expander(f"{icon} {r['source']} — {r['title'][:65]}..."):
                    col_x, col_y = st.columns([3, 1])
                    with col_x:
                        st.write(r["desc"])
                        st.link_button("Read article", r["url"])
                    with col_y:
                        if r["pred"] == 1: st.success("REAL")
                        else:              st.error("FAKE")
                        st.progress(int(r["conf"]))
                        st.caption(f"{r['conf']}%")

with tab4:
    st.subheader("Paste any article URL")
    st.write("Got a link someone shared? Paste it and we will extract and analyse it.")
    url_input = st.text_input(
        "Article URL",
        placeholder="https://www.ndtv.com/india-news/...",
        key="tab4_url"
    )
    if st.button("Fetch and Analyse", type="primary", key="tab4_btn"):
        if url_input.strip() == "":
            st.warning("Please paste a URL first.")
        else:
            with st.spinner("Extracting article from URL..."):
                try:
                    article = Article(url_input)
                    article.download()
                    article.parse()
                    extracted = article.title + " " + article.text
                    if len(extracted.strip()) < 50:
                        st.error("Could not extract article text from this URL.")
                        st.info("Try copying the article text and using the Paste Article tab instead.")
                    else:
                        st.subheader("Extracted article:")
                        with st.expander("See extracted text"):
                            st.write(extracted[:1000] + "...")
                        prediction, confidence = predict(extracted)
                        show_verdict(prediction, confidence)
                        show_factcheckers()
                except Exception as e:
                    st.error(f"Could not fetch this URL: {e}")
                    st.info("""
                    Some websites block automated access. Try:
                    - Copy article text manually → Paste Article tab
                    - Try a different URL
                    - Use Tab 1 to check the headline claim
                    """)
