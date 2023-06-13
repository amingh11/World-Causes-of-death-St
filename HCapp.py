import pandas as pd
import streamlit as st
import hydralit_components as hc
import requests
from streamlit_lottie import st_lottie
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px  
import streamlit_card as st_card
import numpy as np
from pathlib import Path
import base64

#######################################################################################################################################
#######################################################################################################################################

#DATA IMPORTS 
df = pd.read_csv("/Users/aminghobar/Desktop/MSBA Summer 2023/Health Care Anlaytics/Individual Project/annual-number-of-deaths-by-cause.csv")
df_cod = pd.read_csv('/Users/aminghobar/Desktop/MSBA Summer 2023/Health Care Anlaytics/Individual Project/total-number-of-deaths-by-cause.csv')
df1 = pd.read_csv('/Users/aminghobar/Desktop/MSBA Summer 2023/Health Care Anlaytics/Individual Project/annual-number-of-deaths-by-cause.csv')

#Importing the data 
#dropping number of executions, not reliable since it contains a high number of null values 
df=df.drop(['Code', 'Number of executions (Amnesty International)'],axis=1)
# Add the "Conflict and Terrorism" column to "Terrorism"
df['Conflict and terrorism'] +=df['Terrorism']

# Drop the "Conflict and Terrorism" column
df.drop('Terrorism', axis=1, inplace=True)

# Create a list of entity values to be removed
entities_to_remove = ['World Bank High Income', 'World Bank Low Income', 'World Bank Lower Middle Income']
# Remove rows with specified entity values from 'df_cod'
df_cod.drop(df_cod[df_cod['Entity'].isin(entities_to_remove)].index, inplace=True)

#Data Prep for third page 


#######################################################################################################################################
#######################################################################################################################################


# Data for 3rd page of dashboard

# Drop the 'Code' and 'Number of executions (Amnesty International)' columns
columns_to_drop = ['Code', 'Number of executions (Amnesty International)']
df1 = df1.drop(columns_to_drop, axis=1)

# Add the "Conflict and Terrorism" column to "Terrorism"
df1['Conflict and terrorism'] +=df1['Terrorism']

# Drop the "Conflict and Terrorism" column
df1.drop('Terrorism', axis=1, inplace=True)

# Create a new DataFrame with desired columns
df_dnd = pd.DataFrame()
df_dnd['Entity'] = df1['Entity']
df_dnd['Year'] = df1['Year']

# Combine disease causes into a single column
disease_causes = [
    ' Meningitis ', " Alzheimer's disease and other dementias ", "Parkinson's disease ",
    'Nutritional deficiencies ', 'Malaria', 'Tuberculosis ', 'Cardiovascular diseases',
    'Lower respiratory infections', 'Neonatal disorders ', 'Alcohol use disorders ',
    'Diarrheal diseases ', 'HIV/AIDS ', ' Cirrhosis and other chronic liver diseases ',
    'Acute hepatitis ','Chronic respiratory diseases', 'Digestive diseases'
]
df_dnd['Disease Causes'] = df1[disease_causes].sum(axis=1)

# Combine non-disease causes into a single column
non_disease_causes = [
    'Drowning', 'Interpersonal violence ', ' Maternal disorders', 'Drug use disorders',
    'Exposure to forces of nature ', 'Environmental heat and cold exposure', 'Conflict and terrorism', 'Road injuries', ' Fire, heat, and hot substances','Poisonings'
]
df_dnd['Non-Disease Causes'] = df1[non_disease_causes].sum(axis=1)

##################################################################################################

#Visuals = General Overview for Deaths Overview page on streamlit

# Exclude the 'Year' column from the sum calculation
numeric_columns = df.select_dtypes(include=[int, float]).columns.drop('Year')
total_deaths_by_country = df.groupby('Entity')[numeric_columns].sum()


#figure1 
# Print the total deaths for each country
for country, row in total_deaths_by_country.iterrows():
    total_deaths = row.sum()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# Group the data by year and calculate the total deaths for each year
total_deaths_by_year = df.groupby('Year').sum().sum(axis=1)

# Create a line plot for the total deaths per year
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=total_deaths_by_year.index, y=total_deaths_by_year, mode='lines'))

