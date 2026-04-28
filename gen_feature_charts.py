import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

OUT = "ppt_assets"
df = pd.read_csv("student_habits_performance.csv").dropna()
target = 'exam_score'
PALETTE = ["#4361EE","#F72585","#7209B7","#3A0CA3","#4CC9F0","#2DC653"]
sns.set_theme(style="whitegrid", palette=PALETTE)

def savefig(name):
    plt.tight_layout()
    plt.savefig(f"{OUT}/{name}", dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  saved {name}")

# 1. Attendance vs Score scatter
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.scatter(df['attendance_percentage'], df[target], alpha=0.4, color='#4361EE', s=20, edgecolors='white', lw=0.3)
m, b = np.polyfit(df['attendance_percentage'], df[target], 1)
x = np.linspace(df['attendance_percentage'].min(), df['attendance_percentage'].max(), 200)
ax.plot(x, m*x+b, color='#F72585', lw=2, label=f'Trend (r=0.58)')
ax.set_title("Attendance % vs Exam Score", fontweight='bold', fontsize=10)
ax.set_xlabel("Attendance %"); ax.set_ylabel("Exam Score"); ax.legend(fontsize=8)
savefig("f_attendance_vs_score.png")

# 2. Social Media vs Score scatter
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.scatter(df['social_media_hours'], df[target], alpha=0.4, color='#7209B7', s=20, edgecolors='white', lw=0.3)
m2, b2 = np.polyfit(df['social_media_hours'], df[target], 1)
x2 = np.linspace(df['social_media_hours'].min(), df['social_media_hours'].max(), 200)
ax.plot(x2, m2*x2+b2, color='#F72585', lw=2, label=f'Trend (r=-0.31)')
ax.set_title("Social Media Hours vs Exam Score", fontweight='bold', fontsize=10)
ax.set_xlabel("Social Media Hours"); ax.set_ylabel("Exam Score"); ax.legend(fontsize=8)
savefig("f_social_media_vs_score.png")

# 3. Correlation heatmap (compact, poster-friendly)
num_cols = ['study_hours_per_day','attendance_percentage','mental_health_rating',
            'sleep_hours','exercise_frequency','social_media_hours','netflix_hours','exam_score']
fig, ax = plt.subplots(figsize=(5.5, 4.5))
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            linewidths=0.5, ax=ax, cbar_kws={'shrink':0.7}, annot_kws={'size':7})
ax.set_title("Correlation Heatmap", fontweight='bold', fontsize=10)
ax.tick_params(labelsize=7)
savefig("f_heatmap.png")

# 4. Exam score distribution (compact)
fig, ax = plt.subplots(figsize=(5, 3))
ax.hist(df[target], bins=30, color='#4361EE', edgecolor='white', alpha=0.85)
ax.axvline(df[target].mean(), color='#F72585', lw=2, ls='--', label=f'Mean={df[target].mean():.1f}')
ax.set_title("Exam Score Distribution", fontweight='bold', fontsize=10)
ax.set_xlabel("Exam Score"); ax.set_ylabel("Frequency"); ax.legend(fontsize=8)
savefig("f_exam_dist.png")

# 5. Exercise frequency vs Score
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.scatter(df['exercise_frequency'], df[target], alpha=0.4, color='#2DC653', s=20, edgecolors='white', lw=0.3)
m3, b3 = np.polyfit(df['exercise_frequency'], df[target], 1)
x3 = np.linspace(df['exercise_frequency'].min(), df['exercise_frequency'].max(), 200)
ax.plot(x3, m3*x3+b3, color='#F72585', lw=2, label=f'Trend (r=0.28)')
ax.set_title("Exercise Frequency vs Exam Score", fontweight='bold', fontsize=10)
ax.set_xlabel("Exercise (Days/Week)"); ax.set_ylabel("Exam Score"); ax.legend(fontsize=8)
savefig("f_exercise_vs_score.png")

# 6. 2x3 grid of ALL scatter plots (compact multi-plot)
features_scatter = [
    ('study_hours_per_day', 'Study Hours/Day', '#4361EE', '0.83'),
    ('attendance_percentage', 'Attendance %', '#3A0CA3', '0.58'),
    ('mental_health_rating', 'Mental Health', '#7209B7', '0.49'),
    ('sleep_hours', 'Sleep Hours', '#4CC9F0', '0.35'),
    ('exercise_frequency', 'Exercise Freq', '#2DC653', '0.28'),
    ('social_media_hours', 'Social Media Hrs', '#F72585', '-0.31'),
]
fig, axes = plt.subplots(2, 3, figsize=(12, 6.5))
axes = axes.ravel()
for i, (col, label, color, r_val) in enumerate(features_scatter):
    axes[i].scatter(df[col], df[target], alpha=0.35, color=color, s=12, edgecolors='white', lw=0.2)
    m_, b_ = np.polyfit(df[col], df[target], 1)
    xl = np.linspace(df[col].min(), df[col].max(), 200)
    axes[i].plot(xl, m_*xl+b_, color='#EF233C', lw=2)
    axes[i].set_title(f"{label} vs Score (r={r_val})", fontweight='bold', fontsize=9)
    axes[i].set_xlabel(label, fontsize=8)
    axes[i].set_ylabel("Exam Score", fontsize=8)
    axes[i].tick_params(labelsize=7)
savefig("f_all_scatter_grid.png")

print("\nAll feature analysis charts done!")
