import streamlit as st
import pandas as pd
import numpy as np
from curves import linear_curve, gaussian_curve, exponential_curve, event_calc
from indicators import get_indicators
from data import load_data
from model import forecast
# Dummy model prediction function
def model_predict(events_df, indicators):
    years = sorted(events_df['Year'].unique())
    data = []
    for year in years:
        for indicator in indicators:
            value = np.random.rand() * 100  # Dummy value, replace with real model
            data.append({'Year': year, 'Event': ', '.join(events_df[events_df['Year'] == year]['Event']),
                         'Indicator': indicator, 'Predicted Value': value})
    return pd.DataFrame(data)

st.title("Economic Event Impact Simulator (2023–2035)")

# Step 1: Choose year range
start_year = 2023
end_year = st.slider("Select Year Range", start_year, 2035, 2030)
years = list(range(start_year, end_year + 1))

st.header("Define Events for Each Year")
events_data = []
for year in years:
    with st.expander(f"Configure Year {year}", expanded=False):
        event_name = st.text_input(f"Event name for {year}", key=f"event_{year}")
        event_type = st.selectbox(f"Type of event", ["Good", "Bad"], key=f"type_{year}")
        peak_value = st.slider(f"Peak value for {event_name}", 0.0, 1.0, value=0.5, step=0.1, key=f"peak_{year}")
        duration = st.slider(f"Duration of the event (months)", 1, 12, 3, key=f"duration_{year}")
        curve = st.selectbox(f"Choose curve shape", ["Linear", "Gaussian", "Exponential"], key=f"curve_{year}")

        if event_name:
            events_data.append({
                "Date": f"{year}-01-01",
                "Event": event_name,
                "Type": event_type,
                "Peak": peak_value,
                "Duration": duration,
                "Curve": curve
            })

dates = pd.date_range(start="2023-01-01", end=f"{end_year}-12-01", freq="MS")
exog_data = pd.DataFrame(index=dates)
exog_data["event"] = 0.0  # initialize with 0s

for event in events_data:
    event_calc(exog_data, 
                event["Date"],
                event["Type"],
                event["Peak"],
                event["Duration"],
                event["Curve"]
    )

st.dataframe(exog_data)

# Step 2: Choose economic indicators
st.header("Select Economic Indicators")
all_indicators = get_indicators()
selected_indicators = st.multiselect("Choose indicators to simulate", all_indicators)

# Step 3: Creating the input for each model
df = load_data() # Load the actual data

# Step 4: Predict & display
if st.button("Simulate Impact"):
    if not events_data or not selected_indicators:
        st.warning("Please define at least one event and select indicators.")
    else:
        preds_df = forecast(df, exog_data, start_year, end_year, selected_indicators)

        st.subheader("Predicted Values")
        st.dataframe(preds_df)


