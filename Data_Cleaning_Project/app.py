import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    page_icon="🧹",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: white;
}

div[data-testid="metric-container"] {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #334155;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🧹 Data Cleaning & Reporting Automation")
st.markdown("### Automate Data Cleaning and Report Generation")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("sample_data.csv")

# ---------------- ORIGINAL DATA ----------------
st.subheader("📋 Original Dataset")

st.dataframe(df, use_container_width=True)

# ---------------- DATA CLEANING ----------------

# Count missing values
missing_values = df.isnull().sum().sum()

# Count duplicate rows
duplicate_rows = df.duplicated().sum()

# Remove duplicates
df_cleaned = df.drop_duplicates()

# Fill missing values
df_cleaned["Age"] = df_cleaned["Age"].fillna(df_cleaned["Age"].mean())
df_cleaned["Department"] = df_cleaned["Department"].fillna("Unknown")
df_cleaned["Salary"] = df_cleaned["Salary"].fillna(df_cleaned["Salary"].mean())

# ---------------- KPI SECTION ----------------
st.subheader("📌 Data Cleaning Summary")

col1, col2, col3 = st.columns(3)

col1.metric("⚠ Missing Values", missing_values)
col2.metric("🔁 Duplicate Rows", duplicate_rows)
col3.metric("✅ Cleaned Rows", len(df_cleaned))

st.markdown("---")

# ---------------- CLEANED DATA ----------------
st.subheader("🧼 Cleaned Dataset")

st.dataframe(df_cleaned, use_container_width=True)

# ---------------- SALARY CHART ----------------
st.subheader("📊 Salary Distribution")

fig1 = px.bar(
    df_cleaned,
    x="Name",
    y="Salary",
    color="Department",
    text_auto=True,
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- AGE CHART ----------------
st.subheader("📈 Age Distribution")

fig2 = px.histogram(
    df_cleaned,
    x="Age",
    color="Department",
    nbins=10,
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- SUMMARY REPORT ----------------
st.subheader("📑 Automated Report")

st.success(f"""
Total Rows in Original Data: {len(df)}

Duplicate Rows Removed: {duplicate_rows}

Missing Values Handled: {missing_values}

Final Clean Dataset Rows: {len(df_cleaned)}
""")

# ---------------- DOWNLOAD BUTTON ----------------
csv = df_cleaned.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Cleaned Data",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)

