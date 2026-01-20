import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import os
import glob
import requests

st.set_page_config(layout="wide", page_title="Aadhaar Data Dashboard")

ST_TITLE = "NeevDrishti Dashboard"
st.title(ST_TITLE)

# --- Data Loading & Cleaning ---

@st.cache_data(show_spinner=False, ttl=600)  # Cache for 10 minutes
def load_data(folder_name):
    """Loads all CSVs from a specific folder."""
    path = os.path.join("data", "raw", folder_name, "*.csv")
    files = glob.glob(path)
    if not files:
        return pd.DataFrame()
    
    df_list = []
    for f in files:
        try:
            df_list.append(pd.read_csv(f))
        except Exception as e:
            st.warning(f"Could not read {f}: {e}")
    
    if not df_list:
        return pd.DataFrame()
        
    df = pd.concat(df_list, ignore_index=True)
    return df

@st.cache_data(show_spinner=False)
def get_geojson():
    """Fetches India States GeoJSON."""
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

def clean_state_names(df):
    if "state" not in df.columns:
        return df
        
    # Official whitelist (as per analysis.py)
    official_states = {
        'andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar',
        'chandigarh', 'chhattisgarh', 'dadra and nagar haveli and daman and diu', 'delhi', 'goa',
        'gujarat', 'haryana', 'himachal pradesh', 'jammu and kashmir', 'jharkhand', 'karnataka',
        'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya',
        'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu',
        'telangana', 'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal'
    }

    fix_map = {
        "orissa": "odisha",
        "pondicherry": "puducherry",
        "uttaranchal": "uttarakhand",
        "west bangal": "west bengal",
        "westbengal": "west bengal",
        "west bengli": "west bengal",
        "chhatisgarh": "chhattisgarh",
        "tamilnadu": "tamil nadu",
        "jammu & kashmir": "jammu and kashmir",
        "jammu&kashmir": "jammu and kashmir",
        "andaman & nicobar islands": "andaman and nicobar islands",
        "andaman&nicobar islands": "andaman and nicobar islands",
        "andaman & nicobar": "andaman and nicobar islands",
        "andaman and nicobar": "andaman and nicobar islands",
        "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
        "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
        "daman & diu": "dadra and nagar haveli and daman and diu",
        "daman and diu": "dadra and nagar haveli and daman and diu",
        "daman&diu": "dadra and nagar haveli and daman and diu",
        "uttarpradesh": "uttar pradesh",
        "u.p.": "uttar pradesh",
        "up": "uttar pradesh",
        "u p": "uttar pradesh",
        "madhyapradesh": "madhya pradesh",
        "m.p.": "madhya pradesh",
        "andhrapradesh": "andhra pradesh",
        "arunachalpradesh": "arunachal pradesh",
        "himachalpradesh": "himachal pradesh",
    }
    
    # Clean state names: lowercase, strip, normalize whitespace
    df["state_clean"] = df["state"].astype(str).str.lower().str.strip().str.replace(r"\s+", " ", regex=True)
    
    # Apply fix map for known variations
    df["state_clean"] = df["state_clean"].replace(fix_map)
    
    # Filter to only official states
    before_count = len(df)
    df = df[df["state_clean"].isin(official_states)]
    after_count = len(df)
    
    # Log filtering stats (useful for debugging)
    if before_count > after_count:
        filtered = before_count - after_count
        # Debug: Show which states were filtered out
        # print(f"Filtered out {filtered} rows with invalid state names")
    
    return df

# --- Load Data ---
st.header("Loading Data...")
with st.spinner("Loading datasets..."):
    df_demo = load_data("demographic")
    df_bio = load_data("biometric")
    df_enrol = load_data("enrolment")
    
    df_demo = clean_state_names(df_demo)
    df_bio = clean_state_names(df_bio)
    df_enrol = clean_state_names(df_enrol)
    
    geojson = get_geojson()

st.success("Data Loaded!")

# --- Visualizations ---

tab1, tab2, tab3 = st.tabs(["Biometric", "Demographic", "Enrolment"])

