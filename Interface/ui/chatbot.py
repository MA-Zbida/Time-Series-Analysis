import streamlit as st
import re
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional
import pandas as pd

class EventExtractor:
    """Classe pour extraire les informations d'événements à partir de texte naturel"""
    
    def __init__(self):
        # Patterns regex pour extraction
        self.date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',  # DD/MM/YYYY ou DD-MM-YYYY
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',  # YYYY/MM/DD ou YYYY-MM-DD
            r'(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})',
            r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})',
            r'(en|dans|pour)\s+(\d{4})',
            r'(début|milieu|fin)\s+(\d{4})',
            r'(premier|deuxième|troisième|quatrième)\s+trimestre\s+(\d{4})',
        ]
        
        # Mots-clés pour catégorisation
        self.categories = {
            " Infrastructure & Transport": [
                "route", "autoroute", "pont", "tunnel", "port", "aéroport", "gare", "train", 
                "métro", "tramway", "transport", "infrastructure", "construction", "lgv",
                "ligne", "ferroviaire", "maritime", "aérien"
            ],
            " Énergie & Environnement": [
                "énergie", "électricité", "solaire", "éolien", "hydraulique", "barrage",
                "centrale", "renouvelable", "environnement", "écologie", "carbone",
                "dessalement", "eau", "nucléaire", "gaz", "pétrole"
            ],
            " Industrie & Manufacturing": [
                "usine", "industrie", "manufacturing", "production", "fabrication",
                "automobile", "textile", "chimie", "métallurgie", "zone industrielle",
                "factory", "assemblage", "batteries", "technologie"
            ],
            " Agriculture & Agroalimentaire": [
                "agriculture", "agricole", "ferme", "élevage", "irrigation", "céréales",
                "fruits", "légumes", "agroalimentaire", "pêche", "foresterie",
                "rural", "agriculteur", "récolte", "plantation"
            ],
            " Tourisme & Culture": [
                "tourisme", "hôtel", "resort", "musée", "culture", "festival",
                "patrimoine", "archéologie", "art", "théâtre", "cinéma",
                "station balnéaire", "vacances", "coupe du monde", "sport"
            ],
            " Santé & Éducation": [
                "hôpital", "clinique", "santé", "médical", "école", "université",
                "éducation", "formation", "recherche", "laboratoire", "campus",
                "médecine", "traitement", "centre de santé"
            ],
            " Digital & Technologies": [
                "digital", "numérique", "technologie", "informatique", "internet",
                "5g", "fibre", "data center", "intelligence artificielle", "ia",
                "blockchain", "cybersécurité", "software", "app", "plateforme"
            ],
            " Économie & Finance": [
                "banque", "finance", "économie", "bourse", "investissement",
                "fonds", "crédit", "assurance", "startup", "entreprise",
                "commerce", "export", "import", "pib", "croissance"
            ]
        }
        
        # Mots-clés pour sentiment/type
        self.positive_keywords = [
            "inauguration", "ouverture", "lancement", "création", "développement",
            "expansion", "croissance", "amélioration", "modernisation", "innovation",
            "succès", "réussite", "progrès", "avancement", "nouveau", "nouvelle"
        ]
        
        self.negative_keywords = [
            "crise", "fermeture", "recession", "chômage", "inflation", "pénurie",
            "conflit", "guerre", "catastrophe", "problème", "difficulté",
            "baisse", "diminution", "réduction", "échec", "faillite"
        ]
        
        # Mots-clés pour durée
        self.duration_keywords = {
            "court": ["jour", "semaine", "mois", "court terme"],
            "moyen": ["trimestre", "semestre", "moyen terme", "quelques mois"],
            "long": ["année", "années", "long terme", "décennie", "permanent"]
        }
        
        # Mots-clés pour intensité
        self.intensity_keywords = {
            "faible": ["léger", "modéré", "petit", "faible"],
            "moyen": ["important", "significatif", "notable", "moyen"],
            "fort": ["majeur", "crucial", "énorme", "massive", "révolutionnaire"]
        }
        
        # Villes du Maroc pour NER
        self.moroccan_cities = [
            "casablanca", "rabat", "fès", "marrakech", "agadir", "tanger",
            "meknès", "oujda", "kenitra", "tétouan", "safi", "mohammedia",
            "khouribga", "beni mellal", "el jadida", "nador", "settat",
            "berrechid", "khemisset", "inezgane", "sale", "larache",
            "ksar el kebir", "guelmim", "errachidia", "ouarzazate",
            "tiznit", "berkane", "taourirt", "sidi kacem", "midelt",
            "ifrane", "azrou", "chefchaouen", "al hoceima", "dakhla",
            "laayoune", "smara", "boujdour", "tarfaya", "nouaceur"
        ]

    def extract_date(self, text: str) -> Optional[str]:
        """Extrait la date du texte"""
        text_lower = text.lower()
        
        # Mois en français
        months = {
            'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
            'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
            'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
        }
        
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                match = matches[0]
                if isinstance(match, tuple):
                    if 'trimestre' in pattern:
                        quarter_map = {'premier': '01', 'deuxième': '04', 'troisième': '07', 'quatrième': '10'}
                        if match[0] in quarter_map:
                            return f"{match[1]}-{quarter_map[match[0]]}-01"
                    elif any(month in match for month in months.keys()):
                        for i, part in enumerate(match):
                            if part in months:
                                if i == 0 and len(match) == 2:  # "janvier 2030"
                                    return f"{match[1]}-{months[part]}-01"
                                elif i == 1 and len(match) == 3:  # "15 janvier 2030"
                                    return f"{match[2]}-{months[part]}-{match[0].zfill(2)}"
                    elif match[0] in ['en', 'dans', 'pour']:
                        return f"{match[1]}-06-01"  # Milieu d'année par défaut
                    elif match[0] in ['début', 'milieu', 'fin']:
                        month_map = {'début': '03', 'milieu': '06', 'fin': '09'}
                        return f"{match[1]}-{month_map[match[0]]}-01"
                else:
                    # Format direct de date
                    if '/' in match or '-' in match:
                        parts = re.split('[/-]', match)
                        if len(parts) == 3:
                            if len(parts[0]) == 4:  # YYYY-MM-DD
                                return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                            else:  # DD/MM/YYYY
                                return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        
        return None

    def extract_category(self, text: str) -> str:
        """Détermine la catégorie de l'événement"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "💼 Économie & Finance"  # Catégorie par défaut

    def extract_sentiment(self, text: str) -> str:
        """Détermine le type d'impact (Good/Bad)"""
        text_lower = text.lower()
        
        positive_score = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_score = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        if negative_score > positive_score:
            return "Bad"
        else:
            return "Good"

    def extract_peak_intensity(self, text: str, event_type: str) -> float:
        """Estime l'intensité de l'impact"""
        text_lower = text.lower()
        
        # Score de base selon le type
        base_intensity = 0.5 if event_type == "Good" else -0.5
        
        # Ajustement selon les mots-clés d'intensité
        for intensity, keywords in self.intensity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                if intensity == "faible":
                    multiplier = 0.6
                elif intensity == "moyen":
                    multiplier = 1.0
                else:  # fort
                    multiplier = 1.5
                return base_intensity * multiplier
        
        return base_intensity

    def extract_duration(self, text: str) -> int:
        """Estime la durée de l'impact en mois"""
        text_lower = text.lower()
        
        # Recherche de durées explicites
        duration_match = re.search(r'(\d+)\s*(mois|années?|ans?)', text_lower)
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2)
            if 'année' in unit or 'ans' in unit:
                return value * 12
            else:
                return value
        
        # Estimation basée sur les mots-clés
        for duration_type, keywords in self.duration_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                if duration_type == "court":
                    return 6
                elif duration_type == "moyen":
                    return 12
                else:  # long
                    return 24
        
        return 12  # Durée par défaut

    def extract_curve_type(self, text: str) -> str:
        """Détermine le type de courbe d'impact"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["progressif", "graduel", "linéaire", "constant"]):
            return "Linear"
        elif any(word in text_lower for word in ["explosif", "rapide", "exponentiel", "accélération"]):
            return "Exponential"
        elif any(word in text_lower for word in ["pic", "temporaire", "court", "ponctuel"]):
            return "Gaussian"
        
        return "Linear"  # Par défaut

    def extract_location(self, text: str) -> List[str]:
        """Extrait les villes mentionnées"""
        text_lower = text.lower()
        locations = []
        
        for city in self.moroccan_cities:
            if city in text_lower:
                locations.append(city.title())
        
        return locations

    def parse_event(self, text: str) -> Dict:
        """Parse un événement à partir de texte naturel"""
        # Extraction de tous les éléments
        date = self.extract_date(text)
        category = self.extract_category(text)
        event_type = self.extract_sentiment(text)
        peak = self.extract_peak_intensity(text, event_type)
        duration = self.extract_duration(text)
        curve = self.extract_curve_type(text)
        locations = self.extract_location(text)
        
        # Génération du nom de l'événement
        event_name = self.generate_event_name(text, locations)
        
        return {
            "Date": date or f"{datetime.now().year + 1}-06-01",
            "Event": event_name,
            "Type": event_type,
            "Peak": peak,
            "Duration": duration,
            "Curve": curve,
            "Description": text[:100] + "..." if len(text) > 100 else text,
            "Category": category,
            "Locations": locations
        }

    def generate_event_name(self, text: str, locations: List[str]) -> str:
        """Génère un nom d'événement basé sur le texte"""
        # Extraction des mots-clés principaux
        important_words = []
        text_words = text.lower().split()
        
        # Filtrage des mots importants
        stop_words = ['le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou', 'à', 'au', 'aux']
        for word in text_words[:10]:  # Premiers mots
            if len(word) > 3 and word not in stop_words:
                important_words.append(word.title())
                if len(important_words) >= 3:
                    break
        
        # Ajout de la localisation si disponible
        if locations:
            important_words.append(locations[0])
        
        return " ".join(important_words[:4])


