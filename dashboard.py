import streamlit as st
import pandas as pd

df = pd.read_csv("Atlantic_France.csv")

st.title("France Top 50 Analysis")

st.write("Dataset preview")
st.dataframe(df.head())

st.bar_chart(df['is_explicit'].value_counts())
st.bar_chart(df['album_type'].value_counts())

st.subheader("Album Type Distribution")
st.bar_chart(df['album_type'].value_counts())

#Clean columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

#Convert duration
df['duration_min'] = df['duration_ms'] / 60000

st.title("🎵 France Top 50 Music Analysis")

#🔥 KPIs
st.subheader("Key Performance Indicators")

col1, col2, col3, = st.columns(3)

col1.metric("Explicit content %",round(df['is_explicit'].mean()*100,2))
col2.metric("Avg Duration (min)",round(df['duration_min'].mean(),2))
col3.metric("Total Tracks", len(df))

#Charts
st.subheader("Explicit vs Clean Content")
st.bar_chart(df['is_explicit'].value_counts())

st.subheader("Album Type Distribution")
st.bar_chart(df['album_type'].value_counts())

#Filter by Top N songs
top_n = st.slider("select Top N Positions",10, 50, 50)

filtered_df = df[df['position'] <= top_n]

st.subheader(f"Top {top_n} Songs Analysis")
st.bar_chart(filtered_df['album_type'].value_counts())

st.subheader("Song Duration Distribution")
st.line_chart(df['duration_min'])


# 🔥 DEFINE TABS FIRST
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Analysis", "🧠 Insights"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Explicit Content %", round(df['is_explicit'].mean()*100, 2))
    col2.metric("Avg Duration (min)", round(df['duration_min'].mean(), 2))
    col3.metric("Total Tracks", len(df))

    st.subheader("Explicit vs Clean Content")
    st.bar_chart(df['is_explicit'].value_counts())

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Album Type Distribution")
    st.bar_chart(df['album_type'].value_counts())

    st.subheader("Song Duration")
    st.line_chart(df['duration_min'])

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("Key Insights")

    st.write("• Clean content dominates the playlist")
    st.write("• Singles are more common than albums")
    st.write("• Medium duration songs perform better")

