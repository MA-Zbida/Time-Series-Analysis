import streamlit as st
from datetime import datetime
import json
import random
from PIL import Image
# Événements démonstratifs organisés par secteurs au Maroc
DEMO_EVENTS_BY_SECTOR = {
    " Infrastructure & Transport": [
        {
            "Date": "2030-06-15",
            "Event": "Inauguration LGV Casablanca-Marrakech",
            "Type": "Good",
            "Peak": 0.8,
            "Duration": 6,
            "Curve": "Exponential",
            "Description": "Ligne à grande vitesse reliant Casablanca à Marrakech"
        },
        {
            "Date": "2028-12-01",
            "Event": "Port Atlantique Dakhla",
            "Type": "Good",
            "Peak": 0.6,
            "Duration": 12,
            "Curve": "Linear",
            "Description": "Nouveau port commercial à Dakhla"
        },
        {
            "Date": "2029-03-15",
            "Event": "Aéroport International Agadir",
            "Type": "Good",
            "Peak": 0.5,
            "Duration": 8,
            "Curve": "Gaussian",
            "Description": "Extension de l'aéroport d'Agadir"
        }
    ],
    " Énergie & Environnement": [
        {
            "Date": "2027-09-01",
            "Event": "Complexe Solaire Noor Midelt",
            "Type": "Good",
            "Peak": 0.7,
            "Duration": 10,
            "Curve": "Linear",
            "Description": "Nouveau complexe solaire à Midelt"
        },
        {
            "Date": "2028-05-20",
            "Event": "Parc Éolien Offshore Atlantique",
            "Type": "Good",
            "Peak": 0.6,
            "Duration": 8,
            "Curve": "Exponential",
            "Description": "Premier parc éolien offshore du Maroc"
        },
        {
            "Date": "2026-11-10",
            "Event": "Station Dessalement Agadir",
            "Type": "Good",
            "Peak": 0.4,
            "Duration": 6,
            "Curve": "Gaussian",
            "Description": "Nouvelle station de dessalement"
        }
    ],
    " Industrie & Manufacturing": [
        {
            "Date": "2029-07-01",
            "Event": "Cité Mohammed VI Tanger Tech",
            "Type": "Good",
            "Peak": 0.9,
            "Duration": 12,
            "Curve": "Linear",
            "Description": "Nouvelle zone industrielle technologique"
        },
        {
            "Date": "2027-04-15",
            "Event": "Usine Batteries Électriques Kenitra",
            "Type": "Good",
            "Peak": 0.7,
            "Duration": 10,
            "Curve": "Exponential",
            "Description": "Première usine de batteries au Maroc"
        },
        {
            "Date": "2028-10-01",
            "Event": "Hub Logistique Nouaceur",
            "Type": "Good",
            "Peak": 0.5,
            "Duration": 8,
            "Curve": "Gaussian",
            "Description": "Nouveau hub logistique près de Casablanca"
        }
    ],
    " Agriculture & Agroalimentaire": [
        {
            "Date": "2027-02-01",
            "Event": "Plan Maroc Vert 2030",
            "Type": "Good",
            "Peak": 0.6,
            "Duration": 24,
            "Curve": "Linear",
            "Description": "Nouvelle stratégie agricole nationale"
        },
        {
            "Date": "2028-08-15",
            "Event": "Complexe Agro-industriel Meknès",
            "Type": "Good",
            "Peak": 0.5,
            "Duration": 12,
            "Curve": "Gaussian",
            "Description": "Nouveau complexe agroalimentaire"
        },
        {
            "Date": "2026-12-01",
            "Event": "Barrage Al Wahda Extension",
            "Type": "Good",
            "Peak": 0.4,
            "Duration": 6,
            "Curve": "Exponential",
            "Description": "Extension du barrage pour l'irrigation"
        }
    ],
    " Tourisme & Culture": [
        {
            "Date": "2030-06-13",
            "Event": "Coupe du Monde FIFA 2030",
            "Type": "Good",
            "Peak": 1.2,
            "Duration": 2,
            "Curve": "Gaussian",
            "Description": "Organisation conjointe de la Coupe du Monde"
        },
        {
            "Date": "2029-01-15",
            "Event": "Musée National Rabat",
            "Type": "Good",
            "Peak": 0.3,
            "Duration": 12,
            "Curve": "Linear",
            "Description": "Inauguration du nouveau musée national"
        },
        {
            "Date": "2028-07-01",
            "Event": "Station Balnéaire Taghazout",
            "Type": "Good",
            "Peak": 0.8,
            "Duration": 18,
            "Curve": "Exponential",
            "Description": "Nouvelle station touristique"
        }
    ],
    " Santé & Éducation": [
        {
            "Date": "2027-09-01",
            "Event": "Cité Médicale Casablanca",
            "Type": "Good",
            "Peak": 0.6,
            "Duration": 12,
            "Curve": "Linear",
            "Description": "Nouveau complexe hospitalier"
        },
        {
            "Date": "2028-02-15",
            "Event": "Université Internationale Rabat",
            "Type": "Good",
            "Peak": 0.5,
            "Duration": 24,
            "Curve": "Exponential",
            "Description": "Nouvelle université internationale"
        },
        {
            "Date": "2026-11-01",
            "Event": "Centre Formation Professionnelle",
            "Type": "Good",
            "Peak": 0.4,
            "Duration": 8,
            "Curve": "Gaussian",
            "Description": "Centres de formation dans tout le pays"
        }
    ],
    " Digital & Technologies": [
        {
            "Date": "2027-06-01",
            "Event": "Maroc Digital 2030",
            "Type": "Good",
            "Peak": 0.8,
            "Duration": 36,
            "Curve": "Linear",
            "Description": "Stratégie nationale de digitalisation"
        },
        {
            "Date": "2028-03-15",
            "Event": "Data Center Rabat",
            "Type": "Good",
            "Peak": 0.6,
            "Duration": 12,
            "Curve": "Exponential",
            "Description": "Nouveau data center national"
        },
        {
            "Date": "2029-10-01",
            "Event": "5G Deployment National",
            "Type": "Good",
            "Peak": 0.7,
            "Duration": 18,
            "Curve": "Linear",
            "Description": "Déploiement national de la 5G"
        }
    ],
    " Économie & Finance": [
        {
            "Date": "2027-01-01",
            "Event": "Casablanca Finance City 2030",
            "Type": "Good",
            "Peak": 0.9,
            "Duration": 24,
            "Curve": "Linear",
            "Description": "Expansion du centre financier"
        },
        {
            "Date": "2028-06-15",
            "Event": "Bourse Casablanca Digitale",
            "Type": "Good",
            "Peak": 0.5,
            "Duration": 12,
            "Curve": "Exponential",
            "Description": "Modernisation de la bourse"
        },
        {
            "Date": "2029-04-01",
            "Event": "Fonds Souverain Maroc",
            "Type": "Good",
            "Peak": 0.7,
            "Duration": 36,
            "Curve": "Linear",
            "Description": "Création du fonds souverain"
        }
    ],
    " Risques & Défis": [
        {
            "Date": "2028-07-15",
            "Event": "Sécheresse Prolongée",
            "Type": "Bad",
            "Peak": -0.8,
            "Duration": 12,
            "Curve": "Gaussian",
            "Description": "Impact climatique sur l'agriculture"
        },
        {
            "Date": "2029-03-01",
            "Event": "Crise Énergétique Globale",
            "Type": "Bad",
            "Peak": -0.6,
            "Duration": 8,
            "Curve": "Exponential",
            "Description": "Impact des prix énergétiques"
        },
        {
            "Date": "2027-11-15",
            "Event": "Tensions Géopolitiques Régionales",
            "Type": "Bad",
            "Peak": -0.4,
            "Duration": 6,
            "Curve": "Gaussian",
            "Description": "Instabilité régionale"
        }
    ]
}

