
import streamlit as st
from google.cloud import bigquery
from utils import  query_size, scatter_plot, hist_plot, brushing_scatter_plot
import time


PROJECT_ID ='your_project_id'
DATA_SET_ID = 'your_data_set_id'
features_table_name = 'your_features_table'
model_prefix_name = 'kmeans_'
client = bigquery.Client()


def main():
    st.markdown("# Interactive dashboard for clustering")
    st.markdown('<style>description{color:blue;}</style>', unsafe_allow_html=True)
    st.markdown("<description>This web-app shows some interactive plots that "+
                "helps analysing clustering results. It runs SQL queries on a "+
                "BigQuery public dataset: the London bicycles (EU region).</description>", unsafe_allow_html=True
                )
    st.sidebar.markdown("## Select the analysis step")
    step = st.sidebar.radio("", ["Show features", "Show clusters"])
    if step == "Show features":
        run_features()
    elif step == "Show clusters":
        run_clustering()


def run_features():
    features_query = f'''
     SELECT *
     FROM `{PROJECT_ID}.{DATA_SET_ID}.{features_table_name}`
     ORDER BY distance_from_city_center ASC
     '''
    size = query_size(features_query, client)
    st.info(f'First query to gather data will process {size:.5f} GB on BigQuery.')
    features_df  = api_request(features_query).to_dataframe()
    st.markdown("### Features data frame")
    if st.checkbox('Show dataframe'):
        st.write(features_df)
    st.markdown("### Features distributions")
    feature = st.selectbox('Select a feature', features_df.columns[2:6])
    st.altair_chart(hist_plot(features_df, feature))
    st.markdown("### Scatter plots")
    var_x = st.selectbox('Feature on x?', features_df.columns[2:6])
    var_y = st.selectbox('Feature on y?', features_df.columns[2:6])
    st.altair_chart(scatter_plot(features_df, var_x, var_y))


def run_clustering():
    k = st.sidebar.slider("Choose number of clusters", 2, 7, 3, 1)
    model_name = model_prefix_name + str(k)
    clustering_query = f'''
    CREATE OR REPLACE MODEL {DATA_SET_ID}.{model_name}
    OPTIONS(model_type='kmeans', num_clusters={k}, standardize_features = true) AS
    SELECT * except(station_name, isweekday)
    FROM `{PROJECT_ID}.{DATA_SET_ID}.{features_table_name}`
    '''
    eval_query = f'''
    SELECT  davies_bouldin_index,
            mean_squared_distance
    FROM ML.EVALUATE(MODEL {DATA_SET_ID}.{model_name})
    '''
    predict_query = f'''
    SELECT * EXCEPT(nearest_centroids_distance)
    FROM ML.PREDICT(MODEL {DATA_SET_ID}.{model_name},
        ( SELECT *
          FROM `{PROJECT_ID}.{DATA_SET_ID}.{features_table_name}`
        ))
    '''
    size = query_size(clustering_query, client)
    st.info(f'The first clustering query for the selected number of cluters will process {size:.5f} on BigQuery.')
    query_job_train = api_request(clustering_query)
    time.sleep(5)
    eval_metrics  = api_request(eval_query).to_dataframe()
    st.markdown("### Model evaluation metrics" )
    st.write(eval_metrics)
    df_score = api_request(predict_query).to_dataframe()
    st.markdown("### Clusters: labeled data" )
    st.altair_chart(brushing_scatter_plot(df_score))


@st.cache(allow_output_mutation=True)
def api_request(query):
    return client.query(query)


main()