def render_chatbot_tab():
    """Rendu de l'onglet chatbot"""
    st.header(" AI Assistant - Event Creation")
    
    # Initialisation de l'extracteur
    if 'event_extractor' not in st.session_state:
        st.session_state.event_extractor = EventExtractor()
    
    # Section d'aide
    with st.expander(" How to describe your event", expanded=False):
        st.markdown("""
        **Examples of event descriptions:**
        - "Inauguration d'une nouvelle usine automobile à Casablanca en mars 2028"
        - "Crise économique majeure prévue pour le deuxième trimestre 2027"
        - "Ouverture d'un grand complexe touristique à Agadir fin 2029"
        - "Lancement du projet de modernisation des ports en 2030"
        
        **The AI will extract:**
        -  Date and timeline
        -  Category and type
        -  Impact intensity and duration
        -  Geographic location
        -  Impact curve type
        """)
    
    # Zone de saisie pour l'événement
    st.subheader(" Describe Your Event")
    
    # Choix du mode de saisie
    input_mode = st.radio(
        "Choose input mode:",
        [" Natural Language", " Structured Form"],
        horizontal=True
    )
    
    if input_mode == " Natural Language":
        render_natural_language_input()
    else:
        render_structured_form_input()
    
    # Affichage des événements actuels
    render_current_events()


