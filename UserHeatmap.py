import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests
import json

# Set page config to wide mode
st.set_page_config(layout="wide")

def load_data():
    file_path = "https://raw.githubusercontent.com/talvinramnahTheModernMilkman/Delivery-Map/refs/heads/main/TMM_waitlist-with-coordinates.csv"
    df = pd.read_csv(file_path)
    # Filter on region if needed
    return df[
        (df['LATITUDE'].between(49.8, 60.9)) & 
        (df['LONGITUDE'].between(-8.6, 1.8))    
    ]

def load_borough_geojson():
    # Replace this with the raw link to your GeoJSON file
    url = "https://raw.githubusercontent.com/radoi90/housequest-data/master/house_price_london_boroughs_simplified.geojson"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def borough_style(feature):
    """
    A simple style function for the GeoJSON polygons
    """
    return {
        'fillColor': '#0099cc',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.2
    }

def create_cluster_map(data):
    # Initialize the map
    m = folium.Map(location=[54.7, -3.2], zoom_start=6, tiles='cartodbpositron')
    
    # Load the borough GeoJSON
    borough_geojson = load_borough_geojson()
    
    # Add the borough layer
    folium.GeoJson(
        borough_geojson,
        name="London Boroughs",
        style_function=borough_style
    ).add_to(m)
    
    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, row in data.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=3,
            color='blue',
            fill=True,
            popup=f"Customer {idx}"
        ).add_to(marker_cluster)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def main():
    st.title("TMM Waitlist with London Boroughs")
    df = load_data()
    m = create_cluster_map(df)
    
    # Make map bigger using custom CSS
    st.markdown("""
        <style>
            iframe {
                width: 100%;
                min-height: 800px;
                height: 80vh;
            }
        </style>
    """, unsafe_allow_html=True)
    
    folium_static(m)
    st.write(f"Total customers plotted: {len(df)}")

if __name__ == "__main__":
    main()
