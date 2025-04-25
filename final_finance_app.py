
import streamlit as st
import numpy as np
import yfinance as yf
import requests

st.set_page_config(page_title="Finance App", page_icon=":bar_chart:", layout="wide")

# Custom colored header
st.markdown("<h1 style='text-align: center; color: #00008B;'>📊 Financial Analysis </h1>", unsafe_allow_html=True)

st.markdown("---")

# Live USD to INR exchange rate fetching
def get_usd_to_inr():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data['rates']['INR']
    except Exception:
        return 83  # fallback static value

usd_to_inr = get_usd_to_inr()

currency = st.sidebar.radio("Select Currency", ["USD", "INR"])

def fx(value):
    return value if currency == "USD" else value * usd_to_inr

def format_currency(value):
    symbol = "$" if currency == "USD" else "₹"
    return f"{symbol}{value:,.2f}"

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page =st.sidebar.selectbox("Navigation"
, ["🏠 Home",
    "🧮 Valuation",
    
    "📈 Beta & SML",
    "🔀 Put-Call Parity",
    "📉 Risk Aversion",
    "💰 Intrinsic Value",
    "📉 Inflation",
    "💵 Bonds",
    "📊 ROIC"
] )

# Pages logic
if page == "🏠 Home":
    st.header("🏠 Home")
    st.markdown("Explore various financial concepts with live data and valuation tools.")

elif page == "🧮 Valuation":
    st.header("🧮 Valuation Model (Indian Stocks Example)")
    st.caption("Made by Harsh Shah")
    ticker = st.text_input("Enter Indian stock ticker (example: RELIANCE.NS, INFY.NS, TCS.NS)", "RELIANCE.NS").upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        st.subheader(info.get("longName", "Company Info"))
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Current Price:** {format_currency(fx(info.get('currentPrice', 0)))}")
        st.write(f"**Market Cap:** {format_currency(fx(info.get('marketCap', 0)))}")

        st.markdown("### Valuation Assumptions")
        profit = st.number_input("Expected Annual Profit (in USD)", value=100.0)
        growth = st.number_input("Annual Growth Rate (%)", value=5.0)
        discount_rate = st.number_input("Discount Rate (%)", value=10.0)
        years = st.slider("Projection Period (Years)", 1, 10, 5)

        dcf = sum([
            (profit * ((1 + growth/100) ** t)) / ((1 + discount_rate/100) ** t)
            for t in range(1, years + 1)
        ])

        st.success(f"**Estimated Valuation:** {format_currency(fx(dcf))}")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

elif page == "📈 Beta & SML":
    st.header("📈 CAPM / SML")
    rf = st.number_input("Risk-Free Rate (%)", value=2.0)
    rm = st.number_input("Market Return (%)", value=8.0)
    beta = st.slider("Beta", 0.0, 2.0, 1.0)
    expected_return = rf + beta * (rm - rf)
    st.write(f"**Expected Return:** {expected_return:.2f}%")

elif page == "🔀 Put-Call Parity":
    st.header("🔀 Put-Call Parity")
    call = st.number_input("Call Price", value=10.0)
    strike = st.number_input("Strike Price", value=100.0)
    stock = st.number_input("Stock Price", value=95.0)
    rate = st.number_input("Interest Rate (%)", value=5.0)
    time = st.slider("Time to Maturity (Years)", 1, 10, 1)
    put = call + strike / (1 + rate/100) ** time - stock
    st.write(f"**Implied Put Price:** {format_currency(fx(put))}")

elif page == "📉 Risk Aversion":
    st.header("📉 Risk Aversion")
    expected_return = st.slider("Expected Return (%)", 0.0, 20.0, 10.0)
    risk = st.slider("Standard Deviation (%)", 0.0, 20.0, 5.0)
    aversion = st.slider("Risk Aversion Coefficient (A)", 1.0, 10.0, 3.0)
    utility = expected_return - 0.5 * aversion * (risk ** 2) / 100
    st.write(f"**Investor Utility:** {utility:.2f}")

elif page == "💰 Intrinsic Value":
    st.header("💰 Intrinsic Value Calculator")
    cash_flow = st.number_input("Initial Cash Flow", value=100.0)
    growth = st.number_input("Growth Rate (%)", value=5.0)
    discount = st.number_input("Discount Rate (%)", value=10.0)
    years = st.slider("Years", 1, 10, 5)
    value = sum([cash_flow * ((1 + growth/100) ** t) / ((1 + discount/100) ** t) for t in range(1, years + 1)])
    st.write(f"**Intrinsic Value:** {format_currency(fx(value))}")

elif page == "📉 Inflation":
    st.header("📉 Inflation Adjusted Return")
    nominal_return = st.number_input("Nominal Return (%)", value=10.0)
    inflation = st.number_input("Inflation Rate (%)", value=3.0)
    real_return = ((1 + nominal_return/100) / (1 + inflation/100)) - 1
    st.write(f"**Real Return:** {real_return*100:.2f}%")

elif page == "💵 Bonds":
    st.header("💵 Bond Pricing")
    face_value = st.number_input("Face Value", value=1000.0)
    coupon_rate = st.number_input("Coupon Rate (%)", value=5.0)
    years = st.slider("Years to Maturity", 1, 30, 10)
    discount_rate = st.number_input("Discount Rate (%)", value=4.0)
    coupon = face_value * (coupon_rate / 100)
    discount = discount_rate / 100
    price = sum([coupon / (1 + discount) ** t for t in range(1, years + 1)]) + face_value / (1 + discount) ** years
    st.write(f"**Bond Price:** {format_currency(fx(price))}")

elif page == "📊 ROIC":
    st.header("📊 Return on Invested Capital")
    nopat = st.number_input("NOPAT", value=100.0)
    invested_capital = st.number_input("Invested Capital", value=1000.0)
    roic = nopat / invested_capital * 100 if invested_capital else 0
    st.write(f"**ROIC:** {roic:.2f}%")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made by Harsh Shah</div>", unsafe_allow_html=True)
