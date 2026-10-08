import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# ============================================================
# 🌷 NOVA — LIGHT MONTHLY EXPENSE TRACKER
# ============================================================

st.set_page_config(
    page_title="NOVA Monthly Expense Tracker",
    page_icon="🌷",
    layout="wide"
)

DATA_FILE = "nova_monthly_expenses.json"

# -----------------------------
# LIGHT CREATIVE STYLE
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #f7f9fc;
        color: #263238;
    }

    [data-testid="stSidebar"] {
        background: #eef4f8;
        border-right: 1px solid #d9e3ea;
    }

    [data-testid="stSidebar"] * {
        color: #334155;
    }

    .hero {
        background: linear-gradient(135deg, #e8f5f2, #eef3fb, #f9edf5);
        border: 1px solid #dce7ed;
        border-radius: 22px;
        padding: 28px 32px;
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: #334155;
        margin: 0;
    }

    .hero-sub {
        color: #718096;
        font-size: 15px;
        margin-top: 5px;
    }

    .metric {
        background: white;
        border: 1px solid #e1e8ee;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(80, 100, 120, .06);
    }

    .metric-label {
        color: #7b8794;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-value {
        color: #334155;
        font-size: 27px;
        font-weight: 800;
        margin-top: 6px;
    }

    .section {
        color: #475569;
        font-size: 22px;
        font-weight: 800;
        margin: 28px 0 12px 0;
    }

    .category-box {
        background: white;
        border: 1px solid #e4ebf0;
        border-radius: 16px;
        padding: 13px 16px;
        margin-bottom: 8px;
    }

    .small-note {
        color: #8793a1;
        font-size: 13px;
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e1e8ee;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 4px 18px rgba(70, 90, 110, .05);
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #e1e8ee;
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

CATEGORIES = {
    "🛒 Groceries": "Groceries",
    "🛍️ Shopping": "Shopping",
    "⚡ Electricity": "Electricity",
    "💧 Water": "Water",
    "🏠 Rent": "Rent",
    "📱 Mobile / Internet": "Mobile / Internet",
    "🍚 Food": "Food",
    "🚌 Transport": "Transport",
    "🏥 Medical": "Medical",
    "🎓 Education": "Education",
    "💳 EMI / Loan": "EMI / Loan",
    "🎬 Entertainment": "Entertainment",
    "🧹 Household": "Household",
    "📦 Other": "Other"
}

PAYMENT_MODES = [
    "Cash",
    "UPI",
    "Debit Card",
    "Credit Card",
    "Bank Transfer"
]

PEOPLE = [
    "Me",
    "Father",
    "Mother",
    "Brother",
    "Sister",
    "Partner",
    "Family",
    "Other"
]


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return pd.DataFrame(json.load(f))
        except Exception:
            pass

    return pd.DataFrame(columns=[
        "Month", "Year", "Category", "Amount",
        "Payment Mode", "Used By", "Notes"
    ])


def save_data(df):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=4)


if "expenses" not in st.session_state:
    st.session_state.expenses = load_data()

df = st.session_state.expenses.copy()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🌷 NOVA")
    st.caption("MONTHLY MONEY MANAGER")
    st.divider()

    month = st.selectbox(
        "📅 Month",
        range(1, 13),
        index=date.today().month - 1,
        format_func=lambda x: date(2000, x, 1).strftime("%B")
    )

    year = st.number_input(
        "📆 Year",
        min_value=2020,
        max_value=2100,
        value=date.today().year,
        step=1
    )

    budget = st.number_input(
        "💰 Monthly Budget / Income",
        min_value=0.0,
        value=50000.0,
        step=500.0
    )

    st.divider()

    st.markdown("### 💡 How it works")
    st.caption("1. Choose the month")
    st.caption("2. Enter every category amount")
    st.caption("3. Select Cash / UPI / Card")
    st.caption("4. Select who spent it")
    st.caption("5. View the final table")

    st.divider()
    st.caption("Simple • Clear • Organized 🌿")


month_name = date(int(year), int(month), 1).strftime("%B %Y")


# ============================================================
# HEADER
# ============================================================

st.markdown(f"""
<div class="hero">
    <div class="hero-title">🌷 Monthly Expense Planner</div>
    <div class="hero-sub">
        Enter your expenses for <b>{month_name}</b> and get an organized
        monthly spending report.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CATEGORY-BY-CATEGORY INPUT
# ============================================================

st.markdown(
    '<div class="section">📝 Enter This Month\'s Expenses</div>',
    unsafe_allow_html=True
)

st.info(
    "You can enter an amount for any category. Leave unused categories as ₹0."
)

with st.form("monthly_expense_form"):

    entered = {}

    for category_display, category_name in CATEGORIES.items():

        st.markdown(
            f'<div class="category-box"><b>{category_display}</b></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns([1.25, 1.25, 1.25, 2])

        with c1:
            amount = st.number_input(
                f"{category_name} amount (₹)",
                min_value=0.0,
                step=100.0,
                key=f"amount_{category_name}"
            )

        with c2:
            payment = st.selectbox(
                "Payment",
                PAYMENT_MODES,
                key=f"payment_{category_name}"
            )

        with c3:
            person = st.selectbox(
                "Used / Paid by",
                PEOPLE,
                key=f"person_{category_name}"
            )

        with c4:
            notes = st.text_input(
                "Notes",
                placeholder=f"Example: {category_name} bill",
                key=f"notes_{category_name}"
            )

        entered[category_name] = {
            "amount": amount,
            "payment": payment,
            "person": person,
            "notes": notes
        }

    st.divider()

    save_month = st.form_submit_button(
        "💾 SAVE MONTHLY EXPENSES",
        use_container_width=True
    )

    if save_month:

        # Remove previous saved entries for this month/year
        existing = st.session_state.expenses

        if not existing.empty:
            existing = existing[
                ~(
                    (existing["Month"] == month) &
                    (existing["Year"] == year)
                )
            ]

        rows = []

        for category_name, values in entered.items():
            if values["amount"] > 0:
                rows.append({
                    "Month": month,
                    "Year": year,
                    "Category": category_name,
                    "Amount": float(values["amount"]),
                    "Payment Mode": values["payment"],
                    "Used By": values["person"],
                    "Notes": values["notes"]
                })

        if rows:
            new_df = pd.DataFrame(rows)
            st.session_state.expenses = pd.concat(
                [existing, new_df],
                ignore_index=True
            )

            save_data(st.session_state.expenses)

            st.success(
                f"🎉 {month_name} expenses saved successfully!"
            )
            st.rerun()
        else:
            st.warning("Please enter at least one expense amount.")


# ============================================================
# MONTHLY RESULTS
# ============================================================

df = st.session_state.expenses.copy()

if not df.empty:
    monthly = df[
        (df["Month"] == month) &
        (df["Year"] == year)
    ].copy()
else:
    monthly = pd.DataFrame()


total_spent = float(monthly["Amount"].sum()) if not monthly.empty else 0
remaining = budget - total_spent
transaction_count = len(monthly)


# ============================================================
# SUMMARY
# ============================================================

st.markdown(
    '<div class="section">📊 Monthly Result</div>',
    unsafe_allow_html=True
)

a, b, c, d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Total Spent</div>
        <div class="metric-value">₹{total_spent:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Monthly Budget</div>
        <div class="metric-value">₹{budget:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Amount Remaining</div>
        <div class="metric-value">₹{remaining:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Categories Used</div>
        <div class="metric-value">{transaction_count}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FINAL TABLE
# ============================================================

st.markdown(
    '<div class="section">📋 Complete Monthly Expense Table</div>',
    unsafe_allow_html=True
)

if not monthly.empty:

    result = monthly.copy()

    result.insert(
        0,
        "S.No",
        range(1, len(result) + 1)
    )

    result["Amount"] = result["Amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    st.dataframe(
        result[
            [
                "S.No",
                "Category",
                "Amount",
                "Payment Mode",
                "Used By",
                "Notes"
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "S.No": st.column_config.NumberColumn(
                "S.No",
                width="small"
            ),
            "Category": st.column_config.TextColumn(
                "Category",
                width="medium"
            ),
            "Amount": st.column_config.TextColumn(
                "Amount",
                width="medium"
            ),
            "Payment Mode": st.column_config.TextColumn(
                "Payment",
                width="medium"
            ),
            "Used By": st.column_config.TextColumn(
                "Who Used / Paid",
                width="medium"
            ),
            "Notes": st.column_config.TextColumn(
                "Notes",
                width="large"
            )
        }
    )

    # Total row
    st.markdown(f"""
    <div class="category-box" style="margin-top:15px;">
        <b>💰 GRAND TOTAL</b>
        <span style="float:right; font-size:20px;">
            <b>₹{total_spent:,.2f}</b>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # PAYMENT SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section">💳 Payment Summary</div>',
        unsafe_allow_html=True
    )

    payment_summary = (
        monthly.groupby("Payment Mode")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    payment_summary["Amount"] = payment_summary["Amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    st.dataframe(
        payment_summary,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # PERSON SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section">👨‍👩‍👧‍👦 Person-wise Summary</div>',
        unsafe_allow_html=True
    )

    person_summary = (
        monthly.groupby("Used By")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    person_summary["Amount"] = person_summary["Amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    st.dataframe(
        person_summary,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        f"No expenses have been saved for {month_name} yet. "
        "Enter the category amounts above and click SAVE. 🌱"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    "<center>🌷 NOVA • Plan your money • Track your spending • Save better</center>",
    unsafe_allow_html=True
)
