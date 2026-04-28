import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

A = "ppt_assets"
OUT_PPT = "Student_Risk_Prediction_PPT.pptx"

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

DARK   = RGBColor(0x0D,0x1B,0x2A)
BLUE   = RGBColor(0x43,0x61,0xEE)
PINK   = RGBColor(0xF7,0x25,0x85)
WHITE  = RGBColor(0xFF,0xFF,0xFF)
LGRAY  = RGBColor(0xF0,0xF4,0xFF)
GREEN  = RGBColor(0x2D,0xC6,0x53)

BLANK  = prs.slide_layouts[6]   # completely blank

# ─── helpers ────────────────────────────────────────────────────
def bg(slide, color=DARK):
    fill = slide.background.fill
    fill.solid(); fill.fore_color.rgb = color

def txbox(slide, text, l,t,w,h, size=18, bold=False,
          color=WHITE, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    p  = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = color
    return tb

def img(slide, path, l, t, w, h=None):
    if not os.path.exists(path): return
    if h:
        slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(w), Inches(h))
    else:
        slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w))

def accent_bar(slide, color=BLUE):
    bar = slide.shapes.add_shape(1,Inches(0),Inches(0),Inches(13.33),Inches(0.55))
    bar.fill.solid(); bar.fill.fore_color.rgb = color
    bar.line.fill.background()

