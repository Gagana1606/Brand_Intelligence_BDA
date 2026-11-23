
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, when, length
from pyspark.sql.types import DoubleType, StringType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

spark = SparkSession.builder.appName("BrandIntelligence").master("local[*]").getOrCreate()

print("Loading reviews...")

df = spark.read.option("header", True).csv("data/brand_reviews_raw.csv")
df = df.dropna(subset=["Review", "Rating"])
df = df.dropDuplicates(["Review_ID"])

analyzer = SentimentIntensityAnalyzer()

def sentiment_score(review):
    return float(analyzer.polarity_scores(str(review))["compound"])

def identify_aspect(review):
    text = str(review).lower()
    aspects = {
        "Delivery": ["delivery", "shipping", "delayed", "late", "courier"],
        "Payment": ["payment", "refund", "money", "upi", "transaction"],
        "App Usability": ["app", "crash", "loading", "slow", "bug", "error"],
        "Product Display": ["image", "picture", "size", "colour", "color"],
        "Login and Account": ["login", "password", "account", "otp"],
        "Customer Support": ["support", "customer care", "service", "response"]
    }
    for aspect, words in aspects.items():
        if any(word in text for word in words):
            return aspect
    return "General Experience"

score_udf = udf(sentiment_score, DoubleType())
aspect_udf = udf(identify_aspect, StringType())

df = df.withColumn("Sentiment_Score", score_udf(col("Review")))
df = df.withColumn(
    "Predicted_Sentiment",
    when(col("Sentiment_Score") >= 0.05, "positive")
    .when(col("Sentiment_Score") <= -0.05, "negative")
    .otherwise("neutral")
)

df = df.withColumn("Aspect", aspect_udf(col("Review")))
df = df.withColumn("Review_Length", length(col("Review")))

result = df.toPandas()

# Safe rating conversion outside Spark
result["Rating"] = pd.to_numeric(result["Rating"], errors="coerce")
result = result.dropna(subset=["Rating"])

result["Rating_Category"] = result["Rating"].apply(
    lambda x: "High" if x >= 4 else ("Medium" if x == 3 else "Low")
)

result.to_csv("data/processed_brand_reviews.csv", index=False)

print("\n========== PROJECT SUMMARY ==========")
print("Total processed reviews:", len(result))
print("Brands analysed:", result["Brand"].nunique())

print("\nReviews per brand:")
print(result.groupby("Brand").size())

print("\nSentiment distribution:")
print(result["Predicted_Sentiment"].value_counts())

print("\nAverage rating by brand:")
print(result.groupby("Brand")["Rating"].mean().round(2))

print("\nAspect distribution:")
print(result["Aspect"].value_counts())

print("\nSaved: data/processed_brand_reviews.csv")

spark.stop()
