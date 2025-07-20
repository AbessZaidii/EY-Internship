import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("aviation_grievance.csv")

data = load_data()

# Dashboard Title
st.title("BAII Embedded System - Grievance Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
category = st.sidebar.multiselect("Select Grievance Category", options=data['category'].unique(), default=data['category'].unique())
subcategory = st.sidebar.multiselect("Select Subcategory", options=data['subcategory'].unique(), default=data['subcategory'].unique())
type_filter = st.sidebar.multiselect("Select Grievance Type", options=data['type'].unique(), default=data['type'].unique())

# Apply filters
filtered_data = data[
    (data['category'].isin(category)) &
    (data['subcategory'].isin(subcategory)) &
    (data['type'].isin(type_filter))
]

# Display Data
st.subheader("Filtered Grievance Data")
st.dataframe(filtered_data)

# Plotly Visualization
st.subheader("Grievance Count by Category")
graph_data = filtered_data['category'].value_counts().reset_index()
graph_data.columns = ['Category', 'Count']
fig = px.bar(graph_data, x='Category', y='Count', title='Grievances per Category', color='Category')
st.plotly_chart(fig)

# Pie Chart for Active vs Closed Grievances
graph_status = pd.DataFrame({
    "Status": ["Active (No Escalation)", "Active (Escalated)", "Closed (No Escalation)", "Closed (Escalated)"],
    "Count": [
        filtered_data['activeGrievancesWithoutEscalation'].sum(),
        filtered_data['activeGrievancesWithEscalation'].sum(),
        filtered_data['closedGrievancesWithoutEscalation'].sum(),
        filtered_data['closedGrievancesWithEscalation'].sum()
    ]
})
fig2 = px.pie(graph_status, names='Status', values='Count', title='Grievance Status Distribution')
st.plotly_chart(fig2)

# Grievance Count by Type
st.subheader("Grievance Count by Type")
graph_type = filtered_data['type'].value_counts().reset_index()
graph_type.columns = ['Type', 'Count']
fig3 = px.bar(graph_type, x='Type', y='Count', title='Grievances per Type', color='Type')
st.plotly_chart(fig3)

st.success("Dashboard Loaded Successfully!")
