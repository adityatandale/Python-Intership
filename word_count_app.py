"""
Word Count & Frequency Analyzer
-------------------------------
A simple, interactive Streamlit web app. Paste text or upload a .txt file
and instantly see word/line/character counts plus a word frequency chart.

Run with:
    pip install -r requirements.txt
    streamlit run word_count_app.py
"""

import re
from collections import Counter

import pandas as pd
import streamlit as st

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "so", "of", "at",
    "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up",
    "down", "in", "out", "on", "off", "over", "under", "again", "further",
    "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now", "is", "was", "are",
    "were", "be", "been", "being", "have", "has", "had", "having", "do",
    "does", "did", "doing", "it", "its", "it's", "this", "that", "these",
    "those", "i", "you", "he", "she", "we", "they", "them", "his", "her",
    "our", "your", "their", "as", "which", "who", "whom", "what", "my",
    "me", "him", "us",
}

WORD_RE = re.compile(r"[A-Za-z']+")


def analyze_text(text: str, exclude_stopwords: bool, top_n: int) -> dict:
    lines = text.splitlines()
    line_count = len(lines) if text else 0
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))

    raw_words = WORD_RE.findall(text)
    words = [w.strip("'").lower() for w in raw_words if w.strip("'")]
    word_count = len(words)
    unique_words = len(set(words))
    avg_word_length = round(sum(len(w) for w in words) / word_count, 2) if word_count else 0
    longest_word = max(words, key=len) if words else ""

    counted = [w for w in words if (not exclude_stopwords) or (w not in STOP_WORDS)]
    top_words = Counter(counted).most_common(top_n)

    return {
        "word_count": word_count,
        "line_count": line_count,
        "char_count": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "unique_words": unique_words,
        "avg_word_length": avg_word_length,
        "longest_word": longest_word,
        "top_words": top_words,
    }


# ---------------- Page setup ----------------

st.set_page_config(page_title="Word Count Analyzer", page_icon="📝", layout="centered")

st.title("📝 Word Count & Frequency Analyzer")
st.caption("Paste text or upload a .txt file. Results update instantly as you type.")

# ---------------- Input ----------------

tab_paste, tab_upload = st.tabs(["✏️ Paste text", "📁 Upload file"])

text = ""

with tab_paste:
    text = st.text_area(
        "Your text",
        height=220,
        placeholder="Start typing or paste a passage here…",
        label_visibility="collapsed",
    )

with tab_upload:
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8", errors="replace")
        st.text_area("Preview", value=text, height=180, disabled=True)

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    exclude_stopwords = st.checkbox(
        "Exclude common words (the, and, of, ...)", value=True
    )
with col2:
    top_n = st.slider("Top N words", min_value=5, max_value=25, value=10)

# ---------------- Results ----------------

if text and text.strip():
    result = analyze_text(text, exclude_stopwords, top_n)

    st.subheader("Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Words", f"{result['word_count']:,}")
    m2.metric("Lines", f"{result['line_count']:,}")
    m3.metric("Characters", f"{result['char_count']:,}")
    m4.metric("Unique words", f"{result['unique_words']:,}")

    d1, d2, d3 = st.columns(3)
    d1.metric("Characters (no spaces)", f"{result['char_count_no_spaces']:,}")
    d2.metric("Avg. word length", f"{result['avg_word_length']}")
    d3.metric("Longest word", result["longest_word"] or "—")

    st.subheader("Most frequent words")

    if result["top_words"]:
        df = pd.DataFrame(result["top_words"], columns=["Word", "Count"])
        c1, c2 = st.columns([1, 1])
        with c1:
            st.dataframe(df, hide_index=True, use_container_width=True)
        with c2:
            st.bar_chart(df.set_index("Word"))
    else:
        st.info("No words found yet.")

else:
    st.info("Add some text above (or upload a .txt file) to see the analysis.")
