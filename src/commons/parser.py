import argparse

def get_parser():
    parser = argparse.ArgumentParser("configuration for model server")
    parser.add_argument("--config", '-c', help="path to yaml file to import the engine",
                        default="../../egs/summarization/config.yaml")
    return parser
