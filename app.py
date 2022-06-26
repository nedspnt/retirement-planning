import streamlit as st
import pandas as pd
import numpy as np

st.subheader(f"Assumptions")

with st.form(key='columns_in_form'):
    c1, c2, c3 = st.columns(3)
    c4, c5 = st.columns(2)
    with c1:
        age = st.number_input("Your age", value=30, step=1)
    with c2:
        age_of_retirement = st.number_input("Expected retirement age", value=65, step=1)
    with c3:
        age_of_death = st.number_input("Expected age of death", value=85, step=1)

    with c4:
        monthly_cost = st.number_input("Current monthly cost of living", value=30000, step=500)
    with c5:
        inflation_rate = st.number_input("Expected inflation rate (%)", value=2.0, step=0.5) / 100

    submitButton = st.form_submit_button(label='Calculate')

if submitButton:

    st.subheader(f"Cost of Living with Inflation")

    monthly_cost_series = np.round(np.cumprod(np.ones(age_of_death - age) * (1 + inflation_rate)) * monthly_cost, decimals=-2)

    st.markdown(f"Be careful of an inflation! To purchase the same goods and services, your cost of living of {monthly_cost} "
                f"will increase to {int(monthly_cost_series[age_of_retirement-age])} when you are {age_of_retirement}, "
                f"and it will be {int(monthly_cost_series[-1])} when you turn {age_of_death}")
    chart_data = pd.DataFrame(
        {
            "pre-retirement": np.concatenate((monthly_cost_series[:age_of_retirement-age], np.zeros(age_of_death-age_of_retirement))),
            "post-retirement": np.concatenate((np.zeros(age_of_retirement - age), monthly_cost_series[age_of_retirement-age:]))
        },
        index=np.arange(age, age_of_death)
    )
    st.bar_chart(chart_data)

    cash_for_retirement = int(np.sum(monthly_cost_series[age_of_retirement-age:]) * 12)
    st.markdown(f"If you don't invest after retirement, you'll need to have {cash_for_retirement} at your retirement age ({age_of_retirement})")