# Set the layout of the figure
fig1.update_layout(
    title='',
    xaxis_title='Year',
    yaxis_title='Total Deaths',
    plot_bgcolor='white',  # Set the background color to white
    yaxis=dict(showgrid=False),  # Remove y-axis grid lines
    xaxis=dict(showgrid=False)  # Remove x-axis grid lines
)

#figure2
# data set with total number of death by cause for each year
# Group the data by year and calculate the sum of deaths for each cause column
total_deaths_by_cause = df.groupby('Year').sum()





########################################################################################################################################
#######################################################################################################################################


# Creating Navigation Bar for streamlit app
#make it look nice from the start
st.set_page_config(layout='wide' ,page_title= 'Death Rates',
page_icon= '🏥', initial_sidebar_state= 'expanded')

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    """
    function to display major headers at user interface
    ----------
    main_txt: str -> the major text to be displayed
    sub_txt: str -> the minor text to be displayed 
    is_sidebar: bool -> check if its side panel or major panel
    """

    html_temp = f"""
    <h2 style = "color:#010101; text_align:center; font-weight: bold;"> {main_txt} </h2>
    <p style = "color:#010101; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)


# specify the primary menu definition
menu_data = [
    {'icon': "🌍", 'label':"World Deaths Overview",'ttip':"eda"},
    {'icon': "🆚", 'label':"Disease vs Non-Disease",'ttip':"discover"},
    {'icon': "💰", 'label':"Death and Income Levels"}
]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded



over_theme = {'menu_background':'#375892'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home', #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    hide_streamlit_markers=False,
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
)

def load_lottieurl(url):
    r= requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie= load_lottieurl('https://assets8.lottiefiles.com/packages/lf20_tutvdkg0.json')
lottie2 = load_lottieurl('https://assets2.lottiefiles.com/private_files/lf30_ps1145pz.json')
#get the id of the menu item clicked

####################################################################################################################################

#First Page of streamlit dashboard - "Home Page"

if menu_id== 'Home':
    st.markdown("<h1 style='text-align: center;'>World Causes of Death Healthcare Analysis</h1>", unsafe_allow_html=True)
    left, right= st.columns((1,1))
    with left:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        display_app_header(main_txt='Introduction',
                   sub_txt="Welcome to the World Causes of Death Healthcare Analysis app! This Streamlit application has been developed as part of my individual project for the MSBA 350E Healthcare Analytics course.\n\n"
                           "In this analysis, I delve into the years 1990-2019 to conduct a comprehensive exploration of various trends and patterns related to causes of death. My primary focus is to gain insights into the overall global death trends and their changing patterns. Additionally, I aim to uncover the distinctions between disease-related deaths and non-disease causes. I conduct an in-depth analysis of disease-caused deaths, with a specific emphasis on communicable and non-communicable diseases.\n\n"
                           "Furthermore, I present a straightforward examination of the effects of income on mortality across different regions of the world. To provide a more nuanced perspective, I concentrate on the year 2019 and classify countries into different categories for comparison.\n\n"
                           "By the end of this analysis, I will provide conclusions and recommendations, identifying potential areas for improvement and suggesting directions for further research.\n\n"
                           "Please explore the different sections of this app to gain valuable insights into the world causes of death and healthcare trends."
                   )
    
        display_app_header(main_txt='The Data',
        sub_txt= 'The data was retrieved from Our world in Data website: https://ourworldindata.org/. The Data sets used mainly come from other sources such as WHO data.\n\n'
        'Two main data sets were used:\n\n'
        '   • Annual Number of deaths by cause: A data set that includes data for the total number of deaths for all countries across the world based on 32 causes of death.\n\n'
        '   •Total Number of deaths by cause: A data set that includes the total number of deaths across all countries between 1990-2019, caused by communicable diseases, Non-Communicable diseases and Injuries.')
        st.write('')

        st.subheader('1. Annual Number of deaths by different causes Data')
        # Slider for year selection
        selected_year = st.slider('Select Year', min_value=1990, max_value=2019, value=2019, key= 'yearslider1')

        # Dropdown for country selection
        selected_country = st.selectbox('Select Country', df['Entity'].unique())

        # Filtered data based on selection
        filtered_data = df[(df['Year'] == selected_year) & (df['Entity'] == selected_country)]

        # Display filtered data on Streamlit
        st.write('Selected Data:')
        st.dataframe(filtered_data)
        st.write('')
        st.subheader('2. Total Number of deaths by causes:  *Communicable, Non-communicable and Injuries* Data')
        # Slider for year selection
        selected_year = st.slider('Select Year', min_value=1990, max_value=2019, value=2019, key = 'yearslider2')

        # Dropdown for country selection
        selected_country = st.selectbox('Select Country', df_cod['Entity'].unique())

        # Filtered data based on selection
        filtered_data = df_cod[(df_cod['Year'] == selected_year) & (df_cod['Entity'] == selected_country)]

        # Display filtered data on Streamlit
        st.write('Selected Data:')
        st.dataframe(filtered_data)
    with right:
        st_lottie(lottie, height= 600,key= 'coding')
        st_lottie(lottie2, height= 500,key= 'coding2')

########################################################################################################################################

#Second Page of streamlit dashboard - "Worrld Deaths Overview Dashboard"
if menu_id== 'World Deaths Overview':
    st.markdown("<h1 style='text-align: center;'>Dashboard: General Overview on World Death Causes</h1>", unsafe_allow_html=True)

#Figure 1 view

    st.subheader('Total Number of Deaths in the World Over Time')

    col11,col22 = st.columns((2,1))

    with col11:
        st.plotly_chart(fig1, use_container_width=True)
    with col22:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('The following plot shows the overall trend in the total number of deaths per year in the world, clearly showing that overall the number of deaths is increasing.')


        


    st.write('')
    st.write('')
    st.write('')

#figure2 view 
    st.subheader('Total Number of Deaths by Cause Over Time')


    #   Create a list of causes of death
    cause_of_death_list = total_deaths_by_cause.columns.tolist()

    col111,col222 = st.columns((1,4))

    with col111:

        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
# Checkbox for showing all causes of death
        show_all_causes = st.checkbox("Show All Causes", key='checkboxfig1')

# Filter the data based on the selected cause(s)
        if show_all_causes:
            selected_causes = cause_of_death_list
        else:
            selected_cause = st.selectbox("Select Cause of Death", cause_of_death_list, key='selectboxfig2')
            selected_causes = [selected_cause]

# Create a line plot for the selected cause(s) of death
    fig2 = go.Figure()

    for cause in selected_causes:
        fig2.add_trace(go.Scatter(
        x=total_deaths_by_cause.index,
        y=total_deaths_by_cause[cause],
        name=cause,
        mode='lines',
        text=[cause] * len(total_deaths_by_cause),  # Add the cause of death as text labels
        hovertemplate="Cause of Death: %{text}<br>Total Deaths: %{y}<extra></extra>"  # Define hover template
    ))

# Set the layout of the figure
    fig2.update_layout(
        title=f'Total Deaths due to {selected_causes}',
        xaxis_title='Year',
        yaxis_title='Total Deaths',
        plot_bgcolor='white',  # Set the background color to white
        hovermode='x'  # Show hover information on the x-axis
)

# Adjust the legend position and spacing
    if len(selected_causes) > 1:
        fig2.update_layout(
        showlegend=False,  # Show legend
    )
    else:
        fig2.update_layout(
        showlegend=False  # Hide legend
    )

    with col222:

    # Display the line plot on Streamlit
        st.plotly_chart(fig2, use_container_width=True)

    st.write('')
    st.write('')
    st.write('')



#figure 3 View
    st.subheader('World Map for Different Causes of Death')
    col1,col2 = st.columns((1,4))

    with col1:

        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')

# Create a slider for selecting the year


        year = st.slider("Select Year", min_value=1990, max_value=2019, value=2019, step=1, key= 'sliderfig3')

# Create a selectbox for selecting the cause of death
        causes_of_death = df.columns[2:]  # Assuming columns 2 onwards contain the causes of death
        cause_of_death = st.selectbox("Select Cause of Death", causes_of_death, key = 'selectboxfig3')

# Filter the data based on the selected year and cause of death
        filtered_data = df[(df['Year'] == year) & (df[cause_of_death] > 0)]

# Draw the map
        fig3 = px.choropleth(filtered_data, locations='Entity',
                     locationmode='country names',
                     color=cause_of_death,
                     color_continuous_scale=['lightblue', 'dodgerblue', 'navy'],
                     labels={cause_of_death: 'Total Deaths'},
                     title=f'Total Deaths due to {cause_of_death} in {year}')

        fig3.update_geos(showcountries=True, countrycolor="lightgray")

# Display the map on Streamlit

    with col2:
        st.plotly_chart(fig3, use_container_width=True)



########################################################################################################################################

###Third Page of streamlit dashboard - "Disease Vs Non-Disease"
if menu_id== 'Disease vs Non-Disease':
        st.markdown("<h1 style='text-align: center;'>Dashboard: Disease Vs Non-Disease related Deaths</h1>", unsafe_allow_html=True)

        col_l,col_r = st.columns((1,1))

        with col_l:

            # Calculate the total deaths
            total_deaths = df_dnd['Disease Causes'].sum() + df_dnd['Non-Disease Causes'].sum()

            # Calculate the percentage of disease causes and non-disease causes
            disease_percentage = (df_dnd['Disease Causes'].sum() / total_deaths) * 100
            non_disease_percentage = (df_dnd['Non-Disease Causes'].sum() / total_deaths) * 100

            # Create a pie chart using Plotly
            labels = ['Disease Causes', 'Non-Disease Causes']
            values = [disease_percentage, non_disease_percentage]

            # Define colors
            colors = ['#375892', '#66b3ff']

            # Configure layout
            layout = {
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white',
                'autosize': False,
                'width': 400,
                'height': 400
}

            fig4 = px.pie(names=labels, values=values, color_discrete_sequence=colors,
                title='Percentage of Disease Causes and Non-Disease Causes of Deaths')
            fig4.update_layout(layout)

            st.plotly_chart(fig4, use_container_width=True)
    
        with col_r:
            #st.markdown('**Comparison of Disease related deaths to Non-Disease related with regards to Total World Deaths**')

            # Calculate the total deaths for each year
            df_total_deaths = df_dnd.groupby('Year')[['Disease Causes', 'Non-Disease Causes']].sum().reset_index()
            df_total_deaths['Total Deaths'] = df_total_deaths['Disease Causes'] + df_total_deaths['Non-Disease Causes']

            # Create three subplots for each line
            fig5 = make_subplots(rows=1, cols=3, subplot_titles=('Disease Causes', 'Non-Disease Causes', 'Total Deaths'))

            # Add traces for disease causes, non-disease causes, and total deaths
            fig5.add_trace(go.Scatter(x=df_total_deaths['Year'], y=df_total_deaths['Disease Causes'],
                          mode='lines', name='Disease Causes', line=dict(color='#375892')), row=1, col=1)
            fig5.add_trace(go.Scatter(x=df_total_deaths['Year'], y=df_total_deaths['Non-Disease Causes'],
                          mode='lines', name='Non-Disease Causes', line=dict(color='#66b3ff')), row=1, col=2)
            fig5.add_trace(go.Scatter(x=df_total_deaths['Year'], y=df_total_deaths['Total Deaths'],
                          mode='lines', name='Total Deaths', line=dict(color='rgb(100, 100, 100)')), row=1, col=3)

            # Update the layout
            fig5.update_layout(
                title='Disease Vs Non-Disease Vs Total Deaths',
                title_x=0,  # Center the title horizontally
                xaxis_title='Year',
                yaxis_title='Number of Deaths',
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False
)
            # Use Streamlit to display the figure
            st.plotly_chart(fig5, use_container_width=True)

        st.write('● Clealry, since 1990 up until 2019 the majority of deaths has been caused by Disease related causes.')
        st.write('● Overall, since 1990 Disease related deaths have been increasing in paralel with the total number of deaths, while non-disease related deaths have been decreasing.')

        col_1,col_2 = st.columns((1,1))

        with col_1:
            # Top 3 disease causes
            top_disease_causes = df1[disease_causes].sum().nlargest(3)
            fig_disease = go.Figure(data=go.Bar(
            x=top_disease_causes.index,
            y=top_disease_causes.values,
            marker=dict(color='#375892')
))
            fig_disease.update_layout(
                title='Top 3 Disease Causes of Death',
                xaxis_title='Cause',
                yaxis_title='Number of Deaths',
                xaxis_tickangle=0,  # Set the x-axis label angle to 0 degrees (horizontal)
)
            st.plotly_chart(fig_disease, use_container_width=True)

            # Sort the DataFrame by year in ascending order
            df_dnd = df_dnd.sort_values('Year')

            # Create a map for disease causes
            fig_diseases2 = px.choropleth(
                data_frame=df_dnd,
                locations='Entity',
                locationmode='country names',
                color='Disease Causes',
                hover_name='Entity',
                hover_data=['Disease Causes'],
                animation_frame='Year',
                color_continuous_scale='Blues',
                range_color=(0, df_dnd['Disease Causes'].max()),
                title='Disease Causes by Country',
                labels={'Disease Causes': 'Total Deaths'}
)
            # Update the layout for both maps
            map_layout = dict(
                height=600,
                width=800,
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='natural earth'
                    ),
                coloraxis_colorbar=dict(
                title='Total Deaths'
    )
)
            fig_diseases2.update_layout(title_x=0, **map_layout)

            st.plotly_chart(fig_diseases2, use_container_width=True)






        with col_2:
            # Top 3 non-disease causes
            top_non_disease_causes = df1[non_disease_causes].sum().nlargest(3)
            fig_non_disease = go.Figure(data=go.Bar(
                x=top_non_disease_causes.index,
                y=top_non_disease_causes.values,
                marker=dict(color='#375892')
))
            fig_non_disease.update_layout(
                title='Top 3 Non-Disease Causes of Death',
                xaxis_title='Cause',
                yaxis_title='Number of Deaths',
                xaxis_tickangle=0,  # Set the x-axis label angle to 0 degrees (horizontal)
)
            st.plotly_chart(fig_non_disease, use_container_width=True)

            # Create a map for non-disease causes
            fig_non_diseases2 = px.choropleth(
                data_frame=df_dnd,
                locations='Entity',
                locationmode='country names',
                color='Non-Disease Causes',
                hover_name='Entity',
                hover_data=['Non-Disease Causes'],
                animation_frame='Year',
                color_continuous_scale='Blues',
                range_color=(0, df_dnd['Non-Disease Causes'].max()),
                title='Non-Disease Causes by Country',
                labels={'Non-Disease Causes': 'Total Deaths'}
)
            fig_non_diseases2.update_layout(title_x=0, **map_layout)
            st.plotly_chart(fig_non_diseases2, use_container_width=True)

########################################################################################################################################################

#second part of page 3

        st.markdown("<h3 style='text-align: left;'>Analysis with focus on Disease Caused Deaths</h3>", unsafe_allow_html=True)

        #data prep
        disease_columns = ['Entity', 'Year'] + disease_causes
        df_dis = df1[disease_columns].copy()

        # Group the dataframe by year and calculate the sum of disease causes
        df_total_deaths = df_dis.groupby('Year')[disease_causes].sum().reset_index()

        # Create the line plot using Plotly Express
        fig7 = px.line(df_total_deaths, x='Year', y=disease_causes, title='Total Deaths by Cause')
        fig7.update_layout(xaxis_title='Year', yaxis_title='Total Deaths')

        # Use Streamlit to display the figure
        st.plotly_chart(fig7, use_container_width=True)

        st.write('**The Diseases causing the most deaths are:**')
        st.write('● Cardiovascular Disease - Highest cause')
        st.write('● Chronic Respiratory Diseases - 2nd Highest cause')
        st.write('Cardiovascular disease has been the leading cause of death since 1990, and overall for both disease and non-disease caused Deats.')


        st.markdown("<h5 style='text-align: left;'> A glimpse into Communicable Diseases Vs Non-Communicable disease caused deaths</h5>", unsafe_allow_html=True)

        col_11,col_22 = st.columns((1,1))

        with col_11:

            #data prep for  communicable vs non -comm
            df_cod = pd.read_csv('/Users/aminghobar/Desktop/MSBA Summer 2023/Health Care Anlaytics/Individual Project/total-number-of-deaths-by-cause.csv')
            # Create a list of entity values to be removed
            entities_to_remove = ['World Bank High Income', 'World Bank Low Income', 'World Bank Lower Middle Income']

            # Remove rows with specified entity values from 'df_cod'
            df_cod.drop(df_cod[df_cod['Entity'].isin(entities_to_remove)].index, inplace=True)

            # Group the DataFrame by the 'Year' column and calculate the sum of deaths for each year
            df_total_deaths = df_cod.groupby('Year').agg({'Communicable': 'sum', 'Non-communicable': 'sum'}).reset_index()

            # Drop rows with missing values in 'Communicable' or 'Non-Communicable' columns
            df_total_deaths.dropna(subset=['Communicable', 'Non-communicable'], inplace=True)

            # Create the line plot
            fig8 = px.line(df_total_deaths, x='Year', y=['Communicable', 'Non-communicable'],
                labels={'value': 'Number of Deaths', 'Year': 'Year'},
                title='Total Deaths for Communicable and Non-Communicable Diseases over the Years')
        
            st.plotly_chart(fig8, use_container_width=True)
            st.write('**Non-Communicable Diseases:**')
            st.write('● Causing Higher number of deaths since 1990')
            st.write('● Increasing over the years')
            st.write('**Communicable Diseases:**')
            st.write('● Decreasing over the years')
        
        with col_22:
            # Calculate the total deaths for each cause
            total_communicable_deaths = df_cod['Communicable'].sum()
            total_non_communicable_deaths = df_cod['Non-communicable'].sum()
            total_injury_deaths = df_cod['Injuries'].sum()

            # Create a DataFrame for the pie chart
            df_pie = pd.DataFrame({
            'Cause': ['Communicable', 'Non-communicable', 'Injuries'],
            'Total Deaths': [total_communicable_deaths, total_non_communicable_deaths, total_injury_deaths],
})
            # Create a pie chart using Plotly
            fig9 = px.pie(df_pie, values='Total Deaths', names='Cause',
                    title='Percentage of Deaths by Cause',
                    color_discrete_sequence=['#375892', '#66b3ff'])
            
            # Modify the layout
            fig9.update_layout(
            width=600,
            height=400,
)
            st.plotly_chart(fig9, use_container_width=True)

        st.markdown("<h3 style='text-align: left;'>Analysis with focus on Non - Disease Caused Deaths</h3>", unsafe_allow_html=True)

        # Select the non-disease cause columns
        non_disease_causes = [
                'Drowning', 'Interpersonal violence ', ' Maternal disorders', 'Drug use disorders',
                'Exposure to forces of nature ', 'Environmental heat and cold exposure', 'Conflict and terrorism', 'Road injuries', ' Fire, heat, and hot substances','Poisonings'
]

        # Create a new DataFrame with only the non-disease cause columns
        df_non_disease_causes = df1[['Entity', 'Year'] + non_disease_causes].copy()

        # Calculate the total deaths by cause over time
        df_non_disease_totals = df_non_disease_causes.groupby('Year').sum()

        # Create a line plot for each cause
        fig10 = go.Figure()
        for cause in df_non_disease_totals.columns:
            fig10.add_trace(go.Scatter(x=df_non_disease_totals.index, y=df_non_disease_totals[cause], name=cause))

        # Customize the layout
        fig10.update_layout(
        title='Total Deaths by Non-Disease Causes over Time',
        xaxis_title='Year',
        yaxis_title='Total Deaths',
        showlegend=True,
        legend_title='Cause',
        height=500,  # Set the height of the plot
        width=800,  # Set the width of the plot
)

        # Use Streamlit to display the figure
        st.plotly_chart(fig10, use_container_width=True, label='fig.10')

#####################################################################################################################################################################
df_incomes = pd.read_csv('Income world deaths.csv')
df_incomes = df_incomes.drop(columns=['Code', 'Number of executions (Amnesty International)'])

import plotly.subplots as sp

if menu_id== 'Death and Income Levels':
    st.markdown("<h1 style='text-align: center;'>Dashboard: Death Numbers Based on Incomes</h1>", unsafe_allow_html=True)
    # Summing all the cause columns to calculate the total number of deaths for each entity
    df_incomes['Total Deaths'] = df_incomes.iloc[:, 3:].sum(axis=1)

    # Grouping the DataFrame by 'Entity' and summing the total number of deaths for each year
    grouped_df = df_incomes.groupby(['Entity', 'Year'])['Total Deaths'].sum().reset_index()

    # Plotting the total number of deaths for each entity over time
    fig12 = px.line(grouped_df, x='Year', y='Total Deaths', color='Entity',
                title='Total Number of Deaths by Entity over Time')

    # Use Streamlit to display the figure
    st.plotly_chart(fig12, use_container_width=True, label='fig12')


        # Define the disease and non-disease cause lists
    disease_causes1 = [
        'Meningitis', "Alzheimer's disease and other dementias", "Parkinson's disease",
        'Nutritional deficiencies', 'Malaria', 'Tuberculosis', 'Cardiovascular diseases',
        'Lower respiratory infections', 'Neonatal disorders', 'Alcohol use disorders',
        'Diarrheal diseases', 'HIV/AIDS', 'Cirrhosis and other chronic liver diseases',
        'Acute hepatitis', 'Chronic respiratory diseases', 'Digestive diseases'
]

    non_disease_causes1 = [
        'Drowning', 'Interpersonal violence', 'Maternal disorders', 'Drug use disorders',
        'Exposure to forces of nature', 'Environmental heat and cold exposure', 'Conflict and terrorism',
        'Road injuries', 'Fire, heat, and hot substances', 'Poisonings'
]

    # Create a new DataFrame
    df_dnd1 = pd.DataFrame()

    # Include 'Entity' and 'Year' columns in the new DataFrame
    df_dnd1['Entity'] = df_incomes['Entity']
    df_dnd1['Year'] = df_incomes['Year']

    # Calculate the sum of disease causes and non-disease causes for each row
    df_dnd1['Disease Causes'] = df_incomes[disease_causes1].sum(axis=1)
    df_dnd1['Non-Disease Causes'] = df_incomes[non_disease_causes1].sum(axis=1)

    # Create a plot for Disease Causes
    fig13 = go.Figure()
    for entity in df_dnd1['Entity'].unique():
        entity_data = df_dnd1[df_dnd1['Entity'] == entity]
        fig13.add_trace(go.Scatter(x=entity_data['Year'], y=entity_data['Disease Causes'],
                              mode='lines', name=entity))

    fig13.update_layout(title='Deaths due to Disease Causes over Time',
                   xaxis_title='Year', yaxis_title='Number of Deaths')

    # Create a plot for Non-Disease Causes
    fig14 = go.Figure()
    for entity in df_dnd1['Entity'].unique():
        entity_data = df_dnd1[df_dnd1['Entity'] == entity]
        fig14.add_trace(go.Scatter(x=entity_data['Year'], y=entity_data['Non-Disease Causes'],
                              mode='lines', name=entity))

    fig14.update_layout(title='Deaths due to Non-Disease Causes over Time',
                   xaxis_title='Year', yaxis_title='Number of Deaths')

    # Use Streamlit to display the figures
    st.plotly_chart(fig13, use_container_width=True, label='fig13')
    st.plotly_chart(fig14, use_container_width=True, label='fig14')



    # Grouping the DataFrame by 'Entity' and summing the values for each year and cause of death
    grouped_df = df_incomes.groupby(['Entity', 'Year']).sum().reset_index()

    # Reshaping the DataFrame to have cause of death as a column
    melted_df = grouped_df.melt(id_vars=['Entity', 'Year'], var_name='Cause of Death', value_name='Number of Deaths')

    # Creating subplots
    fig11 = sp.make_subplots(rows=len(grouped_df['Entity'].unique()), cols=1,
                        subplot_titles=list(grouped_df['Entity'].unique()))

    # Looping over each entity to create line plots
    for i, entity in enumerate(grouped_df['Entity'].unique(), start=1):
        entity_df = melted_df[melted_df['Entity'] == entity]
        for cause in entity_df['Cause of Death'].unique():
            cause_df = entity_df[entity_df['Cause of Death'] == cause]
            fig11.add_trace(go.Scatter(x=cause_df['Year'], y=cause_df['Number of Deaths'],
                                  mode='lines', name=cause), row=i, col=1)

    # Updating layout and displaying the plot
    fig11.update_layout(showlegend=False, height=800, title_text='Total Number of Deaths by Income Level and Cause of Death')

    # Use Streamlit to display the figure
    st.plotly_chart(fig11, use_container_width=True, label='fig11')



