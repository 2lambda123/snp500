import yaml
import argparse
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import torch
from train import TimeSeriesDataset, TSModel
from test import descale
import pandas as pd
import os

with open("model/params.yaml", "r") as params_file:
    params = yaml.safe_load(params_file)

data_dir = params['data_dir']
save_path = params['save_path']
sequence_length = params['sequence_length']


def predict2022(data_dir, sequence_length):
    scaler = joblib.load(params['scaler_path'])

    model = TSModel(6)
    model.load_state_dict(torch.load(save_path))
    model.eval()

    tickers = []
    predictions = []
    with torch.no_grad():
        for filename in os.listdir(data_dir):
            ticker_name = filename[7:-4]

            df = pd.read_csv(os.path.sep.join([data_dir, filename])).drop('Date', axis=1)

            if len(df) < sequence_length: # ignore ticker with insufficient data
                continue

            df = pd.DataFrame(scaler.transform(df),
                              index=df.index,
                              columns=df.columns)

            historical_data = np.array(df.tail(sequence_length))

            features = torch.Tensor(historical_data)
            output = model(features)

            tickers.append(ticker_name)
            predictions.append(output.item())

    descaler = MinMaxScaler()
    descaler.min_, descaler.scale_ = scaler.min_[0], scaler.scale_[0]
    predictions_descaled = descale(descaler, predictions)

    return pd.DataFrame(predictions_descaled, index=tickers).T


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence-length", type=int, default=params['sequence_length'])
    args = parser.parse_args()

    # save to csv
    predictions = predict2022(params['data_dir'], args.sequence_length)
    predictions.to_csv('model/prediction2022.csv', index=False)

    predictions = pd.read_csv('model/prediction2022.csv')

    # or save to db
    colls = [{'ticker': ticker, 'prediction': prediction}
             for ticker, prediction in zip(list(predictions),
                                           predictions.loc[0].values.tolist())]

    from db_connect import get_db
    mydb = get_db()
    mycoll = mydb["prediction-2022"]
    mycoll.insert_many(colls)

