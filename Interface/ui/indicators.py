import streamlit as st

def render_indicators_tab():
    """Rendu de l'onglet sélection d'indicateurs"""
    st.markdown("###  Economic Indicators")
    
    # Chargement des indicateurs
    try:
        from ui.indicator_list import get_indicators
        all_indicators = get_indicators()
        
        st.markdown(f"""
        <div class="status-success">
             Successfully loaded {len(all_indicators)} indicators
        </div>
        """, unsafe_allow_html=True)
        
        # Catégorisation automatique
        categories = categorize_indicators(all_indicators)
        
    except Exception as e:
        st.markdown(f"""
        <div class="status-warning">
             Using default indicators: {str(e)[:50]}...
        </div>
        """, unsafe_allow_html=True)
        
        # Indicateurs par défaut
        categories = get_default_categories()
    
    # Interface de sélection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Select Indicators by Category")
        
        # Affichage par catégories
        for category, indicators in categories.items():
            if indicators:
                with st.expander(f"{category} ({len(indicators)} indicators)", expanded=True):
                    
                    # Sélection groupée
                    col_select, col_clear = st.columns([3, 1])
                    with col_select:
                        if st.button(f"Select All {category.split(' ')[1] if ' ' in category else category}", 
                                   key=f"select_all_{category}"):
                            for ind in indicators:
                                if ind not in st.session_state.selected_indicators:
                                    st.session_state.selected_indicators.append(ind)
                            st.rerun()
                    
                    with col_clear:
                        if st.button(f"Clear {category.split(' ')[1] if ' ' in category else category}", 
                                   key=f"clear_{category}"):
                            for ind in indicators:
                                if ind in st.session_state.selected_indicators:
                                    st.session_state.selected_indicators.remove(ind)
                            st.rerun()
                    
                    # Checkboxes individuelles
                    for indicator in indicators:
                        is_selected = indicator in st.session_state.selected_indicators
                        if st.checkbox(indicator, value=is_selected, key=f"ind_{indicator}"):
                            if indicator not in st.session_state.selected_indicators:
                                st.session_state.selected_indicators.append(indicator)
                        elif indicator in st.session_state.selected_indicators:
                            st.session_state.selected_indicators.remove(indicator)
    
    with col2:
        st.markdown("#### Selection Summary")
        
        # Métriques de sélection
        total_selected = len(st.session_state.selected_indicators)
        total_available = sum(len(indicators) for indicators in categories.values())
        
        st.metric("Selected", total_selected)
        st.metric("Available", total_available)
        st.metric("Progress", f"{(total_selected/total_available*100):.0f}%" if total_available > 0 else "0%")
        
        # Actions rapides
        st.markdown("#### Quick Actions")
        
        if st.button(" Clear All", use_container_width=True):
            st.session_state.selected_indicators = []
            st.rerun()
        
        if st.button(" Select Popular", use_container_width=True):
            popular_indicators = [
                "GDP Growth Rate (%)",
                "Inflation Rate (%)", 
                "Unemployment Rate (%)",
                "Exchange Rate"
            ]
            st.session_state.selected_indicators = [
                ind for ind in popular_indicators 
                if any(ind in cat_inds for cat_inds in categories.values())
            ]
            st.rerun()
        
        # Liste des indicateurs sélectionnés
        if st.session_state.selected_indicators:
            st.markdown("#### Selected Indicators")
            for i, indicator in enumerate(st.session_state.selected_indicators, 1):
                if st.button(f" {indicator[:25]}...", key=f"remove_{i}"):
                    st.session_state.selected_indicators.remove(indicator)
                    st.rerun()

def categorize_indicators(indicators):
    """Catégorise automatiquement les indicateurs"""
    categories = {
        " Economic Growth": [],
        " Trade & Finance": [],
        " Market Indicators": [],
        " Social Indicators": [],
        " Sectoral Data": [],
        " Other": []
    }
    
    for indicator in indicators:
        indicator_lower = indicator.lower()
        categorized = False
        
        # Croissance économique
        if any(word in indicator_lower for word in ['gdp', 'growth', 'pib', 'investissement', 'ide']):
            categories[" Economic Growth"].append(indicator)
            categorized = True
        
        # Commerce et finance
        elif any(word in indicator_lower for word in ['export', 'import', 'exchange', 'reer', 'taux']):
            categories[" Trade & Finance"].append(indicator)
            categorized = True
        
        # Indicateurs de marché
        elif any(word in indicator_lower for word in ['oil', 'gold', 'price', 'petrole', 'or']):
            categories[" Market Indicators"].append(indicator)
            categorized = True
        
        # Indicateurs sociaux
        elif any(word in indicator_lower for word in ['unemployment', 'chômage', 'inflation', 'démographie']):
            categories[" Social Indicators"].append(indicator)
            categorized = True
        
        # Données sectorielles
        elif any(word in indicator_lower for word in ['wheat', 'tourism', 'consumption', 'blé', 'tourisme']):
            categories[" Sectoral Data"].append(indicator)
            categorized = True
        
        # Autres
        if not categorized:
            categories[" Other"].append(indicator)
    
    return categories

def get_default_categories():
    """Retourne les catégories par défaut"""
    return {
        " Economic Growth": [
            "GDP Growth Rate (%)",
            "Foreign Direct Investment (USD)",
            "Government Expenditure (USD)"
        ],
        " Trade & Finance": [
            "Exchange Rate",
            "Export Value (USD)",
            "Import Value (USD)"
        ],
        " Market Indicators": [
            "Oil Price (USD/barrel)",
            "Gold Price (USD/oz)",
            "Stock Market Index"
        ],
        " Social Indicators": [
            "Inflation Rate (%)",
            "Unemployment Rate (%)",
            "Population Growth (%)"
        ]
    }