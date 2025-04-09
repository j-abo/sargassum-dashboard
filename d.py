# The usual imports
import pandas as pd 
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

# Read CSV files
UP1_df = pd.read_csv("data\\UP-1_Anomaly_Detection_SynData.csv", parse_dates=["Timestamp"])
UP2_df = pd.read_csv("data\\UP-2_Data_Fusion_Testing_SynData.csv", parse_dates=["Timestamp"])
UP3_df = pd.read_csv("data\\UP-3-Integration_Local_Observations_Dataset.csv", parse_dates=["Timestamp"])
UP4_df = pd.read_csv("data\\UP-4_Maintenance_Analysis_SynData.csv", parse_dates=["Timestamp"])
UP5_df = pd.read_csv("data\\UP-5_Impact_Modeling_SynData.csv", parse_dates=["Timestamp"])

# Merge datasets
earlier_df = UP1_df.merge(UP5_df, on="Timestamp", how="inner")
later_df = UP2_df.merge(UP3_df, on="Timestamp", how="inner").merge(UP4_df, on="Timestamp", how="inner")

# App initialization
app = dash.Dash(__name__)

# Map visualizations
fig_map01 = px.scatter_mapbox(later_df, lat="Latitude", lon="Longitude", hover_data=["Timestamp"], title="GPS Positions (Later Data)", mapbox_style="open-street-map")
fig_map02 = px.scatter_mapbox(earlier_df, lat="Latitude", lon="Longitude", hover_data=["Timestamp"], title="GPS Positions (Earlier Data)", mapbox_style="open-street-map")

# Earlier data time series
fig_temp = px.line(earlier_df, x="Timestamp", y="Water_Temperature_C", title="Water Temperature (Earlier Data)")
fig_speed = px.line(earlier_df, x="Timestamp", y="Speed_mps", title="Speed (Earlier Data)")
fig_battery = px.line(earlier_df, x="Timestamp", y="Battery_Level_Percent", title="Battery Level (Earlier Data)")
fig_impact_temp = px.scatter(earlier_df, x="Water_Temperature_C", y="Impact_Likelihood_Percent", title="Impact Likelihood vs Temperature (Earlier Data)", color="Anomaly_Flag")

# Later data time series
fig_temp_later = px.line(later_df, x="Timestamp", y="Temperature_C_x", title="Temperature (Later Data)")
fig_salinity = px.line(later_df, x="Timestamp", y="Salinity_PSU", title="Salinity (Later Data)")

app.layout = html.Div([
    html.H1("Sargassum Dashboard"),

    html.H2("GPS Maps"),
    dcc.Graph(figure=fig_map01),
    dcc.Graph(figure=fig_map02),

    html.H2("Time Series (Earlier Data)"),
    dcc.Graph(figure=fig_temp),
    dcc.Graph(figure=fig_speed),
    dcc.Graph(figure=fig_battery),
    dcc.Graph(figure=fig_impact_temp),

    html.H2("Time Series (Later Data)"),
    dcc.Graph(figure=fig_temp_later),
    dcc.Graph(figure=fig_salinity),
])

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
