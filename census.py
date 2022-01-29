import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above. 

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required 

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Census")
# Using the 'if' statement, display raw data on the click of the checkbox.
if st.sidebar.checkbox("Show Datasets"):
  st.subheader("Full Datasets")
  st.dataframe(census_df)
# Add a multiselect widget to allow the user to select multiple visualisations.
# Add a subheader in the sidebar with the label "Visualisation Selector"
st.sidebar.subheader("Visualisation Selector")

# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
plot_type=st.sidebar.multiselect("Select the charts",("Count plot","Pie Plot","Box Plot"))

# Display pie plot using matplotlib module and 'st.pyplot()'
if "Pie Plot" in plot_type:
  plt.figure(figsize=(16,6))
  select=st.sidebar.selectbox("Select the column to create pie plot",("income","gender"))
  if select == "income":
    plt.pie(census_df["income"].value_counts(),labels=census_df["income"].value_counts().index,autopct="%1.2f%%",shadow=True)
  elif select=="gender":
    b=census_df["gender"].value_counts()
    plt.pie(b,labels=b.index,autopct="%1.2f%%",shadow=True)
  st.pyplot()

if "Count plot" in plot_type:
	plt.figure(figsize=(16,6))
	sns.countplot(x="workclass",data=census_df,hue="income")
	st.pyplot()

if "Box Plot" in plot_type:
	plt.figure(figsize=(16,6))
	st.subheader("Box plot for the hours worked per week")
	select=st.sidebar.selectbox("Select the column to create box plot",("gender","income"))
	sns.boxplot(x="hours-per-week",y=select,data=census_df)
	st.pyplot()

