import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64

# Import des modules nécessaires
from data import load_data
from model import forecast
from curves import event_calc

def render_simulation_tab(end_year):
    """Rendu de l'onglet simulation avec tous les résultats et visualisations"""
    st.markdown("###  Economic Simulation Results")
    
    # Bouton de simulation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Configurez vos événements et indicateurs, puis lancez la simulation.")
    
    with col2:
        simulate_button = st.button(
            " Lancer la Simulation", 
            type="primary",
            help="Démarrer la simulation d'impact économique",
            use_container_width=True
        )
    
    # Traitement de la simulation
    if simulate_button:
        _handle_simulation(end_year)
    
    # Affichage des résultats
    if st.session_state.simulation_results is not None:
        _display_simulation_results(end_year)

def _handle_simulation(end_year):
    """Gère le processus de simulation"""
    if not st.session_state.events_data or not st.session_state.selected_indicators:
        st.markdown("""
        <div class="status-warning">
             Veuillez configurer au moins un événement et sélectionner des indicateurs avant de lancer la simulation
        </div>
        """, unsafe_allow_html=True)
        return
    
    with st.spinner(" Simulation en cours..."):
        try:
            # Chargement et validation des données
            raw_data = load_data()
            
            # Conversion en DataFrame si nécessaire
            if isinstance(raw_data, dict):
                # Si c'est un dictionnaire, essayer de le convertir en DataFrame
                if 'data' in raw_data:
                    df = pd.DataFrame(raw_data['data'])
                elif 'df' in raw_data:
                    df = raw_data['df']
                else:
                    # Essayer de convertir directement le dictionnaire
                    df = pd.DataFrame(raw_data)
            elif isinstance(raw_data, pd.DataFrame):
                df = raw_data
            else:
                st.error(" Format de données non supporté")
                return
            
            # Validation du DataFrame
            if df.empty:
                st.warning(" Les données chargées sont vides. Génération de données de démonstration...")
                df = _generate_demo_base_data()
            
            # Création des données exogènes
            start_year = 2023
            dates = pd.date_range(start="2023-01-01", end=f"{end_year}-12-01", freq="MS")
            exog_data = pd.DataFrame(index=dates)
            exog_data["event"] = 0.0
            
            # Application des événements
            for event in st.session_state.events_data:
                try:
                    event_calc(exog_data, 
                              event["Date"],
                              event["Type"],
                              event["Peak"],
                              event["Duration"],
                              event["Curve"]
                    )
                except Exception as event_error:
                    st.warning(f" Erreur lors du traitement de l'événement {event.get('Event', 'Non nommé')}: {event_error}")
            
            # Tentative de prévision réelle
            try:
                # Vérifier d'abord si nous avons un modèle ajusté disponible
                if hasattr(st.session_state, 'fitted_models') and st.session_state.fitted_models:
                    # Utiliser les modèles déjà ajustés
                    preds_result = forecast(st.session_state.fitted_models, exog_data, start_year, end_year, st.session_state.selected_indicators)
                else:
                    # Essayer d'ajuster et de faire la prévision
                    preds_result = forecast(df, exog_data, start_year, end_year, st.session_state.selected_indicators)
                
                # Gestion des différents formats de retour de la fonction forecast
                if isinstance(preds_result, pd.DataFrame):
                    preds_df = preds_result
                elif isinstance(preds_result, dict):
                    if 'predictions' in preds_result:
                        preds_df = preds_result['predictions']
                    elif 'forecast' in preds_result:
                        preds_df = preds_result['forecast']
                    elif 'data' in preds_result:
                        preds_df = pd.DataFrame(preds_result['data'])
                    else:
                        # Si c'est un dictionnaire avec des données, essayer de le convertir
                        preds_df = pd.DataFrame(preds_result)
                else:
                    raise ValueError("Format de retour de forecast non reconnu")
                
                # Validation du DataFrame de prédictions
                if not isinstance(preds_df, pd.DataFrame):
                    raise ValueError("Les prédictions ne sont pas au format DataFrame")
                
                if preds_df.empty:
                    raise ValueError("Les prédictions sont vides")
                
                st.session_state.simulation_results = preds_df
                st.success(" Simulation terminée avec succès!")
                
            except Exception as model_error:
                st.warning(f" Modèle non disponible: {model_error}. Génération de données de démonstration...")
                
                # Simulation de démonstration
                preds_df = _generate_demo_simulation(start_year, end_year, exog_data)
                st.session_state.simulation_results = preds_df
                st.info(" Données de démonstration générées pour la visualisation")
            
        except Exception as e:
            st.error(f" Erreur durant la simulation: {str(e)}")
            st.error(" Tentative de génération de données de démonstration...")
            
            # Fallback complet
            try:
                start_year = 2023
                dates = pd.date_range(start="2023-01-01", end=f"{end_year}-12-01", freq="MS")
                exog_data = pd.DataFrame(index=dates)
                exog_data["event"] = 0.0
                
                preds_df = _generate_demo_simulation(start_year, end_year, exog_data)
                st.session_state.simulation_results = preds_df
                st.warning(" Simulation de secours activée")
            except Exception as fallback_error:
                st.error(f" Échec complet de la simulation: {fallback_error}")

