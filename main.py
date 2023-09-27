from scipy.interpolate import CubicSpline
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from create_figures import *

st.set_page_config(layout="wide")

# ---------------------------------- #
st.markdown("""
    <style>
        footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)

st.write("""
    <style>
        div.block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
    </style>""", unsafe_allow_html=True)

st.write("""
    <style>
        div[data-testid="block-container"] {
            margin-top: -40px;
        }
    </style>""", unsafe_allow_html=True)

# st.write("""
#     <style>
#         div[data-testid="stImage"] {
#             margin-top: 0px;
#         }
#     </style>""", unsafe_allow_html=True)

st.write("""
    <style>
        [data-testid="column"]:has(div.PortMarker) {
         box-shadow: rgb(0 0 0 / 40%) 0px 2px 1px -1px,
            rgb(0 0 0 / 25%) 0px 1px 1px 0px, rgb(0 0 0 / 25%) 0px 1px 3px 0px;
         border-radius: 15px;
         padding: 1% 1% 1% 1%;}
    </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
        div[data-testid="stMetricValue"] > div {
            background-color: #f7f5eb;
            padding-left: 5%;
            border-radius: 0px 0px 10px 10px;
        }
    </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .st-emotion-cache-17c4ue.e1i5pmia2 {
            background-color: #f7f5eb;
            padding-left: 5%;
            border-radius: 10px 10px 0px 0px;
        }
    </style>""", unsafe_allow_html=True)
# ---------------------------------- #

# Define session state infor
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'codeset' not in st.session_state:
    st.session_state.codeset = False

def update():
    # st.session_state.submitted = False
    st.session_state.codeset = add_multiselect_code_set

def compute_metrics(da, add_number=None, add_slider=None):

    if add_number is not None:
        y = da['percent_patients_found'].values
        x = da['percent_persons_contacted'].values

        cs = CubicSpline(x, y)

        percent_persons_contacted = add_number / da['number_persons_contacted'].max()
        number_persons_contacted = add_number
        percent_patients_found = cs(percent_persons_contacted)
        number_patients_found = percent_patients_found * da['number_patients_found'].max()
        percentile_minimum = (1 - percent_persons_contacted)

    if add_slider is not None:
        ds = da[da['percentile'] >= add_slider].reset_index(drop=True)

        percent_persons_contacted = ds['percent_persons_contacted'].max()
        number_persons_contacted = ds['number_persons_contacted'].max()
        percent_patients_found = ds['percent_patients_found'].max()
        number_patients_found = ds['number_patients_found'].max()
        percentile_minimum = ds['percentile'].min()

    return (percent_persons_contacted,
            number_persons_contacted,
            percent_patients_found,
            number_patients_found,
            percentile_minimum)

def compute_suffix(x):

    if str(int(np.round(x))) in ['11', '12', '13']:
        return 'th'
    elif str(int(np.round(x)))[-1] == '1':
        return 'st'
    elif str(int(np.round(x)))[-1] == '2':
        return 'nd'
    elif str(int(np.round(x)))[-1] == '3':
        return 'rd'
    else:
        return 'th'


# ---------------- #
# Read in the Data #
# ---------------- #
df = pd.read_csv('model_data2.csv')

tab_1, tab_2 = st.tabs(['Audience Insights', 'Available Models'])

with tab_1:

    # -------------------------- #
    # Add Sidebar Title and Logo #
    # -------------------------- #
    st.sidebar.image('webmd-ignite_full-color.png', use_column_width=True)

    st.sidebar.title('Audience Selector')

    # ---------------------- #
    # Choose a Model by Type #
    # ---------------------- #
    add_selectbox_model_name = None

    add_selectbox_model_by = st.sidebar.selectbox('Choose a model by', ('Name', 'Diagnosis', 'Procedure', 'MS-DRG', 'Service Line'), index=None)

    if add_selectbox_model_by == 'Name':

        # ---------------------- #
        # Choose a Model by Name #
        # ---------------------- #
        model_names = df['model'].unique().tolist()

        add_selectbox_model_name = st.sidebar.selectbox('Select a model', (model_names), index=None)

    elif add_selectbox_model_by == 'Service Line':

        # ------------------------------ #
        # Choose a Model by Service Line #
        # ------------------------------ #
        service_line_names = df['service_line'].dropna().unique().tolist()

        add_selectbox_service_line = st.sidebar.selectbox('Select a service line', (service_line_names), index=None)

        if add_selectbox_service_line:

            model_names = df[df['service_line'] == add_selectbox_service_line]['model'].unique().tolist()

            add_selectbox_model_name = st.sidebar.selectbox('Select a model', (model_names), index=None)

    elif add_selectbox_model_by in ['Diagnosis', 'Procedure', 'MS-DRG']:

        # ---------------------------------------------- #
        # Choose a Model by Diagnosis, Procedure, MS-DRG #
        # ---------------------------------------------- #
        add_selectbox_model_using = st.sidebar.selectbox('Select a model by', ('Name', 'Code Set'), index=None)

        if add_selectbox_model_using == 'Name':

            model_names = df['model'].unique().tolist()

            add_selectbox_model_name = st.sidebar.selectbox('Select a model', (model_names), index=None)

        elif add_selectbox_model_using == 'Code Set':

            # Choose the appropriate code set
            full_code_list = pd.read_csv('diagnosis_codes.csv')[:100]['code'].tolist()

            with st.sidebar.form('my_form'):

                add_multiselect_code_set = st.multiselect(f'Enter {add_selectbox_model_by.lower()} code set', full_code_list)

                submitted = st.form_submit_button('Submit', on_click=update())

                ######################
                # Execute query here #
                #####################
                # model_names returned from query
                model_names = df['model'].unique().tolist()

            if st.session_state.codeset:

                add_selectbox_model_name = st.sidebar.selectbox('Select best-matching model', (model_names), index=None)

    # -------------------------------------------- #
    # Once model is chosen, execute the code below #
    # -------------------------------------------- #
    if add_selectbox_model_name:

        add_selectbox_audience = st.sidebar.selectbox('Select audience by', ('Top Scoring', 'Risk Percentile'), index=None)

        # Filter data using dropdown values
        da = df[df['model'] == add_selectbox_model_name].reset_index(drop=True)

        add_slider, add_number = None, None

        if add_selectbox_audience == 'Top Scoring':

            add_number = st.sidebar.number_input('Selected audience size',
                                                min_value=int(da['number_persons_contacted'].min()),
                                                max_value=da['number_persons_contacted'].max(),
                                                value=int(np.ceil(da['number_persons_contacted'].max() * 0.1)))

        elif add_selectbox_audience == 'Risk Percentile':

            add_slider = st.sidebar.slider('Select percentile minimum', min_value=0.0, max_value=0.99, value=0.9)


        if add_slider or add_number:

            (
                percent_persons_contacted,
                number_persons_contacted,
                percent_patients_found,
                number_patients_found,
                percentile_minimum
            ) = compute_metrics(da, add_number, add_slider)

            suffix = compute_suffix(100 * percentile_minimum)


            col_1, col_2 = st.columns(spec=[0.4, 0.6])

            with col_1:
                col_a, col_b = st.columns(spec=2)

                col_a.metric('% Total Audience Selected', f"{100 * percent_persons_contacted:0.1f}%")
                col_a.metric('Selected Audience Size', f"{int(np.round(number_persons_contacted)):,}")
                col_a.metric('Percentile Minimum', f"{int(np.round(100 * percentile_minimum))}{suffix}")

                col_b.metric('Est. % of Goal Patients', f"{100 * percent_patients_found:0.1f}%")
                col_b.metric('Est. Future Patients to Goal', f"{int(np.round(number_patients_found)):,}")
                col_b.metric('Expected Lift', f"{percent_patients_found/percent_persons_contacted:0.1f}x")

                st.info(f"""Based on your historical data, choosing an audience of this
                        size will reach :red[{100 * percent_patients_found:0.1f}%] of patients
                        who will have an encounter for :red[{add_selectbox_model_name.split(':')[-1]}]
                        in the next 12 months.""")

                st.write("""<div class='PortMarker'/>""", unsafe_allow_html=True)

                for i in range(1):
                    st.write("###")

                st.write('**Cumulative Gains**')
                create_figure_l1(percent_persons_contacted, percent_patients_found, da)

            with col_2:
                st.write("""<div class='PortMarker'/>""", unsafe_allow_html=True)

                st.write('**Age and Gender Breakdown**')
                create_figure_r1(percent_persons_contacted, percent_patients_found, da)

                st.write('**Household Income**')
                create_figure_r1(percent_persons_contacted, percent_patients_found, da)

with tab_2:

    dm = pd.read_csv('available_models.csv')[['Description', 'Category']]

    dm.columns = ['Model Name', 'Category']

    st.dataframe(dm, hide_index=True, width=800, height=850)