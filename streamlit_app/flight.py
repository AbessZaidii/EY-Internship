import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("aviation_grievance.csv")

data = load_data()

st.title("BAII Embedded System - Grievance Dashboard")

st.sidebar.header("Filter Options")
category = st.sidebar.multiselect("Select Grievance Category", options=data['category'].unique(), default=data['category'].unique())
subcategory = st.sidebar.multiselect("Select Subcategory", options=data['subcategory'].unique(), default=data['subcategory'].unique())
type_filter = st.sidebar.multiselect("Select Grievance Type", options=data['type'].unique(), default=data['type'].unique())

filtered_data = data[
    (data['category'].isin(category)) & 
    (data['subcategory'].isin(subcategory)) &
    (data['type'].isin(type_filter))
]

st.subheader("Filtered Grievance Data")
st.dataframe(filtered_data)


st.subheader("Grievance Count by Category")
graph_data = filtered_data['category'].value_counts().reset_index()
graph_data.columns = ['Category', 'Count']
fig1 = px.bar(graph_data, x='Category', y='Count', title='Grievances per Category', color='Category', height=800, width=1200)
st.plotly_chart(fig1)


st.subheader("Grievance Count by Type")
graph_type_data = filtered_data['type'].value_counts().reset_index()
graph_type_data.columns = ['Type', 'Count']


x_order = ["Other", "Person With Disability", "Cleanliness", "Flight Delays", "Baggage", "Staff/Crew Behavior"]
graph_type_data = graph_type_data[graph_type_data["Type"].isin(x_order)]  # Filter only relevant types
graph_type_data["Type"] = pd.Categorical(graph_type_data["Type"], categories=x_order, ordered=True)  # Keep order

fig2 = px.bar(graph_type_data, x='Type', y='Count', title='Grievances per Type', color='Type', height=600, width=900)
st.plotly_chart(fig2)


graph_status = pd.DataFrame({
    "Status": ["Active (No Escalation)", "Active (Escalated)", "Closed (No Escalation)", "Closed (Escalated)", "Additional Info Not Provided", "Without Feedback"],
    "Count": [
        filtered_data['activeGrievancesWithoutEscalation'].sum(),
        filtered_data['activeGrievancesWithEscalation'].sum(),
        filtered_data['closedGrievancesWithoutEscalation'].sum(),
        filtered_data['closedGrievancesWithEscalation'].sum(),
        filtered_data['grievancesAdditionalInfoNotProvided'].sum(),
        filtered_data['grievancesWithoutFeedback'].sum()
    ]
})
st.subheader("Grievance Status Distribution")
fig3 = px.pie(graph_status, names='Status', values='Count', title='Grievance Status Distribution', height=600, width=900)
st.plotly_chart(fig3)

  
st.subheader("Unresolved Grievances by Category")
selected_categories = ["Airline", "DGCA", "Customs", "Immigration", "Airport"]
unresolved_data = filtered_data[filtered_data['category'].isin(selected_categories)]
unresolved_counts = unresolved_data.groupby('category')['activeGrievancesWithoutEscalation'].sum().reset_index()

fig4 = px.bar(unresolved_counts, x='category', y='activeGrievancesWithoutEscalation', 
              title='Unresolved Grievances for Airline, DGCA, Customs, Immigration, and Airport',
              color='category', height=600, width=900)

st.plotly_chart(fig4)
