import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv("layoffs.csv", parse_dates=['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%B')
df['percentage_laid_off'] = (df['total_laid_off'] / df.groupby('company')['total_laid_off'].transform('sum')) * 100

st.set_page_config(page_title="Tech Layoffs Dashboard", layout="wide")
st.title("\U0001F4C9 Tech Layoffs Interactive Dashboard (2022–2025)")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_countries = st.sidebar.multiselect("Select Country", df['country'].dropna().unique(), default=['United States'])
selected_industries = st.sidebar.multiselect("Select Industry", df['industry'].dropna().unique())

filtered_df = df[df['country'].isin(selected_countries)]
if selected_industries:
    filtered_df = filtered_df[filtered_df['industry'].isin(selected_industries)]

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "\U0001F4C8 Trends Over Time",
    "\U0001F3E2 Company & Industry Insights",
    "\U0001F30D Country-Level Patterns",
    "\U0001F4CA Statistical Distributions",
    "\U0001F4B0 Funding vs Layoffs",
])

# --- Tab 1: Time-Based Trends ---
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("\U0001F4C8 Monthly Total Layoffs Over Time")
        monthly = filtered_df.groupby(pd.Grouper(key='date', freq='M'))['total_laid_off'].sum()
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        monthly.plot(ax=ax1, color='teal')
        ax1.set_ylabel("Total Laid Off")
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.subheader("\U0001F5D3️ Heatmap of Layoffs by Year & Month")
        df['month_num'] = df['date'].dt.month
        pivot = df.pivot_table(index='year', columns='month_num', values='total_laid_off', aggfunc='sum')
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax2, annot_kws={"size": 7})
        st.pyplot(fig2, use_container_width=True)

# --- Tab 2: Company & Industry ---
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("\U0001F3E2 Top 10 Companies by Total Layoffs")
        top_companies = filtered_df['company'].value_counts().head(10)
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        top_companies.plot(kind='bar', color='salmon', ax=ax3)
        ax3.set_ylabel("Layoffs")
        st.pyplot(fig3, use_container_width=True)

    with col2:
        st.subheader("\U0001F3ED Average Layoffs by Industry")
        avg_industry = df.groupby('industry')['total_laid_off'].mean().sort_values(ascending=False).head(10)
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        avg_industry.plot(kind='bar', color='orchid', ax=ax4)
        st.pyplot(fig4, use_container_width=True)

# --- Tab 3: Country-Level Patterns ---
with tab3:
    st.subheader("\U0001F4CA Layoff % Distribution by Country (Top 10)")
    top_countries = df['country'].value_counts().head(10).index
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df[df['country'].isin(top_countries)],
                x='country', y='percentage_laid_off',
                palette='Set2', ax=ax5)
    plt.xticks(rotation=45)
    st.pyplot(fig5, use_container_width=True)

# --- Tab 4: Statistical Distributions ---
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("\U0001F4CC Distribution of Layoff Percentages")
        fig6, ax6 = plt.subplots(figsize=(6, 4))
        sns.histplot(df['percentage_laid_off'].dropna(), bins=20, kde=True, ax=ax6, color='steelblue')
        st.pyplot(fig6, use_container_width=True)

    with col2:
        st.subheader("\U0001F9E0 Correlation Between Numerical Fields")
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        sns.heatmap(df[['total_laid_off', 'percentage_laid_off']].dropna().corr(), annot=True, cmap='coolwarm', ax=ax7)
        st.pyplot(fig7, use_container_width=True)


# --- Tab 5: Company Stage Analysis ---
with tab5:
    st.subheader("\U0001F4B0 Total Layoffs by Company Stage")
    if 'stage' in df.columns:
        stage_layoffs = df.groupby('stage')['total_laid_off'].sum().sort_values()
        fig9, ax9 = plt.subplots(figsize=(6, 4))
        stage_layoffs.plot(kind='barh', ax=ax9, color='purple')
        st.pyplot(fig9, use_container_width=True)
    else:
        st.info("No 'stage' column found in dataset.")

# Footer
st.markdown("---")
st.markdown("Created by Ujwal | Data Source: Tech Layoffs Dataset (2022–2025)")
