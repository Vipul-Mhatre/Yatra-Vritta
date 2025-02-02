# frontend.py
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import altair as alt

# Configure page
st.set_page_config(
    page_title="Medical Tourism Advisor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add these imports at the top of frontend.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pdf_report(data):
    """
    Generate a PDF report from the medical tourism data
    """
    # Create buffer for PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Medical Tourism Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Selected City Details
    story.append(Paragraph("Selected Destination", styles['Heading2']))
    selected_data = [
        ['Metric', 'Value'],
        ['City', data['selected']['name']],
        ['Country', data['selected']['countrycode']],
        ['Medical Tourism Score', f"{data['selected']['Medical Tourism Score']:.2f}"],
        ['Healthcare Index', f"{data['selected']['Hospital Beds per 1,000']:.2f}"],
        ['Safety Score', f"{data['selected']['Safety Index (Homicide Rate)']:.2f}"],
        ['Health Spending', f"${data['selected']['Health Spending per Capita (USD)']:,.2f}"]
    ]
    
    selected_table = Table(selected_data, colWidths=[2*inch, 4*inch])
    selected_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(selected_table)
    story.append(Spacer(1, 20))

    # Create visualizations for the report
    # Healthcare Comparison Chart
    plt.figure(figsize=(8, 4))
    healthcare_data = pd.DataFrame(data['recommendations']).head(5)
    plt.bar(healthcare_data['name'], healthcare_data['Hospital Beds per 1,000'])
    plt.title('Healthcare Infrastructure Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    
    # Add plot to PDF
    story.append(Paragraph("Healthcare Comparison", styles['Heading2']))
    img = Image(img_buffer, width=6*inch, height=3*inch)
    story.append(img)
    story.append(Spacer(1, 20))

    # Top Recommendations
    story.append(Paragraph("Top Recommendations", styles['Heading2']))
    story.append(Spacer(1, 12))

    # Create recommendations table
    recommendations_data = [['City', 'Country', 'Score', 'Healthcare', 'Safety']]
    for rec in data['recommendations'][:5]:
        recommendations_data.append([
            rec['name'],
            rec['countrycode'],
            f"{rec['Medical Tourism Score']:.2f}",
            f"{rec['Hospital Beds per 1,000']:.2f}",
            f"{rec['Safety Index (Homicide Rate)']:.2f}"
        ])

    recommendations_table = Table(recommendations_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch, 1*inch])
    recommendations_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(recommendations_table)

    # Add timestamp
    story.append(Spacer(1, 30))
    timestamp = Paragraph(
        f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Italic']
    )
    story.append(timestamp)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
# API configuration
BASE_URL = "http://localhost:5000"

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-title {
        font-size: 16px;
        color: #666;
    }
    .trend-up {
        color: #2ecc71;
    }
    .trend-down {
        color: #e74c3c;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data(ttl=3600)
def get_countries():
    try:
        response = requests.get(f"{BASE_URL}/countries")
        if response.ok:
            return response.json()['countries']
        st.error("Failed to fetch countries")
        return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def get_cities(country):
    try:
        response = requests.get(f"{BASE_URL}/cities", params={'country': country})
        if response.ok:
            return response.json()['cities']
        st.error("Failed to fetch cities")
        return []
    except Exception as e:
        st.error(f"Error fetching cities: {str(e)}")
        return []

def get_recommendations(country, city):
    try:
        payload = {"country": country, "city": city}
        response = requests.post(f"{BASE_URL}/recommend", json=payload)
        if response.ok:
            return response.json()
        st.error("Failed to get recommendations")
        return None
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return None

def create_metric_card(title, value, trend=None):
    trend_html = ""
    if trend is not None:
        trend_class = "trend-up" if trend >= 0 else "trend-down"
        trend_arrow = "↑" if trend >= 0 else "↓"
        trend_html = f'<div class="{trend_class}">{trend_arrow} {abs(trend):.1f}%</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-title">{title}</div>
        {trend_html}
    </div>
    """

def create_comparison_chart(data, feature, title):
    fig = go.Figure()
    
    # Add selected city
    fig.add_trace(go.Scatter(
        x=['Selected City'],
        y=[data['selected'][feature]],
        mode='markers',
        marker=dict(size=15, color='red'),
        name='Selected City'
    ))
    
    # Add recommended cities
    rec_names = [rec['name'] for rec in data['recommendations']]
    rec_values = [rec[feature] for rec in data['recommendations']]
    
    fig.add_trace(go.Scatter(
        x=rec_names,
        y=rec_values,
        mode='markers',
        marker=dict(size=10),
        name='Recommendations'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Cities",
        yaxis_title=feature,
        height=500,
        showlegend=True,
        xaxis_tickangle=45
    )
    
    return fig

# Main app
st.title("🏥 Medical Tourism Recommendation System")

# Sidebar
with st.sidebar:
    st.header("Search Parameters")
    countries = get_countries()
    selected_country = st.selectbox("Select Country", options=countries)
    
    if selected_country:
        cities = get_cities(selected_country)
        selected_city = st.selectbox("Select City", options=cities)
        
        analyze_btn = st.button("Analyze Destination", type="primary")
        
        st.markdown("---")
        st.markdown("### Filters")
        min_safety = st.slider("Minimum Safety Score", 0, 100, 50)
        max_cost = st.slider("Maximum Cost (USD)", 1000, 10000, 5000)

# Main content
if selected_country and selected_city and analyze_btn:
    with st.spinner("Analyzing destination..."):
        data = get_recommendations(selected_country, selected_city)
        
    if data:
        # Key Metrics Section
        st.header("📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Tourism Score",
                f"{data['selected']['Medical Tourism Score']:.1f}",
                5.2
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Healthcare Index",
                f"{data['selected']['Hospital Beds per 1,000']:.1f}",
                3.1
            ), unsafe_allow_html=True)
            
        with col3:
            st.markdown(create_metric_card(
                "Safety Score",
                f"{data['selected']['Safety Index (Homicide Rate)']:.1f}",
                1.8
            ), unsafe_allow_html=True)
            
        with col4:
            st.markdown(create_metric_card(
                "Cost Index",
                f"${data['selected']['Health Spending per Capita (USD)']:,.0f}",
                -2.3
            ), unsafe_allow_html=True)
        
        # Visualizations Section
        st.header("📈 Comparative Analysis")
        
        tab1, tab2, tab3 = st.tabs([
            "Healthcare Infrastructure",
            "Cost Analysis",
            "Safety Comparison"
        ])
        
        with tab1:
            fig_healthcare = create_comparison_chart(
                data,
                'Hospital Beds per 1,000',
                'Healthcare Infrastructure Comparison'
            )
            st.plotly_chart(fig_healthcare, use_container_width=True)
            
        with tab2:
            # Create scatter plot for cost analysis
            cost_data = pd.DataFrame(data['recommendations'])
            fig_cost = px.scatter(
                cost_data,
                x='Health Spending per Capita (USD)',
                y='Medical Tourism Score',
                size='GDP per Capita (USD)',
                hover_data=['name'],
                title='Cost vs Quality Analysis'
            )
            st.plotly_chart(fig_cost, use_container_width=True)
            
        with tab3:
            fig_safety = create_comparison_chart(
                data,
                'Safety Index (Homicide Rate)',
                'Safety Index Comparison'
            )
            st.plotly_chart(fig_safety, use_container_width=True)
        
        # Recommendations Section
        st.header("🎯 Top Recommendations")
        
        # Filter recommendations based on sidebar criteria
        filtered_recommendations = [
            rec for rec in data['recommendations']
            if (rec['Safety Index (Homicide Rate)'] >= min_safety and
                rec['Health Spending per Capita (USD)'] <= max_cost)
        ]
        
        if filtered_recommendations:
            for rec in filtered_recommendations[:5]:
                with st.container():
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h3>{rec['name']}, {rec['countrycode']}</h3>
                        <p>Medical Tourism Score: {rec['Medical Tourism Score']:.1f}</p>
                        <p>Healthcare Index: {rec['Hospital Beds per 1,000']:.1f}</p>
                        <p>Safety Score: {rec['Safety Index (Homicide Rate)']:.1f}</p>
                        <p>Cost: ${rec['Health Spending per Capita (USD)']:,.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations match your criteria. Try adjusting the filters.")
        
        # Export Options
        st.header("📤 Export Results")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download Report (PDF)"):
                st.download_button(
                    "Download",
                    data=generate_pdf_report(data),
                    file_name=f"medical_tourism_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        with col2:
            if st.button("Export Data (CSV)"):
                csv_data = pd.DataFrame(filtered_recommendations).to_csv(index=False)
                st.download_button(
                    "Download",
                    data=csv_data,
                    file_name=f"medical_tourism_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
else:
    st.info("👈 Select a country and city from the sidebar to get started")
    
    # Show sample insights
    st.header("💡 Did you know?")
    with st.expander("Medical Tourism Trends"):
        st.write("""
        - The global medical tourism market is expected to reach $207.9 billion by 2027
        - Popular destinations include Thailand, India, and Turkey
        - Common procedures include dental work, cosmetic surgery, and orthopedic treatments
        """)
    
    # Show feature preview
    st.header("🌟 Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🔍 Comprehensive Analysis
        - Healthcare infrastructure assessment
        - Safety metrics evaluation
        - Cost comparison
        """)
    with col2:
        st.markdown("""
        ### 📊 Interactive Visualizations
        - Compare multiple destinations
        - Analyze trends
        - Filter by preferences
        """)
    with col3:
        st.markdown("""
        ### 📑 Detailed Reports
        - Customizable exports
        - PDF reports
        - Data downloads
        """)

if __name__ == "__main__":
    st.markdown("---")
    st.markdown("Made with ❤️ for medical tourists worldwide")