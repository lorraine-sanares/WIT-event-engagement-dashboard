import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="WIT Event Engagement Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.title("🚀 WIT Event Engagement Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("### Filters")

# Create sample data to avoid API issues
@st.cache_data
def create_sample_data():
    # Sample event data
    events = [
        "Women in Internships Workshop",
        "Macquarie Technical Workshop", 
        "Networking Cocktail",
        "Emergence Conference",
        "Tech Career Panel",
        "Python Coding Workshop",
        "Industry Mentorship Event",
        "AI & Machine Learning Talk"
    ]
    
    # Generate sample data
    np.random.seed(42)  # For reproducible results
    data = []
    
    for event in events:
        # Random data for each event
        attendees = np.random.randint(15, 100)
        rating = round(np.random.uniform(3.5, 5.0), 1)
        responses = np.random.randint(5, attendees//2)
        
        # Random date in the past year
        days_ago = np.random.randint(1, 365)
        event_date = datetime.now() - timedelta(days=days_ago)
        
        data.append({
            "Event Name": event,
            "Date": event_date.strftime("%Y-%m-%d"),
            "Attendees": attendees,
            "Survey Responses": responses,
            "Avg Rating": rating,
            "Response Rate": round((responses / attendees) * 100, 1),
            "Event Type": np.random.choice(["Workshop", "Networking", "Conference", "Panel"])
        })
    
    return pd.DataFrame(data)

# Load data
df = create_sample_data()

# Sidebar filters
event_types = st.sidebar.multiselect(
    "Select Event Types",
    options=df["Event Type"].unique(),
    default=df["Event Type"].unique()
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

# Filter data based on selections
filtered_df = df[
    (df["Event Type"].isin(event_types)) & 
    (df["Avg Rating"] >= min_rating)
]

# Main dashboard content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Events",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} from total"
    )

with col2:
    avg_rating = filtered_df["Avg Rating"].mean()
    st.metric(
        label="Average Rating",
        value=f"{avg_rating:.1f}/5.0",
        delta=f"{avg_rating - df['Avg Rating'].mean():.1f}"
    )

with col3:
    total_attendees = filtered_df["Attendees"].sum()
    st.metric(
        label="Total Attendees",
        value=total_attendees,
        delta=f"{total_attendees - df['Attendees'].sum()} from total"
    )

with col4:
    avg_response_rate = filtered_df["Response Rate"].mean()
    st.metric(
        label="Avg Response Rate",
        value=f"{avg_response_rate:.1f}%",
        delta=f"{avg_response_rate - df['Response Rate'].mean():.1f}%"
    )

st.markdown("---")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Event Ratings Distribution")
    fig_ratings = px.bar(
        filtered_df.sort_values("Avg Rating", ascending=False),
        x="Event Name",
        y="Avg Rating",
        color="Event Type",
        title="Average Rating by Event"
    )
    fig_ratings.update_xaxes(tickangle=45)
    st.plotly_chart(fig_ratings, use_container_width=True)

with col2:
    st.subheader("👥 Attendance vs Response Rate")
    fig_scatter = px.scatter(
        filtered_df,
        x="Attendees",
        y="Response Rate",
        size="Avg Rating",
        color="Event Type",
        hover_data=["Event Name"],
        title="Attendance vs Survey Response Rate"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Event performance table
st.subheader("📋 Event Performance Overview")
st.dataframe(
    filtered_df.sort_values("Avg Rating", ascending=False),
    use_container_width=True,
    hide_index=True
)

# Top performers section
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Rated Events")
    top_rated = filtered_df.nlargest(3, "Avg Rating")[["Event Name", "Avg Rating", "Attendees"]]
    for i, (_, row) in enumerate(top_rated.iterrows(), 1):
        st.write(f"{i}. **{row['Event Name']}** - {row['Avg Rating']}/5.0 ⭐ ({row['Attendees']} attendees)")

with col2:
    st.subheader("📈 Highest Attendance")
    top_attendance = filtered_df.nlargest(3, "Attendees")[["Event Name", "Attendees", "Avg Rating"]]
    for i, (_, row) in enumerate(top_attendance.iterrows(), 1):
        st.write(f"{i}. **{row['Event Name']}** - {row['Attendees']} attendees (Rating: {row['Avg Rating']}/5.0)")

# Add some insights
st.markdown("---")
st.subheader("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    best_event = filtered_df.loc[filtered_df["Avg Rating"].idxmax()]
    st.info(f"**Best Rated Event**: {best_event['Event Name']} ({best_event['Avg Rating']}/5.0)")

with col2:
    most_attended = filtered_df.loc[filtered_df["Attendees"].idxmax()]
    st.success(f"**Most Attended**: {most_attended['Event Name']} ({most_attended['Attendees']} people)")

with col3:
    best_response = filtered_df.loc[filtered_df["Response Rate"].idxmax()]
    st.warning(f"**Best Response Rate**: {best_response['Event Name']} ({best_response['Response Rate']}%)")

# Footer
st.markdown("---")
st.markdown("*Dashboard created for Women in Tech Unimelb - Event Engagement Analytics*") 