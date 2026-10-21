import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

spacex_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "spacex_launch_dash.csv"))
min_payload, max_payload = spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()
SITES = sorted(spacex_df["Launch Site"].unique())
SITE_COLORS = dict(zip(SITES, ["#0F62FE", "#8A3FFC", "#009D9A", "#E8590C"]))
BOOSTER_COLORS = {"v1.0": "#A6C8FF", "v1.1": "#8A3FFC", "FT": "#0F62FE", "B4": "#009D9A", "B5": "#E8590C"}

# screenshot state can be preset through env vars (defaults = the lab's defaults)
init_site = os.environ.get("SITE", "ALL")
init_range = [float(v) for v in os.environ.get("RANGE", f"{min_payload},{max_payload}").split(",")]

app = Dash(__name__)
app.layout = html.Div(style={"fontFamily": "Arial", "maxWidth": "1100px", "margin": "0 auto"}, children=[
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center", "color": "#0B49CB", "fontSize": 34}),
    dcc.Dropdown(id="site-dropdown",
                 options=[{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in SITES],
                 value=init_site, placeholder="Select a Launch Site here", searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)}, value=init_range),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def get_pie_chart(site):
    if site == "ALL":
        d = spacex_df.groupby("Launch Site", as_index=False)["class"].sum()
        fig = px.pie(d, values="class", names="Launch Site", color="Launch Site", color_discrete_map=SITE_COLORS,
                     title="Total Successful Launches by Site")
    else:
        d = spacex_df[spacex_df["Launch Site"] == site]["class"].map({1: "Success", 0: "Failure"}).value_counts().reset_index()
        d.columns = ["Outcome", "count"]
        fig = px.pie(d, values="count", names="Outcome", color="Outcome",
                     color_discrete_map={"Success": "#0F62FE", "Failure": "#E8590C"},
                     title=f"Success vs. Failure for site {site}")
    fig.update_traces(textinfo="percent+label", textfont_size=14, marker_line_color="white", marker_line_width=2)
    return fig

@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def get_scatter(site, payload):
    d = spacex_df[spacex_df["Payload Mass (kg)"].between(payload[0], payload[1])]
    if site != "ALL":
        d = d[d["Launch Site"] == site]
    fig = px.scatter(d, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                     color_discrete_map=BOOSTER_COLORS, hover_data=["Launch Site"],
                     title=f"Payload vs. Launch Outcome — {'all sites' if site == 'ALL' else site} "
                           f"({payload[0]:,.0f}–{payload[1]:,.0f} kg)")
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color="white")))
    fig.update_yaxes(tickvals=[0, 1], ticktext=["0 = failed", "1 = landed"], range=[-0.3, 1.3])
    fig.update_layout(plot_bgcolor="white")
    return fig

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8050)), debug=False)
