
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Style
plt.style.use('ggplot')

# Title
st.markdown('<h1 style="text-align: center;">A movie Recommendation App</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 16px; font-weight: bold;text-align: center;">(by Group3)</p>', unsafe_allow_html=True)
st.markdown('---')
# Load Data
df = pd.read_csv('Highest Holywood Grossing Movies.csv')
df['percentage_DomesticSales'] =  100 * df['Domestic Sales (in $)'] / (df['Domestic Sales (in $)'] + df['International Sales (in $)'])
df['percentage_InternationalSales'] = 100 * df['International Sales (in $)'] / (df['Domestic Sales (in $)'] + df['International Sales (in $)'])
distributors = [
    'Twentieth Century Fox',
    'Walt Disney Studios Motion Pictures',
    'Paramount Pictures',
    'Universal Pictures',
    'Sony Pictures Entertainment (SPE)',
    'Warner Bros.'
]
df["Distributor"] = df["Distributor"].apply(lambda x: "Others" if x not in distributors else x)

# add a ration to select genre
st.sidebar.info('**Step 1:**')
opt1 = ('Action','Adventure', 'Animation', 'Comedy', 'Drama', 'Family', 'Fantasy', 'Musical','Sci-Fi')
Genre_filter = st.sidebar.radio("**Choose your preferred genre**", opt1)
con = df["Genre"].apply(lambda x: True if Genre_filter in x else False)

# add a multiselect by Distributor
st.sidebar.info('**Step 2:**')
opt2 = ['Twentieth Century Fox', 
        'Walt Disney Studios Motion Pictures', 
        'Paramount Pictures', 
        'Universal Pictures', 
        'Sony Pictures Entertainment (SPE)', 
        'Warner Bros.', 
        'Others']
Distributor_filter = st.sidebar.multiselect(
    '**choose your preferred distributor**', 
    opt2,  # add 'Others' to include all other distributors
    default=['Twentieth Century Fox', 'Walt Disney Studios Motion Pictures']  #I am not sure about the default
)

# add multiselect by years
years = [list(range(start_year, start_year + 5)) for start_year in range(df['Year'].min(), df['Year'].max() + 1, 5)]
st.sidebar.info('**Step 3:**')
selected_years = st.sidebar.multiselect('**Choose release years**', years)
selected_years = [j for i in selected_years for j in i]

# Clean the sales columns in the original dataframe (if necessary)
sales_cols = ['Domestic Sales (in $)', 'International Sales (in $)', 'World Wide Sales (in $)']
df[sales_cols] = df[sales_cols].replace('[\$,]', '', regex=True).astype(float)

# Filter dataframe based on distributors
if len(Distributor_filter)!=0:
    df0 = df[df['Distributor'].isin(Distributor_filter)].copy()
else:
    df0 = df.copy()

# Group the data by 'Distributor' and calculate the average sales figures for displayed distributors and others.
grouped_sales = df0.groupby('Distributor')[sales_cols].mean().reset_index()

# Create a bar chart
st.markdown('<h2 style="text-align: center;">Average Sales by Distributor</h2>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(9, 8))
x = np.arange(len(grouped_sales['Distributor'])) 
width = 0.2  

rects1 = ax.bar(x - width, grouped_sales['Domestic Sales (in $)'], width, label='Average Domestic Sales')
rects2 = ax.bar(x, grouped_sales['International Sales (in $)'], width, label='Average International Sales')
rects3 = ax.bar(x + width, grouped_sales['World Wide Sales (in $)'], width, label='Average Worldwide Sales')

# Add some text for labels, title, and custom x-axis tick labels
ax.set_ylabel('Sales in $')
ax.set_title('Average Sales by Distributor')
ax.set_xticks(x)
ax.set_xticklabels(grouped_sales['Distributor'], rotation=45)
ax.legend()

ax.bar_label(rects1, padding=0, rotation=90, label_type="center", color="white")
ax.bar_label(rects2, padding=0, rotation=90, label_type="center", color="white")
ax.bar_label(rects3, padding=0, rotation=90, label_type="center", color="white")
fig.tight_layout()

# Display the plot in Streamlit app
st.pyplot(fig)

# pie data
if len(Distributor_filter)==0 and len(selected_years)!=0:
    df1 = df[df['Year'].isin(selected_years) & con].copy()
elif len(Distributor_filter)!=0 and len(selected_years)==0:
    df1 = df[df['Distributor'].isin(Distributor_filter) & con].copy()
elif len(Distributor_filter)==0 and len(selected_years)==0:
    df1 = df[con].copy()
else:
    df1 = df[df['Distributor'].isin(Distributor_filter) & df['Year'].isin(selected_years) & con].copy()

# Pie chart
st.markdown('<h2 style="text-align: center;">Sales Distribution</h2>', unsafe_allow_html=True)
st.markdown('''> **The piechart below may give you a general view on whether the movie selected by you more popular in the United States or in other countries outside of the United States.**''')
x = [df1['Domestic Sales (in $)'].mean(), df1['International Sales (in $)'].mean()]
pct = ["%1.1f%%"%(i/sum(x)*100) for i in x]
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
labels = ['Domestic Sales', 'International Sales']
labels = [i+"("+j+")" for i, j in zip(labels, pct)]
fig, ax = plt.subplots(figsize=(9, 9))
ax.pie(x, labels=labels, colors=colors, radius=1.5, center=(2, 2), labeldistance=0.4,
       wedgeprops={"linewidth": 0.5, "edgecolor": "white"}, frame=True)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
st.pyplot(fig)

# Display recommended movies
st.markdown('<h2 style="text-align: center;">Recommended Movies Based on Your Choice</h2>', unsafe_allow_html=True)
st.write(df1[['Title', 'Genre', 'Distributor', 'Year']])


