"""
Basic Web Scraper - Streamlit App
Task 4

Scrapes headlines (or any text) from a given URL using Requests + BeautifulSoup.
Lets the user either pick a common tag (h1/h2/h3/a, etc.) or supply a custom
CSS selector, since different sites structure their HTML differently.

Run with:
    pip install streamlit requests beautifulsoup4
    streamlit run web_scraper.py
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

st.set_page_config(page_title="Web Scraper", page_icon="🕸️", layout="centered")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


@st.cache_data(ttl=600, show_spinner=False)
def fetch_html(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text


def extract_elements(html: str, selector: str):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)
    results = []
    for el in elements:
        text = el.get_text(strip=True)
        if not text:
            continue
        link = el.get("href") if el.name == "a" else None
        if link is None:
            a_tag = el.find("a")
            link = a_tag.get("href") if a_tag else None
        results.append({"text": text, "link": link})
    return results


def dedupe(items):
    seen = set()
    unique = []
    for item in items:
        if item["text"] not in seen:
            seen.add(item["text"])
            unique.append(item)
    return unique


# ---------------------------------------------------------------------------
# Sidebar - guidance
# ---------------------------------------------------------------------------

st.sidebar.header("How this works")
st.sidebar.write(
    "1. Enter a URL\n"
    "2. Pick a tag/selector that matches the data you want\n"
    "3. Click Scrape\n\n"
    "Different sites use different HTML structures, so if the default "
    "tag (h1, h2, h3) returns nothing, try a custom CSS selector "
    "(e.g. `.headline`, `article h3 a`, `#main-content li`)."
)
st.sidebar.info(
    "Only scrape sites that allow it. Check the site's robots.txt and "
    "terms of service before scraping. This tool is for educational use."
)

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------

st.title("🕸️ Basic Web Scraper")
st.write("Extract headlines or other text content from any public webpage.")

url = st.text_input("Website URL", placeholder="https://example.com/news")

col1, col2 = st.columns([2, 3])
with col1:
    mode = st.radio("Selector mode", ["Common tag", "Custom CSS selector"])
with col2:
    if mode == "Common tag":
        tag_choice = st.selectbox(
            "Tag to extract",
            ["h1", "h2", "h3", "h2 a", "h3 a", "a"],
            index=2,
            help="Most news sites put headlines in h1/h2/h3 tags, "
                 "often wrapped in a link (a).",
        )
        selector = tag_choice
    else:
        selector = st.text_input(
            "CSS selector",
            placeholder="e.g. .headline, article h3, .post-title a",
        )

max_items = st.slider("Max results to show", 5, 100, 25)
scrape_clicked = st.button("🔍 Scrape", type="primary")

# ---------------------------------------------------------------------------
# Scrape + display
# ---------------------------------------------------------------------------

if scrape_clicked:
    if not url:
        st.warning("Enter a URL first.")
    elif not is_valid_url(url):
        st.warning("That doesn't look like a valid URL. Include http:// or https://")
    elif not selector:
        st.warning("Enter or select a tag/selector to scrape.")
    else:
        with st.spinner("Fetching page..."):
            try:
                html = fetch_html(url)
            except requests.exceptions.Timeout:
                st.error("The request timed out. The site may be slow or unreachable.")
                st.stop()
            except requests.exceptions.ConnectionError:
                st.error("Could not connect. Check the URL and your internet connection.")
                st.stop()
            except requests.exceptions.HTTPError as e:
                st.error(f"The site returned an error: {e}")
                st.stop()
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
                st.stop()

        try:
            items = extract_elements(html, selector)
        except Exception as e:
            st.error(
                f"Couldn't parse that selector ('{selector}'). "
                f"Double-check the CSS syntax. Details: {e}"
            )
            st.stop()

        items = dedupe(items)[:max_items]

        if not items:
            st.warning(
                "No matching elements found. The site may use a different "
                "structure — try 'Custom CSS selector' and inspect the "
                "page's HTML (right-click → Inspect) to find the right tag/class."
            )
        else:
            st.success(f"Found {len(items)} item(s).")
            df = pd.DataFrame(items)
            df.index = df.index + 1

            for i, row in df.iterrows():
                if row["link"]:
                    href = row["link"]
                    if href.startswith("/"):
                        parsed = urlparse(url)
                        href = f"{parsed.scheme}://{parsed.netloc}{href}"
                    st.markdown(f"**{i}.** [{row['text']}]({href})")
                else:
                    st.markdown(f"**{i}.** {row['text']}")

            st.markdown("---")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download as CSV", data=csv, file_name="scraped_data.csv", mime="text/csv"
            )
