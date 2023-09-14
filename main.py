from scipy.interpolate import CubicSpline
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Enable wide layout
st.set_page_config(layout="wide")

# Load the data
#df = pd.read_csv('model_data.csv')
df = pd.read_csv('model_data.csv')

# Define function to compute metrics
def compute_metrics(da, add_number=None, add_slider=None):

    if add_number is not None:
        y = da['percent_patients_found'].values
        x = da['percent_persons_contacted'].values

        cs = CubicSpline(x, y)

        percent_persons_contacted = add_number / da['market_size'].max()
        number_persons_contacted = add_number
        percent_patients_found = cs(number_persons_contacted / da['market_size'].max())
        number_patients_found = percent_patients_found * (da['market_size'].max() * da['incidence_rate'].max())
        percentile_minimum = percent_persons_contacted

    if add_slider is not None:
        ds = da[da['percentile'] >= add_slider].reset_index(drop=True)

        percent_persons_contacted = ds['percent_persons_contacted'].max()
        number_persons_contacted = percent_persons_contacted * ds['market_size'].max()
        percent_patients_found = ds['percent_patients_found'].max()
        number_patients_found = ds['percent_patients_found'].max() * ds['market_size'].max() * ds['incidence_rate'].max()
        percentile_minimum = ds['percentile'].min()

    return (percent_persons_contacted,
            number_persons_contacted,
            percent_patients_found,
            number_patients_found,
            percentile_minimum)


# Add a sidebar title
st.sidebar.title('Model Selector Tool')

# Add a dropdown to the sidebar
add_selectbox_model = st.sidebar.selectbox('Select a model',
                                           (['PDI5_01: Cardiology: Cardiology',
                                             'PDI4_11_02: Oncology & Hematology: Breast Cancer',
                                             'PDI4_10I: Orthopedics: Sports medicine orthopedic injuries']))

# Add a dropdown to the sidebar
add_selectbox_audience = st.sidebar.selectbox('Select audience by', ('Top Scoring', 'Percentile'))

# Filter data using dropdown values
da = df[(df['model'] == add_selectbox_model)].reset_index(drop=True)

if add_selectbox_audience == 'Top Scoring':

    add_number = st.sidebar.number_input('Number of Individuals', min_value=int(da['percent_persons_contacted'].min() * da['market_size'].max()),
                                      max_value=da['market_size'].max(),
                                      value=int(np.round(da['market_size'].max()/2)))
    add_slider = None

elif add_selectbox_audience == 'Percentile':

    add_slider = st.sidebar.slider('Select minimum percentile', min_value=0.0, max_value=1.0, value=0.5)

    add_number = None

(
    percent_persons_contacted,
    number_persons_contacted,
    percent_patients_found,
    number_patients_found,
    percentile_minimum
) = compute_metrics(da, add_number, add_slider)


col_1, col_2 = st.columns(spec=[0.4, 0.6])

with col_1:
    col_a, col_b = st.columns(spec=2)

    col_a.metric('Percent Persons Contacted', f"{100 * percent_persons_contacted:0.1f}%")
    col_a.metric('Number Persons Contacted', f"{int(number_persons_contacted):,}")
    col_a.metric('Percentile Minimum', f"{percentile_minimum:0.2f}")

    col_b.metric('Percent Patients Found', f"{100 * percent_patients_found:0.1f}%")
    col_b.metric('Number Patients Found', f"{int(number_patients_found):,}")
    col_b.metric('Expected Lift', f"{percent_patients_found/percent_persons_contacted:0.1f}")

with col_2:
    fig = px.line(100 * da[['percent_persons_contacted', 'percent_patients_found']],
                  x='percent_persons_contacted',
                  y='percent_patients_found', width=650, height=700)

    fig.update_layout(yaxis_range=[-1, 101])
    fig.update_layout(xaxis_range=[-1, 101])
    fig.update_yaxes(zeroline=True)
    fig.update_xaxes(zeroline=True)
    fig.update_layout(xaxis_title='Percent of Persons Contacted',
                      yaxis_title='Percent of Patients Found')
    
    fig.update_traces(hovertemplate="<br>".join(["percent persons contacted: %{x:0.1f}%",
                                                 "percent patients found: %{y:0.1f}%"]))

    fig.update_xaxes(showspikes=True, spikecolor='gray', spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor='gray', spikethickness=1)

    fig.add_trace(go.Scatter(x=[0, 100 * percent_persons_contacted],
                             y=[100 * percent_patients_found, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))
    
    fig.add_trace(go.Scatter(x=[100 * percent_persons_contacted, 100 * percent_persons_contacted],
                             y=[0, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))
    
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=False)
