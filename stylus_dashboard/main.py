import streamlit as st
from .config import PAGE_CONFIG
from .components.overview import render_overview
from .components.ecosystem_health import render_ecosystem_health
from .components.activity_analysis import render_activity_analysis
from .components.project_deep_dive import render_project_deep_dive
from .components.risk_assessment import render_risk_assessment
from .components.network_analysis import render_network_analysis
from .components.grantee_impact import render_grantee_impact

def main():
    # Set page configuration
    st.set_page_config(**PAGE_CONFIG)

    # Display banner image
    # banner_image = Image.open('./images/banner.jpg')
    # col1, col2, col3 = st.columns([1, 2, 1])
    # with col2:
    #     st.image(banner_image)

    # Main title
    st.title("📊 Stylus Sprint Ecosystem Dashboard")
    st.caption("Powered by [Open Source Observer](https://opensource.observer)")

    # Create tabs
    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Developer Ecosystem Health",
        "Stylus Sprint Activity Analysis",
        "Project Deep Dive",
        "Project Adoption & Dependencies",
        "Network Analysis"
    ])

    # Render each tab
    with tab0:
        render_overview()

    with tab1:
        render_ecosystem_health()

    with tab2:
        render_activity_analysis()

    with tab3:
        render_project_deep_dive()

    with tab4:
        render_grantee_impact()

    with tab5:
        render_network_analysis()

if __name__ == "__main__":
    main() 