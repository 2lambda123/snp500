import yaml
import joblib
import argparse
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler


with open("model/params.yaml", "r") as params_file:
    params = yaml.safe_load(params_file)

data_dir = params['data_dir']


def split_data(dfs, train_frac):
    train_dfs = []
    test_dfs = []
    for df in dfs:
        train_size = int(len(df) * train_frac)
        train_dfs.append(df[:train_size])
        test_dfs.append(df[train_size:])

    return train_dfs, test_dfs


def rescale_data(dfs):
    """Rescale all features using MinMaxScaler() to same scale, between 0 and 1."""

    scaler = MinMaxScaler()
    scaler = scaler.fit(pd.concat(dfs, ignore_index=True))

    scaled_dfs = [pd.DataFrame(scaler.transform(df),
                               index=df.index,
                               columns=df.columns) for df in dfs if not df.empty]

    # save trained data scaler
    joblib.dump(scaler, params['scaler_path'])

    return scaled_dfs


def prep_data(dfs, train_frac):
    # split into train/test datasets
    train_dfs, test_dfs = split_data(dfs, train_frac)

    # rescale data
    train_dfs = rescale_data(train_dfs)

    scaler = joblib.load(params['scaler_path'])
    test_dfs = [pd.DataFrame(scaler.transform(test_df),
                             index=test_df.index,
                             columns=test_df.columns) for test_df in test_dfs if not test_df.empty]

    return train_dfs, test_dfs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default=params['data_dir'])
    parser.add_argument("--train-frac", type=float, default=params['train_frac'])
    args = parser.parse_args()

    dfs = [pd.read_csv(os.path.sep.join([args.data_dir, filename])).drop('Date', axis=1)
                       for filename in os.listdir(args.data_dir)]
    prep_data(dfs, args.train_frac)