def _generate_demo_base_data():
    """Génère des données de base pour la démonstration"""
    dates = pd.date_range(start="2020-01-01", end="2022-12-01", freq="MS")
    demo_base = {"date": dates}
    
    # Génération de données historiques pour quelques indicateurs
    base_indicators = ["PIB", "Inflation", "Chomage", "Investissement", "Consommation"]
    
    for indicator in base_indicators:
        if indicator == "PIB":
            trend = np.linspace(1000, 1100, len(dates))
        elif indicator == "Inflation":
            trend = np.linspace(2, 4, len(dates))
        elif indicator == "Chomage":
            trend = np.linspace(8, 6, len(dates))
        else:
            trend = np.linspace(100, 120, len(dates))
        
        noise = np.random.normal(0, np.std(trend) * 0.1, len(dates))
        demo_base[indicator] = trend + noise
    
    return pd.DataFrame(demo_base)

def _generate_demo_simulation(start_year, end_year, exog_data):
    """Génère une simulation de démonstration"""
    demo_dates = pd.date_range(f"{start_year}-01-01", f"{end_year}-12-01", freq="MS")
    demo_data = {"date": demo_dates}
    
    # Limiter le nombre d'indicateurs pour la performance
    selected_indicators = st.session_state.selected_indicators[:8] if len(st.session_state.selected_indicators) > 8 else st.session_state.selected_indicators
    
    for indicator in selected_indicators:
        # Définir une tendance de base selon l'indicateur
        if "PIB" in indicator.upper() or "CROISSANCE" in indicator.upper():
            base_trend = np.linspace(1000, 1200, len(demo_dates))
            volatility = 20
        elif "INFLATION" in indicator.upper():
            base_trend = np.linspace(2, 3.5, len(demo_dates))
            volatility = 0.5
        elif "CHOMAGE" in indicator.upper():
            base_trend = np.linspace(8, 6.5, len(demo_dates))
            volatility = 0.8
        elif "TAUX" in indicator.upper():
            base_trend = np.linspace(1.5, 2.5, len(demo_dates))
            volatility = 0.3
        else:
            base_trend = np.linspace(100, 130, len(demo_dates))
            volatility = 5
        
        # Ajout du bruit
        noise = np.random.normal(0, volatility, len(demo_dates))
        
        # Influence des événements
        if len(exog_data) > 0:
            # Interpoler les événements sur la période de simulation
            event_influence = np.interp(
                np.arange(len(demo_dates)), 
                np.arange(len(exog_data)), 
                exog_data["event"].values
            ) * (volatility * 2)
        else:
            event_influence = np.zeros(len(demo_dates))
        
        # Combiner tous les effets
        demo_data[indicator] = base_trend + noise + event_influence
        
        # S'assurer que les valeurs restent positives pour certains indicateurs
        if any(term in indicator.upper() for term in ["PIB", "INVESTISSEMENT", "CONSOMMATION"]):
            demo_data[indicator] = np.maximum(demo_data[indicator], 
                                             np.mean(demo_data[indicator]) * 0.1)
    
    return pd.DataFrame(demo_data)

def _display_simulation_results(end_year):
    """Affiche les résultats de simulation"""
    preds_df = st.session_state.simulation_results
    
    # Validation des données
    if preds_df is None or preds_df.empty:
        st.error(" Aucun résultat de simulation à afficher")
        return
    
    st.markdown("###  Résultats de la Simulation")
    
    # Métriques de résultats
    _display_result_metrics(preds_df)
    
    # Tableau des résultats
    st.markdown("####  Résultats Détaillés")
    with st.expander("Voir les données brutes", expanded=False):
        st.dataframe(preds_df, use_container_width=True)
    
    # Graphiques interactifs
    _display_interactive_charts(preds_df)
    
    # Options de téléchargement
    _display_download_options(preds_df, end_year)
    
    # Graphique de comparaison global
    _display_comparison_chart(preds_df)

