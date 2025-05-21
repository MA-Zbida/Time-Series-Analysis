import numpy as np
import pandas as pd

def linear_curve(peak, duration, step):
    return peak * (1 - step / duration)

def exponential_curve(peak, duration, step):
    return peak * np.exp(-2 * step / duration)

def gaussian_curve(peak, duration, step):
    center = duration / 2
    sigma = duration / 6  # + large = effet plus lissé
    return peak * np.exp(-((step - center) * 2) / (2 * sigma * 2))

def event_calc(events_df, start_date, event_type, peak_value, duration, curve):
    start = pd.to_datetime(start_date)

    for m in range(duration):
        # compute the date m months after the start
        current = start + pd.DateOffset(months=m)
        if current in events_df.index:
            if curve.lower() == "linear":
                intensity = linear_curve(peak_value, duration, m)
            elif curve.lower() == "exponential":
                intensity = exponential_curve(peak_value, duration, m)
            elif curve.lower() == "gaussian":
                intensity = gaussian_curve(peak_value, duration, m)
            else:
                raise ValueError(f"Unknown curve: {curve}")

            sign = 1 if event_type.lower() == "good" else -1
            events_df.loc[current, "event"] += sign * intensity
