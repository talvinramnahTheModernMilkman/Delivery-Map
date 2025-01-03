import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Set page config to wide mode
st.set_page_config(layout="wide")

def load_data():
    file_path = "https://raw.githubusercontent.com/talvinramnahTheModernMilkman/Delivery-Map/refs/heads/main/TMM_waitlist-with-coordinates.csv"
    df = pd.read_csv(file_path)
    return df[
        (df['LATITUDE'].between(49.8, 60.9)) & 
        (df['LONGITUDE'].between(-8.6, 1.8))    
    ]

def create_cluster_map(data):
    m = folium.Map(location=[54.7, -3.2], zoom_start=6, tiles='cartodbpositron')
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, row in data.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=3,
            color='blue',
            fill=True,
            popup=f"Customer {idx}"
        ).add_to(marker_cluster)
    
    return m

def main():
    st.title("Customer Distribution Map")
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
