import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_figure_l1(percent_persons_contacted, percent_patients_found, da):

    fig = px.line(100 * da[['percent_persons_contacted', 'percent_patients_found']],
                  x='percent_persons_contacted',
                  y='percent_patients_found',
                  color_discrete_sequence=['#38ACF5'],width=450, height=400)

    fig.update_layout(xaxis_range=[-1, 105],
                      yaxis_range=[-1, 105],
                      xaxis_title='% of Total Audience',
                      yaxis_title='% of Goal Patients',
                      margin=dict(t=0, b=0), showlegend=False)

    fig.update_yaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)
    fig.update_xaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)

    fig.update_traces(hovertemplate='<br>'.join(['% of Total Audience: %{x:0.1f}%',
                                                 '% of Goal Patients: %{y:0.1f}%']))

    fig.add_trace(go.Scatter(x=[0, 100 * percent_persons_contacted],
                             y=[100 * percent_patients_found, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))
        
    fig.add_trace(go.Scatter(x=[100 * percent_persons_contacted, 100 * percent_persons_contacted],
                             y=[0, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))

    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)


def create_figure_r1(data):

    columns_age_gender = [(i[-5:].replace('_', '-').replace('lt-', '< ').replace('gt-', '> '), i[:-6], data[i].iloc[0])
                          for i in data.columns if ('male' in i) or ('female' in i)]

    dr = pd.DataFrame(columns_age_gender, columns=['age_group', 'gender', 'count'])

    fig = px.bar(dr, x='age_group', y='count', color='gender', width=450, height=400)

    fig.update_layout(margin=dict(t=0, b=0),
                      xaxis_title='Selected Audience Age and Gender',
                      yaxis_title='Count')

    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)


def create_figure_r2(data):

    columns_income = [i for i in data.columns if 'income' in i]

    fig = px.bar(x=columns_income,
                 y=(data[columns_income].iloc[0]),
                 color_discrete_sequence=['#38ACF5'],
                 width=450, height=400)

    fig.update_layout(margin=dict(t=0, b=0),
                      xaxis_title='Selected Audience Income',
                      yaxis_title='Count',
                      xaxis=dict(tickmode='array',
                                 tickvals=columns_income,
                                 ticktext=[i.split('_')[-1] for i in columns_income]))

    fig.update_traces(hovertemplate='%{y}')

    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)
