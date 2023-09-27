import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def create_figure_l1(percent_persons_contacted, percent_patients_found, da):

    fig = px.line(100 * da[['percent_persons_contacted', 'percent_patients_found']],
                  x='percent_persons_contacted',
                  y='percent_patients_found', color_discrete_sequence=['#38ACF5'], width=450, height=400)

    fig.update_layout(xaxis_range=[-1, 105],
                      yaxis_range=[-1, 105],
                      xaxis_title='Percent Persons Contacted',
                      yaxis_title='Percent Patients Found',
                      margin=dict(t=0, b=0), showlegend=False)

    fig.update_yaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)
    fig.update_xaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)

    fig.update_traces(hovertemplate="<br>".join(["Percent Persons Contacted: %{x:0.1f}%",
                                                 "Percent Patients Found: %{y:0.1f}%"]))

    fig.add_trace(go.Scatter(x=[0, 100 * percent_persons_contacted],
                             y=[100 * percent_patients_found, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))
        
    fig.add_trace(go.Scatter(x=[100 * percent_persons_contacted, 100 * percent_persons_contacted],
                             y=[0, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))

    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)


def create_figure_r1(percent_persons_contacted, percent_patients_found, da):

    fig = px.line(100 * da[['percent_persons_contacted', 'percent_patients_found']],
                  x='percent_persons_contacted',
                  y='percent_patients_found', color_discrete_sequence=['#38ACF5'], width=450, height=350)

    fig.update_layout(xaxis_range=[-1, 105],
                      yaxis_range=[-1, 105],
                      xaxis_title='Percent Persons Contacted',
                      yaxis_title='Percent Patients Found',
                      margin=dict(t=0, b=0), showlegend=False)

    fig.update_yaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)
    fig.update_xaxes(zeroline=True, showspikes=True, spikecolor='gray', spikethickness=1)

    fig.update_traces(hovertemplate="<br>".join(["Percent Persons Contacted: %{x:0.1f}%",
                                                 "Percent Patients Found: %{y:0.1f}%"]))

    fig.add_trace(go.Scatter(x=[0, 100 * percent_persons_contacted],
                             y=[100 * percent_patients_found, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))
        
    fig.add_trace(go.Scatter(x=[100 * percent_persons_contacted, 100 * percent_persons_contacted],
                             y=[0, 100 * percent_patients_found],
                             mode='lines', line=dict(color='red', width=1)))

    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)