def side_bar(slide, color=BLUE, w=0.35):
    bar = slide.shapes.add_shape(1,Inches(0),Inches(0),Inches(w),Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = color
    bar.line.fill.background()

def slide_header(slide, title, subtitle=""):
    accent_bar(slide, BLUE)
    txbox(slide, title, 0.5,0.05,12,0.5, size=22, bold=True, color=WHITE)
    if subtitle:
        txbox(slide, subtitle, 0.5,0.6,12,0.45, size=13, color=LGRAY)

def divider(slide, y, color=BLUE):
    ln = slide.shapes.add_shape(1,Inches(0.5),Inches(y),Inches(12.3),Inches(0.04))
    ln.fill.solid(); ln.fill.fore_color.rgb = color
    ln.line.fill.background()

# ════════════════════════════════════════════════════════════════
# SLIDE 1 – Title
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
# gradient left strip
side_bar(sl, BLUE, 0.7)
grad = sl.shapes.add_shape(1,Inches(0.7),Inches(0),Inches(4.5),Inches(7.5))
grad.fill.solid(); grad.fill.fore_color.rgb = RGBColor(0x1a,0x2a,0x4a)
grad.line.fill.background()
# title text
txbox(sl,"Student Performance AI",1.4,1.4,11,1.2,size=42,bold=True,color=WHITE)
txbox(sl,"Predicting Student Exam Risk Using Machine Learning",1.4,2.7,10,0.7,size=20,color=LGRAY)
divider(sl,3.55,PINK)
txbox(sl,"Dataset: 1,000 Students  |  16 Features  |  Best Model: XGBoost  |  R² = 0.8613",
      1.4,3.7,11,0.5,size=13,color=RGBColor(0x4C,0xC9,0xF0))
txbox(sl,"JK Lakshmipat University  |  B.Tech CSE (AI)  |  2024BTech029 – Garv Sharma",
      1.4,6.6,11,0.5,size=11,color=RGBColor(0x88,0x99,0xBB))
# QR
img(sl, f"{A}/17_qr_code.png", 10.3, 4.5, 2.5)
txbox(sl,"Scan for GitHub",10.3,6.75,2.5,0.4,size=10,color=LGRAY,align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# SLIDE 2 – Agenda
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Agenda","What we'll cover today")
items = [
    ("01","Problem Statement","Why student risk prediction matters"),
    ("02","Dataset Overview","1,000 students, 16 features, data quality"),
    ("03","Exploratory Data Analysis","Distributions, correlations, insights"),
    ("04","Feature Engineering","Selecting the 6 best predictors"),
    ("05","Model Training","LR · Decision Tree · Random Forest · XGBoost"),
    ("06","Evaluation & Results","R², RMSE, MAE, MAPE comparison"),
    ("07","Deployment","Streamlit app + risk classifier"),
    ("08","GitHub & Conclusion","Repo, QR code, next steps"),
]
for i,(num,title,desc) in enumerate(items):
    row = i % 4; col = i // 4
    lx = 0.5 + col*6.5; ty = 1.2 + row*1.5
    box = sl.shapes.add_shape(1,Inches(lx),Inches(ty),Inches(6.0),Inches(1.25))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0x1a,0x2a,0x4a)
    box.line.color.rgb = BLUE
    txbox(sl,num, lx+0.1, ty+0.05, 0.6, 0.45, size=18, bold=True, color=PINK)
    txbox(sl,title, lx+0.65, ty+0.05, 5.2, 0.45, size=15, bold=True, color=WHITE)
    txbox(sl,desc,  lx+0.65, ty+0.55, 5.2, 0.5,  size=11, color=LGRAY)

# ════════════════════════════════════════════════════════════════
# SLIDE 3 – Problem Statement
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Problem Statement","The challenge of student academic risk")
side_bar(sl, PINK, 0.3)
txbox(sl,
    "Many students silently fall behind until it's too late for intervention.\n\n"
    "Traditional grading systems only flag failure AFTER it happens.\n\n"
    "Goal: Build a predictive ML model that identifies at-risk students EARLY\n"
    "using daily habits and behavioural data — enabling proactive support.",
    0.7,1.1,7.8,3.5,size=16,color=WHITE)
# stat boxes
stats = [("1,000","Students Surveyed"),("16","Features Collected"),
         ("91","Missing Values Handled"),("4","ML Models Compared")]
for i,(val,lab) in enumerate(stats):
    bx = 9.0; by = 1.2 + i*1.45
    box=sl.shapes.add_shape(1,Inches(bx),Inches(by),Inches(3.8),Inches(1.2))
    box.fill.solid(); box.fill.fore_color.rgb = BLUE
    box.line.fill.background()
    txbox(sl,val,bx+0.1,by+0.05,3.6,0.55,size=28,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    txbox(sl,lab,bx+0.1,by+0.6, 3.6,0.45,size=12,color=LGRAY,align=PP_ALIGN.CENTER)
img(sl,f"{A}/16_pipeline.png",0.5,4.8,12.3,2.4)

# ════════════════════════════════════════════════════════════════
# SLIDE 4 – Dataset Overview
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Dataset Overview","student_habits_performance.csv — 1,000 rows × 16 columns")
img(sl,f"{A}/02_desc_stats.png",0.3,1.05,12.7,3.3)
img(sl,f"{A}/01_missing_values.png",0.3,4.45,6.2,2.8)
txbox(sl,
    "Key Dataset Facts\n\n"
    "• 1,000 students, 909 after cleaning\n"
    "• 91 missing values → dropped rows\n"
    "• 0 duplicate records\n"
    "• Target: exam_score (continuous, 0–100)\n"
    "• Mix of numerical & categorical features",
    6.7,4.45,6.2,2.8,size=13,color=WHITE)

# ════════════════════════════════════════════════════════════════
# SLIDE 5 – EDA: Distributions
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Exploratory Data Analysis","Numerical feature distributions")
img(sl,f"{A}/03_exam_score_dist.png",0.3,1.05,6.2,3.1)
img(sl,f"{A}/07_cat_distributions.png",6.6,1.05,6.5,3.1)
img(sl,f"{A}/08_boxplots_categorical.png",0.3,4.2,12.7,3.1)

# ════════════════════════════════════════════════════════════════
# SLIDE 6 – EDA: Correlations
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"EDA: Correlation Analysis","How features relate to exam performance")
img(sl,f"{A}/04_correlation_heatmap.png",0.3,1.05,7.5,5.8)
img(sl,f"{A}/05_correlation_bar.png",8.0,1.05,5.0,3.1)
txbox(sl,
    "Key Findings\n\n"
    "• study_hours_per_day: strongest +ve r\n"
    "• mental_health_rating: strong +ve\n"
    "• attendance_percentage: +ve impact\n"
    "• social_media_hours: -ve impact\n"
    "• sleep_hours: moderate +ve\n"
    "• netflix_hours: mild -ve",
    8.0,4.3,5.0,2.5,size=13,color=WHITE)

# ════════════════════════════════════════════════════════════════
# SLIDE 7 – Feature Analysis scatter plots
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Feature Analysis","Scatter plots — individual feature vs exam score")
img(sl,f"{A}/06_study_vs_score.png",0.3,1.05,6.3,3.0)
img(sl,f"{A}/14_sleep_vs_score.png",6.7,1.05,6.3,3.0)
img(sl,f"{A}/15_mental_health_violin.png",0.3,4.2,12.6,3.1)

# ════════════════════════════════════════════════════════════════
# SLIDE 8 – Feature Engineering
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Feature Engineering","Selecting the 6 most impactful features")
img(sl,f"{A}/09_feature_importance.png",0.3,1.05,7.2,3.5)
# feature cards
feats = [
    ("study_hours_per_day","Strongest predictor","#4361EE"),
    ("mental_health_rating","Cognitive readiness","#7209B7"),
    ("attendance_percentage","Classroom engagement","#F72585"),
    ("social_media_hours","Distraction factor (-)","#480CA8"),
    ("sleep_hours","Recovery & focus","#4CC9F0"),
    ("exercise_frequency","Physical wellbeing","#2DC653"),
]
for i,(feat,desc,col) in enumerate(feats):
    r=i%3; c=i//3
    lx=7.7+c*2.8; ty=1.1+r*1.95
    box=sl.shapes.add_shape(1,Inches(lx),Inches(ty),Inches(2.6),Inches(1.7))
    box.fill.solid(); box.fill.fore_color.rgb=RGBColor.from_string(col[1:])
    box.line.fill.background()
    txbox(sl,feat,lx+0.1,ty+0.1,2.4,0.6,size=11,bold=True,color=WHITE)
    txbox(sl,desc,lx+0.1,ty+0.75,2.4,0.6,size=10,color=LGRAY)
txbox(sl,
    "Strategy: Ensemble Mixed Selection\n"
    "Balanced statistical dependency + Pearson correlation\n"
    "→ 6 features selected from 14 candidates",
    0.3,4.7,7.0,2.3,size=13,color=WHITE)

# ════════════════════════════════════════════════════════════════
# SLIDE 9 – Model Training
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Model Training","4 algorithms benchmarked with GridSearchCV (5-fold CV)")
models_info = [
    ("Linear Regression","Baseline model\nNo hyperparameters\nFast & interpretable","#4361EE"),
    ("Decision Tree","max_depth: [3,5,10]\nmin_samples_split: [2,5]\nNon-linear splits","#7209B7"),
    ("Random Forest","n_estimators: [50,100]\nmax_depth: [5,10]\nEnsemble of trees","#F72585"),
    ("XGBoost ★","Gradient boosting\nRegularization\nBEST PERFORMER","#2DC653"),
]
for i,(name,info,col) in enumerate(models_info):
    lx=0.4+i*3.2; ty=1.15
    box=sl.shapes.add_shape(1,Inches(lx),Inches(ty),Inches(3.0),Inches(2.5))
    box.fill.solid(); box.fill.fore_color.rgb=RGBColor.from_string(col[1:])
    box.line.fill.background()
    txbox(sl,name,lx+0.1,ty+0.1,2.8,0.55,size=14,bold=True,color=WHITE)
    txbox(sl,info, lx+0.1,ty+0.75,2.8,1.5,size=11,color=LGRAY)

txbox(sl,"Training Configuration",0.4,3.85,12.5,0.4,size=14,bold=True,color=BLUE)
cfg = [
    "Train/Test Split: 80% / 20%  (727 / 182 samples)",
    "Cross-Validation: 5-Fold GridSearchCV",
    "Optimization Metric: neg_mean_squared_error",
    "Label Encoding applied to all categorical features",
    "No feature scaling needed for tree-based models",
]
for i,c in enumerate(cfg):
    txbox(sl,f"• {c}",0.5,4.35+i*0.42,12.3,0.42,size=12,color=WHITE)

# ════════════════════════════════════════════════════════════════
# SLIDE 10 – Model Evaluation: metrics table
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Model Evaluation","Quantitative comparison across all 4 models")
img(sl,f"{A}/10_model_comparison.png",0.3,1.05,12.7,3.2)
img(sl,f"{A}/11_metrics_grouped.png",0.3,4.35,12.7,2.95)

# ════════════════════════════════════════════════════════════════
# SLIDE 11 – XGBoost deep dive
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Best Model: XGBoost","Actual vs Predicted & Residual Analysis")
img(sl,f"{A}/12_xgb_actual_predicted.png",0.3,1.05,9.0,3.5)
metrics_box = [
    ("R² Score","0.8613"),("MAE","4.82"),
    ("RMSE","6.21"),("MAPE","7.84%"),
]
for i,(lab,val) in enumerate(metrics_box):
    bx=9.5; by=1.15+i*1.6
    box=sl.shapes.add_shape(1,Inches(bx),Inches(by),Inches(3.5),Inches(1.35))
    box.fill.solid(); box.fill.fore_color.rgb=BLUE
    box.line.fill.background()
    txbox(sl,lab,bx+0.1,by+0.05,3.3,0.5,size=12,bold=True,color=LGRAY,align=PP_ALIGN.CENTER)
    txbox(sl,val, bx+0.1,by+0.6, 3.3,0.6,size=26,bold=True,color=WHITE,align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# SLIDE 12 – Risk Classification
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Risk Classification System","Post-prediction risk level assignment")
img(sl,f"{A}/13_risk_distribution.png",0.3,1.05,6.2,4.5)
risk_info = [
    ("High Risk ⚠️",   "Score < 40",  "#EF233C", "Immediate intervention required"),
    ("Medium Risk 🟠",  "Score 40–60", "#F77F00", "Needs improvement to pass"),
    ("Low Risk 🟢",    "Score 60–80", "#4361EE", "Performing well, room to grow"),
    ("Excellent 🌟",   "Score ≥ 80",  "#2DC653", "Outstanding performance!"),
]
for i,(level,rng,col,desc) in enumerate(risk_info):
    ty=1.15+i*1.55
    box=sl.shapes.add_shape(1,Inches(6.7),Inches(ty),Inches(6.3),Inches(1.35))
    box.fill.solid(); box.fill.fore_color.rgb=RGBColor.from_string(col[1:])
    box.line.fill.background()
    txbox(sl,level,6.8,ty+0.05,4.0,0.5,size=14,bold=True,color=WHITE)
    txbox(sl,rng,  10.8,ty+0.05,2.0,0.5,size=12,color=WHITE,align=PP_ALIGN.RIGHT)
    txbox(sl,desc, 6.8,ty+0.65,6.0,0.5,size=11,color=LGRAY)

# ════════════════════════════════════════════════════════════════
# SLIDE 13 – Streamlit Deployment
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Deployment: Streamlit App","Interactive prediction dashboard")
side_bar(sl,GREEN,0.3)
features_used = [
    "study_hours_per_day","mental_health_rating",
    "attendance_percentage","social_media_hours",
    "sleep_hours","exercise_frequency",
]
txbox(sl,"App Features",0.6,1.15,6.0,0.45,size=16,bold=True,color=BLUE)
app_feats=[
    "Interactive sliders for all 6 input features",
    "Real-time exam score prediction",
    "Risk level badge (High / Medium / Low / Excellent)",
    "Model info panel with feature list & R² score",
    "Deployed via Streamlit Cloud",
]
for i,f in enumerate(app_feats):
    txbox(sl,f"✓  {f}",0.6,1.7+i*0.72,6.0,0.6,size=13,color=WHITE)
txbox(sl,"Input Features (6)",0.6,5.3,6.0,0.4,size=14,bold=True,color=PINK)
for i,f in enumerate(features_used):
    txbox(sl,f"→ {f}",0.6+3.0*(i//3),5.75+(i%3)*0.42,2.8,0.42,size=11,color=LGRAY)
# model pkl info
txbox(sl,"Saved Model",7.0,1.15,5.9,0.45,size=16,bold=True,color=BLUE)
pkl=[
    "best_student_model.pkl  — XGBoost (final)",
    "Trained with GridSearchCV best params",
    "Input shape: (n, 6)  |  Output: float (score)",
    "Loaded via: joblib.load()",
]
for i,p in enumerate(pkl):
    txbox(sl,f"• {p}",7.0,1.7+i*0.72,6.0,0.6,size=12,color=WHITE)
img(sl,f"{A}/09_feature_importance.png",7.0,4.0,6.0,3.3)

# ════════════════════════════════════════════════════════════════
# SLIDE 14 – GitHub & QR Code
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"GitHub Repository","Access full project source code & notebook")
side_bar(sl,BLUE,0.3)
img(sl,f"{A}/17_qr_code.png",0.6,1.3,4.0,4.0)
txbox(sl,"Scan to access the repo",0.6,5.35,4.0,0.5,size=13,color=LGRAY,align=PP_ALIGN.CENTER)
txbox(sl,"Repository Details",5.1,1.15,7.9,0.45,size=16,bold=True,color=BLUE)
repo_details=[
    "🔗  https://github.com/2024BTech029GarvSharma/ML-Student-Risk",
    "📁  ml_project.ipynb  — Full analysis notebook",
    "📁  ml.py  — Streamlit prediction app",
    "📁  best_student_model.pkl  — Trained XGBoost model",
    "📁  student_habits_performance.csv  — Dataset",
    "📁  README.md  — Project documentation",
]
for i,d in enumerate(repo_details):
    txbox(sl,d,5.1,1.75+i*0.75,7.8,0.65,size=13,color=WHITE)
txbox(sl,"Tech Stack",5.1,6.1,7.9,0.4,size=14,bold=True,color=PINK)
txbox(sl,"Python · Pandas · Scikit-learn · XGBoost · Matplotlib · Seaborn · Streamlit · Joblib",
      5.1,6.55,7.8,0.5,size=12,color=LGRAY)

# ════════════════════════════════════════════════════════════════
# SLIDE 15 – Conclusion
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
slide_header(sl,"Conclusion & Future Work","Key takeaways and next steps")
conclusions = [
    ("✅","Best Model","XGBoost achieved R²=0.8613, MAE=4.82 — best overall balance"),
    ("✅","Key Drivers","Study hours, mental health & attendance drive performance most"),
    ("✅","Risk System","4-tier risk classifier enables proactive student intervention"),
    ("✅","Deployment","Live Streamlit app for real-time predictions"),
]
future = [
    "Deep learning models (LSTM for longitudinal tracking)",
    "Real-time data pipeline integration with LMS",
    "Expand dataset to 10,000+ students across institutions",
    "Add explainability layer with SHAP values",
    "Mobile app deployment for student self-assessment",
]
for i,(ico,title,desc) in enumerate(conclusions):
    ty=1.15+i*1.35
    box=sl.shapes.add_shape(1,Inches(0.4),Inches(ty),Inches(7.5),Inches(1.15))
    box.fill.solid(); box.fill.fore_color.rgb=RGBColor(0x1a,0x2a,0x4a)
    box.line.color.rgb=BLUE
    txbox(sl,f"{ico} {title}",0.55,ty+0.05,7.2,0.45,size=14,bold=True,color=BLUE)
    txbox(sl,desc,0.55,ty+0.58,7.2,0.45,size=12,color=WHITE)

txbox(sl,"Future Roadmap",8.2,1.1,4.9,0.45,size=15,bold=True,color=PINK)
for i,f in enumerate(future):
    txbox(sl,f"→ {f}",8.2,1.65+i*0.98,4.8,0.85,size=12,color=WHITE)

# ════════════════════════════════════════════════════════════════
# SLIDE 16 – Thank You
# ════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK); bg(sl, DARK)
side_bar(sl,BLUE,0.7)
grad2=sl.shapes.add_shape(1,Inches(0.7),Inches(0),Inches(4.5),Inches(7.5))
grad2.fill.solid(); grad2.fill.fore_color.rgb=RGBColor(0x1a,0x2a,0x4a)
grad2.line.fill.background()
txbox(sl,"Thank You!",1.4,1.8,11,1.2,size=52,bold=True,color=WHITE)
txbox(sl,"Garv Sharma  |  2024BTech029  |  B.Tech CSE (AI)",
      1.4,3.2,11,0.6,size=18,color=LGRAY)
txbox(sl,"JK Lakshmipat University, Jaipur",1.4,3.9,11,0.5,size=15,color=LGRAY)
divider(sl,4.6,PINK)
txbox(sl,"github.com/2024BTech029GarvSharma/ML-Student-Risk",
      1.4,4.75,8.5,0.55,size=14,color=RGBColor(0x4C,0xC9,0xF0))
img(sl,f"{A}/17_qr_code.png",10.3,4.3,2.7)

prs.save(OUT_PPT)
print(f"Saved: {OUT_PPT}")
