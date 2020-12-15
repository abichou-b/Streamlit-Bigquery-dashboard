# Streamlit-Bigquery-dashboard
Interactive dashboard for clustering analysis 

## Clustering analysis on Streamlit
This project creates a data web-app with [Streamlit](https://streamlit.io) that shows interactive charts to facilitate clustering analysis. It run queries on [BigQuery](https://cloud.google.com/bigquery/) public dataset: the London bicycles (EU region). This data app is based on a segmentation use case study posted at the Toward data science Medium publication by Lak Lakshmanan: *How to use K-Means clustering in BigQuery ML to understand and describe your data better*.
Data visualization tools used are: [Altair](https://altair-viz.github.io/) and [Seaborn](https://seaborn.pydata.org/).


## Deployement
For local running, a credential JSON file to use the python Bigquery API is needed. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable should be set to the created file path.
For deployment on [App Engine](https://cloud.google.com/appengine), a Dockerfile, an app.yaml file and a requirement.txt file with needed python packages are added to the application scripts.
