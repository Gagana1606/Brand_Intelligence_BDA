
# AI-Based Brand Intelligence and Consumer Perception Analytics Using Big Data

## 1. Project Overview

This project analyses customer reviews from 20 fashion and shopping applications to understand customer satisfaction, consumer perception and app experience.

It combines Apache PySpark for big data processing, VADER for sentiment analysis, keyword-based aspect classification, and Streamlit with Plotly for interactive visualisation.

The project provides brand-wise and platform-wise insights into customer feedback to support data-driven business decisions.

## 2. Problem Statement

Fashion shopping applications receive large volumes of customer feedback. Manually analysing these reviews makes it difficult to identify customer satisfaction patterns and recurring issues.

This project automates review processing, sentiment classification and customer experience analysis to identify areas that may require improvement.

## 3. Objectives

- Collect customer reviews from fashion and shopping applications.
- Analyse customer sentiment and ratings.
- Process review data using Apache PySpark.
- Identify common customer experience aspects.
- Compare customer feedback across 20 applications.
- Develop an interactive business intelligence dashboard.
- Generate insights to support customer experience improvement.

## 4. Dataset Description

The project uses publicly available Google Play application reviews collected using the Google Play Scraper Python library.

The dataset contains 5,734 processed reviews collected across 20 shopping applications.

### Dataset attributes

| Column | Description |
|---|---|
| Brand | Shopping app or brand name |
| App_ID | Google Play application identifier |
| App_Category | Application category |
| Review_ID | Unique review identifier |
| Review | Customer-written review |
| Rating | App review rating |
| Review_Date | Date of review |
| Thumbs_Up | Review helpfulness count |
| Sentiment_Score | VADER compound score |
| Predicted_Sentiment | Positive, negative or neutral |
| Aspect | Customer experience category |
| Rating_Category | High, medium or low |

## 5. Applications Analysed

The project includes 20 shopping applications:

1. Zara
2. H&M
3. adidas
4. Myntra
5. Nykaa Fashion
6. Flipkart
7. Meesho
8. Tata CLiQ
9. Max Fashion
10. Lifestyle
11. Shoppers Stop
12. The Souled Store
13. SNITCH
14. Savana
15. Littlebox
16. NEWME
17. Westside
18. M&S India
19. Fabindia
20. Rare Rabbit

Applications are grouped into fashion retailers, marketplaces, department stores and sportswear.

## 6. Technologies Used

- Python 3.12
- Apache PySpark
- Pandas
- VADER Sentiment Analysis
- Google Play Scraper
- Streamlit
- Plotly
- Java 21

## 7. Methodology

### Step 1: Data Collection
Customer reviews are collected from Google Play applications using the Google Play Scraper library.

### Step 2: Data Cleaning
- Remove missing reviews and ratings.
- Remove duplicate review records.
- Convert ratings into numeric values.
- Retain valid review information.

### Step 3: Big Data Processing
Apache PySpark is used to process review records through a local Spark session.

### Step 4: Sentiment Analysis
VADER calculates compound sentiment scores and classifies reviews into positive, negative and neutral categories.

### Step 5: Aspect Classification
Keyword-based classification identifies:
- General Experience
- App Usability
- Delivery
- Payment
- Customer Support
- Product Display
- Login and Account

### Step 6: Feature Engineering
Additional features include sentiment score, review length and rating category.

### Step 7: Dashboard Development
Streamlit and Plotly provide interactive visualisations, including:
- Brand-wise average ratings
- Sentiment distribution
- Customer experience aspect comparison
- Brand performance summary
- Customer review explorer

## 8. Project Results

The processing pipeline produced:

| Metric | Result |
|---|---:|
| Applications analysed | 20 |
| Processed reviews | 5,734 |
| Positive reviews | 3,384 |
| Negative reviews | 1,432 |
| Neutral reviews | 918 |

### Customer Experience Aspects

| Aspect | Reviews |
|---|---:|
| General Experience | 3,112 |
| App Usability | 1,505 |
| Delivery | 471 |
| Payment | 349 |
| Customer Support | 202 |
| Product Display | 63 |
| Login and Account | 32 |

## 9. Project Structure

```text
Brand_Intelligence_BDA/
│
├── app.py
├── collect_reviews.py
├── final_app_check.py
├── process_brand_data.py
├── process_data.py
├── requirements.txt
├── README.md
│
└── data/
    ├── brand_reviews_raw.csv
    ├── processed_brand_reviews.csv
    ├── final_app_check_results.csv
    └── processed_reviews.csv
```

## 10. Installation and Execution

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Collect reviews:

```bash
py collect_reviews.py
```

Process brand reviews:

```bash
py process_brand_data.py
```

Launch dashboard:

```bash
py -m streamlit run app.py
```

## 11. Limitations

- Review counts differ across applications.
- Google Play reviews may not represent all customers.
- VADER may not correctly interpret sarcasm or complex language.
- Aspect classification uses predefined keywords.
- App-store ratings measure application experience, not clothing quality.
- Marketplace applications and individual brand-owned applications represent different business models.
- PySpark runs in local mode rather than on a distributed cluster.

## 12. Future Enhancements

- Advanced machine-learning-based aspect classification.
- Transformer-based sentiment analysis.
- Review trend analysis over time.
- More comprehensive data collection.
- Distributed Spark cluster implementation.

## 13. Conclusion

This project demonstrates how Big Data processing and Natural Language Processing can be applied to customer feedback analysis.

By analysing reviews from 20 shopping applications, the system identifies customer sentiment, ratings and frequently discussed experience areas.

The interactive dashboard provides a business intelligence perspective that can help identify customer concerns and opportunities to improve digital shopping experiences.
```

### Step 3 — Save it

Scroll down and click **Commit changes**.

Commit message:

`Update README with brand intelligence analysis`

Tell me when done. Next we'll check your `requirements.txt` and Streamlit deployment.
