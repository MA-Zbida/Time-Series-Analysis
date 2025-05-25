import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
model_config = {
    "eco_model1": {
        "path" : "models/eco_model1.keras",
        "seq_len": 12,
        "indicators": [
            "IDE(USD)",
            "REER(2010 = 100)",
            "annual_gold_prices(USD/oz)",
            "InterTourismeReceipts(usd)",
            "Dépenses nationales brutes (unités de devises locales courantes)",
            "Importation de bien et de services ($ US)",
            "Exportation de biens et de services ($ US)"
        ]
    },
    "eco_model2" : {
        "path" : "models/eco_model2.keras",
        "seq_len":  6,
        "indicators" : ['brent_oil_prices(USD/barrel)',
            'crude_oil_prices(USD/barrel)',
            'daily_natural_gas_prices(USD/MMBtu)'
        ]
    },
    "demo_model" : {
        "path" : "models/demo_model.keras",
        "seq_len" : 23,
        "indicators" : ['Demographie', 
            'Pauvrete', 
            'Analphabetisme'
        ]
    },
    "rate_model" : {
        "path" : "models/rate_model.keras",
        "seq_len" : 17,
        "indicators" : ['Inflation, prix à la consommation (%\xa0annuel)',
            'Chômage, total (%\xa0de la population)',
            'Chômage, total jeune entre 15-24  (%\xa0de la population)'
        ]
    },
    "prod_model" : {
        "path" : "models/prod_model.keras",
        "seq_len" : 6,
        "indicators" : ['wheat_production (Million Bushels)']
    },
    "consum_model" : {
        "path" : "models/consum_model.keras",
        "seq_len" : 10,
        "indicators" : ['Consommation finals des ménages']
    }
}

def eco_model1_pred(df, exog_data, start_year, end_year):
    cfg = model_config["eco_model1"]
    seq_len = cfg["seq_len"]
    model = load_model(cfg["path"])
    indicators = cfg["indicators"]

    X_hist = df[indicators].iloc[-seq_len:].values          # shape: (seq_len, n_ind)
    exog_hist = df["event"].values.reshape(-1, 1)[-seq_len:]   # exogenous history

    n_steps = (end_year - start_year) * 12
    dates = pd.date_range(start=f"{start_year}-01-01",
                            periods=n_steps,
                            freq="MS")

    preds = np.zeros((n_steps, len(indicators)))  # each column ↔ one indicator

    X_seq = X_hist.copy()
    exog_seq = exog_hist.copy()

    for i in range(n_steps):
        # model expects shape (batch, seq_len, n_ind) + (batch, seq_len, n_exog)
        y_hat = model.predict(
            [X_seq[np.newaxis, ...], exog_seq[np.newaxis, ...]],
            verbose=0
        )[0]               # shape (n_ind,)  ← assuming 1-step vector output

        preds[i] = y_hat   # store for this month

        # shift windows forward one step
        X_seq = np.vstack([X_seq[1:], y_hat.reshape(1, -1)])
        exog_seq = np.vstack([exog_seq[1:], exog_data[i].reshape(1, -1)])

    pred_df = pd.DataFrame(preds, columns=indicators)
    pred_df.insert(0, "date", dates)

    return pred_df
