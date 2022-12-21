"""
Flask server Endpoints.
Contains all url end-points.
"""
import importlib
import sys
import os
import argparse

import pydantic
import yaml

import uvicorn
from fastapi import FastAPI
from commons import Logger, get_model, get_parser
from engine.base_engine import BaseEngine

# logger
my_logger = Logger.get_logger(__name__)

model_runner = None
input_type = None
input_type_schema = None
output_type = None
output_type_schema = None

parser = get_parser()
args = parser.parse_args()

with open(args.config, 'r') as fh:
    yaml_config = yaml.safe_load(fh)

model = get_model(yaml_config)

def init_models():
    global model_runner, input_type, input_type_schema, output_type, output_type_schema
    my_logger.info("Checking if the server is configured")

    my_logger.info("Initializing the model")
    model_runner = model() # os.env['ModelInterface']()
    my_logger.info("model runner is")
    my_logger.info(str(model_runner))
    input_type = model_runner.get_input_type()
    input_type_schema = input_type.schema_json()
    output_type = model_runner.get_output_type()
    output_type_schema = output_type.schema_json()
    assert isinstance(model_runner, BaseEngine), "this model has not proper interface"
    my_logger.info("model is up and running")



def init_params():
    try:
        # logging started
        my_logger.info("#" * 100)
        my_logger.info("Server Init")

        init_models()  # load models for later usage.

        my_logger.info("Models Initialized Successfully!")

    except Exception as e:
        my_logger.fatal(f"Server Failed to initialize with exception: {e}")
        # extype, value, tb = sys.exc_info()
        sys.exit(1)




init_params()

""" Model Server End-points """
app = FastAPI()

@app.post("/v1/process/")
def process(request: input_type):
    my_logger.info(f"message")
    try:
        return model_engine.run(request), 201
    except Exception as e:
        my_logger.critical("message")
        return {'error': e}, 502


@app.get("/v1/get-input-type")
def input_type():
    global input_type_schema
    my_logger.info(f"model called by")
    result = "model_runner.get_input_type()"
    print(":")
    print(input_type)
    print(":")
    return input_type_schema


@app.get("/v1/get-output-type")
def output_type():
    global output_type_schema
    my_logger.info(f"model called by")
    return output_type_schema

@app.get("/get-engines")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    config = uvicorn.Config("server.main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()