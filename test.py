import dash
from dash import html
from dash.dependencies import Input, Output
import datetime
import time
import dash_core_components as dcc


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(id="output"),
        dcc.Interval(
            id="interval-component",
            interval=20 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)

@app.callback(Output("output", "children"), [Input("interval-component", "n_intervals")])
def update_output(n):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(current_time)
    return f"Callback triggered. Current time: {current_time}"

if __name__ == "__main__":
    app.run_server(debug=True)