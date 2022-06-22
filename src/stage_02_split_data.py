from email import header
from pkgutil import get_data
import pandas as pd
import argparse
from src.utils.common_utils import (
    read_params,
    create_dir,
    save_local_df)
import logging
from sklearn.model_selection import train_test_split


def split_and_save_data(config_path):
    config = read_params(config_path)

    # print(config)

    artifacts = config["artifacts"]
    
    raw_local_data= artifacts["raw_local_data"]

    split_data = artifacts["split_data"]
    processed_data_dir = split_data["processed_data_dir"]
    test_data_path = split_data["test_path"]
    train_data_path = split_data["train_path"]

    # clean_prev_dirs_if_exist(artifacts_dir)

    create_dir([processed_data_dir])

    base = config["base"]
    split_ratio = base["test_size"]
    random_seed = base["random_state"]

    df = pd.read_csv(raw_local_data, sep=",")

    train, test = train_test_split(df, test_size=split_ratio, random_state=random_seed)

    for data, data_path in (test, test_data_path), (train, train_data_path):
        save_local_df(data, data_path)

    # return None

if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    # parse_args will take the arguments you provide on the command line when you run your program and interpret them according to the arguments you have added to your ArgumentParser object.

    try:
        data = split_and_save_data(config_path=parsed_args.config)
    except Exception as e:
        raise e
