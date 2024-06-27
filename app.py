import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import pydeck as pdk
import tempfile
import os

st.set_page_config(layout="wide", page_title="PALM-4U Domain Overview")

st.write("Test")

def load_shapefile(file):
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(file.read())
            tmpfile.flush()
            return gpd.read_file(tmpfile.name).to_crs(epsg=4326)
    return None

# Create columns
col1, col2, col3, col4 = st.columns(4)

# Upload shapefiles
with col1:
    uploaded_parent = st.file_uploader("Upload Parent Shapefile", type="shp")
with col2:
    uploaded_child_i = st.file_uploader("Upload Child I Shapefile", type="shp")
with col3:
    uploaded_child_ii = st.file_uploader("Upload Child II Shapefile", type="shp")
with col4:
    uploaded_buildings = st.file_uploader("Upload Buildings GeoJSON", type="geojson")

gdf_parent = load_shapefile(uploaded_parent)
gdf_child_i = load_shapefile(uploaded_child_i)
gdf_child_ii = load_shapefile(uploaded_child_ii)

# Read buildings
if uploaded_buildings is not None:
    gdf_buildings = gpd.read_file(uploaded_buildings).to_crs(epsg=4326)
    gdf_buildings_2 = gdf_buildings.iloc[:, [11, -1]]
    gdf_buildings_exploded = gdf_buildings_2.explode(index_parts=True)
    gdf_buildings_exploded = gdf_buildings_exploded.reset_index(drop=True)
else:
    gdf_buildings = None
    gdf_buildings_exploded = None

# Display information
if gdf_parent is not None:
    st.write("Parent Shapefile:")
    st.write(gdf_parent)

if gdf_child_i is not None:
    st.write("Child I Shapefile:")
    st.write(gdf_child_i)

if gdf_child_ii is not None:
    st.write("Child II Shapefile:")
    st.write(gdf_child_ii)

if gdf_buildings_exploded is not None:
    st.write("Buildings GeoJSON:")
    st.write(gdf_buildings_exploded)
    
    
def load_pydeck_domain_overview():
    st.write("Pydeck map goes here")
    parent_layer = pdk.Layer(
        "PolygonLayer",
        data=gdf_parent,
        get_polygon="geometry.coordinates",
        get_fill_color=[150, 150, 250],
        get_line_color=[250, 250, 250],  # Specify the line color
        get_line_width=2.5,  # Specify the line width
        get_elevation=128 * 16,  # Map the "B_hoeh" column to elevation
        #  filled=False,
        opacity=0.025,
        wireframe=True,
        extruded=True,
        pickable=False,
    )
    view_state = pdk.ViewState(
        latitude=47.6660,
        longitude=9.1750,
        zoom=12,
        max_zoom=18,
        pitch=50,
        bearing=-30,
    )
    r = pdk.Deck(
        layers=[parent_layer,],
        views=[pdk.View(type="MapView", controller=True)],
        initial_view_state=view_state,
        map_style="road",
    )
    st.pydeck_chart(r)

with st.container(height=500, border=True):
    st.write("Container")
    load_pydeck_domain_overview()

