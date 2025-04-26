# Code modified from sisense.com article Plotly Choropleth With Slider (Map Charts Over Time): https://community.sisense.com/t5/cdt/plotly-choropleth-with-slider-map-charts-over-time/ta-p/9387
# Geojson file & usage from Mikael Ahonen: https://mikaelahonen.com/en/data/finland-postal-codes-data/ & https://mikaelahonen.com/en/data/postal-codes-map-python/
# Price data from avoindata.fi Price per square meter of old dwellings in Helsinki by postal code: https://www.avoindata.fi/data/en_GB/dataset/helsingin-vanhojen-asunto-osakehuoneistojen-neliohinnat-postinumeroalueittain-vuodesta-2000

from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Load sales data from Excel & ensure postal codes are in string format
df_long = pd.read_excel('Asuntojen_hinnat_postinumeroalueittain kopio.xlsx', dtype={'Postinumero': str})
# Ensure postal codes have 5 digits
df_long['Postinumero'] = df_long['Postinumero'].str.zfill(5)

# Load geojson file of Finnish postal codes
with open("finland-postal-codes.geojson", encoding='utf-8') as f:
    geojson = json.load(f)

# Filter necessary postal codes from geojson based on unique values in sales Excel
excel_postinumerot = df_long['Postinumero'].unique()
geojson_filtered = {
    "type": "FeatureCollection",
    "features": [f for f in geojson['features'] if str(f['properties']['postinumeroalue']).zfill(5) in excel_postinumerot]
}

df_long_filtered = df_long[df_long['Postinumero'].isin(excel_postinumerot)]

# Add year & prices as new columns
df_long_melted = pd.melt(df_long_filtered, id_vars=["Postinumero", "Toimipaikka"], var_name="Vuosi", value_name="Hinta")
df_long_melted['Vuosi'] = df_long_melted['Vuosi'].astype(int)
df_long_melted['Hinta'] = pd.to_numeric(df_long_melted['Hinta'], errors='coerce')

@app.route('/')
def index():
    # Draw a map of Helsinki postal codes
    fig = px.choropleth_mapbox(
        df_long_melted,
        geojson=geojson_filtered,
        locations="Postinumero",
        featureidkey="properties.postinumeroalue",
        color="Hinta",
        mapbox_style="carto-positron",
        zoom=11,
        center={"lat": 60.1699, "lon": 24.9384},  # Center the map in downtown Helsinki
        color_continuous_scale="Greens",
        animation_frame="Vuosi",  # Animate based on year
        hover_name="Toimipaikka"
    )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    graph_html = pio.to_html(fig, full_html=False)

    # Render index.html
    return render_template('index.html', graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)