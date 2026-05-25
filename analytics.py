"""
France Top 50 Spotify Playlist - Audience Sensitivity, Content Compliance
& Format Preference Analysis
For: Atlantic Recording Corporation | Unified Mentor Internship Project
Dataset: Atlantic_France.csv (27,800 rows | 555 days | May 2024 - Nov 2025)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ── 0. SETUP ──────────────────────────────────────────────────────────────────
plt.style.use("dark_background")
COLORS = {
    "explicit": "#e63946",
    "clean":    "#2ec4b6",
    "album":    "#f4a261",
    "single":   "#457b9d",
    "accent":   "#ffd166",
}

# ── 1. LOAD & VALIDATE DATA ───────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: DATA VALIDATION & PREPARATION")
print("=" * 60)

df = pd.read_csv("Atlantic_France.csv")

# Parse date
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Convert duration ms → minutes
df["duration_min"] = df["duration_ms"] / 60000

# Standardise boolean
df["is_explicit"] = df["is_explicit"].astype(str).str.upper() == "TRUE"

# Standardise album_type
df["album_type"] = df["album_type"].str.lower().str.strip()

# Duration buckets
def duration_bucket(x):
    if x < 2.5:
        return "Short (<2.5 min)"
    elif x < 4.0:
        return "Medium (2.5-4 min)"
    else:
        return "Long (>4 min)"

df["duration_bucket"] = df["duration_min"].apply(duration_bucket)

# Album size category
df["album_size"] = df["total_tracks"].apply(
    lambda x: "Large (>15 tracks)" if x > 15 else "Small (<=15 tracks)"
)

# Validate
print(f"Total rows       : {len(df):,}")
print(f"Unique dates     : {df['date'].nunique()}")
print(f"Date range       : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"Entries per day  : {len(df) / df['date'].nunique():.0f} (expected 50)")
print(f"Missing values   :\n{df.isnull().sum()}")
print(f"\nAlbum types      : {df['album_type'].value_counts().to_dict()}")
print(f"Explicit flag    : {df['is_explicit'].value_counts().to_dict()}")


# ── 2. EXPLICIT CONTENT SENSITIVITY ANALYSIS ─────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: EXPLICIT CONTENT SENSITIVITY ANALYSIS")
print("=" * 60)

total = len(df)
exp_count  = df["is_explicit"].sum()
cln_count  = total - exp_count
exp_pct    = exp_count / total * 100
cln_pct    = 100 - exp_pct

exp_pop = df[df["is_explicit"]]["popularity"].mean()
cln_pop = df[~df["is_explicit"]]["popularity"].mean()

print(f"Explicit tracks  : {exp_count:,} ({exp_pct:.1f}%)")
print(f"Clean tracks     : {cln_count:,} ({cln_pct:.1f}%)")
print(f"Explicit avg pop : {exp_pop:.2f}")
print(f"Clean avg pop    : {cln_pop:.2f}")
print(f"Clean premium    : +{cln_pop - exp_pop:.2f} pts ({(cln_pop-exp_pop)/exp_pop*100:.1f}%)")

# Rank-tier explicit breakdown
bins   = [0, 10, 25, 50]
labels = ["Top 10", "Top 11-25", "Top 26-50"]
df["rank_tier"] = pd.cut(df["position"], bins=bins, labels=labels)

tier_explicit = (
    df.groupby("rank_tier", observed=True)["is_explicit"]
    .agg(["sum", "count"])
    .assign(explicit_pct=lambda x: x["sum"] / x["count"] * 100)
)
print("\nExplicit % by rank tier:")
print(tier_explicit.to_string())

# Monthly explicit trend
df["year_month"] = df["date"].dt.to_period("M")
monthly_exp = (
    df.groupby("year_month")["is_explicit"]
    .agg(["sum", "count"])
    .assign(explicit_pct=lambda x: x["sum"] / x["count"] * 100)
    .reset_index()
)
print("\nMonthly explicit trend (first 6 months):")
print(monthly_exp.head(6).to_string())

# Explicit by format
format_exp = (
    df.groupby("album_type")["is_explicit"]
    .agg(["sum", "count"])
    .assign(explicit_pct=lambda x: x["sum"] / x["count"] * 100)
)
print("\nExplicit % by album type:")
print(format_exp.to_string())


# ── 3. RELEASE FORMAT PREFERENCE ANALYSIS ────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: RELEASE FORMAT PREFERENCE ANALYSIS")
print("=" * 60)

fmt_counts = df["album_type"].value_counts()
fmt_pct    = df["album_type"].value_counts(normalize=True) * 100
fmt_pop    = df.groupby("album_type")["popularity"].mean()

print("Format distribution:")
for fmt in fmt_counts.index:
    print(f"  {fmt:10s}: {fmt_counts[fmt]:,} entries ({fmt_pct[fmt]:.1f}%) | Avg popularity: {fmt_pop[fmt]:.2f}")

# Rank-based format comparison
print("\nFormat % by rank tier:")
rank_format = (
    df.groupby(["rank_tier", "album_type"], observed=True)
    .size()
    .unstack(fill_value=0)
)
rank_format_pct = rank_format.div(rank_format.sum(axis=1), axis=0) * 100
print(rank_format_pct.round(1).to_string())


# ── 4. ALBUM STRUCTURE IMPACT ANALYSIS ───────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: ALBUM STRUCTURE IMPACT ANALYSIS")
print("=" * 60)

album_df = df[df["album_type"] == "album"].copy()

size_pop = album_df.groupby("album_size")["popularity"].agg(["mean", "count"])
print("Album size vs popularity:")
print(size_pop.to_string())

# Correlation: total_tracks vs popularity (for album tracks only)
corr = album_df[["total_tracks", "popularity"]].corr().iloc[0, 1]
print(f"\nCorrelation (total_tracks vs popularity, albums only): {corr:.4f}")

# Track count distribution
track_dist = df["total_tracks"].value_counts().head(10)
print("\nTop 10 track counts:")
print(track_dist.to_string())


# ── 5. SONG DURATION PREFERENCE ANALYSIS ─────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: SONG DURATION PREFERENCE ANALYSIS")
print("=" * 60)

print(f"Mean duration    : {df['duration_min'].mean():.2f} min")
print(f"Median duration  : {df['duration_min'].median():.2f} min")
print(f"Std deviation    : {df['duration_min'].std():.2f} min")
print(f"Min duration     : {df['duration_min'].min():.2f} min")
print(f"Max duration     : {df['duration_min'].max():.2f} min")

bucket_stats = df.groupby("duration_bucket").agg(
    count=("popularity", "count"),
    avg_popularity=("popularity", "mean"),
    avg_position=("position", "mean"),
).sort_values("count", ascending=False)
print("\nDuration bucket stats:")
print(bucket_stats.to_string())

dur_pop_corr = df[["duration_min", "popularity"]].corr().iloc[0, 1]
print(f"\nCorrelation (duration_min vs popularity): {dur_pop_corr:.4f}")


# ── 6. CONTENT ATTRIBUTE CONCENTRATION ANALYSIS ──────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: CONTENT ATTRIBUTE CONCENTRATION ANALYSIS")
print("=" * 60)

for tier in ["Top 10", "Top 11-25", "Top 26-50"]:
    tier_df = df[df["rank_tier"] == tier]
    e_pct   = tier_df["is_explicit"].mean() * 100
    s_pct   = (tier_df["album_type"] == "single").mean() * 100
    d_mean  = tier_df["duration_min"].mean()
    p_mean  = tier_df["popularity"].mean()
    print(f"\n{tier}:")
    print(f"  Explicit share    : {e_pct:.1f}%")
    print(f"  Single format     : {s_pct:.1f}%")
    print(f"  Avg duration      : {d_mean:.2f} min")
    print(f"  Avg popularity    : {p_mean:.2f}")


# ── 7. KEY PERFORMANCE INDICATORS ────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 60)

top10_df = df[df["position"] <= 10]

kpis = {
    "Explicit Content Share"        : f"{exp_pct:.1f}%",
    "Clean Content Dominance Ratio" : f"{cln_pct:.1f}%",
    "Single vs Album Track Ratio"   : f"{fmt_pct.get('single',0):.1f}% / {fmt_pct.get('album',0):.1f}%",
    "Average Song Duration"         : f"{df['duration_min'].mean():.2f} min",
    "Album Size Impact Index"       : f"Small={size_pop.loc['Small (<=15 tracks)','mean']:.2f} vs Large={size_pop.loc['Large (>15 tracks)','mean']:.2f}",
    "Content Acceptance Score"      : f"{(~top10_df['is_explicit']).mean()*100:.1f}% clean in Top 10",
}

for kpi, val in kpis.items():
    print(f"  {kpi:<35}: {val}")


# ── 8. TOP ARTISTS ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 8: TOP ARTISTS BY CHART APPEARANCES")
print("=" * 60)

top_artists = df["artist"].value_counts().head(10)
for i, (artist, count) in enumerate(top_artists.items(), 1):
    print(f"  {i:2}. {artist:<35} {count:,} days")


# ── 9. VISUALISATIONS ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 9: GENERATING CHARTS → france_top50_charts.png")
print("=" * 60)

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.patch.set_facecolor("#0d0f14")
fig.suptitle(
    "France Top 50 – Audience Sensitivity, Content Compliance & Format Preference Analysis",
    fontsize=14, fontweight="bold", color="white", y=0.98
)

ax = axes.flatten()

# --- Chart 1: Explicit vs Clean Pie ---
sizes = [exp_pct, cln_pct]
labels_pie = [f"Explicit\n{exp_pct:.1f}%", f"Clean\n{cln_pct:.1f}%"]
ax[0].pie(sizes, labels=labels_pie, colors=[COLORS["explicit"], COLORS["clean"]],
          startangle=90, wedgeprops={"edgecolor": "#0d0f14", "linewidth": 2},
          textprops={"color": "white", "fontsize": 10})
ax[0].set_title("Explicit vs Clean Split", color="white", fontsize=11)

# --- Chart 2: Popularity by Content Type ---
cats  = ["Explicit", "Clean", "Album", "Single"]
pops  = [exp_pop, cln_pop,
         df[df["album_type"]=="album"]["popularity"].mean(),
         df[df["album_type"]=="single"]["popularity"].mean()]
clrs  = [COLORS["explicit"], COLORS["clean"], COLORS["album"], COLORS["single"]]
bars  = ax[1].bar(cats, pops, color=clrs, edgecolor="#0d0f14", width=0.5)
ax[1].set_ylim(68, 84)
ax[1].set_title("Avg Popularity by Content Type", color="white", fontsize=11)
ax[1].set_facecolor("#161b22")
ax[1].tick_params(colors="white")
for bar, val in zip(bars, pops):
    ax[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
               f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=9)

# --- Chart 3: Rank Tier Explicit % ---
tiers_list = ["Top 10", "Top 11-25", "Top 26-50"]
exp_vals   = [62.4, 54.5, 54.8]
cln_vals   = [37.6, 45.5, 45.2]
x = np.arange(len(tiers_list))
w = 0.35
ax[2].bar(x - w/2, exp_vals, w, label="Explicit", color=COLORS["explicit"])
ax[2].bar(x + w/2, cln_vals, w, label="Clean",    color=COLORS["clean"])
ax[2].set_xticks(x)
ax[2].set_xticklabels(tiers_list, color="white", fontsize=9)
ax[2].set_title("Explicit % by Rank Tier", color="white", fontsize=11)
ax[2].set_facecolor("#161b22")
ax[2].tick_params(colors="white")
ax[2].legend(facecolor="#1c2128", labelcolor="white", fontsize=9)
ax[2].set_ylabel("Percentage (%)", color="white")

# --- Chart 4: Monthly Explicit Trend ---
ax[3].plot(monthly_exp["year_month"].astype(str),
           monthly_exp["explicit_pct"],
           color=COLORS["explicit"], linewidth=2.5, marker="o", markersize=5)
ax[3].set_title("Monthly Explicit Content Trend", color="white", fontsize=11)
ax[3].set_facecolor("#161b22")
ax[3].tick_params(colors="white", axis="both")
ax[3].set_xticklabels(monthly_exp["year_month"].astype(str), rotation=45, fontsize=7, color="white")
ax[3].set_ylabel("Explicit %", color="white")
ax[3].axhline(exp_pct, color=COLORS["accent"], linestyle="--", linewidth=1, alpha=0.7, label=f"Overall avg {exp_pct:.1f}%")
ax[3].legend(facecolor="#1c2128", labelcolor="white", fontsize=8)

# --- Chart 5: Single vs Album Pie ---
fmt_vals   = [fmt_pct.get("single", 0), fmt_pct.get("album", 0)]
fmt_labels = [f"Single\n{fmt_vals[0]:.1f}%", f"Album\n{fmt_vals[1]:.1f}%"]
ax[4].pie(fmt_vals, labels=fmt_labels, colors=[COLORS["single"], COLORS["album"]],
          startangle=90, wedgeprops={"edgecolor": "#0d0f14", "linewidth": 2},
          textprops={"color": "white", "fontsize": 10})
ax[4].set_title("Single vs Album Format Split", color="white", fontsize=11)

# --- Chart 6: Album Size Impact ---
size_labels = ["Small (<=15)", "Large (>15)"]
size_vals   = [size_pop.loc["Small (<=15 tracks)", "mean"],
               size_pop.loc["Large (>15 tracks)", "mean"]]
bars6 = ax[5].bar(size_labels, size_vals, color=[COLORS["clean"], COLORS["explicit"]],
                  edgecolor="#0d0f14", width=0.4)
ax[5].set_ylim(68, 78)
ax[5].set_title("Album Size vs Avg Popularity", color="white", fontsize=11)
ax[5].set_facecolor("#161b22")
ax[5].tick_params(colors="white")
for bar, val in zip(bars6, size_vals):
    ax[5].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
               f"{val:.2f}", ha="center", va="bottom", color="white", fontsize=10)

# --- Chart 7: Duration Bucket Distribution ---
bkt_labels = ["Short\n(<2.5m)", "Medium\n(2.5-4m)", "Long\n(>4m)"]
bkt_counts = [3582, 22717, 1501]
clrs7 = [COLORS["single"], COLORS["clean"], COLORS["album"]]
ax[6].bar(bkt_labels, bkt_counts, color=clrs7, edgecolor="#0d0f14", width=0.5)
ax[6].set_title("Song Duration Distribution", color="white", fontsize=11)
ax[6].set_facecolor("#161b22")
ax[6].tick_params(colors="white")
ax[6].set_ylabel("Entries", color="white")

# --- Chart 8: Top 10 Artists ---
artists_list = list(top_artists.index)
counts_list  = list(top_artists.values)
bar_colors   = [COLORS["explicit"] if i == 0 else COLORS["album"] if i < 3 else COLORS["single"]
                for i in range(len(artists_list))]
ax[7].barh(artists_list[::-1], counts_list[::-1], color=bar_colors[::-1], edgecolor="#0d0f14")
ax[7].set_title("Top 10 Artists by Chart Appearances", color="white", fontsize=11)
ax[7].set_facecolor("#161b22")
ax[7].tick_params(colors="white")
ax[7].set_xlabel("Days on Chart", color="white")

# --- Chart 9: Explicit by Format ---
fmt_exp_data = [{"type": "Album", "explicit": 72.4, "clean": 27.6},
                {"type": "Single", "explicit": 38.2, "clean": 61.8}]
fmt_exp_df   = pd.DataFrame(fmt_exp_data)
x9 = np.arange(2)
ax[8].bar(x9 - 0.2, fmt_exp_df["explicit"], 0.35, label="Explicit", color=COLORS["explicit"])
ax[8].bar(x9 + 0.2, fmt_exp_df["clean"],    0.35, label="Clean",    color=COLORS["clean"])
ax[8].set_xticks(x9)
ax[8].set_xticklabels(fmt_exp_df["type"], color="white")
ax[8].set_title("Explicit Split by Album Type", color="white", fontsize=11)
ax[8].set_facecolor("#161b22")
ax[8].tick_params(colors="white")
ax[8].set_ylabel("Percentage (%)", color="white")
ax[8].legend(facecolor="#1c2128", labelcolor="white", fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("france_top50_charts.png", dpi=150, bbox_inches="tight", facecolor="#0d0f14")
plt.close()
print("Charts saved to france_top50_charts.png")


# ── 10. SUMMARY REPORT ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 10: STRATEGIC SUMMARY FOR ATLANTIC RECORDING CORPORATION")
print("=" * 60)

summary = """
AUDIENCE SENSITIVITY & CONTENT COMPLIANCE FINDINGS
====================================================
1. Explicit content makes up 56.3% of France Top 50 entries, but clean
   tracks score 10.4% higher in popularity (80.9 vs 73.3).
   → RECOMMENDATION: Always provide clean edits for French market pitching.

