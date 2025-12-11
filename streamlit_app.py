import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# -----------------------------------
# Load Data
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("legus_cleaned.csv")


df = load_data()

# Make the title 
st.set_page_config(page_title="Legume Nutrient Dashboard", layout="wide")
st.title("🌱 Legume Nutrient Dashboard")
st.write("Explore nutrient profiles for legumes using your cleaned USDA dataset.")


# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Controls")

legume = st.sidebar.selectbox("Select a Legume", df["Category"].unique())


# Minerals to use in radar chart
radar_minerals = [
    "Protein (g)", "Fat (g)", "Carbs (g)", "Starch (g)", "Iron (mg)",
    "Magnesium (mg)", "Phosphorus (mg)", "Potassium (mg)", "Sodium (mg)",
    "Zinc (mg)", "Copper (mg)", "Manganese (mg)"
]


# -----------------------------------
# Filter Data
# -----------------------------------
legume_df = df[df["Category"] == legume].mean(numeric_only=True)


# -----------------------------------
# Radar Chart
# -----------------------------------
st.subheader(f"Radar Chart for {legume}")

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[legume_df[m] for m in radar_minerals],
    theta=radar_minerals,
    fill='toself',
    name=legume
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# Data Table
# -----------------------------------
st.subheader("Dataset Preview")
st.dataframe(df, use_container_width=True)


# -----------------------------------
# Correlation Heatmap
# -----------------------------------
st.subheader("Correlation Heatmap of Nutrients")

numeric = df.select_dtypes(include="number")
corr = numeric.corr()

heatmap = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(heatmap, use_container_width=True)
