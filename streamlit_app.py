import streamlit as st
import pandas as pd
from db_connect import get_db


# function to update chart whenever user enter new symbols
def update_chart():
    symbols = st.session_state.symbols.split()
    if not symbols: # if pass an empty list
        return

    chart_data = []
    db = get_db()

    for symbol in symbols:
        hist_data = db['historical-data'].find_one({'ticker': symbol},
                                                   {'_id': 0, 'historical_data.Close': 1})
        prediction = db['prediction-2022'].find_one({'ticker': symbol}, {'_id': 0, 'prediction': 1})

        if hist_data is None: # invalid symbol
            print(f'Symbol {symbol} not found')
            continue

        hist_df = pd.DataFrame(hist_data['historical_data'])
        hist_df.columns = [symbol]
        chart_data.append(hist_df)

        if prediction is None: # can not predict this symbol
            print(f'Symbol {symbol} is not predictable')
            continue

        pred_df = pd.DataFrame({symbol: {'2022-01-01': prediction['prediction']}})
        # add the last row of hist_df to make 2 line connected
        pred_df = pd.concat([pred_df, hist_df.tail(1)])
        pred_df.columns = [f'{symbol} prediction']
        chart_data.append(pred_df)

    # concatenate all df
    chart_data = pd.concat(chart_data, axis=1)
    chart_data.index = chart_data.index.str[:10]

    # update chart
    chart = st.line_chart(chart_data)


# Add symbols input to sidebar
text_input = st.sidebar.text_input('Symbols',
                                   key='symbols',
                                   placeholder='List of symbols separated by space. For example: "SPY AAPL"',
                                   on_change=update_chart)