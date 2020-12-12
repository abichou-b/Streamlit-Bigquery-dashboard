
from google.cloud import bigquery
import altair as alt


def query_size(query, bq_client):
    job_config = bigquery.QueryJobConfig()
    job_config.dry_run = True
    job_config.use_query_cache = False
    query_job = bq_client.query(query, job_config=job_config)
    return query_job.total_bytes_processed / 2**30


def scatter_plot(df, var1, var2):
    chart = alt.Chart(df).mark_circle(size=60).encode(
    x=var1,
    y=var2,
    color='isweekday',
    tooltip='station_name'
    ).interactive()
    return chart


def hist_plot(df, var):
    chart = alt.Chart(df).mark_bar().encode(
    alt.X(var, bin=True),
    y='count()',
    color='isweekday'
    )
    return chart

def brushing_scatter(df):
    brush = alt.selection(type='interval')
    df['Clustering label'] = df['CENTROID_ID'].apply(lambda x: 'cluster '+str(x))
    points = alt.Chart(df).mark_point().encode(
        x='duration',
        y='distance_from_city_center',
        color=alt.condition(brush, 'Clustering label',alt.value('grey')),
        tooltip='station_name'
    ).add_selection(brush)
    ranked_text = alt.Chart(df).mark_text().encode(
        y=alt.Y('row_number:O',axis=None)
    ).transform_window(
        row_number='row_number()'
    ).transform_filter(
        brush
    ).transform_window(
        rank='rank(row_number)'
    ).transform_filter(
        alt.datum.rank<15
    )
    isweekday = ranked_text.encode(text='isweekday').properties(title='isweekday')
    trips = ranked_text.encode(text='num_trips').properties(title='num_trips')
    bikes = ranked_text.encode(text='bikes_count').properties(title='num_bikes')
    text = alt.hconcat(isweekday,trips,bikes)
    chart = alt.hconcat(
        points,
        text
    ).resolve_legend(
        color="independent"
    )
    return chart
