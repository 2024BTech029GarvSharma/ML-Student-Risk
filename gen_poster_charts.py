import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

OUT = "ppt_assets"
PALETTE = ["#4361EE","#F72585","#7209B7","#3A0CA3","#4CC9F0","#2DC653"]

def savefig(name):
    plt.tight_layout()
    plt.savefig(f"{OUT}/{name}", dpi=180, bbox_inches='tight', transparent=False, facecolor='white')
    plt.close()
    print(f"  saved {name}")

# ── Model Accuracy vs R² grouped bar (poster version) ────────
models = ['Linear\nRegression','Decision\nTree','Random\nForest','XGBoost']
r2   = [0.8411, 0.7198, 0.7913, 0.8613]
mae  = [5.346,  6.800,  5.900,  4.82 ]

fig, ax = plt.subplots(figsize=(6,3.5))
x = np.arange(len(models))
w = 0.35
b1 = ax.bar(x - w/2, [v*100 for v in r2], w, label='R² Score (%)', color='#4361EE', edgecolor='white')
b2 = ax.bar(x + w/2, mae, w, label='MAE', color='#F72585', edgecolor='white')
ax.bar_label(b1, fmt='%.1f', padding=2, fontsize=8, fontweight='bold')
ax.bar_label(b2, fmt='%.2f', padding=2, fontsize=8, fontweight='bold')
ax.set_ylabel('Value', fontweight='bold')
ax.set_title('Model R² Score (%) vs MAE', fontweight='bold', fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(models, fontsize=8)
ax.legend(fontsize=8); ax.set_ylim(0, 100)
savefig("p_model_accuracy_bar.png")

# ── Metrics comparison table image (poster version) ──────────
fig, ax = plt.subplots(figsize=(6, 2.2))
ax.axis('off')
data = [
    ['Linear Regression', '0.8411', '6.497', '5.346', '8.56%'],
    ['Decision Tree',     '0.7198', '8.643', '6.800', '11.03%'],
    ['Random Forest',     '0.7913', '7.446', '5.900', '9.63%'],
    ['XGBoost ★',         '0.8613', '6.21',  '4.82',  '7.84%'],
]
cols = ['Model', 'R² Score', 'RMSE', 'MAE', 'MAPE']
tbl = ax.table(cellText=data, colLabels=cols, cellLoc='center', loc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.6)
for (r,c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor('#1B2A4A'); cell.set_text_props(color='white', fontweight='bold')
    elif r == 4:  # XGBoost row
        cell.set_facecolor('#E8F5E9'); cell.set_text_props(fontweight='bold')
    else:
        cell.set_facecolor('#F5F7FF' if r%2==0 else 'white')
    cell.set_edgecolor('#D0D5DD')
savefig("p_metrics_table.png")

# ── Pipeline flowchart (poster version, cleaner) ────────────
fig, ax = plt.subplots(figsize=(7, 1.8))
ax.axis('off')
steps = ["Data\nCollection","Data\nCleaning","EDA","Feature\nSelection","Model\nTraining","Evaluation\n& Deploy"]
colors_flow = ["#4361EE","#7209B7","#F72585","#3A0CA3","#4CC9F0","#2DC653"]
for i, (s, c) in enumerate(zip(steps, colors_flow)):
    rect = mpatches.FancyBboxPatch((i*1.8, 0.2), 1.5, 1.0,
                                    boxstyle="round,pad=0.08", linewidth=1.5,
                                    edgecolor='white', facecolor=c, alpha=0.92)
    ax.add_patch(rect)
    ax.text(i*1.8+0.75, 0.7, s, ha='center', va='center',
            fontsize=8, fontweight='bold', color='white')
    if i < len(steps)-1:
        ax.annotate("", xy=((i+1)*1.8-0.05, 0.7), xytext=(i*1.8+1.55, 0.7),
                    arrowprops=dict(arrowstyle="-|>", color='#333', lw=2))
ax.set_xlim(-0.15, 11); ax.set_ylim(0, 1.5)
savefig("p_pipeline.png")

# ── Feature selection reasoning table ──────────────────────
fig, ax = plt.subplots(figsize=(5.5, 3))
ax.axis('off')
data2 = [
    ['study_hours_per_day',    '0.83', 'Strong +ve driver of scores'],
    ['mental_health_rating',   '0.49', 'Cognitive wellness factor'],
    ['attendance_percentage',  '0.58', 'Engagement measure'],
    ['social_media_hours',     '-0.31','Distraction (negative)'],
    ['sleep_hours',            '0.35', 'Rest & recovery impact'],
    ['exercise_frequency',     '0.28', 'Physical well-being'],
]
cols2 = ['Feature', 'Corr (r)', 'Reason Selected']
tbl2 = ax.table(cellText=data2, colLabels=cols2, cellLoc='center', loc='center',
               colWidths=[0.42, 0.18, 0.4])
tbl2.auto_set_font_size(False); tbl2.set_fontsize(8.5); tbl2.scale(1, 1.65)
for (r,c), cell in tbl2.get_celld().items():
    if r == 0:
        cell.set_facecolor('#1B2A4A'); cell.set_text_props(color='white', fontweight='bold')
    elif c == 1 and r > 0:
        val = float(data2[r-1][1])
        cell.set_facecolor('#E8F5E9' if val > 0 else '#FFEBEE')
        cell.set_text_props(fontweight='bold', color='#2E7D32' if val > 0 else '#C62828')
    else:
        cell.set_facecolor('#F5F7FF' if r%2==0 else 'white')
    cell.set_edgecolor('#D0D5DD')
ax.set_title('Feature Selection — Ensemble Mixed Strategy', fontweight='bold', fontsize=10, pad=8)
savefig("p_feature_table.png")

# ── Risk distribution bar (poster version) ──────────────
labels = ['High Risk\n(< 40)','Medium Risk\n(40–60)','Low Risk\n(60–80)','Excellent\n(≥ 80)']
counts = [47, 182, 380, 300]  # approximate from dataset
colors_r = ['#EF233C','#F77F00','#4361EE','#2DC653']
fig, ax = plt.subplots(figsize=(5, 3))
bars = ax.bar(labels, counts, color=colors_r, edgecolor='white', width=0.55)
ax.bar_label(bars, padding=3, fontsize=9, fontweight='bold')
ax.set_title('Student Risk Level Distribution', fontweight='bold', fontsize=11)
ax.set_ylabel('Count')
savefig("p_risk_bar.png")

print("\nExtra poster assets done!")
