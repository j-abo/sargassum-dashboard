# The usual imports
import pandas as pd 
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Lets read each CSV as unique dataframes
UP1_df = pd.read_csv("data\\UP-1_Anomaly_Detection_SynData.csv", parse_dates=["Timestamp"])
UP2_df = pd.read_csv("data\\UP-2_Data_Fusion_Testing_SynData.csv", parse_dates=["Timestamp"])
UP3_df = pd.read_csv("data\\UP-3-Integration_Local_Observations_Dataset.csv", parse_dates=["Timestamp"])
UP4_df = pd.read_csv("data\\UP-4_Maintenance_Analysis_SynData.csv", parse_dates=["Timestamp"])
UP5_df = pd.read_csv("data\\UP-5_Impact_Modeling_SynData.csv", parse_dates=["Timestamp"])

# And then merge them as appropriate
earlier_df = UP1_df.merge(UP5_df, on="Timestamp", how="inner")
later_df = UP2_df.merge(UP3_df, on="Timestamp", how="inner").merge(UP4_df, on="Timestamp", how="inner")

app = dash.Dash(__name__)

# Plotting the GPS positions on maps
fig_map01 = px.scatter_mapbox(later_df, lat="Latitude", lon="Longitude", hover_data=["Timestamp"], title="GPS Positions in Later Data", mapbox_style="open-street-map")
fig_map02 = px.scatter_mapbox(earlier_df, lat="Latitude", lon="Longitude", hover_data=["Timestamp"], title="GPS Positions in Earlier Data", mapbox_style="open-street-map")

# Plotting Water Temperature in earlier_df
fig_temp = px.line(earlier_df, x="Timestamp", y="Water_Temperature_C", title="Water Temperature Over Time (Earlier Data)")

# Plotting Temperature in later_df for Temperature_C_x (assuming it's the correct column)
fig_temp_later = px.line(later_df, x="Timestamp", y="Temperature_C_x", title="Temperature Over Time (Later Data)")

# Plotting Speed over Time (Earlier Data)
fig_speed = px.line(earlier_df, x="Timestamp", y="Speed_mps", title="Speed Over Time (Earlier Data)")

# Plotting Battery Level over Time (Earlier Data)
fig_battery = px.line(earlier_df, x="Timestamp", y="Battery_Level_Percent", title="Battery Level Over Time (Earlier Data)")

# Plotting Salinity over Time (Later Data)
fig_salinity = px.line(later_df, x="Timestamp", y="Salinity_PSU", title="Salinity Over Time (Later Data)")

# Plotting Impact Likelihood vs Temperature (Earlier Data) - Now correctly uses earlier_df
fig_impact_temp = px.scatter(earlier_df, x="Water_Temperature_C", y="Impact_Likelihood_Percent", title="Impact Likelihood vs Temperature (Earlier Data)", color="Anomaly_Flag")

# Layout of the app
app.layout = html.Div([
    html.H1("Sargassum Dashboard"),
    
    # Map visualizations
    dcc.Graph(id="map1", figure=fig_map01),
    dcc.Graph(id="map2", figure=fig_map02),
    
    # Time series for temperature
    dcc.Graph(id="temperature-plot", figure=fig_temp),
    dcc.Graph(id="temperature-plot-later", figure=fig_temp_later),
    
    # Speed and Battery level plots
    dcc.Graph(id="speed-plot", figure=fig_speed),
    dcc.Graph(id="battery-plot", figure=fig_battery),
    
    # Salinity and Impact-Likelihood vs Temperature plots
    dcc.Graph(id="salinity-plot", figure=fig_salinity),
    dcc.Graph(id="impact-temp-plot", figure=fig_impact_temp)
])

if __name__ == '__main__':
    app.run(debug=True)



# THE OLD CODE
'''
Author: John Abo
We're going to try out dash to make a dashboard using the data we have rn
It'll meet the final requirements we set for ourselves. but we'll need a
statement in our report that the data itself is kaput, and that we're only
trying to show as much as we can, but there isn't much to show.
'''
'''
# The usual imports
import pandas as pd 
import dash
from dash import dcc, html
import plotly.express as px

# Lets read each CSVs as unique dataframes
UP1_df = pd.read_csv("data\\UP-1_Anomaly_Detection_SynData.csv", parse_dates=["Timestamp"])
UP2_df = pd.read_csv("data\\UP-2_Data_Fusion_Testing_SynData.csv", parse_dates=["Timestamp"])
UP3_df = pd.read_csv("data\\UP-3-Integration_Local_Observations_Dataset.csv", parse_dates=["Timestamp"])
UP4_df = pd.read_csv("data\\UP-4_Maintenance_Analysis_SynData.csv", parse_dates=["Timestamp"])
UP5_df = pd.read_csv("data\\UP-5_Impact_Modeling_SynData.csv", parse_dates=["Timestamp"])

# And then merge them as appropriate
earlier_df = UP1_df.merge(UP5_df, on="Timestamp", how="inner")
later_df = UP2_df.merge(UP3_df, on="Timestamp", how="inner").merge(UP4_df, on="Timestamp", how="inner")

# Creates the app object, not sure what exactly these ever mean whenever
# I see them, but here we are.
app = dash.Dash(__name__)

# Sample plots they say
fig_map01 = px.scatter_mapbox(later_df,
                            lat="Latitude", lon="Longitude",
                            hover_data=["Timestamp"],
                            title="GPS Positions",
                            mapbox_style="open-street-map")
fig_map02 = px.scatter_mapbox(earlier_df,
                            lat="Latitude", lon="Longitude",
                            hover_data=["Timestamp"],
                            title="GPS Positions",
                            mapbox_style="open-street-map")

app.layout = html.Div([
    html.H1("Sargassum Dashboard"),
    dcc.Graph(id="map1", figure=fig_map01),
    dcc.Graph(id="map2", figure=fig_map02),
])

if __name__ == '__main__':
    app.run(debug=True)
'''