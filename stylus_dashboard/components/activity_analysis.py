import streamlit as st
import pandas as pd
from ..config import DATA_PATHS, TIME_WINDOWS, AVAILABLE_METRICS
from ..utils.data_processing import load_data, filter_data_by_time_window, calculate_pct_change
from ..utils.visualization import create_developer_trend_plot, create_activity_heatmap

def render_activity_analysis():
    """Render the Stylus Sprint activity analysis tab content."""
    st.header("Stylus Sprint Activity Analysis")

    st.markdown("""
    This section provides a comprehensive analysis of developer engagement and project activity within the Stylus Sprint program. 
    You'll find:
    
    - **Developer Activity Trends**: Track the evolution of active developers over time
    - **Project Activity Heatmap**: Compare key metrics (commits, issues, PRs, etc.) across all projects
    - **Time-based Analysis**: Select different time windows to analyze patterns and growth
    """)
    
    # Add time window selector
    time_window = st.radio(
        "Select a time window to analyze developer activity trends and project metrics:",
        options=list(TIME_WINDOWS.keys()),
        horizontal=True,
        index=1,  # Default to 6 months
        key="overview_time_window"
    )

    st.markdown(f"### Monthly Active Developers Trend ({time_window})")

    # Load and process data
    df = load_data(DATA_PATHS["stylus_metrics"])
    df = filter_data_by_time_window(
        df[df['Metric'] == 'GITHUB_active_developers_monthly'],
        time_window
    )
    
    # Aggregate data across all projects
    aggregated_df = df.groupby('Date')['Value'].sum().reset_index()
    aggregated_df = calculate_pct_change(aggregated_df)
    
    # Create and display the trend plot
    fig = create_developer_trend_plot(aggregated_df)
    st.plotly_chart(fig, use_container_width=True)

    st.header(f"Project Activity Analysis ({time_window})")

    st.warning("""
    **Note:** Development metrics like commits, issues closed, and PRs merged can vary widely based on a project's workflow, team size, or codebase structure. These numbers aren't meant for head-to-head comparisons, but rather to track changes within the same project over time. Use them as directional signals to guide deeper, qualitative evaluation.
    """)
    
    # Metric selection with radio buttons
    selected_metric = st.radio(
        "Select Metric for Heatmap",
        options=list(AVAILABLE_METRICS.keys()),
        format_func=lambda x: AVAILABLE_METRICS[x],
        horizontal=True
    )
    
    # Filter data for selected metric and time window
    heatmap_data = load_data(DATA_PATHS["stylus_metrics"])
    heatmap_data = filter_data_by_time_window(
        heatmap_data[heatmap_data['Metric'] == selected_metric],
        time_window
    )
    
    # Aggregate data to handle duplicates
    heatmap_data = heatmap_data.groupby(['Name', 'Date'])['Value'].sum().reset_index()
    
    # Create and display the heatmap
    fig = create_activity_heatmap(heatmap_data, AVAILABLE_METRICS[selected_metric])
    st.plotly_chart(fig, use_container_width=True) 