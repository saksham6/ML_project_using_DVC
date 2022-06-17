from email import header
from pkgutil import get_data
import pandas as pd
import argparse
from src.utils.common_utils import read_params, clean_prev_dirs_if_exist,create_dir,save_local_df
import logging


def get_data(config_path):
    config = read_params(config_path)

    # print(config)

    data_path = config["data_source"]["s3_source"]
    artifacts_dir= config["artifacts"]["artifacts_dir"]
    raw_local_data_dir= config["artifacts"]["raw_local_data_dir"]
    raw_local_data= config["artifacts"]["raw_local_data"]

    clean_prev_dirs_if_exist(artifacts_dir)

    create_dir(dirs=[artifacts_dir, raw_local_data_dir])

    df = pd.read_csv(data_path, sep=";")

    print(df)

    save_local_df(df, raw_local_data, header=True)

    # return None

if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    # parse_args will take the arguments you provide on the command line when you run your program and interpret them according to the arguments you have added to your ArgumentParser object.

    try:
        data = get_data(config_path=parsed_args.config)
    except Exception as e:
        raise e
