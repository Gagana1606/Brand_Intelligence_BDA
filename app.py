
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Brand Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_brand_reviews.csv")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Review_Date"] = pd.to_datetime(df["Review_Date"], errors="coerce")
    return df.dropna(subset=["Review", "Rating"])

df = load_data()

st.title("AI-Based Brand Intelligence and Consumer Perception Analytics")
st.caption("Big Data Analytics | Fashion Shopping App Customer Experience")

st.sidebar.header("Dashboard Filters")

brands = sorted(df["Brand"].dropna().unique())
selected_brands = st.sidebar.multiselect(
    "Select brands",
    brands,
    default=brands
)

sentiments = sorted(df["Predicted_Sentiment"].dropna().unique())
selected_sentiments = st.sidebar.multiselect(
    "Select sentiment",
    sentiments,
    default=sentiments
)

aspects = sorted(df["Aspect"].dropna().unique())
selected_aspects = st.sidebar.multiselect(
    "Select customer experience aspect",
    aspects,
    default=aspects
)

filtered = df[
    df["Brand"].isin(selected_brands)
    & df["Predicted_Sentiment"].isin(selected_sentiments)
    & df["Aspect"].isin(selected_aspects)
]

if filtered.empty:
    st.warning("No reviews match the selected filters.")
    st.stop()

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Reviews", f"{len(filtered):,}")
c2.metric("Brands Analysed", filtered["Brand"].nunique())
c3.metric("Average Rating", f"{filtered['Rating'].mean():.2f}/5")
c4.metric(
    "Positive Reviews",
    f"{(filtered['Predicted_Sentiment'] == 'positive').mean() * 100:.1f}%"
)

st.divider()

# Brand rating comparison
st.subheader("1. Brand-wise Average Rating")

rating_data = (
    filtered.groupby("Brand", as_index=False)
    .agg(Average_Rating=("Rating", "mean"),
         Review_Count=("Review", "count"))
    .sort_values("Average_Rating", ascending=False)
)

fig = px.bar(
    rating_data,
    x="Brand",
    y="Average_Rating",
    color="Average_Rating",
    hover_data=["Review_Count"],
    range_y=[0, 5],
    title="Average Customer Rating by Shopping App"
)
st.plotly_chart(fig, use_container_width=True)

# Sentiment comparison
st.subheader("2. Sentiment Distribution by Brand")

sentiment_data = (
    filtered.groupby(["Brand", "Predicted_Sentiment"])
    .size()
    .reset_index(name="Review_Count")
)

fig = px.bar(
    sentiment_data,
    x="Brand",
    y="Review_Count",
    color="Predicted_Sentiment",
    barmode="stack",
    title="Positive, Negative and Neutral Reviews"
)
st.plotly_chart(fig, use_container_width=True)

# Aspect analysis
st.subheader("3. Customer Experience Issues")

aspect_data = (
    filtered.groupby(["Brand", "Aspect"])
    .size()
    .reset_index(name="Review_Count")
)

fig = px.bar(
    aspect_data,
    x="Brand",
    y="Review_Count",
    color="Aspect",
    barmode="stack",
    title="Customer Experience Aspects Across Brands"
)
st.plotly_chart(fig, use_container_width=True)

# Overall aspect distribution
st.subheader("4. Overall Customer Complaint Categories")

overall_aspects = (
    filtered["Aspect"].value_counts()
    .reset_index()
)
overall_aspects.columns = ["Aspect", "Review_Count"]

fig = px.pie(
    overall_aspects,
    names="Aspect",
    values="Review_Count",
    title="Distribution of Customer Experience Aspects"
)
st.plotly_chart(fig, use_container_width=True)

# Brand summary
st.subheader("5. Brand Performance Summary")

summary = (
    filtered.groupby("Brand")
    .agg(
        Total_Reviews=("Review", "count"),
        Average_Rating=("Rating", "mean"),
        Positive_Reviews=(
            "Predicted_Sentiment",
            lambda x: (x == "positive").sum()
        ),
        Negative_Reviews=(
            "Predicted_Sentiment",
            lambda x: (x == "negative").sum()
        )
    )
    .reset_index()
)

summary["Average_Rating"] = summary["Average_Rating"].round(2)
summary["Positive_Percentage"] = (
    summary["Positive_Reviews"] / summary["Total_Reviews"] * 100
).round(1)

st.dataframe(summary, use_container_width=True, hide_index=True)

# Review explorer
st.subheader("6. Customer Review Explorer")

search = st.text_input("Search review keywords")

reviews_view = filtered.copy()

if search:
    reviews_view = reviews_view[
        reviews_view["Review"].str.contains(
            search, case=False, na=False
        )
    ]

st.dataframe(
    reviews_view[
        ["Brand", "Rating", "Predicted_Sentiment",
         "Aspect", "Review", "Review_Date"]
    ].sort_values("Review_Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# Download
st.download_button(
    "Download Filtered Reviews CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="brand_intelligence_results.csv",
    mime="text/csv"
)

st.divider()

st.subheader("Methodology and Limitations")

st.write("""
- Public customer reviews were collected from 20 Google Play shopping apps.
- PySpark was used for data cleaning and processing.
- VADER was used for rule-based sentiment classification.
- Keyword-based classification was used to identify customer experience aspects.
- Ratings represent app-store ratings, not direct product-quality scores.
- Review counts differ between apps, and the collected sample is not necessarily representative of all customers.
- Sentiment and aspect labels are automated estimates and may contain classification errors.
""")

st.caption("Academic Big Data Analytics Project | Fashion Shopping App Intelligence")
