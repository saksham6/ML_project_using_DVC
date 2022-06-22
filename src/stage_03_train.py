from os import sep
import pandas as pd
import argparse
from src.utils.common_utils import (
    read_params,
    create_dir,
    save_reports)
import logging
from sklearn.linear_model import ElasticNet
import joblib


def train(config_path):
    config = read_params(config_path)

    # print(config)

    artifacts = config["artifacts"]
    split_data = artifacts["split_data"]
    train_data_path = split_data["train_path"]

    base = config["base"]
    random_seed = base["random_state"]
    
    reports= artifacts["reports"]
    reports_dir = reports["reports_dir"]
    params_file = reports["params"]

    ElasticNet_params = config["estimators"]["ElasticNet"]["params"]
    alpha = ElasticNet_params["alpha"]
    l1_ratio = ElasticNet_params["l1_ratio"]

    train = pd.read_csv(train_data_path, sep=",")
    print(train.shape)
    print(train.columns)

    target = base["target_col"]
    # print(target)
    train_y = train[target]
    train_x = train.drop(target, axis=1)  
    # train_y = train[['insurance_cost']]

    # train_x = train.drop('insurance_cost', axis=1) 
    print(train_x.shape)

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_seed)
    lr.fit(train_x, train_y)

    model_dir = artifacts["model_dir"]
    model_path = artifacts["model_path"]

    create_dir([model_dir, reports_dir])

    params = {
        "alpha": alpha,
        "l1_ratio": l1_ratio,
    }

    save_reports(params_file, params)

    joblib.dump(lr, model_path)


if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    # parse_args will take the arguments you provide on the command line when you run your program and interpret them according to the arguments you have added to your ArgumentParser object.

    try:
        data = train(config_path=parsed_args.config)
    except Exception as e:
        raise e
