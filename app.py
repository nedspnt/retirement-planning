import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.subheader(f"Welcome to Retirement Planning Simulator")
st.write("by datatipsy")

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

with st.expander("What is inflation?"):
    st.write(f"""An [inflation](https://www.investopedia.com/terms/i/inflation.asp) of {inflation_rate*100}% this year means, 
    on average, you need to pay {inflation_rate*100}% more to get the same goods and services purchased in a previous year. Check out [Thailand historical inflation](https://tradingeconomics.com/thailand/inflation-cpi) to make your guess about the future.
    """)
with st.expander("What to put as a current monthly cost of living?"):
    st.write("Let's assume your will be retired today, how much money do you think you'll need as a cost of living per month. You can exclude your rent or housing loan payment if you assume that you'll be debt-free after retirement.")


if submitButton:

    st.subheader(f"Understand how inflation will impact your cost of living")

    monthly_cost_series = np.round(np.cumprod(np.ones(age_of_death - age) * (1 + inflation_rate)) * monthly_cost, decimals=-2)

    st.markdown(f"Be careful of an inflation! To purchase the same goods and services, your cost of living of **{'{:,}'.format(monthly_cost)} THB** "
                f"will increase to **{'{:,}'.format(int(monthly_cost_series[age_of_retirement-age]))} THB** when you are **{age_of_retirement}**, "
                f"and it will be **{'{:,}'.format(int(monthly_cost_series[-1]))} THB** when you turn **{age_of_death}**")
    chart_data = pd.DataFrame(
        {
            "year": np.arange(age, age_of_death),
            "pre-retirement": np.concatenate((monthly_cost_series[:age_of_retirement-age], np.zeros(age_of_death-age_of_retirement))),
            "post-retirement": np.concatenate((np.zeros(age_of_retirement - age), monthly_cost_series[age_of_retirement-age:])),
            "cost_series": monthly_cost_series
        }
    )
    chart_data['label'] = chart_data['year'].apply(lambda x: "post-retirement" if x >= age_of_retirement else "pre-retirement")

    c = alt.Chart(chart_data).mark_bar().encode(x=alt.X('year'),
                                                y=alt.Y('cost_series'),
                                                color=alt.condition(alt.datum.label=='post-retirement',
                                                                    alt.value('#570A57'),
                                                                    alt.value('grey'))
                                                )
    st.altair_chart(c, use_container_width=True)
    # st.bar_chart(chart_data)

    result1, result2 = st.columns(2)

    with result1:

        cash_for_retirement = int(np.sum(monthly_cost_series[age_of_retirement-age:]) * 12)
        st.markdown(f"##### Cash needed when you retire at **{age_of_retirement}**  \n (without investment after retirement)")
        st.subheader(f"{'{:,}'.format(cash_for_retirement)} THB")

    with result2:
        st.markdown(f"##### Saving per month  \n (without investment before retirement)")
        st.subheader(f"{'{:,}'.format(int(cash_for_retirement/((age_of_retirement-age)*12)))} THB")
