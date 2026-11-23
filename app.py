
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Brand Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Based Brand Intelligence & Consumer Perception Analytics")
st.markdown(
    "Analyzing customer reviews, sentiment and app experience "
    "in the fast-fashion mobile application sector."
)

st.divider()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/processed_reviews.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Processed dataset not found. Run process_data.py first.")
    st.stop()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

sentiments = ["All"] + sorted(df["Predicted_Sentiment"].dropna().unique().tolist())

selected_sentiment = st.sidebar.selectbox(
    "Filter by Predicted Sentiment",
    sentiments
)

aspects = ["All"] + sorted(df["Aspect"].dropna().unique().tolist())

selected_aspect = st.sidebar.selectbox(
    "Filter by Customer Experience Aspect",
    aspects
)

filtered_df = df.copy()

if selected_sentiment != "All":
    filtered_df = filtered_df[
        filtered_df["Predicted_Sentiment"] == selected_sentiment
    ]

if selected_aspect != "All":
    filtered_df = filtered_df[
        filtered_df["Aspect"] == selected_aspect
    ]

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.header("Business Overview")

total_reviews = len(filtered_df)

avg_rating = filtered_df["Rating"].mean() if total_reviews else 0

positive_pct = (
    (filtered_df["Predicted_Sentiment"] == "positive").mean() * 100
    if total_reviews else 0
)

negative_pct = (
    (filtered_df["Predicted_Sentiment"] == "negative").mean() * 100
    if total_reviews else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", f"{total_reviews:,}")
col2.metric("Average Rating", f"{avg_rating:.2f} / 5")
col3.metric("Positive Reviews", f"{positive_pct:.1f}%")
col4.metric("Negative Reviews", f"{negative_pct:.1f}%")

st.divider()

# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

st.header("1. Customer Sentiment Analysis")

col1, col2 = st.columns(2)

sentiment_counts = (
    filtered_df["Predicted_Sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = ["Sentiment", "Count"]

with col1:
    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Predicted Sentiment Distribution",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Number of Reviews by Sentiment",
        text="Count"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# RATING ANALYSIS
# --------------------------------------------------

st.divider()
st.header("2. Customer Rating Analysis")

rating_counts = (
    filtered_df["Rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = ["Rating", "Count"]

fig = px.bar(
    rating_counts,
    x="Rating",
    y="Count",
    title="Distribution of Customer Ratings",
    text="Count",
    color="Rating"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# ASPECT ANALYSIS
# --------------------------------------------------

st.divider()
st.header("3. Customer Experience Aspect Analysis")

aspect_counts = (
    filtered_df["Aspect"]
    .value_counts()
    .reset_index()
)

aspect_counts.columns = ["Aspect", "Review Count"]

fig = px.bar(
    aspect_counts,
    x="Review Count",
    y="Aspect",
    orientation="h",
    title="Reviews by Customer Experience Aspect",
    text="Review Count"
)

st.plotly_chart(fig, use_container_width=True)

aspect_sentiment = pd.crosstab(
    filtered_df["Aspect"],
    filtered_df["Predicted_Sentiment"]
).reset_index()

fig = px.bar(
    aspect_sentiment,
    x="Aspect",
    y=["positive", "negative", "neutral"],
    title="Sentiment Across Customer Experience Aspects",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# SENTIMENT SCORE ANALYSIS
# --------------------------------------------------

st.divider()
st.header("4. Sentiment Score Analysis")

fig = px.histogram(
    filtered_df,
    x="Sentiment_Score",
    color="Predicted_Sentiment",
    nbins=30,
    title="Distribution of VADER Sentiment Scores"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# REVIEW EXPLORER
# --------------------------------------------------

st.divider()
st.header("5. Customer Review Explorer")

review_type = st.selectbox(
    "Select Review Category",
    ["All", "Negative", "Positive", "Neutral"]
)

review_df = filtered_df.copy()

if review_type != "All":
    review_df = review_df[
        review_df["Predicted_Sentiment"] == review_type.lower()
    ]

st.write(f"Showing {len(review_df):,} reviews")

st.dataframe(
    review_df[
        [
            "Review",
            "Rating",
            "Sentiment",
            "Predicted_Sentiment",
            "Aspect",
            "Sentiment_Score"
        ]
    ].head(200),
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.divider()
st.header("6. Business Insights")

if len(filtered_df) > 0:

    most_discussed = filtered_df["Aspect"].value_counts().idxmax()

    negative_reviews = filtered_df[
        filtered_df["Predicted_Sentiment"] == "negative"
    ]

    st.write(
        f"- **Most discussed experience area:** {most_discussed}"
    )

    st.write(
        f"- **Negative reviews:** {len(negative_reviews):,}"
    )

    if len(negative_reviews) > 0:
        negative_aspect = negative_reviews["Aspect"].value_counts().idxmax()

        st.write(
            f"- **Most frequently mentioned aspect in negative reviews:** "
            f"{negative_aspect}"
        )

    st.write(
        f"- **Average customer rating:** {avg_rating:.2f} out of 5"
    )

else:
    st.info("No reviews match the selected filters.")

# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("About This Project")

st.write(
    """
    This project uses customer review data from fast-fashion mobile
    applications to study consumer perception and app experience.

    **Technologies:** Python, Pandas, PySpark pipeline, VADER NLP,
    Streamlit and Plotly.

    **Data limitation:** The supplied dataset does not contain an
    individual brand identifier. Therefore, this dashboard analyses
    overall fast-fashion app experiences rather than comparing
    individual brands.

    **Methodology note:** Original sentiment labels are supplied by
    the dataset. Predicted sentiment is independently calculated
    using VADER. These two labels may differ.
    """
)

st.caption("AI-Based Brand Intelligence and Consumer Perception Analytics")
