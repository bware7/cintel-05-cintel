# --------------------------------------------
# Imports
# --------------------------------------------
from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats
from faicons import icon_svg

# --------------------------------------------
# Constants
# --------------------------------------------
UPDATE_INTERVAL_SECS: int = 3
DEQUE_SIZE: int = 10

# --------------------------------------------
# Reactive Data Wrapper
# --------------------------------------------
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Reactive Calculation for Live Data
# --------------------------------------------
@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    
    # Generate new random temperature data
    temp = round(random.uniform(-20, -10), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"temp": temp, "timestamp": timestamp}
    
    # Add to reactive deque
    reactive_value_wrapper.get().append(new_entry)
    deque_snapshot = reactive_value_wrapper.get()
    
    # Create a DataFrame for visualization
    df = pd.DataFrame(deque_snapshot)
    return deque_snapshot, df, new_entry

# --------------------------------------------
# Shiny UI
# --------------------------------------------
ui.page_opts(title="Bin's Continuous Intelligence App", fillable=True)

# Sidebar content
with ui.sidebar(open="open"):
    ui.h2("Live Weather Dashboard", class_="text-center")
    ui.p("This app demonstrates real-time temperature monitoring.", class_="text-center")
    ui.hr()
    ui.h6("Links:")
    ui.a("GitHub Repository", href="https://github.com/bware7/cintel-05-cintel", target="_blank")
    ui.a("Shiny Documentation", href="https://shiny.posit.co/py/", target="_blank")

# Main Layout
with ui.layout_columns():
    # Temperature Value Box
    with ui.value_box(
        showcase=icon_svg("thermometer"),  # Updated valid icon
        theme="bg-gradient-blue",
    ):
        "Current Temperature"

        @render.text
        def display_temp():
            _, _, latest_entry = reactive_calc_combined()
            return f"{latest_entry['temp']} °C"

        "Updated Continuously"

    # Timestamp Card
    with ui.card(full_screen=True):
        ui.card_header("Current Timestamp")

        @render.text
        def display_time():
            _, _, latest_entry = reactive_calc_combined()
            return f"{latest_entry['timestamp']}"

# Data and Chart Layout
with ui.card(full_screen=True):
    ui.card_header("Recent Data Readings")

    @render.data_frame
    def display_data():
        _, df, _ = reactive_calc_combined()
        return df

with ui.card():
    ui.card_header("Temperature Trend Chart")

    @render_plotly
    def display_chart():
        _, df, _ = reactive_calc_combined()

        if not df.empty and len(df) > 1:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            fig = px.scatter(
                df, 
                x="timestamp", 
                y="temp", 
                title="Temperature Readings with Trend Line",
                labels={"temp": "Temperature (°C)", "timestamp": "Time"}
            )

            # Linear Regression - Ensure sufficient data
            x_vals = range(len(df))
            y_vals = df["temp"]

            if len(set(y_vals)) > 1:  # Ensure variation in data
                slope, intercept, *_ = stats.linregress(x_vals, y_vals)
                df["trend_line"] = [slope * x + intercept for x in x_vals]
                # Add trend line to plot
                fig.add_scatter(x=df["timestamp"], y=df["trend_line"], mode="lines", name="Trend Line")
            else:
                # Add a note if no variation in data
                fig.add_annotation(
                    text="No trend line: Insufficient variation in data",
                    xref="paper", 
                    yref="paper", 
                    showarrow=False,
                    x=0.5, 
                    y=0.9
                )

            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Temperature (°C)",
                template="plotly_dark"
            )
            return fig
        else:
            # Return an empty figure with a note if there's no data
            return px.scatter(title="Not enough data to calculate trends")
