\# AI-Based Brand Intelligence and Consumer Perception Analytics



\## 1. Project Overview



This project analyses customer reviews of fast-fashion mobile applications to understand consumer perception, customer satisfaction and application experience.



It uses Big Data processing with Apache PySpark, Natural Language Processing (NLP) with VADER Sentiment Analysis, and an interactive Streamlit dashboard to convert unstructured customer reviews into useful business insights.



The analysis focuses on identifying customer sentiment, understanding frequently discussed experience areas and highlighting potential areas for improvement.



\## 2. Problem Statement



Fast-fashion mobile applications receive large volumes of customer feedback. Manually analysing thousands of reviews is time-consuming and makes it difficult to identify recurring customer concerns and satisfaction patterns.



This project addresses the problem by automating review processing, sentiment classification and customer experience analysis to support data-driven business decisions.



\## 3. Objectives



\- Analyse customer reviews from fast-fashion mobile applications.

\- Clean and preprocess unstructured review data.

\- Apply Apache Spark for data processing.

\- Perform sentiment analysis using VADER NLP.

\- Classify reviews into customer experience aspects.

\- Analyse customer ratings and sentiment distribution.

\- Develop an interactive dashboard for visualising results.

\- Generate insights that can help businesses improve customer experience.



\## 4. Dataset Description



The project uses the Mendeley dataset titled "Dataset Improving Fast-Fashion Mobile Application".



The dataset contains customer reviews associated with fast-fashion applications, including Zara, H\&M and Uniqlo.



\### Dataset attributes



| Column | Description |

|---|---|

| Review | Customer-written review |

| Rating | Customer rating |

| Sentiment | Original sentiment label |



The supplied dataset does not contain a separate brand identifier for each review. Therefore, this project analyses overall fast-fashion application experiences rather than making individual brand comparisons.



\## 5. Technologies Used



\- Python 3.12

\- Apache PySpark 4.3.0

\- Pandas

\- VADER Sentiment Analysis

\- Streamlit

\- Plotly

\- NumPy

\- Java 21



\## 6. Methodology



\### Step 1: Data Collection



The original Excel dataset is loaded into the Python environment.



\### Step 2: Data Preprocessing



\- Remove reviews with missing values.

\- Remove duplicate records.

\- Convert ratings into numeric values.

\- Standardise sentiment labels.

\- Remove empty reviews.

\- Retain valid ratings between 1 and 5.



\### Step 3: Big Data Processing



Apache PySpark is used to create a Spark DataFrame and perform distributed-style data processing using local Spark execution.



\### Step 4: Sentiment Analysis



VADER (Valence Aware Dictionary and sEntiment Reasoner) is used to calculate compound sentiment scores.



Reviews are classified into:



\- Positive

\- Negative

\- Neutral



The dataset-provided sentiment labels are also retained for comparison.



\### Step 5: Customer Experience Aspect Classification



Keyword-based classification identifies the following aspects:



\- Login and Account

\- Payment

\- Delivery

\- Customer Support

\- App Usability

\- Product Display

\- General Experience



\### Step 6: Feature Engineering



Additional analytical attributes are generated:



\- Sentiment score

\- Predicted sentiment

\- Review length

\- Rating category



\### Step 7: Data Export



The processed Spark DataFrame is converted into a Pandas DataFrame and exported as a CSV file for dashboard visualisation.



\### Step 8: Dashboard Development



Streamlit and Plotly are used to build an interactive dashboard containing:



\- Business overview and key metrics

\- Sentiment distribution

\- Customer rating distribution

\- Customer experience aspect analysis

\- Sentiment score distribution

\- Customer review explorer

\- Business insights



\## 7. Project Results



The final processing pipeline produced the following results:



| Metric | Result |

|---|---:|

| Original records | 61,150 |

| Processed records | 43,330 |

| Average rating | 3.28 / 5 |

| Predicted positive reviews | 22,471 |

| Predicted negative reviews | 10,462 |

| Predicted neutral reviews | 10,397 |



\### Customer Experience Analysis



| Aspect | Reviews |

|---|---:|

| General Experience | 26,623 |

| Delivery | 4,423 |

| App Usability | 3,652 |

| Payment | 2,781 |

| Product Display | 2,681 |

| Login and Account | 1,990 |

| Customer Support | 1,180 |



These results indicate that general application experience is the most frequently discussed category in the analysed reviews.



\## 8. Project Structure



```text

Brand\_Intelligence\_BDA/

│

├── app.py

├── process\_data.py

├── requirements.txt

├── README.md

│

└── data/

&#x20;   ├── Dataset Improving Fast-Fashion Mobile Application.zip

&#x20;   ├── cleaned\_input.csv

&#x20;   ├── processed\_reviews.csv

&#x20;   │

&#x20;   └── extracted/

&#x20;       └── Dataset Improving Fast-Fashion Mobile Application/

&#x20;           └── sentiment\_analysis.xlsx

```



\## 9. Installation and Execution



\### Install dependencies



```bash

py -m pip install pandas numpy pyspark vaderSentiment streamlit plotly openpyxl

```



\### Configure Java and Python for PySpark (Windows PowerShell)



```powershell

$env:JAVA\_HOME="C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.13.10002-hotspot"

$env:Path="$env:JAVA\_HOME\\bin;$env:Path"

$env:PYSPARK\_PYTHON="C:\\Users\\Gagana T R\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

$env:PYSPARK\_DRIVER\_PYTHON=$env:PYSPARK\_PYTHON

```



\### Run data processing



```powershell

py process\_data.py

```



\### Launch dashboard



```powershell

py -m streamlit run app.py

```



\## 10. Limitations



\- The dataset does not provide individual brand identifiers, preventing reliable brand-wise comparison.

\- Aspect classification is based on predefined keywords and may not capture every contextual meaning.

\- VADER is a lexicon-based sentiment analyser and may not correctly interpret sarcasm or complex language.

\- Spark is configured in local execution mode rather than a multi-node cluster.

\- The dataset represents a particular collection of reviews and may not represent all fast-fashion customers.



\## 11. Future Enhancements



\- Introduce machine-learning-based aspect classification.

\- Use advanced NLP models for improved sentiment detection.

\- Include brand identifiers for individual brand comparisons.

\- Add time-based sentiment trend analysis if review dates become available.

\- Deploy the dashboard online.

\- Scale processing to a distributed Spark cluster.



\## 12. Conclusion



The project demonstrates how Big Data processing and Natural Language Processing can be combined to analyse customer feedback from fast-fashion mobile applications.



By processing customer reviews, identifying sentiment and classifying experience aspects, the system provides an interactive way to understand consumer perception and identify potential areas for business improvement.



The project demonstrates the practical application of Apache PySpark, Python-based NLP and interactive data visualisation in business intelligence.

