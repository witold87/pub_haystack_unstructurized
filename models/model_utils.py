from haystack.reader import FARMReader
from models.supported_models import models_names
from memory_profiler import profile


@profile
def setup_models_at_startup(use_gpu=False):
    loaded_readers = {}
    for key, value in models_names.items():
        reader = FARMReader(model_name_or_path=f'{value}', use_gpu=use_gpu)
        print(f'Fetched model for {key} language')
        loaded_readers[key] = reader
    print(loaded_readers)
    return loaded_readers
