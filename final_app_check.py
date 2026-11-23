
import pandas as pd
import time
from google_play_scraper import app

apps_to_check = [
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

results = []

for brand, app_id, category in apps_to_check:
    print(f"Checking {brand}...")

    try:
        details = app(app_id, lang="en", country="in")

        results.append({
            "Brand": brand,
            "App_ID": app_id,
            "Category": category,
            "App_Title": details.get("title"),
            "Developer": details.get("developer"),
            "Rating": details.get("score"),
            "Rating_Count": details.get("ratings"),
            "Installs": details.get("installs"),
            "Status": "Listing Found"
        })

        print("  Listing found:", details.get("title"))

    except Exception as e:
        results.append({
            "Brand": brand,
            "App_ID": app_id,
            "Category": category,
            "App_Title": None,
            "Developer": None,
            "Rating": None,
            "Rating_Count": None,
            "Installs": None,
            "Status": "Not Found"
        })

        print("  Not found:", str(e)[:100])

    time.sleep(1)

df = pd.DataFrame(results)

df.to_csv("data/final_app_check_results.csv", index=False)

print("\n========== APP VERIFICATION SUMMARY ==========")
print(df[["Brand", "App_Title", "Developer", "Status"]].to_string(index=False))
print("\nListings found:", (df["Status"] == "Listing Found").sum())
print("Not found:", (df["Status"] == "Not Found").sum())
print("\nSaved to data/final_app_check_results.csv")
