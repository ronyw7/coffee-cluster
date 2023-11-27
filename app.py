import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data 
def load_data():
    data = pd.read_csv('data/coffee_cluster.csv', index_col=0)  
    return data

coffee_data = load_data()


st.sidebar.header('Find Similar Beans')
selected_roaster = st.sidebar.selectbox('Select a Roaster or Start Typing', coffee_data['roaster'])  
selected_bean = st.sidebar.selectbox('Select a Coffee Bean or Start Typing', coffee_data[coffee_data['roaster']==selected_roaster]['name']) 

submit = st.sidebar.button('Submit')

if submit:
    n = coffee_data[(coffee_data['roaster']==selected_roaster) & (coffee_data['name'] == selected_bean)]['cluster'].iloc[0] 
    similar_beans = coffee_data[coffee_data['cluster'] == n].sample(frac=1)
    st.write(f"You might like these coffee beans that are similar to {selected_bean} from {selected_roaster}:")
    st.info(f"These are similar coffee beans from cluster {n}. Every time you hit submit, we randomly pick five beans from the cluster, so you get to see some new recommendations!")
    for index, row in similar_beans[:5].iterrows():
        st.header(row['name'] + ', ' + row['roaster'])


    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(similar_beans)
    col1, col2, _, _, _ = st.columns(5)
    col2.download_button("Download", data=csv, file_name="similar_beans.csv", mime='text/csv')    
    col1.button('Back')

else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Number of coffee beans", 2095)
    col2.metric("Number of clusters", 20)
    col3.metric("Average price per 100g", '$9.32')
    col4.metric("Most popular origin", 'Panama')
    fig = px.scatter_3d(coffee_data, x='PCA_1', y='PCA_2', z='PCA_3', color='cluster', hover_data=['name', 'roaster', 'origin_1', 'origin_2'])
    with st.container():
        st.plotly_chart(fig, theme=None)

    st.write('Explore the full table below:')
    st.dataframe(coffee_data)