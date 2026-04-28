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
import warnings
warnings.filterwarnings("ignore")

OUT = "ppt_assets"
df = pd.read_csv("student_habits_performance.csv").dropna()

# Encode categoricals
le = LabelEncoder()
cat_cols = ['gender','part_time_job','diet_quality','parental_education_level','internet_quality','extracurricular_participation']
df_enc = df.copy()
for c in cat_cols:
    df_enc[c] = le.fit_transform(df_enc[c])

features = ['study_hours_per_day','social_media_hours','netflix_hours','attendance_percentage',
            'sleep_hours','exercise_frequency','mental_health_rating','age',
            'gender','part_time_job','diet_quality','parental_education_level','internet_quality','extracurricular_participation']
X = df_enc[features]
y = df_enc['exam_score']

BLUE = '#4361EE'
PINK = '#F72585'
PURPLE = '#7209B7'
GREEN = '#2DC653'

# ═══ 1. Mutual Information Gain ═══
mi = mutual_info_regression(X, y, random_state=42)
mi_series = pd.Series(mi, index=features).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(5.5, 4))
colors = [BLUE if v > mi_series.median() else '#A0B4F0' for v in mi_series.values]
bars = ax.barh(mi_series.index, mi_series.values, color=colors, edgecolor='white', height=0.6)
ax.bar_label(bars, fmt='%.3f', padding=3, fontsize=7, fontweight='bold')
ax.set_title('Feature Ranking — Mutual Information Gain', fontweight='bold', fontsize=10)
ax.set_xlabel('MI Score', fontweight='bold', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(mi_series.median(), color=PINK, ls='--', lw=1.5, label=f'Median={mi_series.median():.3f}')
ax.legend(fontsize=7)
plt.tight_layout()
plt.savefig(f"{OUT}/fa_mutual_info.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_mutual_info.png")

# ═══ 2. Random Forest Feature Importance ═══
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X, y)
imp = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(5.5, 4))
colors2 = [PURPLE if v > imp.median() else '#C4A8E0' for v in imp.values]
bars2 = ax.barh(imp.index, imp.values, color=colors2, edgecolor='white', height=0.6)
ax.bar_label(bars2, fmt='%.3f', padding=3, fontsize=7, fontweight='bold')
ax.set_title('Feature Ranking — Random Forest Importance', fontweight='bold', fontsize=10)
ax.set_xlabel('Importance Score', fontweight='bold', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(imp.median(), color=PINK, ls='--', lw=1.5, label=f'Median={imp.median():.3f}')
ax.legend(fontsize=7)
plt.tight_layout()
plt.savefig(f"{OUT}/fa_rf_importance.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_rf_importance.png")

# ═══ 3. Correlation Analysis ═══
corr = X.corrwith(y).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(5.5, 4))
colors3 = [GREEN if v > 0 else PINK for v in corr.values]
bars3 = ax.barh(corr.index, corr.values, color=colors3, edgecolor='white', height=0.6)
ax.bar_label(bars3, fmt='%.3f', padding=3, fontsize=7, fontweight='bold')
ax.set_title('Feature Ranking — Pearson Correlation', fontweight='bold', fontsize=10)
ax.set_xlabel('Correlation (r)', fontweight='bold', fontsize=8)
ax.tick_params(labelsize=7)
ax.axvline(0, color='black', lw=0.8)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GREEN, label='Positive'), Patch(color=PINK, label='Negative')], fontsize=7)
plt.tight_layout()
plt.savefig(f"{OUT}/fa_correlation.png", dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("  saved fa_correlation.png")

print("\nAll 3 feature analysis charts done!")