def plot_3d_map(df, value_col, state_col="state_clean", title="3D Map"):
    if geojson is None:
        st.error("Could not load GeoJSON for 3D Map")
        return

    # Aggregate by state
    state_df = df.groupby(state_col)[value_col].sum().reset_index()
    
    # Create a title-cased column for GeoJSON matching
    state_df["state_title"] = state_df[state_col].str.title()
    
    # manual fix for GeoJSON keys (jbrobst/india_states.geojson)
    geojson_fix = {
        "Jammu And Kashmir": "Jammu & Kashmir",
        "Andaman And Nicobar Islands": "Andaman & Nicobar Island",
        "Delhi": "NCT of Delhi",
        "Dadra And Nagar Haveli And Daman And Diu": "Dadra and Nagar Haveli and Daman and Diu",
        "Telangana": "Telangana" # Verified match
    }
    state_df["state_title"] = state_df["state_title"].replace(geojson_fix)
    
    # Choropleth with PyDeck using GeoJSON
    # Note: PyDeck with GeoJSON requires matching properties. 
    # The GeoJSON usually has 'ST_NM' or similar. We need to check or map our names to it.
    # For simplicity, let's use Plotly for the '3D' map (Choropleth Mapbox) or standard Choropleth.
    # The user asked for "3d state wise map". 
    # A true 3D extruded map is hard with just names if names don't match perfectly.
    # Let's try basic Plotly Choropleth first as it is robust.
    # IF specific 3D extrusion is needed, we need pydeck PolygonLayer.
    
    # Using Plotly Choropleth Mapbox (which allows for tilt/3D feel)
    fig = px.choropleth_mapbox(
        state_df,
        geojson=geojson,
        featureidkey="properties.ST_NM", # Common key for India GeoJSON
        locations="state_title", # Use the title-cased column we created
        color=value_col,
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=3,
        center = {"lat": 20.5937, "lon": 78.9629},
        opacity=0.7,
        title=title
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)


with tab1:
    st.subheader("Biometric Analysis")
    if not df_bio.empty:
        # Find numeric columns
        cols = df_bio.select_dtypes(include=['float64', 'int64']).columns.tolist()
        metric = st.selectbox("Select Metric for Biometric", cols, index=0)
        
        # 2D
        st.write("#### State-wise Distribution (2D)")
        state_agg = df_bio.groupby("state_clean")[metric].sum().reset_index()
        state_agg = state_agg.sort_values(by=metric, ascending=False)  # Sort descending
        bar_fig = px.bar(state_agg, x="state_clean", y=metric, 
                        title=f"Top States by {metric}")
        bar_fig.update_xaxes(categoryorder='total descending')
        st.plotly_chart(bar_fig, use_container_width=True)
        
        # 3D Map
        st.write("#### State-wise Map (3D View)")
        plot_3d_map(df_bio, metric, title=f"Biometric - {metric}")
    else:
        st.warning("No Biometric Data Found")

with tab2:
    st.subheader("Demographic Analysis")
    if not df_demo.empty:
        cols = df_demo.select_dtypes(include=['float64', 'int64']).columns.tolist()
        metric = st.selectbox("Select Metric for Demographic", cols, index=0)
        
        # 2D
        st.write("#### State-wise Distribution (2D)")
        state_agg = df_demo.groupby("state_clean")[metric].sum().reset_index()
        state_agg = state_agg.sort_values(by=metric, ascending=False)  # Sort descending
        bar_fig = px.bar(state_agg, x="state_clean", y=metric,
                        title=f"Top States by {metric}")
        bar_fig.update_xaxes(categoryorder='total descending')
        st.plotly_chart(bar_fig, use_container_width=True)
        
        # 3D Map
        st.write("#### State-wise Map (3D View)")
        plot_3d_map(df_demo, metric, title=f"Demographic - {metric}")
    else:
        st.warning("No Demographic Data Found")

with tab3:
    st.subheader("Enrolment Analysis")
    if not df_enrol.empty:
        cols = df_enrol.select_dtypes(include=['float64', 'int64']).columns.tolist()
        metric = st.selectbox("Select Metric for Enrolment", cols, index=0)
        
        # 2D
        st.write("#### State-wise Distribution (2D)")
        state_agg = df_enrol.groupby("state_clean")[metric].sum().reset_index()
        state_agg = state_agg.sort_values(by=metric, ascending=False)  # Sort descending
        bar_fig = px.bar(state_agg, x="state_clean", y=metric,
                        title=f"Top States by {metric}")
        bar_fig.update_xaxes(categoryorder='total descending')
        st.plotly_chart(bar_fig, use_container_width=True)
        
        # 3D Map
        st.write("#### State-wise Map (3D View)")
        plot_3d_map(df_enrol, metric, title=f"Enrolment - {metric}")
    else:
        st.warning("No Enrolment Data Found")