def render_natural_language_input():
    """Rendu de la saisie en langage naturel"""
    
    # Zone de texte principale
    user_input = st.text_area(
        "Describe your event in natural language:",
        placeholder="Example: Inauguration d'une nouvelle ligne de train à grande vitesse reliant Casablanca à Rabat en juin 2028, avec un impact économique majeur sur la région...",
        height=100,
        key="event_description"
    )
    
    # Boutons d'action
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button(" Analyze Event", use_container_width=True, disabled=not user_input):
            if user_input:
                with st.spinner("Analyzing your event description..."):
                    # Extraction des informations
                    extracted_event = st.session_state.event_extractor.parse_event(user_input)
                    st.session_state.current_extracted_event = extracted_event
                    
                    # Affichage des résultats
                    st.success(" Event analyzed successfully!")
                    
                    # Affichage des détails extraits
                    with st.expander(" Extracted Information", expanded=True):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"** Date:** {extracted_event['Date']}")
                            st.markdown(f"** Event:** {extracted_event['Event']}")
                            st.markdown(f"** Category:** {extracted_event['Category']}")
                            st.markdown(f"** Type:** {' Positive' if extracted_event['Type'] == 'Good' else ' Negative'}")
                        
                        with col_b:
                            st.markdown(f"** Peak Impact:** {extracted_event['Peak']:.2f}")
                            st.markdown(f"**⏱ Duration:** {extracted_event['Duration']} months")
                            st.markdown(f"** Curve:** {extracted_event['Curve']}")
                            if extracted_event['Locations']:
                                st.markdown(f"** Locations:** {', '.join(extracted_event['Locations'])}")
                        
                        st.markdown(f"** Description:** {extracted_event['Description']}")
    
    with col2:
        if st.button(" Add to Events", use_container_width=True, 
                    disabled='current_extracted_event' not in st.session_state):
            if 'current_extracted_event' in st.session_state:
                # Conversion au format attendu
                event_to_add = {
                    "Date": st.session_state.current_extracted_event['Date'],
                    "Event": st.session_state.current_extracted_event['Event'],
                    "Type": st.session_state.current_extracted_event['Type'],
                    "Peak": st.session_state.current_extracted_event['Peak'],
                    "Duration": st.session_state.current_extracted_event['Duration'],
                    "Curve": st.session_state.current_extracted_event['Curve'],
                    "Description": st.session_state.current_extracted_event['Description']
                }
                
                # Ajout à la session
                if 'events_data' not in st.session_state:
                    st.session_state.events_data = []
                
                st.session_state.events_data.append(event_to_add)
                st.success(f" Event '{event_to_add['Event']}' added successfully!")
                
                # Nettoyage
                if 'current_extracted_event' in st.session_state:
                    del st.session_state.current_extracted_event
                
                st.rerun()


