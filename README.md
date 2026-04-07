# 🏃‍♂️ ¿What Factors Determine Performance in the World Marathon Majors?

<p align="center">
  <img src="images/cover.png" width="700">
</p>

### An Exploratory Data Analysis of London Marathon & World Marathon Majors

---

## 📌 Overview

This project investigates how environmental and physiological factors influence marathon performance. By combining global marathon data with a detailed runner-level dataset from the London Marathon, the analysis explores how variables such as **temperature, runner category, and age** impact finishing times.

The project follows an end-to-end data analysis workflow, including **data collection, cleaning, feature engineering, exploratory data analysis (EDA), and statistical testing**, with a strong focus on building interpretable and defensible insights.

---

## 🎯 Objectives

* Compare performance across World Marathon Majors  
* Analyze the relationship between **temperature and race performance**  
* Investigate differences between **Elite and Mass runners**  
* Evaluate how **age influences marathon performance**  
* Validate findings using statistical hypothesis testing  

---

## 📊 Datasets

### 🔵 World Marathon Majors Dataset

* Manually curated dataset  
* Aggregated marathon-level data  

**Key variables:**

* `Marathon`  
* `Year`  
* Elite and average finishing times  
* Participants and finishers  
* Weather conditions  
* Elevation gain  

---

### 🟢 London Marathon Dataset (2021–2025)

* Web-scraped dataset (Elite + sampled Mass runners)  
* Runner-level granularity  
* Integrated weather data per race  

**Key variables:**

* `Year`  
* `Category` (Elite / Mass)  
* `Age_group`  
* `Finish_seconds`  
* `finish_hours`  
* `Pace_min_km`  
* Weather variables (`Temp_mean`, `Humidity_mean`, `Wind_speed_mean`)  

---

## 🧩 Project Structure

The analysis is structured into two complementary layers:

### 🌍 Global Analysis (World Marathon Majors)

* Cross-marathon comparison  
* Completion rate and participation analysis  
* Elevation and race difficulty exploration  
* Preliminary relationship between temperature and performance  

⚠️ **Limitation:** Aggregated data restricts statistical depth  

---

### 🔬 Deep Dive (London Marathon)

* Elite vs Mass performance comparison  
* Distribution analysis (separated populations)  
* Performance trends across years  
* Age group analysis (Mass runners only)  
* Temperature-performance relationship (aggregated by year)  

---

## 📈 Methodology

### 🔹 Exploratory Data Analysis (EDA)

* Distribution analysis (histograms, boxplots)  
* Comparative analysis (Elite vs Mass)  
* Trend analysis across years  
* Temperature-performance exploration  

### 🔹 Statistical Analysis

The following hypotheses were tested:

---

### 🟣 Elite vs Mass

* **H0:** There is no difference in finishing times between Elite and Mass runners  
* **H1:** There is a significant difference  

✔ **Test used:** Welch’s t-test  
✔ **Result:** p < 0.05 → Reject H0  

👉 Elite runners are significantly faster and more consistent  

---

### 🟡 Age and Performance

* **H0:** There is no difference in performance between age groups  
* **H1:** Age impacts performance  

✔ Approach: grouped comparison (younger vs older runners)  
✔ **Test used:** t-test  
✔ **Result:** p < 0.05 → Reject H0  

👉 Older runners tend to have slower finishing times  

---

### 🔴 Temperature and Performance

* **H0:** Temperature does not affect marathon performance  
* **H1:** Temperature has a significant effect  

✔ **Test used:** Pearson correlation  
✔ **Result:** Positive correlation observed  

👉 Higher temperatures are associated with slower finishing times  

⚠️ Limited statistical power due to small sample size (5 years)

---

## 📊 Key Visualizations

* Completion rate across marathons  
* Participants vs finishers comparison  
* Elevation vs performance context  
* Elite vs Mass boxplots  
* Distribution of finishing times (separated populations)  
* Age group performance analysis  
* Temperature vs performance (year-level aggregation)  

---

## 💡 Key Insights

* Marathon performance is influenced by both **environmental and physiological factors**  
* Higher temperatures are associated with **worse performance outcomes**  
* Elite runners are significantly faster and exhibit **lower variability**  
* Mass runners show **high variability due to heterogeneous profiles**  
* Age has a measurable effect, with performance declining in older groups  
* Aggregated global data provides trends, but **runner-level data is required for robust conclusions**  

---

## ⚠️ Limitations

* Limited number of observations for temperature analysis (5 years)  
* Mass runner dataset is based on sampling  
* Weather data is aggregated at race level  
* External factors not included (training, pacing, nutrition, course strategy)  

---

## 🛠️ Tech Stack

* Python  
* Pandas  
* NumPy  
* Matplotlib / Seaborn  
* SciPy  

---

## 📂 Repository Structure

```bash
marathon-eda/
│
├── src/
│   ├── data/
│   ├── notebooks/
│   ├── scripts/
│   ├── images/
│   ├── reports/
│   └── memoria.ipynb
│
├── main.py
├── pyproject.toml
├── README.md
├── sources.md
└── uv.lock
```

