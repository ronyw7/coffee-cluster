import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data 
def load_data(path):
    data = pd.read_csv(path, index_col=0)  
    return data
coffee_data = load_data('data/coffee_cluster.csv')
cluster_data = load_data('data/clusters.csv')

def display_coffee(row):
    st.subheader(row['name'] + ', ' + row['roaster'])
    st.caption(row['desc_2'])
    with st.expander("Read more"):
        st.write(row['desc_1'])
        st.write("Price per 100g:", row['100g_USD'])
        st.write("Rating:", row['rating'])

@st.cache_data
def main_page():
    st.title("Coffee Cluster :coffee:")
    st.markdown('Hey there, glad you are here! Our clustering algorithm groups **coffee beans** from different roasters based on their **similarities**.')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Number of coffee beans", 2095)
    col2.metric("Number of clusters", 20)
    col3.metric("Average price per 100g", '$9.32')
    col4.metric("Most popular origin", 'Panama')

    fig = px.scatter_3d(coffee_data, x='PCA_1', y='PCA_2', z='PCA_3', color='cluster', hover_data=['name', 'roaster', 'origin_1', 'origin_2'])
    with st.container():
        st.plotly_chart(fig, theme=None)
    


def explore_clusters():
    n = st.selectbox('Explore the Coffee Clusters', cluster_data['cluster'], index=None, placeholder="A number from 0 to 19")  
    if n != None:
        st.write(f"We think these keywords best describe cluster {n}")
        curr = cluster_data.iloc[n, :]
        st.info(curr['keywords'])
        st.write("Average Price per 100g:", curr['average price'])
        st.write("Average Rating:", curr['average rating'])
        ""   
        with st.expander("Example Coffee from this Cluster:"):
            examples = coffee_data[coffee_data['cluster'] == n].sample()
            for index, row in examples.iterrows():
                st.subheader(row['name'] + ', ' + row['roaster'])
                st.caption(row['desc_2'])
                st.write(row['desc_1'])
                st.write("Price per 100g:", row['100g_USD'])
                st.write("Rating:", row['rating'])

st.sidebar.header('Find Similar Beans')
st.sidebar.write("Looking for something new? We got you, just tell us what you've enjoyed.")
selected_roaster = st.sidebar.selectbox('Select a Roaster or Start Typing', coffee_data['roaster'].unique())  
selected_bean = st.sidebar.selectbox('Select a Coffee Bean or Start Typing', coffee_data[coffee_data['roaster']==selected_roaster]['name'].unique()) 

submit = st.sidebar.button('Submit')

if submit:
    n = coffee_data[(coffee_data['roaster']==selected_roaster) & (coffee_data['name'] == selected_bean)]['cluster'].iloc[0] 
    similar_beans = coffee_data[coffee_data['cluster'] == n].sample(frac=1)
    st.subheader(f"We think you might like:")
    st.info(f"Because you like {selected_bean} from {selected_roaster}, we recommend these similar coffee beans from cluster #{n}. Every time you hit submit, we randomly pick five beans from the cluster, so you get to see some new recommendations!")
    for index, row in similar_beans[:5].iterrows():
        with st.expander(row['name'] + ', ' + row['roaster']):
            st.subheader(row['name'] + ', ' + row['roaster'])
            st.caption(row['desc_2'])
            st.write(row['desc_1'])
            st.write("Price per 100g:", row['100g_USD'])
            st.write("Rating:", row['rating'])


    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(similar_beans[:5])
    col1, col2, _, _, _ = st.columns(5)
    download = col2.download_button("Download", data=csv, file_name="similar_beans.csv", mime='text/csv')
    st.balloons()
    col1.button('Back')
    
else:
    main_page()
    explore_clusters()
    ""
    st.write('Explore or download the full coffee cluster database below:')
    st.dataframe(coffee_data)

