import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import des modules de l'interface
from ui.sidebar import render_sidebar
from ui.chatbot import render_chatbot_tab
from ui.indicators import render_indicators_tab
from ui.simulation import render_simulation_tab
from ui.overview import render_overview_tab
from ui.styles import load_custom_css

# Configuration de la page
st.set_page_config(
    page_title="Economic Impact Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des variables de session
def init_session_state():
    """Initialise les variables de session"""
    if 'events_data' not in st.session_state:
        st.session_state.events_data = []
    if 'selected_indicators' not in st.session_state:
        st.session_state.selected_indicators = []
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    """Fonction principale de l'application"""
    # Initialisation
    init_session_state()
    load_custom_css()
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>📊 Economic Impact Simulator</h1>
        <p>Advanced Economic Forecasting & Scenario Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendu de la sidebar et récupération de end_year
    end_year = render_sidebar()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Assistant", 
        "📊 Indicators", 
        "🔮 Simulation", 
        "📋 Overview"
    ])
    
    with tab1:
        render_chatbot_tab()
    
    with tab2:
        render_indicators_tab()
    
    with tab3:
        render_simulation_tab(end_year)
    
    with tab4:
        render_overview_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 1rem;">
        <p><strong>Economic Impact Simulator</strong> | Professional Forecasting Tool</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()