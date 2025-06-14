import streamlit as st

def load_custom_css():
    """Charge les styles CSS personnalisés"""
    st.markdown("""
    <style>
        /* Header principal */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        /* Cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
            margin: 1rem 0;
        }
        
        .event-card {
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            margin: 1rem 0;
            transition: transform 0.2s ease;
        }
        
        .event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        /* Status indicators */
        .status-success {
            background: #dcfce7;
            border: 1px solid #16a34a;
            padding: 1rem;
            border-radius: 8px;
            color: #166534;
            margin: 0.5rem 0;
        }
        
        .status-warning {
            background: #fef3c7;
            border: 1px solid #d97706;
            padding: 1rem;
            border-radius: 8px;
            color: #92400e;
            margin: 0.5rem 0;
        }
        
        .status-error {
            background: #fee2e2;
            border: 1px solid #dc2626;
            padding: 1rem;
            border-radius: 8px;
            color: #991b1b;
            margin: 0.5rem 0;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #f8fafc;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
    </style>
    """, unsafe_allow_html=True)