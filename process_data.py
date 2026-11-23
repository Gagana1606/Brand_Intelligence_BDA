
import os
import glob
import shutil
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, length, udf, when
)
from pyspark.sql.types import StringType, DoubleType

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# 1. Locate and load the original dataset
files = glob.glob(
    "data/extracted/**/*.xlsx",
    recursive=True
)

if not files:
    raise FileNotFoundError("Excel dataset not found!")

df = pd.read_excel(files[0])

print("Original records:", len(df))


# 2. Clean the dataset
df = df.dropna(subset=["Review"])

df["Review"] = df["Review"].astype(str).str.strip()
df["Sentiment"] = df["Sentiment"].astype(str).str.lower().str.strip()
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df = df.dropna(subset=["Rating"])
df = df.drop_duplicates()

df = df[df["Review"] != ""]
df = df[df["Rating"].between(1, 5)]

print("Records after cleaning:", len(df))


# 3. Start PySpark
spark = (
    SparkSession.builder
    .appName("FashionBrandIntelligence")
    .master("local[*]")
    .getOrCreate()
)

# Load cleaned data directly into Spark
spark_df = spark.createDataFrame(df)


# 4. Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(review):
    if not review:
        return "neutral"

    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"


def get_score(review):
    if not review:
        return 0.0

    return float(
        analyzer.polarity_scores(review)["compound"]
    )


sentiment_udf = udf(analyze_sentiment, StringType())
score_udf = udf(get_score, DoubleType())

spark_df = (
    spark_df
    .withColumn("Predicted_Sentiment", sentiment_udf(col("Review")))
    .withColumn("Sentiment_Score", score_udf(col("Review")))
)


# 5. Identify customer experience aspects
def identify_aspect(review):
    text = str(review).lower()

    aspects = {
        "Login and Account": [
            "login", "log in", "sign in", "account", "password",
            "otp", "register"
        ],
        "Payment": [
            "payment", "pay", "upi", "card", "transaction",
            "refund", "checkout"
        ],
        "Delivery": [
            "delivery", "deliver", "shipping", "late",
            "order", "tracking", "courier"
        ],
        "Customer Support": [
            "support", "customer service", "help",
            "response", "complaint"
        ],
        "App Usability": [
            "easy to use", "difficult", "slow", "crash",
            "loading", "navigation", "interface", "bug"
        ],
        "Product Display": [
            "image", "colour", "color", "size",
            "product", "picture", "description"
        ]
    }

    for aspect, keywords in aspects.items():
        if any(word in text for word in keywords):
            return aspect

    return "General Experience"


aspect_udf = udf(identify_aspect, StringType())

spark_df = spark_df.withColumn(
    "Aspect",
    aspect_udf(col("Review"))
)


# 6. Add useful analytical columns
spark_df = (
    spark_df
    .withColumn("Review_Length", length(col("Review")))
    .withColumn(
        "Rating_Category",
        when(col("Rating") <= 2, "Low")
        .when(col("Rating") == 3, "Medium")
        .otherwise("High")
    )
)


# 7. Save processed data using Pandas
output_file = "data/processed_reviews.csv"

processed_df = spark_df.toPandas()
processed_df.to_csv(output_file, index=False)

# 8. Display summary
result = pd.read_csv(output_file)

print("\n========== PROJECT SUMMARY ==========")
print("Processed reviews:", len(result))

print("\nOriginal Sentiment Distribution:")
print(result["Sentiment"].value_counts())

print("\nPredicted Sentiment Distribution:")
print(result["Predicted_Sentiment"].value_counts())

print("\nAverage Rating:", round(result["Rating"].mean(), 2))

print("\nCustomer Experience Aspects:")
print(result["Aspect"].value_counts())

print("\nProcessed file saved at:", output_file)

spark.stop()
