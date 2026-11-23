
import pandas as pd
import time
from google_play_scraper import reviews, Sort

apps = [
    ("Zara", "com.inditex.zara", "Fashion Retailer"),
    ("H&M", "com.hm.goe", "Fashion Retailer"),
    ("adidas", "com.adidas.app", "Sportswear"),
    ("Myntra", "com.myntra.android", "Marketplace"),
    ("Nykaa Fashion", "com.fsn.nds", "Marketplace"),
    ("Flipkart", "com.flipkart.android", "Marketplace"),
    ("Meesho", "com.meesho.supply", "Marketplace"),
    ("Tata CLiQ", "com.tul.tatacliq", "Marketplace"),
    ("Max Fashion", "com.applications.max", "Fashion Retailer"),
    ("Lifestyle", "com.applications.lifestyle", "Department Store"),
    ("Shoppers Stop", "shoppersstop.shoppersstop", "Department Store"),
    ("The Souled Store", "com.thesouledstore", "Fashion Retailer"),
    ("SNITCH", "co.shopney.snitch", "Fashion Retailer"),
    ("Savana", "com.savana.in", "Fashion Retailer"),
    ("Littlebox", "lbindia.android.app", "Fashion Retailer"),
    ("NEWME", "com.newme.mobile", "Fashion Retailer"),
    ("Westside", "com.westside", "Department Store"),
    ("M&S India", "com.mns", "Fashion Retailer"),
    ("Fabindia", "com.fabindia.shopping", "Fashion Retailer"),
    ("Rare Rabbit", "com.coffye.epnksg", "Fashion Retailer")
]

all_reviews = []

for brand, app_id, category in apps:
    print(f"\nCollecting reviews for {brand}...")

    try:
        review_data, continuation_token = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=300
        )

        for review in review_data:
            all_reviews.append({
                "Brand": brand,
                "App_ID": app_id,
                "App_Category": category,
                "Review_ID": review.get("reviewId"),
                "Review": review.get("content"),
                "Rating": review.get("score"),
                "Review_Date": review.get("at"),
                "Thumbs_Up": review.get("thumbsUpCount")
            })

        print(f"Collected: {len(review_data)} reviews")

    except Exception as e:
        print(f"Error for {brand}: {e}")

    time.sleep(2)

df = pd.DataFrame(all_reviews)

if not df.empty:
    df["Review_Date"] = pd.to_datetime(df["Review_Date"], errors="coerce")
    df.drop_duplicates(subset=["Review_ID"], inplace=True)

    df.to_csv("data/brand_reviews_raw.csv", index=False)

    print("\n========== COLLECTION SUMMARY ==========")
    print("Total reviews:", len(df))
    print("\nReviews per brand:")
    print(df.groupby("Brand").size().sort_values(ascending=False))
    print("\nSaved to data/brand_reviews_raw.csv")
else:
    print("\nNo reviews were collected.")
