import streamlit as st
import pandas as pd
from datetime import datetime

def render_overview_tab():
    """Rendu de l'onglet Overview avec résumé des données"""
    
    st.markdown("## 📋 Session Overview")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📅 Events Loaded", 
            len(st.session_state.events_data),
            help="Number of events in the current session"
        )
    
    with col2:
        st.metric(
            "📊 Indicators Selected", 
            len(st.session_state.selected_indicators),
            help="Number of economic indicators selected"
        )
    
    with col3:
        st.metric(
            "💬 Chat Messages", 
            len(st.session_state.chat_history),
            help="Number of messages in chat history"
        )
    
    with col4:
        simulation_status = "Ready" if st.session_state.simulation_results is not None else "Pending"
        st.metric(
            "🔮 Simulation Status", 
            simulation_status,
            help="Current simulation status"
        )
    
    st.markdown("---")
    
    # Détails des événements
    if st.session_state.events_data:
        st.markdown("### 📋 Events Summary")
        
        # Conversion en DataFrame pour affichage
        events_df = pd.DataFrame(st.session_state.events_data)
        
        # Statistiques des événements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Event Statistics")
            
            # Statistiques par type
            if 'Type' in events_df.columns:
                type_counts = events_df['Type'].value_counts()
                for event_type, count in type_counts.items():
                    icon = "✅" if event_type == "Good" else "⚠️"
                    st.write(f"{icon} **{event_type}**: {count} events")
            
            # Statistiques par courbe
            if 'Curve' in events_df.columns:
                st.markdown("**Curve Types:**")
                curve_counts = events_df['Curve'].value_counts()
                for curve, count in curve_counts.items():
                    st.write(f"📈 {curve}: {count}")
        
        with col2:
            st.markdown("#### 📅 Timeline Overview")
            
            # Période couverte
            if 'Date' in events_df.columns:
                dates = pd.to_datetime(events_df['Date'])
                start_date = dates.min()
                end_date = dates.max()
                
                st.write(f"**First Event:** {start_date.strftime('%Y-%m-%d')}")
                st.write(f"**Last Event:** {end_date.strftime('%Y-%m-%d')}")
                st.write(f"**Time Span:** {(end_date - start_date).days} days")
                
                # Événements par année
                yearly_counts = dates.dt.year.value_counts().sort_index()
                st.markdown("**Events by Year:**")
                for year, count in yearly_counts.items():
                    st.write(f"📅 {year}: {count} events")
        
        st.markdown("---")
        
        # Tableau détaillé des événements
        st.markdown("### 📋 Detailed Events Table")
        
        # Configuration d'affichage
        display_columns = st.multiselect(
            "Select columns to display:",
            options=events_df.columns.tolist(),
            default=['Date', 'Event', 'Type', 'Peak', 'Duration'] if len(events_df.columns) > 0 else [],
            help="Choose which columns to show in the table"
        )
        
        if display_columns:
            # Filtrage par type
            event_types = events_df['Type'].unique() if 'Type' in events_df.columns else []
            if len(event_types) > 1:
                selected_types = st.multiselect(
                    "Filter by event type:",
                    options=event_types,
                    default=event_types,
                    help="Filter events by their type"
                )
                filtered_df = events_df[events_df['Type'].isin(selected_types)]
            else:
                filtered_df = events_df
            
            # Affichage du tableau
            if not filtered_df.empty:
                st.dataframe(
                    filtered_df[display_columns],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Options d'export
                col1, col2 = st.columns(2)
                with col1:
                    csv_data = filtered_df[display_columns].to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv_data,
                        file_name=f"events_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    json_data = filtered_df[display_columns].to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_data,
                        file_name=f"events_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            else:
                st.info("No events match the current filters.")
        else:
            st.info("Select columns to display the events table.")
    
    else:
        st.info("No events loaded. Use the sidebar to load demo events or add custom events in the AI Assistant tab.")
    
    st.markdown("---")
    
    # Informations sur les indicateurs
    if st.session_state.selected_indicators:
        st.markdown("### 📊 Selected Indicators")
        
        for i, indicator in enumerate(st.session_state.selected_indicators, 1):
            st.write(f"{i}. **{indicator}**")
    else:
        st.info("No indicators selected. Go to the Indicators tab to select economic indicators.")
    
    # Résultats de simulation
    if st.session_state.simulation_results is not None:
        st.markdown("### 🔮 Simulation Results Summary")
        st.success("Simulation completed successfully!")
        
        # Vous pouvez ajouter ici un résumé des résultats de simulation
        # par exemple, des métriques clés ou des graphiques résumés
        
    else:
        st.info("No simulation results available. Run a simulation to see results here.")
    
    st.markdown("---")
    
    # Informations de session
    st.markdown("### ℹ️ Session Information")
    
    session_info = {
        "Session Started": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Total Events": len(st.session_state.events_data),
        "Total Indicators": len(st.session_state.selected_indicators),
        "Chat Messages": len(st.session_state.chat_history),
        "Simulation Status": "Completed" if st.session_state.simulation_results is not None else "Not Started"
    }
    
    for key, value in session_info.items():
        st.write(f"**{key}:** {value}")