def render_structured_form_input():
    """Rendu du formulaire structuré"""
    
    st.markdown("Fill in the event details manually:")
    
    with st.form("structured_event_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_name = st.text_input("Event Name*", placeholder="e.g., New Solar Plant Ouarzazate")
            event_date = st.date_input("Event Date*", min_value=date(2023, 1, 1))
            event_type = st.selectbox("Impact Type*", ["Good", "Bad"])
            category = st.selectbox("Category*", [
                " Infrastructure & Transport",
                " Énergie & Environnement", 
                " Industrie & Manufacturing",
                " Agriculture & Agroalimentaire",
                " Tourisme & Culture",
                " Santé & Éducation",
                " Digital & Technologies",
                " Économie & Finance"
            ])
        
        with col2:
            peak_impact = st.slider("Peak Impact", -1.0, 1.0, 0.5 if event_type == "Good" else -0.5, 0.1)
            duration = st.number_input("Duration (months)", min_value=1, max_value=60, value=12)
            curve_type = st.selectbox("Impact Curve", ["Linear", "Exponential", "Gaussian"])
            
        description = st.text_area("Description", placeholder="Detailed description of the event...")
        
        submitted = st.form_submit_button(" Add Event", use_container_width=True)
        
        if submitted and event_name and event_date:
            event_to_add = {
                "Date": event_date.strftime("%Y-%m-%d"),
                "Event": event_name,
                "Type": event_type,
                "Peak": peak_impact,
                "Duration": duration,
                "Curve": curve_type,
                "Description": description or f"Manual event: {event_name}"
            }
            
            if 'events_data' not in st.session_state:
                st.session_state.events_data = []
            
            st.session_state.events_data.append(event_to_add)
            st.success(f" Event '{event_name}' added successfully!")
            st.rerun()


def render_current_events():
    """Affichage des événements actuels"""
    
    if st.session_state.events_data:
        st.subheader(f" Current Events ({len(st.session_state.events_data)})")
        
        # Affichage sous forme de tableau
        df = pd.DataFrame(st.session_state.events_data)
        
        # Formatage pour l'affichage
        display_df = df.copy()
        if not display_df.empty:
            display_df = display_df[['Date', 'Event', 'Type', 'Peak', 'Duration', 'Description']]
            display_df['Impact'] = display_df.apply(lambda row: 
                f"{'' if row['Type'] == 'Good' else ''} {row['Peak']:.2f}", axis=1)
            display_df['Duration'] = display_df['Duration'].astype(str) + " months"
        
        st.dataframe(
            display_df[['Date', 'Event', 'Impact', 'Duration', 'Description']], 
            use_container_width=True,
            hide_index=True
        )
        
        # Bouton pour vider les événements
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(" Clear All Events", use_container_width=True):
                st.session_state.events_data = []
                st.success("All events cleared!")
                st.rerun()
    
    else:
        st.info(" No events added yet. Use the AI assistant above to add your first event!")


# Fonction d'assistance pour la gestion des événements
def get_events_summary():
    """Retourne un résumé des événements actuels"""
    if not st.session_state.events_data:
        return "No events currently loaded."
    
    total_events = len(st.session_state.events_data)
    positive_events = sum(1 for event in st.session_state.events_data if event['Type'] == 'Good')
    negative_events = total_events - positive_events
    
    return f"Total: {total_events} events ({positive_events} positive, {negative_events} negative)"