def filter_events_by_period(start_year, end_year):
    """Filtre les événements selon la période de prévision"""
    filtered_events = []
    
    for sector, events in DEMO_EVENTS_BY_SECTOR.items():
        for event in events:
            event_year = int(event['Date'][:4])
            if start_year <= event_year <= end_year:
                # Ajouter l'information du secteur à l'événement
                event_with_sector = event.copy()
                event_with_sector['Sector'] = sector
                filtered_events.append(event_with_sector)
    
    return filtered_events

def render_sidebar():
    """Rendu de la sidebar avec configuration et sélection granulaire d'événements"""
    with st.sidebar:
        
        # Load image from local file
        image = Image.open("ui/logo.png")
        image = image.resize((1000, 2000))
        # Display centered image in the sidebar
        st.sidebar.image(image, use_container_width=True)
        st.markdown("###  Configuration")
        
        # Période de prévision
        st.markdown("####  Forecast Period")
        start_year = 2023
        end_year = st.slider(
            "End Year", 
            start_year, 2035, 2030,
            help="Select forecast horizon",
            key="end_year_slider"
        )
        
        # Métriques rapides
        years = list(range(start_year, end_year + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Years", f"{len(years)}")
        with col2:
            st.metric("Months", f"{len(years) * 12}")
        
        # Calculer les événements disponibles dans la période
        available_events = filter_events_by_period(start_year, end_year)
        st.info(f" {len(available_events)} events available in period {start_year}-{end_year}")
        
        st.markdown("---")
        
        # Sélection granulaire des événements démonstratifs
        st.markdown("####  Event Selection Methods")
        
        # Initialisation de la session state pour les événements sélectionnés
        if 'selected_demo_events' not in st.session_state:
            st.session_state.selected_demo_events = {}
        
        # Mode de sélection
        selection_mode = st.radio(
            "Selection Mode:",
            ["By Sector", "Random Selection"],
            help="Choose how to select events"
        )
        
        if selection_mode == "By Sector":
            # Sélection par secteur avec événements spécifiques
            selected_events_for_loading = []
            
            for sector, events in DEMO_EVENTS_BY_SECTOR.items():
                # Filtrer les événements de ce secteur selon la période
                sector_events_in_period = [e for e in events if start_year <= int(e['Date'][:4]) <= end_year]
                
                if sector_events_in_period:  # Afficher seulement si des événements existent dans la période
                    with st.expander(f"{sector} ({len(sector_events_in_period)} events in period)", expanded=False):
                        # Sélection de tous les événements du secteur
                        select_all_sector = st.checkbox(
                            f"Select all {sector.split(' ')[0]} events",
                            key=f"select_all_{sector}"
                        )
                        
                        # Sélection individuelle des événements
                        sector_selected_events = []
                        for i, event in enumerate(sector_events_in_period):
                            event_key = f"{sector}_{i}_{event['Event']}"
                            
                            # Si "select all" est coché, cocher automatiquement tous les événements
                            default_checked = select_all_sector
                            if event_key in st.session_state.selected_demo_events:
                                default_checked = st.session_state.selected_demo_events[event_key]
                            
                            is_selected = st.checkbox(
                                f" {event['Date'][:4]} - {event['Event']}",
                                value=default_checked if select_all_sector else st.session_state.selected_demo_events.get(event_key, False),
                                key=event_key,
                                help=f"Type: {event['Type']} | Peak: {event['Peak']} | Duration: {event['Duration']} months\n{event['Description']}"
                            )
                            
                            # Stocker l'état de sélection
                            st.session_state.selected_demo_events[event_key] = is_selected
                            
                            if is_selected:
                                sector_selected_events.append(event)
                                selected_events_for_loading.append(event)
                        
                        # Affichage du nombre d'événements sélectionnés dans ce secteur
                        if sector_selected_events:
                            st.success(f" {len(sector_selected_events)} events selected")
                        else:
                            st.info("No events selected")
            
            # Résumé de la sélection
            if selected_events_for_loading:
                st.markdown("####  Selection Summary")
                
                # Grouper par secteur pour l'affichage
                summary_by_sector = {}
                for event in selected_events_for_loading:
                    # Trouver le secteur de cet événement
                    for sector, sector_events in DEMO_EVENTS_BY_SECTOR.items():
                        if event in sector_events:
                            if sector not in summary_by_sector:
                                summary_by_sector[sector] = 0
                            summary_by_sector[sector] += 1
                            break
                
                # Afficher le résumé
                for sector, count in summary_by_sector.items():
                    st.write(f"**{sector}**: {count} events")
                
                st.write(f"**Total**: {len(selected_events_for_loading)} events")
                
                # Bouton pour charger les événements sélectionnés
                if st.button(" Load Selected Events", use_container_width=True, key="load_granular_events"):
                    st.session_state.events_data = selected_events_for_loading
                    st.success(f"Loaded {len(selected_events_for_loading)} events!")
                    st.rerun()
            else:
                st.info("No events selected. Choose events from the sectors above.")
        
        elif selection_mode == "Random Selection":
            # Mode de sélection aléatoire intelligent
            st.markdown(" **Smart Random Selection**")
            
            if available_events:
                # Configuration de la sélection aléatoire
                max_events = len(available_events)
                
                col1, col2 = st.columns(2)
                with col1:
                    num_events = st.number_input(
                        "Number of events:",
                        min_value=1,
                        max_value=max_events,
                        value=min(8, max_events),  # Valeur par défaut raisonnable
                        help=f"Select between 1 and {max_events} events"
                    )
                
                with col2:
                    st.metric("Available", max_events)
                
                # Options de filtrage pour la sélection aléatoire
                st.markdown("**Filtering Options:**")
                
                # Filtrage par type d'événement
                event_types = st.multiselect(
                    "Event types:",
                    ["Good", "Bad"],
                    default=["Good", "Bad"],
                    help="Include positive and/or negative events"
                )
                
                # Filtrage par secteurs
                available_sectors = list(set([event['Sector'] for event in available_events]))
                selected_sectors_for_random = st.multiselect(
                    "Limit to sectors:",
                    available_sectors,
                    default=available_sectors,
                    help="Leave empty or select all for no sector restriction"
                )
                
                # Équilibrage de la sélection
                balance_selection = st.checkbox(
                    "Balance sectors",
                    value=True,
                    help="Try to select events from different sectors equally"
                )
                
                # Filtrer les événements selon les critères
                filtered_for_random = []
                for event in available_events:
                    if event['Type'] in event_types:
                        if not selected_sectors_for_random or event['Sector'] in selected_sectors_for_random:
                            filtered_for_random.append(event)
                
                # Affichage des statistiques de filtrage
                st.info(f" {len(filtered_for_random)} events match your criteria")
                
                if filtered_for_random:
                    # Aperçu de la distribution par secteur
                    sector_distribution = {}
                    for event in filtered_for_random:
                        sector = event.get('Sector', None)
                        sector_distribution[sector] = sector_distribution.get(sector, 0) + 1
                    
                    with st.expander(" Available Distribution", expanded=False):
                        for sector, count in sorted(sector_distribution.items()):
                            st.write(f"**{sector}**: {count} events")
                    
                    # Bouton de sélection aléatoire
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(" Generate Random Selection", use_container_width=True, key="generate_random"):
                            # Logique de sélection aléatoire
                            if balance_selection and len(selected_sectors_for_random) > 1:
                                # Sélection équilibrée par secteur
                                events_per_sector = max(1, num_events // len(selected_sectors_for_random))
                                selected_random_events = []
                                
                                # Grouper par secteur
                                events_by_sector = {}
                                for event in filtered_for_random:
                                    sector = event.get('Sector')
                                    if sector not in events_by_sector:
                                        events_by_sector[sector] = []
                                    events_by_sector[sector].append(event)
                                
                                # Sélectionner de manière équilibrée
                                remaining_slots = num_events
                                for sector, sector_events in events_by_sector.items():
                                    if remaining_slots <= 0:
                                        break
                                    
                                    take = min(events_per_sector, len(sector_events), remaining_slots)
                                    selected_from_sector = random.sample(sector_events, take)
                                    selected_random_events.extend(selected_from_sector)
                                    remaining_slots -= take
                                
                                # Compléter si nécessaire
                                if remaining_slots > 0:
                                    remaining_events = [e for e in filtered_for_random if e not in selected_random_events]
                                    if remaining_events:
                                        additional = random.sample(remaining_events, 
                                                                 min(remaining_slots, len(remaining_events)))
                                        selected_random_events.extend(additional)
                            else:
                                # Sélection complètement aléatoire
                                selected_random_events = random.sample(
                                    filtered_for_random,
                                    min(num_events, len(filtered_for_random))
                                )
                            
                            # Stocker la sélection aléatoire
                            st.session_state.random_selection = selected_random_events
                            st.success(f" Selected {len(selected_random_events)} random events!")
                            st.rerun()
                    
                    with col2:
                        # Afficher la sélection actuelle s'il y en a une
                        if hasattr(st.session_state, 'random_selection') and st.session_state.random_selection:
                            current_count = len(st.session_state.random_selection)
                            st.metric("Selected", current_count)
                    
                    # Afficher la sélection aléatoire actuelle
                    if hasattr(st.session_state, 'random_selection') and st.session_state.random_selection:
                        st.markdown("####  Current Random Selection")
                        
                        # Statistiques de la sélection
                        selection_stats = {}
                        for event in st.session_state.random_selection:
                            sector = event.get('Sector')
                            selection_stats[sector] = selection_stats.get(sector, 0) + 1
                        
                        # Affichage compact des statistiques
                        stats_text = " | ".join([
                                        f"{(sector.split(' ')[0] if sector else 'Unknown')} {count}"
                                        for sector, count in selection_stats.items()
                                    ])

                        st.caption(f"Distribution: {stats_text}")
                        
                        # Liste des événements sélectionnés
                        with st.expander(" View Selected Events", expanded=False):
                            for i, event in enumerate(st.session_state.random_selection, 1):
                                type_icon = "✅" if event['Type'] == "Good" else "⚠️"
                                st.write(f"{i}. {type_icon} **{event['Event']}** ({event['Date'][:4]})")
                                st.caption(f"   {event.get('Sector', 'N/A')} | Peak: {event.get('Peak', 'N/A')} | Duration: {event.get('Duration', 'N/A')}m")

                        
                        # Bouton pour charger la sélection aléatoire
                        if st.button(" Load Random Selection", use_container_width=True, key="load_random_selection"):
                            st.session_state.events_data = st.session_state.random_selection
                            st.success(f"Loaded {len(st.session_state.random_selection)} randomly selected events!")
                            st.rerun()
                else:
                    st.warning("No events match your filtering criteria. Please adjust your filters.")
            else:
                st.warning(f"No events available in the period {start_year}-{end_year}.")
        
        st.markdown("---")
        
        # Actions rapides
        st.markdown("####  Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(" Reset Events", use_container_width=True, key="reset_events"):
                st.session_state.events_data = []
                st.session_state.selected_demo_events = {}
                if hasattr(st.session_state, 'random_selection'):
                    del st.session_state.random_selection
                st.success("Events cleared!")
                st.rerun()
        
        with col2:
            if st.button(" Load ALL", use_container_width=True, key="load_all_events"):
                st.session_state.events_data = available_events
                st.success(f"Loaded {len(available_events)} events from period!")
                st.rerun()
        
        # Bouton pour clear la sélection
        if st.button(" Clear Selection", use_container_width=True, key="clear_selection"):
            st.session_state.selected_demo_events = {}
            if hasattr(st.session_state, 'random_selection'):
                del st.session_state.random_selection
            st.success("Selection cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Status de session
        st.markdown("####  Session Status")
        
        status_data = {
            "Events": len(st.session_state.events_data),
            "Indicators": len(st.session_state.selected_indicators),
            "Messages": len(st.session_state.chat_history)
        }
        
        for key, value in status_data.items():
            st.write(f"**{key}:** {value}")
        
        # Simulation status
        sim_status = " Ready" if st.session_state.simulation_results is not None else " Pending"
        st.write(f"**Simulation:** {sim_status}")
        
        # Affichage des secteurs actifs
        if st.session_state.events_data:
            active_sectors = set()
            for event in st.session_state.events_data:
                # Chercher le secteur de l'événement
                event_sector = None
                for sector, events in DEMO_EVENTS_BY_SECTOR.items():
                    if event in events:
                        event_sector = sector
                        break
                
                # Si pas trouvé, utiliser le secteur stocké dans l'événement (pour les événements filtrés)
                if not event_sector and 'Sector' in event:
                    event_sector = event.get('Sector')
                
                if event_sector:
                    active_sectors.add(event_sector.split(' ')[0])  # Prendre l'emoji du secteur
            
            if active_sectors:
                st.write(f"**Active Sectors:** {' '.join(active_sectors)}")
        
        st.markdown("---")
        
        # Export rapide
        if st.button(" Export Session", use_container_width=True, key="export_session"):
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "forecast_period": {
                    "start_year": start_year,
                    "end_year": end_year
                },
                "events_count": len(st.session_state.events_data),
                "indicators_count": len(st.session_state.selected_indicators),
                "events": st.session_state.events_data,
                "indicators": st.session_state.selected_indicators,
                "selected_demo_events": st.session_state.selected_demo_events,
                "random_selection": getattr(st.session_state, 'random_selection', [])
            }
            
            st.download_button(
                label=" Download JSON",
                data=json.dumps(session_data, indent=2),
                file_name=f"morocco_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    return end_year