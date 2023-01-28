# S&P500 stocks relation

This project is conducted under my application for Delta Cognition.

## Project description

The purpose of this task is to analyze and create a relation graph of S&P500 companies based on their categories and their stock performance from 2009 to 2021. Then, we can further use this relation graph to analyze the prediction for stocks in 2022. For example, the prediction of AAPL in 2022 is X% increase and it leads to Y% decrease in GOOG and Z% decrease in TSLA. Not only building the relation graph and the machine learning model, but we also expected to have an API which generates such relation above. Please refer to the below for the specification of the API.
 
Input: A company symbol and N

Output: The prediction of the stock price of the company in 2022 and top-N companies that are significantly affected by such predicted change.
 
Required tech stack:
- Framework: PyTorch or Tensorflow
- API: FastAPI (Python)
- Presentation: Streamlit (Python)
- Database: SQL or NoSQL

For further information, please refer to the documentation.