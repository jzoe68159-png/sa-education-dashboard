import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="South Africa Education Dashboard", layout="wide")
st.title("📊 South Africa Education Trends (1960–2025)")

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('education_final.csv', sep=';')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
year_min = int(df['year'].min())
year_max = int(df['year'].max())
selected_years = st.sidebar.slider(
    "Select Year Range",
    year_min, year_max,
    (year_min, year_max)
)

# Filter data
df_filtered = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 No Education (Age 15-19)")
    fig, ax = plt.subplots()
    ax.plot(df_filtered['year'], df_filtered['BAR.NOED.1519.ZS'], marker='o', label='Total')
    ax.plot(df_filtered['year'], df_filtered['BAR.NOED.1519.FE.ZS'], marker='s', label='Female')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("📈 Completed Primary (Age 15-19)")
    fig, ax = plt.subplots()
    ax.plot(df_filtered['year'], df_filtered['BAR.PRM.CMPT.1519.ZS'], marker='o', label='Total')
    ax.plot(df_filtered['year'], df_filtered['BAR.PRM.CMPT.1519.FE.ZS'], marker='s', label='Female')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.subheader("🎓 Completed Secondary (Age 20-24)")
    fig, ax = plt.subplots()
    ax.plot(df_filtered['year'], df_filtered['BAR.SEC.CMPT.2024.ZS'], marker='o', label='Total')
    ax.plot(df_filtered['year'], df_filtered['BAR.SEC.CMPT.2024.FE.ZS'], marker='s', label='Female')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("🏛️ Completed Tertiary (Age 25+)")
    fig, ax = plt.subplots()
    ax.plot(df_filtered['year'], df_filtered['BAR.TER.CMPT.25UP.ZS'], marker='o', label='Total')
    ax.plot(df_filtered['year'], df_filtered['BAR.TER.CMPT.25UP.FE.ZS'], marker='s', label='Female')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Gender Parity Index section
st.header("⚖️ Gender Parity Index (GPI)")

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
axes = axes.flatten()

gpi_cols = ['GPI_NOED_1519', 'GPI_PRM_1519', 'GPI_SEC_2024', 'GPI_TER_25UP']
titles = ['No Education (15-19)', 'Primary (15-19)', 'Secondary (20-24)', 'Tertiary (25+)']

for i, col in enumerate(gpi_cols):
    # Plot only where data exists
    plot_df = df_filtered[df_filtered[col].notna()]
    axes[i].plot(plot_df['year'], plot_df[col], marker='o', color='purple')
    axes[i].axhline(y=1.0, color='red', linestyle='--', alpha=0.7)
    axes[i].set_title(titles[i])
    axes[i].set_xlabel('Year')
    axes[i].set_ylabel('GPI (Female/Total)')
    axes[i].grid(True)

plt.tight_layout()
st.pyplot(fig)

# (Optional) raw data display
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(df_filtered)
