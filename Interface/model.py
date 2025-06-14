import numpy as np
import pandas as pd
import joblib
import os
from tensorflow.keras.models import load_model
from custom_functions import masked_mse_loss, sum_pooling
from data import monthly_data

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
model_config = {
    "eco_model1": {
        "path" : "saved_models/eco_model1.keras",
        "path_scaler" : "saved_scalers/eco_scaler1.pkl",
        "seq_len": 15,
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
        "path" : "saved_models/eco_model2.keras",
        "path_scaler" : "saved_scalers/eco_scaler2.pkl",
        "seq_len":  6,
        "indicators" : ['brent_oil_prices(USD/barrel)',
            'crude_oil_prices(USD/barrel)',
            'daily_natural_gas_prices(USD/MMBtu)'
        ]
    },
    "demo_model" : {
        "path" : "saved_models/demo_model.keras",
        "path_scaler" : "saved_scalers/demo_scaler.pkl",
        "seq_len" : 15,
        "indicators" : ['Demographie', 
            'Pauvrete', 
            'Analphabetisme'
        ]
    },
    "rate_model" : {
        "path" : "saved_models/rate_model.keras",
        "path_scaler" : "saved_scalers/rate_scaler.pkl",
        "seq_len" : 17,
        "indicators" : ['Inflation, prix à la consommation (%\xa0annuel)',
            'Chômage, total (%\xa0de la population)',
            'Chômage, total jeune entre 15-24  (%\xa0de la population)'
        ]
    },
    "prod_model" : {
        "path" : "saved_models/prod_model.keras",
        "path_scaler" : "saved_scalers/prod_scaler.pkl",
        "seq_len" : 10,
        "indicators" : ['wheat_production (Million Bushels)']
    },
    "consum_model" : {
        "path" : "saved_models/consum_model.keras",
        "path_scaler" : "saved_scalers/consum_scaler.pkl",
        "seq_len" : 21,
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


def requires_monthly_forecast(model_indicators):
    """Check if any of the model indicators require monthly forecasting"""
    monthly_indicators = monthly_data()
    return any(ind in monthly_indicators for ind in model_indicators)

def forecast(df, exog_data, start_year, end_year, chosen_ind, model_config=model_config):
    # First, determine which models to use
    suitable_models = choose_model(model_config, chosen_ind)
    
    if not suitable_models:
        raise ValueError("No suitable models found for the chosen indicators")
        
    # Initialize results dictionary to store predictions for each indicator
    all_predictions = {}
    
    # Process each model
    for model_name, config in suitable_models.items():
        print(f"Processing model: {model_name}")
        
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
        
        # Get initial sequence for prediction - ensure we have enough data
        if len(df) < seq_len:
            continue
            
        X_first = df[model_indicators].iloc[-seq_len:]
        X_first = scaler.transform(X_first)
        # Get exogenous data for initial sequence
        exog_first = df["event"].values[-seq_len:].reshape(-1, 1)
        
        # Determine if this model needs monthly forecasting
        use_monthly_forecast = requires_monthly_forecast(model_indicators)
        
        if use_monthly_forecast:
            # Basic month-by-month forecasting
            print(f"Using monthly forecast for {model_name}")
            
            # Calculate total months to forecast
            num_years = end_year - start_year
            total_months = num_years * 12
            
            # Initialize predictions array for monthly data
            model_preds = np.zeros((total_months, len(model_indicators)))
            
            # Setup initial sequences
            X_seq = X_first.copy()
            exog_seq = exog_first.copy()
            
            # Generate predictions month by month
            for month in range(total_months):
                # Prepare input
                X_input = X_seq.reshape(1, seq_len, len(model_indicators))
                exog_input = exog_seq[-1].reshape(1, -1)
                
                # Get prediction for next month
                y_hat = model.predict([X_input, exog_input], verbose=0)[0]
                
                # Inverse transform to get actual values
                y_pred_scaled = y_hat.reshape(1, -1)
                y_pred = scaler.inverse_transform(y_pred_scaled)[0]
                model_preds[month] = y_pred
                
                # Update sequence for next prediction (simple rolling window)
                X_seq = np.roll(X_seq, -1, axis=0)
                y_pred_df = pd.DataFrame([y_pred], columns=model_indicators)
                X_seq[-1] = scaler.transform(y_pred_df)[0]
                
                # Update exogenous sequence
                exog_seq = np.roll(exog_seq, -1, axis=0)
                current_exog_idx = len(df) + month
                if current_exog_idx < len(exog_data):
                    exog_seq[-1] = exog_data.iloc[current_exog_idx]
                else:
                    # Keep the last known value or use a pattern
                    exog_seq[-1] = exog_seq[-2] if len(exog_seq) > 1 else exog_seq[-1]
            
            # Convert monthly predictions to yearly (take January values)
            yearly_preds = np.zeros((num_years, len(model_indicators)))
            for year in range(num_years):
                # Take January prediction (month 0, 12, 24, etc.)
                january_idx = year * 12
                yearly_preds[year] = model_preds[january_idx]
            
            model_preds = yearly_preds
            
        else:
            # Use your existing yearly forecasting approach
            print(f"Using yearly forecast for {model_name}")
            
            # Initialize predictions array
            num_years = end_year - start_year
            model_preds = np.zeros((num_years, len(model_indicators)))
            
            # Setup initial sequences
            X_seq = X_first.copy()
            exog_seq = exog_first.copy()
            
            # Generate predictions step by step (one year at a time)
            for i in range(num_years):
                # Ensure correct shape: (1, seq_len, n_features)
                X_input = X_seq.reshape(1, seq_len, len(model_indicators))
                exog_input = exog_seq[-1].reshape(1, -1)
                
                # Get prediction for next year
                y_hat = model.predict([X_input, exog_input], verbose=0)[0]
                
                # Inverse transform to get actual values
                y_pred_scaled = y_hat.reshape(1, -1)
                y_pred = scaler.inverse_transform(y_pred_scaled)[0]
                model_preds[i] = y_pred
                
                # Update sequence for next prediction
                if seq_len % 12 == 0:  # Model expects complete years
                    m = seq_len // 12
                    if m > 1:
                        # Shift by removing the oldest year (first 12 values)
                        X_seq = X_seq[12:].copy() 
                        # Add new prediction as January of the new year
                        new_year = pd.DataFrame(np.zeros((12, len(model_indicators))), columns=model_indicators)
                        new_year.iloc[0] = y_pred  # January
                        new_year_scaled = scaler.transform(new_year)
                        X_seq = np.vstack([X_seq, new_year_scaled])
                    else:
                        # Only one year in sequence, shift everything left
                        X_seq = np.roll(X_seq, -1, axis=0)
                        # Add new prediction at the beginning (January)
                        y_pred_df = pd.DataFrame([y_pred], columns=model_indicators)
                        X_seq[0] = scaler.transform(y_pred_df)[0]
                        
                elif seq_len > 12: # the yearly value exist in the middle of the sequence
                    r = seq_len % 12 # parameter that will position us in the right spot
                    X_seq = X_seq[r:].copy()
                    new_year = pd.DataFrame(np.zeros((r, len(model_indicators))), columns=model_indicators)
                    # Add new prediction at the beginning (January of next year)
                    new_year.iloc[0] = y_pred
                    new_year_scaled = scaler.transform(new_year)
                    X_seq = np.vstack([X_seq, new_year_scaled])
                
                else:  # seq_len < 12
                    # Simple rolling update
                    X_seq = np.roll(X_seq, -1, axis=0)
                    y_pred_df = pd.DataFrame([y_pred], columns=model_indicators)
                    X_seq[-1] = scaler.transform(y_pred_df)[0]
                
                # Update exogenous sequence
                if i + seq_len < len(exog_data):
                    exog_seq = exog_data[i + 1: i + seq_len + 1].values.reshape(-1, 1)
                else:
                    # Handle case where we run out of exogenous data
                    # Shift and use last available value or repeat pattern
                    exog_seq = np.roll(exog_seq, -1, axis=0)
                    if i + seq_len < len(exog_data):
                        exog_seq[-1] = exog_data.iloc[i + seq_len]
                    else:
                        # Keep the last known value
                        exog_seq[-1] = exog_seq[-2] if len(exog_seq) > 1 else exog_seq[-1]
        
        # Store predictions for this model's indicators
        model_pred_df = pd.DataFrame(model_preds, columns=model_indicators)
        
        # Add predictions to the results dictionary
        for ind in indicators_to_forecast:
            if ind in model_pred_df.columns:
                all_predictions[ind] = model_pred_df[ind].values
    
    # Combine all predictions into a single DataFrame
    if not all_predictions:
        raise ValueError("No predictions were generated")
        
    pred_df = pd.DataFrame(all_predictions)
    
    # Create date range for the forecast period
    num_years = end_year - start_year
    date_range = pd.date_range(start=f'{start_year}-01-01', 
                              periods=num_years, 
                              freq='YS')
    pred_df.insert(0, "date", date_range)
    
    return pred_df