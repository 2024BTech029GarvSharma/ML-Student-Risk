# ML-Student-Risk 🎓

> **Predicting Student Exam Performance Using Machine Learning**  
> B.Tech CSE (AI) | JK Lakshmipat University | Garv Sharma (2024BTech029)

---

## 📌 Problem Statement
Many students fall behind academically without early warning signs. This project builds a **predictive ML model** that forecasts a student's exam score based on daily habits and behavioural data — enabling proactive intervention before failure occurs.

---

## 📊 Dataset
- **File:** `student_habits_performance.csv`
- **Size:** 1,000 students × 16 features
- **Target:** `exam_score` (continuous, 0–100)
- **After cleaning:** 909 rows (91 missing values dropped, 0 duplicates)

### Features
| Type | Columns |
|------|---------|
| Numerical | `age`, `study_hours_per_day`, `social_media_hours`, `netflix_hours`, `attendance_percentage`, `sleep_hours`, `exercise_frequency`, `mental_health_rating` |
| Categorical | `gender`, `part_time_job`, `diet_quality`, `parental_education_level`, `internet_quality`, `extracurricular_participation` |

---

## 🔬 Methodology

```
Data Collection → EDA → Feature Engineering → Model Training → Evaluation → Deployment
```

### Feature Selection (6 selected)
`study_hours_per_day` · `mental_health_rating` · `attendance_percentage`  
`social_media_hours` · `sleep_hours` · `exercise_frequency`

**Strategy:** Ensemble Mixed Selection — balanced Pearson correlation + statistical dependency

---

## 🤖 Models Trained

| Model | R² Score | RMSE | MAE | MAPE |
|-------|----------|------|-----|------|
| Linear Regression | 0.8411 | 6.497 | 5.346 | 8.56% |
| Decision Tree | 0.7198 | 8.643 | 6.800 | 11.03% |
| Random Forest | 0.7913 | 7.446 | 5.900 | 9.63% |
| **XGBoost ★** | **0.8613** | **6.21** | **4.82** | **7.84%** |

All models tuned with **GridSearchCV (5-fold CV)**.

---

## 🏆 Best Model: XGBoost
- **R² Score:** 0.8613  
- **MAE:** 4.82  
- **RMSE:** 6.21  
- **Optimization:** GridSearchCV on `n_estimators`, `max_depth`, `learning_rate`

---

## ⚠️ Risk Classification System

| Risk Level | Score Range | Action |
|-----------|-------------|--------|
| 🔴 High Risk | < 40 | Immediate intervention |
| 🟠 Medium Risk | 40–60 | Needs improvement |
| 🔵 Low Risk | 60–80 | Performing well |
| 🟢 Excellent | ≥ 80 | Outstanding! |

---

## 🚀 Deployment

**Streamlit App** (`ml.py`)  
```bash
streamlit run ml.py
```
Interactive sliders for all 6 features → real-time score prediction + risk badge.

---

## 📁 Repository Structure

```
ML-Student-Risk/
├── ml_project.ipynb                  # Full analysis notebook (82 cells)
├── ml.py                             # Streamlit prediction app
├── best_student_model.pkl            # Trained XGBoost model
├── student_habits_performance.csv    # Dataset
├── Student_Risk_Prediction_PPT.pptx  # Presentation (16 slides)
└── README.md
```

---

## 🛠️ Tech Stack
`Python` · `Pandas` · `NumPy` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn` · `Streamlit` · `Joblib`

---

## 📎 QR Code
Scan to access this repository:

![QR Code](ppt_assets/17_qr_code.png)

---

*© 2026 Garv Sharma | JK Lakshmipat University*
