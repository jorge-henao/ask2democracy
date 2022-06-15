
from uvicorn import Config


class Config():
    es_host = "localhost"
    proposals_index = "proposals4"
    #reader_model_name_or_path = "deepset/roberta-base-squad2"
    reader_model_name_or_path = "deepset/xlm-roberta-large-squad2"
    use_gpu = False
    