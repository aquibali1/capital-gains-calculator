
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Capital Gains Calculator", layout="centered")

# Dark mode toggle
dark_mode = st.toggle("🌗 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #121212; color: #e0e0e0; }
        .stTextInput input, .stDateInput input { background-color: #1e1e1e; color: white; }
        .stButton>button { background-color: #007acc; color: white; }
        </style>
    """, unsafe_allow_html=True)

st.title("📊 Capital Gains Calculator (India)")
st.caption("Zerodha/Kite Compatible • Pie/Bar Chart • Mobile-Friendly")

with st.form("capital_form"):
    buy_price = st.number_input("Buy Price per Share (₹)", min_value=0.0, step=0.1)
    sell_price = st.number_input("Sell Price per Share (₹)", min_value=0.0, step=0.1)
    quantity_bought = st.number_input("Total Shares Bought", min_value=1, step=1)
    quantity_sold = st.number_input("Shares Sold", min_value=1, max_value=int(quantity_bought), step=1)
    brokerage = st.number_input("Brokerage (₹)", value=0.0, step=1.0)
    buy_date = st.date_input("Buy Date")
    sell_date = st.date_input("Sell Date")
    chart_type = st.radio("Chart Type", ["Bar Chart", "Pie Chart"], horizontal=True)
    submitted = st.form_submit_button("💡 Calculate")

if submitted:
    try:
        holding_days = (sell_date - buy_date).days
        gross_gain = (sell_price - buy_price) * quantity_sold
        stt = 0.001 * (sell_price * quantity_sold)
        exch_fee = 0.0000325 * (sell_price * quantity_sold)
        sebi_fee = 0.000001 * (sell_price * quantity_sold)
        other_charges = stt + exch_fee + sebi_fee
        total_gain = gross_gain - brokerage - other_charges

        if holding_days < 365:
            tax = total_gain * 0.15
            gain_type = "Short-Term Capital Gain (STCG)"
        else:
            exempt_limit = 100000
            taxable_gain = max(0, total_gain - exempt_limit)
            tax = taxable_gain * 0.10
            gain_type = "Long-Term Capital Gain (LTCG)"

        net_gain = total_gain - tax

        st.success(f"✅ {gain_type}")
        st.markdown(f"""
        - 📦 Bought: **{int(quantity_bought)} shares**
        - 📤 Sold: **{int(quantity_sold)} shares**
        - 📆 Holding Period: **{holding_days} days**
        - 💰 Gross Gain: ₹{gross_gain:,.2f}
        - 🔧 Brokerage: ₹{brokerage:.2f}
        - 📑 Other Charges (STT + Exchange + SEBI): ₹{other_charges:.2f}
        - ➡️ Total Gain After Charges: ₹{total_gain:,.2f}
        - 📉 Tax: ₹{tax:,.2f}
        - ✅ **Net Profit After Tax: ₹{net_gain:,.2f}**
        """)

        labels = ['Net Profit', 'Tax', 'Brokerage', 'Other Charges']
        values = [net_gain, tax, brokerage, other_charges]
        colors = ['#4caf50', '#f44336', '#ff9800', '#2196f3']

        fig, ax = plt.subplots()
        if chart_type == "Pie Chart":
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax.axis('equal')
            ax.set_title('Gains Breakdown')
        else:
            bars = ax.bar(labels, values, color=colors)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01*yval, f'₹{yval:,.0f}', ha='center', va='bottom')
            ax.set_ylabel('Amount (₹)')
            ax.set_title('Gains vs Tax vs Charges')
            ax.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)

    except Exception as e:
        st.error("Error calculating gain. Please check your input.")

st.markdown("---")
with st.expander("🧾 How to Use with Zerodha"):
    st.info("""
1. Open [Zerodha Console](https://console.zerodha.com/)
2. Go to *Reports → Tax P&L*
3. Download your Tax Report and input values manually here.
✅ Use this tool to preview your tax impact before filing.
""")
