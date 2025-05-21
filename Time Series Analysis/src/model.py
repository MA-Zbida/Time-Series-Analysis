import numpy as np
import pandas as pd
import joblib
import os
from tensorflow.keras.models import load_model 

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
model_config = {
    "eco_model1": {
        "path" : "models/eco_model1.h5",
        "path_scaler" : "scalers/eco1_scaler.pkl",
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
        "path" : "models/eco_model2.h5",
        "path_scaler" : "scalers/eco2_scaler.pkl",
        "seq_len":  6,
        "indicators" : ['brent_oil_prices(USD/barrel)',
            'crude_oil_prices(USD/barrel)',
            'daily_natural_gas_prices(USD/MMBtu)'
        ]
    },
    "demo_model" : {
        "path" : "models/demo_model.h5",
        "path_scaler" : "scalers/demo_scaler.pkl",
        "seq_len" : 23,
        "indicators" : ['Demographie', 
            'Pauvrete', 
            'Analphabetisme'
        ]
    },
    "rate_model" : {
        "path" : "models/rate_model.h5",
        "path_scaler" : "scalers/rate_scaler.pkl",
        "seq_len" : 13,
        "indicators" : ['Inflation, prix à la consommation (%\xa0annuel)',
            'Chômage, total (%\xa0de la population)',
            'Chômage, total jeune entre 15-24  (%\xa0de la population)'
        ]
    },
    "prod_model" : {
        "path" : "models/prod_model.h5",
        "path_scaler" : "scalers/prod_scaler.pkl",
        "seq_len" : 17,
        "indicators" : ['wheat_production (Million Bushels)']
    },
    "consum_model" : {
        "path" : "models/consum_model.keras",
        "path_scaler" : "scalers/consum_scaler.pkl",
        "seq_len" : 14,
        "indicators" : ['Consommation finals des ménages']
    }
}

def choose_model(model_config, chosen_ind):
    suitable_models = {}
    
    for model_name, config in model_config.items():
        indicators = config["indicators"]
        
        # Check if any of the chosen indicators are in this model
        if any(ind in indicators for ind in chosen_ind):
            suitable_models[model_name] = config
    
    return suitable_models

def forecast(df, exog_data, start_year, end_year, chosen_ind, model_config=model_config):
    # First, determine which models to use
    suitable_models = choose_model(model_config, chosen_ind)
    
    if not suitable_models:
        raise ValueError("No suitable models found for the chosen indicators")
    
    # Create date range for predictions
    n_steps = (end_year - start_year) * 12
    dates = pd.date_range(start=f"{start_year}-01-01",
                          periods=n_steps,
                          freq="MS")
    
    # Initialize results dictionary to store predictions for each indicator
    all_predictions = {}
    
    # Process each model
    for model_name, config in suitable_models.items():
        # Load model and scaler
        model = load_model(config["path"])
        with open(config["path_scaler"], 'rb') as f:
            scaler = joblib.load(f)
        
        model_indicators = config["indicators"]
        seq_len = config["seq_len"]
        
        # Only forecast indicators that are both chosen and available in this model
        indicators_to_forecast = [ind for ind in chosen_ind if ind in model_indicators]
        
        if not indicators_to_forecast:
            continue
        
        # Get historical data for this model's indicators
        X_hist = df[model_indicators].iloc[-seq_len:].values
        X_hist = scaler.transform(X_hist)
        
        # Get exogenous history
        exog_hist = df["event"].values.reshape(-1, 1)[-seq_len:]
        
        # Initialize predictions array for this model
        model_preds = np.zeros((n_steps, len(model_indicators)))
        
        # Setup initial sequences
        X_seq = X_hist.copy()
        exog_seq = exog_hist.copy()
        
        # Generate predictions step by step
        for i in range(n_steps):
            # Model expects shape (batch, seq_len, n_features) + (batch, seq_len, n_exog)
            y_hat = model.predict(
                [X_seq[np.newaxis, ...], exog_seq[np.newaxis, ...]],
                verbose=0
            )[0]
            
            # Inverse transform to get actual values
            model_preds[i] = scaler.inverse_transform(y_hat.reshape(1, -1))[0]
            
            # Update sequences for next prediction
            X_seq = np.vstack([X_seq[1:], y_hat.reshape(1, -1)])
            exog_seq = np.vstack([exog_seq[1:], exog_data[i].reshape(1, -1)])
        
        # Store predictions for this model's indicators
        model_pred_df = pd.DataFrame(model_preds, columns=model_indicators)
        
        # Add predictions to the results dictionary
        for ind in indicators_to_forecast:
            all_predictions[ind] = model_pred_df[ind].values
    
    # Combine all predictions into a single DataFrame
    pred_df = pd.DataFrame(all_predictions)
    pred_df.insert(0, "date", dates)
    
    return pred_df

