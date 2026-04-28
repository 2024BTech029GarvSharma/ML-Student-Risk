import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings("ignore")

OUT = "ppt_assets"
df = pd.read_csv("student_habits_performance.csv").dropna()

le = LabelEncoder()
cat_cols = ['gender','part_time_job','diet_quality','parental_education_level','internet_quality','extracurricular_participation']
df_enc = df.copy()
for c in cat_cols:
    df_enc[c] = le.fit_transform(df_enc[c])

features = ['study_hours_per_day','social_media_hours','netflix_hours','attendance_percentage',
            'sleep_hours','exercise_frequency','mental_health_rating','age',
            'gender','part_time_job','diet_quality','parental_education_level','internet_quality','extracurricular_participation']
feat6 = ['study_hours_per_day','mental_health_rating','attendance_percentage','social_media_hours','sleep_hours','exercise_frequency']
X = df_enc[features]; y = df_enc['exam_score']

BLUE='#4361EE'; PINK='#F72585'; PURPLE='#7209B7'; GREEN='#2DC653'; CYAN='#4CC9F0'; DARK='#3A0CA3'

# ═══════════════════════════════════════════════════════
# 1. Combined 3-in-1 Feature Analysis (side by side)
# ═══════════════════════════════════════════════════════
mi = mutual_info_regression(X, y, random_state=42)
mi_s = pd.Series(mi, index=features).sort_values(ascending=True)

rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X, y)
imp_s = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)

corr_s = X.corrwith(y).sort_values(ascending=True)

fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
fig.suptitle('Feature Analysis — Three Selection Methods Compared', fontweight='bold', fontsize=13, y=0.98)

# MI
ax = axes[0]
colors_mi = [BLUE if v > mi_s.median() else '#A0B4F0' for v in mi_s.values]
bars1 = ax.barh(mi_s.index, mi_s.values, color=colors_mi, edgecolor='white', height=0.65)
ax.bar_label(bars1, fmt='%.3f', padding=3, fontsize=6.5, fontweight='bold')
ax.set_title('Mutual Information Gain', fontweight='bold', fontsize=10, color=BLUE)
ax.set_xlabel('MI Score', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(mi_s.median(), color=PINK, ls='--', lw=1.2, alpha=0.7)

# RF
ax = axes[1]
colors_rf = [PURPLE if v > imp_s.median() else '#C4A8E0' for v in imp_s.values]
bars2 = ax.barh(imp_s.index, imp_s.values, color=colors_rf, edgecolor='white', height=0.65)
ax.bar_label(bars2, fmt='%.3f', padding=3, fontsize=6.5, fontweight='bold')
ax.set_title('Random Forest Importance', fontweight='bold', fontsize=10, color=PURPLE)
ax.set_xlabel('Importance', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(imp_s.median(), color=PINK, ls='--', lw=1.2, alpha=0.7)

# Correlation
ax = axes[2]
colors_c = [GREEN if v > 0 else PINK for v in corr_s.values]
bars3 = ax.barh(corr_s.index, corr_s.values, color=colors_c, edgecolor='white', height=0.65)
ax.bar_label(bars3, fmt='%.3f', padding=3, fontsize=6.5, fontweight='bold')
ax.set_title('Pearson Correlation', fontweight='bold', fontsize=10, color=GREEN)
ax.set_xlabel('Correlation (r)', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(0, color='black', lw=0.8)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GREEN,label='+ve'), Patch(color=PINK,label='-ve')], fontsize=7, loc='lower right')

plt.tight_layout(rect=[0,0,1,0.95])
plt.savefig(f"{OUT}/fa_combined_3in1.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_combined_3in1.png")

# ═══════════════════════════════════════════════════════
# 2. Risk Classification Pie Chart
# ═══════════════════════════════════════════════════════
scores = df['exam_score']
risk_counts = {
    'High Risk\n(< 40)': (scores < 40).sum(),
    'Medium Risk\n(40–60)': ((scores >= 40) & (scores < 60)).sum(),
    'Low Risk\n(60–80)': ((scores >= 60) & (scores < 80)).sum(),
    'Excellent\n(≥ 80)': (scores >= 80).sum(),
}
print("Risk distribution:", {k.replace('\n',' '): v for k,v in risk_counts.items()})

fig, ax = plt.subplots(figsize=(6, 4.5))
colors_pie = ['#EF233C','#F77F00',BLUE,GREEN]
wedges, texts, autotexts = ax.pie(
    risk_counts.values(), labels=risk_counts.keys(), autopct='%1.1f%%',
    colors=colors_pie, startangle=140,
    wedgeprops=dict(edgecolor='white', linewidth=2),
    pctdistance=0.75, labeldistance=1.12
)
for t in texts: t.set_fontsize(9); t.set_fontweight('bold')
for a in autotexts: a.set_fontsize(9); a.set_fontweight('bold'); a.set_color('white')
ax.set_title('Student Risk Level Distribution', fontweight='bold', fontsize=11)

# Add count labels
total = sum(risk_counts.values())
legend_labels = [f"{k.replace(chr(10),' ')}: {v} ({v/total*100:.1f}%)" for k,v in risk_counts.items()]
ax.legend(legend_labels, loc='lower left', fontsize=7.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(f"{OUT}/fa_risk_pie.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_risk_pie.png")

# ═══════════════════════════════════════════════════════
# 3. Actual vs Predicted (XGBoost)
# ═══════════════════════════════════════════════════════
X6 = df_enc[feat6]; y6 = df_enc['exam_score']
X_train, X_test, y_train, y_test = train_test_split(X6, y6, test_size=0.2, random_state=42)

xgb = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"  XGBoost R² = {r2:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Actual vs Predicted scatter
ax = axes[0]
ax.scatter(y_test, y_pred, alpha=0.5, color=BLUE, edgecolors='white', lw=0.3, s=30)
lims = [min(y_test.min(), y_pred.min())-5, max(y_test.max(), y_pred.max())+5]
ax.plot(lims, lims, 'r--', lw=2, label='Perfect Prediction')
ax.set_xlabel('Actual Exam Score', fontweight='bold', fontsize=9)
ax.set_ylabel('Predicted Exam Score', fontweight='bold', fontsize=9)
ax.set_title(f'XGBoost — Actual vs Predicted\n(R² = {r2:.4f})', fontweight='bold', fontsize=10)
ax.legend(fontsize=8)
ax.set_xlim(lims); ax.set_ylim(lims)
ax.grid(True, alpha=0.3)

# Residual distribution
ax2 = axes[1]
residuals = y_test.values - y_pred
ax2.hist(residuals, bins=25, color=BLUE, edgecolor='white', alpha=0.85)
ax2.axvline(0, color='red', lw=2, ls='--', label='Zero Error')
ax2.axvline(residuals.mean(), color=PINK, lw=1.5, ls=':', label=f'Mean={residuals.mean():.2f}')
ax2.set_title('XGBoost — Residual Distribution', fontweight='bold', fontsize=10)
ax2.set_xlabel('Residuals (Actual - Predicted)', fontweight='bold', fontsize=9)
ax2.set_ylabel('Frequency', fontweight='bold', fontsize=9)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUT}/fa_actual_vs_predicted.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_actual_vs_predicted.png")

print("\nAll charts done!")
