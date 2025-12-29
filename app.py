import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Direct Mail Analytics", layout="wide")

@st.cache_data
def load_data():
    # Use Dataset/ to match folder on disk
    df = pd.read_csv('Dataset/direct_mail_campaigns_enriched.csv')
    
    # Calculate Market Tiers (Location based) logic from Phase 2
    location_perf = df.groupby('Location')['cpa'].mean().reset_index()
    cpa_33 = location_perf['cpa'].quantile(0.33)
    cpa_66 = location_perf['cpa'].quantile(0.66)

    def get_tier(cpa):
        if cpa <= cpa_33: return 'Top' # Lower CPA is better
        elif cpa <= cpa_66: return 'Middle'
        else: return 'Lower'

    location_perf['Market_Tier'] = location_perf['cpa'].apply(get_tier)
    df = df.merge(location_perf[['Location', 'Market_Tier']], on='Location')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please run data_prep.py first.")
    st.stop()

st.title("Share Local Media - Direct Mail Analytics")

# Sidebar
st.sidebar.header("Filters")
all_channels = sorted(df['Channel_Used'].unique())
channels = st.sidebar.multiselect('Channel', all_channels, default=all_channels)

all_tiers = ['Top', 'Middle', 'Lower']
tiers = st.sidebar.multiselect('Market Tier', all_tiers, default=all_tiers)

# Filter logic
filtered_df = df.copy()
if channels:
    filtered_df = filtered_df[filtered_df['Channel_Used'].isin(channels)]
if tiers:
    filtered_df = filtered_df[filtered_df['Market_Tier'].isin(tiers)]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}")
col2.metric("Avg CPA", f"${filtered_df['cpa'].mean():.2f}")
col3.metric("Avg ROAS", f"{filtered_df['roas'].mean():.2f}x")
col4.metric("Total Responses", f"{filtered_df['responses'].sum():,.0f}")

# Tabs
tab1, tab2 = st.tabs(["Charts", "Gravity View"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        # Bar: Avg CPA by Channel
        if not filtered_df.empty:
            avg_cpa_channel = filtered_df.groupby('Channel_Used')['cpa'].mean().reset_index()
            fig_cpa = px.bar(avg_cpa_channel, x='Channel_Used', y='cpa', title='Avg CPA by Channel')
            st.plotly_chart(fig_cpa, use_container_width=True)
        else:
            st.info("No data selected")
    
    with c2:
        # Bar: Avg ROAS by Market Tier
        if not filtered_df.empty:
            avg_roas_tier = filtered_df.groupby('Market_Tier')['roas'].mean().reset_index()
            # manual sort
            sorter = {'Top': 1, 'Middle': 2, 'Lower': 3}
            avg_roas_tier['order'] = avg_roas_tier['Market_Tier'].map(sorter)
            avg_roas_tier = avg_roas_tier.sort_values('order')
            fig_roas = px.bar(avg_roas_tier, x='Market_Tier', y='roas', title='Avg ROAS by Market Tier')
            st.plotly_chart(fig_roas, use_container_width=True)
        else:
            st.info("No data selected")

with tab2:
    st.subheader("Gravity View: Audience vs Efficiency")
    st.write("Bubble size = Revenue, Y-axis = -CPA (Higher is Better/More Efficient)")
    
    if not filtered_df.empty:
        # Gravity View: Scatter y=-cpa, size=revenue, color=channel
        filtered_df['inv_cpa'] = -filtered_df['cpa']
        
        fig_grav = px.scatter(filtered_df, x='audience_size_mailed', y='inv_cpa', 
                              size='revenue', color='Channel_Used',
                              hover_data=['Location', 'cpa', 'roas'],
                              title='Gravity View',
                              labels={'inv_cpa': 'Negative CPA (Higher is Better)', 'audience_size_mailed': 'Audience Size'})
        st.plotly_chart(fig_grav, use_container_width=True)
    else:
        st.info("No data selected")
