📈 Moroccan Economy Forecasting with Event Influence
This project aims to forecast the Moroccan economy by predicting key economic indicators using time series models. It uniquely incorporates the influence of significant events (such as holidays, crises, reforms, etc.) occurring during the year. The data is zero-padded monthly to maintain consistent time granularity.

The project features a clean and interactive Streamlit interface for visualizing and exploring forecasts in real-time.

🔍 Overview
Economic forecasting is essential for policy makers, investors, and researchers. This project goes beyond standard forecasting by:

📅 Modeling economic indicators on a monthly basis.

🧠 Including event data (e.g., major holidays, external shocks).

💡 Leveraging Streamlit for intuitive exploration and prediction.

📂 Project Structure
```
Time-Series-Analysis/
├── data/
│   └── Morocco.csv          # Monthly economic dataset (zero-padded)
├── models/                  # Trained forecasting models
    └── eco_model1.h5        # Model for certain economical indicators
    └── eco_model2.h5        # Model for certain economical indicators
    └── prod_model.h5        # Model for production type indicators
    └── rate_model.h5        # Model for rate changes type indicators
    └── demo_model.h5        # Model for demographic type indicators
    └── consum_model.h5      # Model for consumption type indicators         
├── scalers/                 # Preprocessing scalers used in training
    └── eco_scaler1.pkl        # scaler for eco_model1
    └── eco_scaler2.pkl        # scaler for eco_model2
    └── prod_scaler.pkl        # scaler for prd_model
    └── rate_scaler.pkl        # scaler for rate_model
    └── demo_scaler.pkl        # scaler for demo_model
    └── consum_scaler.pkl      # scaler for consum_model
└── src/                     # Streamlit app and supporting scripts
    └── curves.py            # For preprocessing the influence of event
    └── indicators.py        # all economic indicators
    └── model.py             # all model config
    └── data.py              # data
    └── forecast.py          # forecasting new values
    └── app.py               # main interface app
    └── requirement.txt      # scaler for rate_model
```
⚙️ Features
Zero-Padded Monthly Data: Ensures complete time series continuity.

Event-Aware Modeling: Events are integrated into the feature set to enhance model sensitivity to real-world occurrences.

Live Predictions: Users can interact with the forecast through a Streamlit dashboard.

Modular Codebase: Easy to maintain and extend.

🚀 How to Run
Clone the Repository

```
git clone https://github.com/MA-Zbida/Time-Series-Analysis.git
cd Time-Series-Analysis
```
Install Dependencies
```
pip install -r requirements.txt
```
Start the Streamlit App

```
streamlit run src/app.py
```
📊 Example Forecasted Indicators
IDE

REER

Employment Rate

Import/Export Volumes

These indicators are predicted with respect to both time and known impactful events.

🛠️ Future Enhancements
Integration of high-frequency or regional data

Use of NLP for automated event extraction from news articles

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements, bug fixes, or new ideas.

📜 License
This project is licensed under the MIT License.
