import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings("ignore")

#READING THE CLEANED DATAFRAME

df=pd.read_csv("/content/airbnb_data.csv")


st.set_page_config(
                    page_title="Airbnb Data Analysis",
                    page_icon="https://static-00.iconduck.com/assets.00/airbnb-icon-512x512-d9grja5t.png",
                    layout="wide",
                    initial_sidebar_state="collapsed"
                    )
# Creating options menu
select = option_menu(
          menu_title=None,
          options=["Home", "Analysis", "About"],
          icons=["house", "graph-up", "exclamation-triangle"],
          default_index=2,
          orientation="horizontal",
          styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
                  "icon": {"color": "black", "font-size": "20px"},

                  "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#FF5A60"},
                  "nav-link-selected": {"background-color": "#FF5A60"}})

if select == "Home":
    st.header("# Welcome to Airbnb Data Analysis")
    st.write("")
    st.write("This Streamlit web app allows you to explore Airbnb listing data through interactive visualizations.")
    st.write("""***Airbnb is an online marketplace that connects people who want to rent out
              their property with people who are looking for accommodations,
              typically for short stays. Airbnb offers hosts a relatively easy way to
              earn some income from their property.Guests often find that Airbnb rentals
              are cheaper and homier than hotels.***""")
    st.write("")
    st.write("""***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
                   The company has presence in China, India, Japan,
                   Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy,
                   Norway, Portugal, Russia, Spain, Sweden, the UK, and others.
                   Airbnb is headquartered in San Francisco, California, the US.***""")

    st.write("To learn more about this app and its features, visit the 'About' section.")


if select == "Analysis":
    select=option_menu(None,
                        options= ["Insights", "Explore"],
                        default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#FF5A60"}})
    if select=="Insights":

        # Getting user inputs
        country=st.sidebar.multiselect("Select a Country",sorted(df.country.unique()),sorted(df.country.unique()))
        prop= st.sidebar.multiselect("Select a Property_type",sorted(df.property_type.unique()),sorted(df.property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
        max_price=df['price'].quantile(0.95)  # Adjust quantile as needed
        df_filtered = df[df['price'] <= max_price]
        price = st.slider('Select Price',df_filtered['price'].min(),df_filtered['price'].max(),(df_filtered['price'].min(),df_filtered['price'].max()))

        # converting user input into query
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

        col1,col2 = st.columns(2,gap='medium')

        with col1:
          # TOP 10 PROPERTY TYPES BAR CHART
          df1=df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
          fig=px.bar(df1,
                     title='TOP 10 PROPERTY TYPES',
                     x='Listings',
                     y='property_type',
                     orientation='h',
                     color='property_type',
                     color_continuous_scale=px.colors.sequential.Agsunset)
          st.plotly_chart(fig,use_container_width=True)

          # TOP 10 HOSTS BAR CHART
          df2=df.query(query).groupby(['host_name']).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
          fig=px.bar(df2,
                     title="Top 10 Hosts with Highest number of Listings",
                     x='Listings',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
          fig.update_layout(showlegend=False)
          st.plotly_chart(fig,use_container_width=True)


        with col2:
          # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
          df1=df.query(query).groupby(['room_type']).size().reset_index(name='counts')
          fig= px.pie(df1,
                    title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
          fig.update_traces(textposition='outside', textinfo='value+label')
          st.plotly_chart(fig,use_container_width=True)

          # Total Review_scores in each Room type
          rev_df = df.query(query).groupby('room_type',as_index=False)['review_scores'].mean().sort_values(by='review_scores')
          fig = px.bar(data_frame=rev_df,x='room_type',y='review_scores',color='review_scores',
                       title='Total Reviews in each Room type')

          st.plotly_chart(fig,use_container_width=True)

          # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
          country_df = df.query(query).groupby(['country'],as_index=False)['name'].count().rename(columns={'name' : 'Total_Listings'})
          fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
          st.plotly_chart(fig,use_container_width=True)

    if select=="Explore":
        st.markdown("## Explore more about the Airbnb data")

        # getting user inputs
        country=st.sidebar.multiselect("Select a Country",sorted(df.country.unique()),sorted(df.country.unique()))
        prop= st.sidebar.multiselect("Select a Property_type",sorted(df.property_type.unique()),sorted(df.property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
        max_price=df['price'].quantile(0.95)  # Adjust quantile as needed
        df_filtered = df[df['price'] <= max_price]
        price = st.slider('Select Price',df_filtered['price'].min(),df_filtered['price'].max(),(df_filtered['price'].min(),df_filtered['price'].max()))

        #price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))

        query= f'country in {country} & room_type in {room} & property_type in {prop} & price >={price[0]} & price <={price[1]}'

        # heading1

        st.markdown("## Price Analysis")

        col1,col2=st.columns(2,gap='medium')

        with col1:
            # AVG PRICE BY ROOM TYPE BARCHART
            pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
            fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                    )
            st.plotly_chart(fig,use_container_width=True)

            # HEADING 2
            st.markdown("## Availability Analysis")

            # AVAILABILITY BY ROOM TYPE BOX PLOT
            fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by Room_type'
                    )
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            # AVG PRICE IN COUNTRIES SCATTERGEO
            country_df=df.query(query).groupby('country', as_index=False)['price'].mean()
            fig = px.scatter_geo(data_frame=country_df,
                                            locations='country',
                                            color='price',
                                            hover_data=['price'],
                                            locationmode='country names',
                                            size='price',
                                            title= 'Avg Price in each Country',
                                            color_continuous_scale='agsunset'
                                  )
            col2.plotly_chart(fig,use_container_width=True)


            st.markdown("#   ")
            st.markdown("#   ")

            # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
            country_df=df.query(query).groupby('country', as_index=False)['availability_365'].mean()
            country_df.availability_365 = country_df.availability_365.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                            locations='country',
                                            color='availability_365',
                                            hover_data=['availability_365'],
                                            locationmode='country names',
                                            size='availability_365',
                                            title= 'Avg Availability in each Country',
                                            color_continuous_scale='agsunset'
                                  )
            st.plotly_chart(fig,use_container_width=True)


if select == "About":
    st.header("ABOUT THIS PROJECT")
    st.markdown("### :blue[Domain]: Travel Industry, Property Management and Tourism ")
    st.markdown("### :blue[Technologies used]: Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb")

    st.write('''***Gather data from Airbnb's public API or other available sources.
        Collect information on listings, hosts, reviews, pricing, and location data.***''')

    st.write('''***Clean and preprocess the data to handle missing values, outliers, and ensure data quality.
        Convert data types, handle duplicates, and standardize formats.***''')

    st.write('''***Conduct exploratory data analysis to understand the distribution and patterns in the data.
        Explore relationships between variables and identify potential insights.***''')

    st.write('''***Create visualizations to represent key metrics and trends.
        Use charts, and maps to convey information effectively.
        Consider using tools like Matplotlib, Seaborn, or Plotly for visualizations.***''')

    st.write('''***Utilize geospatial analysis to understand the geographical distribution of listings.
        Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.***''')