def _display_result_metrics(preds_df):
    """Affiche les métriques des résultats"""
    col1, col2, col3, col4 = st.columns(4)
    
    indicator_columns = [col for col in preds_df.columns if col != 'date']
    
    with col1:
        st.metric("Période de Prévision", f"{len(preds_df)} mois")
    with col2:
        st.metric("Indicateurs Simulés", len(indicator_columns))
    with col3:
        st.metric("Événements Traités", len(st.session_state.events_data))
    with col4:
        st.metric("Points de Données", len(preds_df) * len(indicator_columns))

def _display_interactive_charts(preds_df):
    """Affiche les graphiques interactifs pour chaque indicateur"""
    st.markdown("####  Visualisations Interactives")
    
    indicator_columns = [col for col in preds_df.columns if col != 'date']
    
    if not indicator_columns:
        st.error(" Aucun indicateur trouvé dans les résultats")
        return
    
    # Sélecteur d'indicateur pour affichage
    if len(indicator_columns) > 1:
        selected_indicator = st.selectbox(
            "Choisir un indicateur à visualiser:",
            indicator_columns,
            key="chart_selector"
        )
        indicators_to_show = [selected_indicator]
    else:
        indicators_to_show = indicator_columns
    
    for indicator in indicators_to_show:
        if indicator in preds_df.columns:
            try:
                # Création du graphique
                fig = _create_indicator_chart(preds_df, indicator)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques de l'indicateur
                _display_indicator_stats(indicator, preds_df)
            except Exception as chart_error:
                st.error(f"❌ Erreur lors de la création du graphique pour {indicator}: {chart_error}")

def _create_indicator_chart(preds_df, indicator):
    """Crée un graphique pour un indicateur donné"""
    fig = go.Figure()
    
    # Vérification des données
    if 'date' not in preds_df.columns:
        st.error("❌ Colonne 'date' manquante dans les données")
        return fig
    
    if indicator not in preds_df.columns:
        st.error(f"❌ Indicateur '{indicator}' non trouvé dans les données")
        return fig
    
    # Ligne principale de l'indicateur
    fig.add_trace(go.Scatter(
        x=preds_df['date'],
        y=preds_df[indicator],
        mode='lines+markers',
        name=indicator,
        line=dict(width=3, color='#3b82f6'),
        marker=dict(size=6, color='#1e40af'),
        hovertemplate='<b>Date</b>: %{x}<br><b>Valeur</b>: %{y:.2f}<extra></extra>'
    ))
    
    # Ajout des événements sur le graphique
    for i, event in enumerate(st.session_state.events_data):
        try:
            event_date = pd.to_datetime(event["Date"])
            if event_date >= preds_df['date'].min() and event_date <= preds_df['date'].max():
                # Trouver la valeur Y la plus proche
                closest_idx = preds_df['date'].sub(event_date).abs().idxmin()
                event_y = preds_df.loc[closest_idx, indicator]
                
                # Couleur selon le type d'événement
                color = "red" if event["Type"] == "Bad" else "green"
                
                fig.add_annotation(
                    x=event_date,
                    y=event_y,
                    text=f" {event.get('Event', f'Événement {i+1}')}",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=color,
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor=color,
                    borderwidth=2
                )
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'événement {i}: {e}")
    
    fig.update_layout(
        title=f"Prévision: {indicator}",
        xaxis_title="Date",
        yaxis_title="Valeur",
        hovermode='x unified',
        showlegend=False,
        template="plotly_white",
        height=500
    )
    
    return fig

def _display_indicator_stats(indicator, preds_df):
    """Affiche les statistiques pour un indicateur"""
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    if len(preds_df) > 0 and indicator in preds_df.columns:
        try:
            current_val = preds_df[indicator].iloc[-1]
            initial_val = preds_df[indicator].iloc[0]
            change_pct = ((current_val - initial_val) / initial_val) * 100 if initial_val != 0 else 0
            volatility = preds_df[indicator].std()
            max_val = preds_df[indicator].max()
            
            with col_stat1:
                st.metric("Valeur Finale", f"{current_val:.2f}")
            with col_stat2:
                st.metric("Changement", f"{change_pct:+.1f}%")
            with col_stat3:
                st.metric("Volatilité", f"{volatility:.2f}")
            with col_stat4:
                st.metric("Maximum", f"{max_val:.2f}")
        except Exception as stats_error:
            st.error(f" Erreur lors du calcul des statistiques: {stats_error}")