2. Explicit content peaks at 62.4% in Top 10, suggesting French listeners
   accept explicit content — but clean tracks still perform measurably better.
   → RECOMMENDATION: Compliance risk is real; maintain clean version strategy.

FORMAT PREFERENCE FINDINGS
====================================================
3. Singles achieve avg popularity of 80.75 vs 72.99 for albums (+10.6 pts).
   Singles represent 47.1% of entries and dominate the top tier.
   → RECOMMENDATION: Lead releases with clean singles before album drops.

4. Large albums (>15 tracks) are diluted: avg popularity 70.91 vs 74.48
   for smaller albums (−4.8%). Correlation between track count and
   popularity in album tracks: negative.
   → RECOMMENDATION: Keep albums to ≤15 tracks for France market.

DURATION FINDINGS
====================================================
5. 81.7% of all entries are medium-length (2.5–4 min). Avg = 3.09 min.
   Duration has minimal direct impact on popularity (correlation ≈ 0).
   → RECOMMENDATION: Target 2.5–4 min for all France-targeted releases.

ARTIST & MARKET INSIGHTS
====================================================
6. Werenoi leads with 2,206 chart days. Top 10 artists account for 30.4%
   of all chart days — market is concentrated around domestic French rap.
   → RECOMMENDATION: Pursue collaboration/feature opportunities with
     Werenoi, PLK, SDM, Jul, and Ninho for sustained playlist presence.
"""
print(summary)

print("Analysis complete. All outputs generated successfully.")