import streamlit as st
import pandas as pd
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import numpy as np


# importing fuctions for data processing
# from functions.categorise_events import categorise_event
# from functions.standardise_headers import standardise_headers
# from functions.load_google_sheet import load_multiple_spreadsheets

from functions.process_data import process_data
from functions.load_google_sheet import load_forms_spreadsheets
from functions.load_humanitix_sheets import load_humanitix_spreadsheets


st.set_page_config(
    page_title="Overview of Events",  # Change this to your desired title
    page_icon="📊",  # Optional: Add a favicon (can be an emoji or a URL)
    layout="centered"  # Optional: Set the page layout (wide or centered)
)

page_bg = """
<style>
    /* Change main page background */
    .stApp {
        background-color: #212751; /* Light gray */
    }

    /* Change sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #1A1A3D; /* Light blue-gray */
    }

    /* Change top navbar (Streamlit menu bar) */
    header[data-testid="stHeader"] {
        background-color: #212751; /* Darker blue */
    }

    /* Change font color in the navbar */
    header[data-testid="stHeader"] * {
        color: white; /* Change text/icon color to white */
    }
</style>
"""

st.title("Welcome to the WIT Event Engagement Dashboard!")


# ------------------------------------------------------------------------------------------*/
# Loading the data

google_forms_data = load_forms_spreadsheets()
humanitix_data = load_humanitix_spreadsheets()

# Process the data to get the main dataframe
df_processed = process_data()

st.title("💻 WIT Event Engagement")
# ------------------------------------------------------------------------------------------*/

with st.expander("How to use this app"):
    st.markdown(
        """
        ### **How to use the app**
        - **Step 1**: Select a Python library of interest in the `Select a Partner tech used in the app` multi-select widget.
        - **Step 2**: Query results should appear after a short page refresh.

        ### **Tips for searching**
        - To retrieve apps built with LangChain **OR** Weaviate, make sure that the `Boolean Search` parameter in the sidebar is set to **`OR`**.
        - To retrieve apps built with LangChain **AND** Weaviate, make sure that the `Boolean Search` parameter in the sidebar is set to **`AND`**.
        
        ### **Disclaimer**
        - To retrieve apps built with LangChain **OR** Weaviate, make sure that the `Boolean Search` parameter in the sidebar is set to **`OR`**.
        - To retrieve apps built with LangChain **AND** Weaviate, make sure that the `Boolean Search` parameter in the sidebar is set to **`AND`**.
        
        """,
        unsafe_allow_html=True
    )



# ------------------------------------------------------------------------------------------*/
st.write("")  # Adds a single empty line
st.subheader("📋 Top 5 Highest Ranked Events")

# Sort by highest rating first
df_top_5 = df_processed.sort_values(by="Avg Event Rating", ascending=False).head(5)

# Display top 5 events as a numbered list
for i, event in enumerate(df_top_5["Event Name"], start=1):
    st.write(f"{i}. {event}")

# ------------------------------------------------------------------------------------------*/
st.markdown("---")
st.subheader("📊 Event Statistics Overview")

# Get statistics
total_events = len(df_processed)
highest_rating = df_processed["Avg Event Rating"].max()
lowest_rating = df_processed["Avg Event Rating"].min()
average_rating = round(df_processed["Avg Event Rating"].mean(), 2)

# Define colored box template
def colored_box(label, value, color):
    return f"""
    <div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; width: 150px; font-size: 16px; font-weight: bold; color: white;">
        {label}<br><span style="font-size: 20px;">{value}</span>
    </div>
    """

# Arrange boxes in a row using columns
col1, col2, col3, col4 = st.columns(4)

# Display each metric with a colored box
with col1:
    st.markdown(colored_box("Total Events", total_events, "#3498db"), unsafe_allow_html=True)
with col2:
    st.markdown(colored_box("Highest Rating", highest_rating, "#2ecc71"), unsafe_allow_html=True)
with col3:
    st.markdown(colored_box("Lowest Rating", lowest_rating, "#e74c3c"), unsafe_allow_html=True)
with col4:
    st.markdown(colored_box("Average Rating", average_rating, "#f39c12"), unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------*/

st.markdown("---")
st.subheader("Overview of All Events")
st.dataframe(df_processed)


st.success("Dashboard successfully loaded! 🎉")




# # Google Sheets API Setup
# def load_data():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
#     client = gspread.authorize(creds)
#     spreadsheet = client.open_by_key("1mNScnRSIOcKGFjGl31XTgSEkttaStMFy6bd1Jw0KJTY")
#     worksheet = spreadsheet.worksheet("Form Responses 1")  # Ensure correct sheet name
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)

#     # Rename headers for better readability
#     df.rename(columns={
#         "Overall, how would you rate this event?": "Event Rating",
#         "How do you think this event has improved your knowledge in getting an internship? ": "Internship Knowledge Gain",
#         "How did you think of the registration, ticketing experience? ": "Registration Experience",
#         "How did you feel about the communication before, during and after the event? \n\n(e.g. receiving emails, communication and instruction given prior and during the event)": "Communication Rating",
#         "Which parts of the event did you like the most?": "Best Parts",
#         "Which parts of the event do you think can be improved on?": "Improvement Areas",
#         "How did you think of the food? ": "Food Rating",
#         "What are some topics / domains that you would like to hear about in our upcoming Women In X events? \n\n(e.g. Software Engineering, Cyber Security, UI/UX...etc.) ": "Future Topics",
#         "Any overall comment or suggestion?": "Feedback Comments",
#         "How likely is it that you would recommend the event to a friend or a peer?": "Recommendation Score"
#     }, inplace=True)

#     return df

# df = load_data()