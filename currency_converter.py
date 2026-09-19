"""
Currency Converter - Streamlit App
Task 5

Uses a live exchange rate API. Default: exchangerate-api.com (free, no API key,
good enough for a coursework project). If you have an Open Exchange Rates
app_id, enter it in the sidebar to use that instead.

Run with:
    pip install streamlit requests
    streamlit run currency_converter.py
"""

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600)  # cache for 1 hour so we don't hammer the API
def get_rates_free(base: str):
    """Free, no-key API. Returns dict of rates or None on failure."""
    url = f"https://open.er-api.com/v6/latest/{base}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "Unknown API error"))
    return data["rates"], data.get("time_last_update_utc", "")


@st.cache_data(ttl=3600)
def get_rates_oxr(base: str, app_id: str):
    """Open Exchange Rates API. Free tier only supports USD as base,
    so if base != USD we fetch USD-based rates and convert manually."""
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise ValueError(data.get("description", "OXR API error"))

    rates_usd_base = data["rates"]
    timestamp = datetime.utcfromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M UTC")

    if base == "USD":
        return rates_usd_base, timestamp

    if base not in rates_usd_base:
        raise ValueError(f"Base currency {base} not available on your OXR plan")

    base_rate = rates_usd_base[base]
    converted = {cur: (rate / base_rate) for cur, rate in rates_usd_base.items()}
    return converted, timestamp


def fetch_rates(base: str, oxr_key: str):
    if oxr_key:
        return get_rates_oxr(base, oxr_key)
    return get_rates_free(base)


# ---------------------------------------------------------------------------
# Sidebar - settings
# ---------------------------------------------------------------------------

st.sidebar.header("Settings")
oxr_key = st.sidebar.text_input(
    "Open Exchange Rates App ID (optional)",
    type="password",
    help="Leave blank to use the free open.er-api.com feed instead.",
)
st.sidebar.caption(
    "Get a free app_id at openexchangerates.org/signup if you want to use OXR."
)

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------

st.title("💱 Currency Converter")
st.write("Convert between currencies using live exchange rates.")

# We need a currency list before the user picks anything, so fetch USD-based
# rates first just to populate the dropdowns.
try:
    seed_rates, _ = fetch_rates("USD", oxr_key)
    currency_list = sorted(seed_rates.keys()) + ["USD"]
    currency_list = sorted(set(currency_list))
except requests.exceptions.RequestException:
    st.error("Could not reach the exchange rate service. Check your internet connection.")
    st.stop()
except ValueError as e:
    st.error(f"API error: {e}")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From", currency_list, index=currency_list.index("USD"))
with col2:
    default_to = "INR" if "INR" in currency_list else currency_list[0]
    to_currency = st.selectbox("To", currency_list, index=currency_list.index(default_to))

swap = st.button("🔄 Swap currencies")
if swap:
    from_currency, to_currency = to_currency, from_currency

amount_str = st.text_input("Amount", value="1")

# ---------------------------------------------------------------------------
# Validation + conversion
# ---------------------------------------------------------------------------

def parse_amount(value: str):
    try:
        amount = float(value)
    except ValueError:
        return None, "Enter a valid number (e.g. 100 or 99.50)."
    if amount < 0:
        return None, "Amount cannot be negative."
    if amount == 0:
        return None, "Amount must be greater than zero."
    return amount, None


amount, error = parse_amount(amount_str)

if error:
    st.warning(error)
else:
    try:
        rates, last_updated = fetch_rates(from_currency, oxr_key)
        if to_currency not in rates:
            st.error(f"No rate available for {to_currency}.")
        else:
            rate = rates[to_currency]
            result = amount * rate

            st.markdown("---")
            st.metric(
                label=f"{amount:,.2f} {from_currency} =",
                value=f"{result:,.2f} {to_currency}",
            )
            st.caption(f"1 {from_currency} = {rate:.6f} {to_currency}")
            if last_updated:
                st.caption(f"Rates last updated: {last_updated}")
    except requests.exceptions.RequestException:
        st.error("Network error while fetching rates. Try again.")
    except ValueError as e:
        st.error(f"API error: {e}")

st.markdown("---")
st.caption(
    "Data source: Open Exchange Rates (if key provided) or open.er-api.com (free fallback)."
)
