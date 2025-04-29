import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from ..config import DATA_PATHS
from ..utils.data_processing import load_data

def render_project_deep_dive():
    """Render the project deep dive analysis tab content."""
    st.header("Project Deep Dive Analysis")
    
    # Load data
    df = load_data(DATA_PATHS["stylus_metrics"])
    
    # Project selection
    all_projects = df['Name'].unique()
    selected_project = st.selectbox(
        "Select Project for Deep Dive",
        all_projects
    )
    
    # Calculate date 180 days ago
    latest_date = df['Date'].max()
    ninety_days_ago = latest_date - timedelta(days=180)
    
    # Filter data for selected project and last 90 days
    project_data = df[
        (df['Name'] == selected_project) &
        (df['Date'] >= ninety_days_ago)
    ]
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Development Velocity")
        
        # Weekly commits
        weekly_commits = project_data[project_data['Metric'] == 'GITHUB_commits_weekly']
        if not weekly_commits.empty:
            fig = px.bar(
                weekly_commits,
                x='Date',
                y='Value',
                title='Weekly Commits'
            )
            fig.update_yaxes(range=[0, weekly_commits['Value'].max() * 1.1])
            st.plotly_chart(fig, use_container_width=True)
        
        # PR merge time
        pr_merge_time = project_data[project_data['Metric'] == 'GITHUB_avg_prs_time_to_merge_quarterly']
        if not pr_merge_time.empty:
            st.metric(
                "Average PR Merge Time",
                f"{pr_merge_time['Value'].iloc[-1]:.1f} days"
            )
    
    with col2:
        st.subheader("Community Health")
        
        # New vs returning contributors
        new_contributors = project_data[project_data['Metric'] == 'GITHUB_new_contributors_monthly']
        active_contributors = project_data[project_data['Metric'] == 'GITHUB_active_contributors_monthly']
        
        if not new_contributors.empty and not active_contributors.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=new_contributors['Date'],
                y=new_contributors['Value'],
                name='New Contributors'
            ))
            fig.add_trace(go.Bar(
                x=active_contributors['Date'],
                y=active_contributors['Value'],
                name='Active Contributors'
            ))
            max_value = max(new_contributors['Value'].max(), active_contributors['Value'].max())
            fig.update_layout(
                title='Contributor Growth',
                barmode='group',
                yaxis=dict(range=[0, max_value * 1.1])
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Full-time vs part-time ratio
        full_time = project_data[project_data['Metric'] == 'GITHUB_full_time_developers_monthly']
        part_time = project_data[project_data['Metric'] == 'GITHUB_part_time_developers_monthly']
        
        if not full_time.empty and not part_time.empty:
            ratio = full_time['Value'].iloc[-1] / (full_time['Value'].iloc[-1] + part_time['Value'].iloc[-1])
            st.metric(
                "Full-time Developer Ratio",
                f"{ratio:.1%}"
            )
    
    with col3:
        st.subheader("Project Growth")
        
        # Forks trend
        forks = project_data[project_data['Metric'] == 'GITHUB_forks_monthly']
        if not forks.empty:
            fig = px.bar(
                forks,
                x='Date',
                y='Value',
                title='Monthly Forks'
            )
            fig.update_yaxes(range=[0, forks['Value'].max() * 1.1])
            st.plotly_chart(fig, use_container_width=True)
        
        # Stars trend
        stars = project_data[project_data['Metric'] == 'GITHUB_stars_monthly']
        if not stars.empty:
            st.metric(
                "Total Stars",
                f"{stars['Value'].sum():,.0f}"
            ) 