def _display_download_options(preds_df, end_year):
    """Affiche les options de téléchargement des données"""
    st.markdown("####  Téléchargement des Données")
    
    col_csv, col_json, col_excel = st.columns(3)
    start_year = 2023
    
    with col_csv:
        try:
            csv = preds_df.to_csv(index=False)
            st.download_button(
                label=" Télécharger CSV",
                data=csv,
                file_name=f"simulation_economique_{start_year}_{end_year}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Erreur CSV: {e}")
    
    with col_json:
        try:
            json_data = preds_df.to_json(orient='records', date_format='iso')
            st.download_button(
                label=" Télécharger JSON",
                data=json_data,
                file_name=f"simulation_economique_{start_year}_{end_year}.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Erreur JSON: {e}")
    
    with col_excel:
        try:
            excel_buffer = _create_excel_export(preds_df, start_year, end_year)
            st.download_button(
                label=" Télécharger Excel",
                data=excel_buffer.getvalue(),
                file_name=f"simulation_economique_{start_year}_{end_year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Erreur Excel: {e}")

def _create_excel_export(preds_df, start_year, end_year):
    """Crée un fichier Excel avec plusieurs feuilles"""
    buffer = io.BytesIO()
    indicator_columns = [col for col in preds_df.columns if col != 'date']
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Feuille principale avec les résultats
        preds_df.to_excel(writer, sheet_name='Simulation_Results', index=False)
        
        # Feuille avec les événements configurés
        if st.session_state.events_data:
            events_df = pd.DataFrame(st.session_state.events_data)
            events_df.to_excel(writer, sheet_name='Events_Config', index=False)
        
        # Feuille avec les métriques et statistiques
        if indicator_columns:
            summary_data = {
                'Indicateur': indicator_columns,
                'Valeur_Initiale': [preds_df[ind].iloc[0] if len(preds_df) > 0 else 0 for ind in indicator_columns],
                'Valeur_Finale': [preds_df[ind].iloc[-1] if len(preds_df) > 0 else 0 for ind in indicator_columns],
                'Changement_Pct': [((preds_df[ind].iloc[-1] - preds_df[ind].iloc[0]) / preds_df[ind].iloc[0]) * 100 
                                 if len(preds_df) > 0 and preds_df[ind].iloc[0] != 0 else 0 for ind in indicator_columns],
                'Volatilite': [preds_df[ind].std() if len(preds_df) > 0 else 0 for ind in indicator_columns],
                'Maximum': [preds_df[ind].max() if len(preds_df) > 0 else 0 for ind in indicator_columns],
                'Minimum': [preds_df[ind].min() if len(preds_df) > 0 else 0 for ind in indicator_columns]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary_Stats', index=False)
        
        # Feuille avec les paramètres de simulation
        simulation_params = {
            'Paramètre': ['Année de début', 'Année de fin', 'Nombre d\'indicateurs', 'Nombre d\'événements'],
            'Valeur': [start_year, end_year, len(indicator_columns), len(st.session_state.events_data)]
        }
        params_df = pd.DataFrame(simulation_params)
        params_df.to_excel(writer, sheet_name='Simulation_Params', index=False)
    
    return buffer

def _display_comparison_chart(preds_df):
    """Affiche le graphique de comparaison globale"""
    st.markdown("####  Comparaison Globale des Indicateurs")
    
    indicator_columns = [col for col in preds_df.columns if col != 'date']
    
    if len(indicator_columns) <= 1:
        st.info("Sélectionnez au moins 2 indicateurs pour voir la comparaison globale.")
        return
    
    # Option pour choisir le type de comparaison
    comparison_type = st.radio(
        "Type de comparaison:",
        ["Normalisée (0-1)", "Valeurs absolues", "Pourcentage de changement"],
        horizontal=True
    )
    
    fig_comparison = go.Figure()
    colors = px.colors.qualitative.Set3
    
    try:
        if comparison_type == "Normalisée (0-1)":
            # Normaliser les données pour la comparaison
            normalized_data = preds_df.copy()
            for col in indicator_columns:
                if col in normalized_data.columns:
                    min_val = normalized_data[col].min()
                    max_val = normalized_data[col].max()
                    if max_val != min_val:
                        normalized_data[col] = (normalized_data[col] - min_val) / (max_val - min_val)
                    else:
                        normalized_data[col] = 0.5  # Valeur constante
            
            for i, indicator in enumerate(indicator_columns):
                fig_comparison.add_trace(go.Scatter(
                    x=normalized_data['date'],
                    y=normalized_data[indicator],
                    mode='lines',
                    name=indicator,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    hovertemplate=f'<b>{indicator}</b><br>Date: %{{x}}<br>Valeur Normalisée: %{{y:.3f}}<extra></extra>'
                ))
            
            y_title = "Valeur Normalisée (0-1)"
            
        elif comparison_type == "Pourcentage de changement":
            # Calculer le pourcentage de changement par rapport à la valeur initiale
            pct_change_data = preds_df.copy()
            for col in indicator_columns:
                if col in pct_change_data.columns and len(pct_change_data) > 0:
                    initial_val = pct_change_data[col].iloc[0]
                    if initial_val != 0:
                        pct_change_data[col] = ((pct_change_data[col] - initial_val) / initial_val) * 100
                    else:
                        pct_change_data[col] = 0
            
            for i, indicator in enumerate(indicator_columns):
                fig_comparison.add_trace(go.Scatter(
                    x=pct_change_data['date'],
                    y=pct_change_data[indicator],
                    mode='lines',
                    name=indicator,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    hovertemplate=f'<b>{indicator}</b><br>Date: %{{x}}<br>Changement: %{{y:.2f}}%<extra></extra>'
                ))
            
            y_title = "Changement (%)"
            
        else:  # Valeurs absolues
            for i, indicator in enumerate(indicator_columns):
                fig_comparison.add_trace(go.Scatter(
                    x=preds_df['date'],
                    y=preds_df[indicator],
                    mode='lines',
                    name=indicator,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    hovertemplate=f'<b>{indicator}</b><br>Date: %{{x}}<br>Valeur: %{{y:.2f}}<extra></extra>'
                ))
            
            y_title = "Valeur"
        
        fig_comparison.update_layout(
            title=f"Comparaison des Indicateurs Économiques ({comparison_type})",
            xaxis_title="Date",
            yaxis_title=y_title,
            hovermode='x unified',
            template="plotly_white",
            height=600,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Bouton de téléchargement du graphique de comparaison
        _display_comparison_chart_download(fig_comparison)
        
    except Exception as comparison_error:
        st.error(f" Erreur lors de la création du graphique de comparaison: {comparison_error}")

def _display_comparison_chart_download(fig_comparison):
    """Affiche l'option de téléchargement du graphique de comparaison"""
    col_download, col_info = st.columns([1, 3])
    
    with col_download:
        if st.button(" Télécharger Graphique", key="download_comparison"):
            try:
                img_bytes = fig_comparison.to_image(format="png", width=1400, height=800)
                st.download_button(
                    label=" PNG",
                    data=img_bytes,
                    file_name="comparaison_indicateurs.png",
                    mime="image/png",
                    key="save_comparison_png"
                )
            except Exception as e:
                st.warning(f"Génération PNG non disponible: {e}")
                # Fallback vers HTML
                html_str = fig_comparison.to_html()
                st.download_button(
                    label=" HTML",
                    data=html_str,
                    file_name="comparaison_indicateurs.html",
                    mime="text/html",
                    key="save_comparison_html"
                )
    
    with col_info:
        st.info(" Utilisez les contrôles de zoom et de pan pour explorer le graphique en détail.")

def get_simulation_summary():
    """Retourne un résumé de la simulation actuelle"""
    if st.session_state.simulation_results is None:
        return None

    preds_df = st.session_state.simulation_results
    indicator_columns = [col for col in preds_df.columns if col != 'date']
    
    summary = {
        'total_periods': len(preds_df),
        'total_indicators': len(indicator_columns),
        'total_events': len(st.session_state.events_data),
        'date_range': {
            'start': preds_df['date'].min().strftime('%Y-%m-%d') if len(preds_df) > 0 else None,
            'end': preds_df['date'].max().strftime('%Y-%m-%d') if len(preds_df) > 0 else None
        },
        'indicators': indicator_columns
    }
    
    return summary