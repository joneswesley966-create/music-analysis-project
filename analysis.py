import pandas as pd

df = pd.read_csv("Atlantic_France.csv")

#convert date
df['date'] = pd.to_datetime(df['date'])

#convert duration
df['duration_min'] =df['duration_ms'] / 60000

#convert explict to numeric
df['is_explicit'] =df['is_explicit'].astype(int)

#standerdize album type
df['album_type'] =df['album_type'].str.lower()

#validate 50 entries per day
entries_per_day = df.groupby('date').size()
print(entries_per_day.head())

explicit_share = df['is_explicit'].value_counts(normalize=True)
print(explicit_share)

rank_explicit = df.groupby('position') ['is_explicit'].mean()

popularity_compare = df.groupby('is_explicit') ['popularity'].mean()

format_count =df['album_type'].value_counts()
format_rank =df.groupby('album_type') ['position'].mean()
format_popularity =df.groupby('album_type') ['position'].mean()


#album size distribution
album_dist =df['total_tracks'].describe()

#album size vs popularity
album_impact =df.groupby('total_tracks') ['popularity'].mean()

#create categories
df['duration_category'] =pd.cut(df['duration_min'],

bins=[0,2.5,4,10],

labels=['short','medium','long'])

duration_dist =df['duration_category'].value_counts()
duration_popularity =df.groupby('duration_category') ['popularity'].mean()

#KPI 1: Explicit content share
explicit_kpi = df['is_explicit'].mean()

# KPI 2: Clean content Dominance
clean_kpi = 1 - explicit_kpi

#KPI 3: Single vs Album Ratio
format_kpi = df['album_type'].value_counts(normalize=True)

#KPI 4: Average Duration
avg_duration = df['duration_min'].mean()

print(explicit_kpi,clean_kpi,format_kpi,avg_duration)

import matplotlib.pyplot as plt

#Explicit vs Clean
df['is_explicit'].value_counts().plot(kind='bar')
plt.title("Explicit vs Clean Content")
plt.show()

#Album type
df['album_type'].value_counts().plot(kind='pie',autopct='%1.1f%%')
plt.title("Single vs Album")
plt.show()

#Duration
df['duration_min'].hist()
plt.title("Song Duration Distribution")
plt.show()

