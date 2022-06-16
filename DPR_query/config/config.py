
from uvicorn import Config


class Config():
    es_host = "ask2democracy.es.us-central1.gcp.cloud.es.io"
    es_user = "elastic"
    es_password = "siKAHmmk2flwEaKNqQVZwp49"
    proposals_index = "petrolfo"
    #reader_model_name_or_path = "deepset/roberta-base-squad2"
    reader_model_name_or_path = "deepset/xlm-roberta-large-squad2"
    use_gpu = False
    