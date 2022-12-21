from abc import ABC
from abc import abstractmethod
from pydantic import BaseModel

class BaseInputType(BaseModel):
    inp: int

class BaseOutputType(BaseModel):
    out: str

class BaseEngine(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_input_type(self):
        pass

    @abstractmethod
    def get_output_type(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class BaseDummyEngine(BaseEngine):

    def __init__(self, real_api):
        super(BaseEngine).__init__()
        print("initiating the dummy model")
        self.model = real_api()

    def get_input_type(self):
        return BaseInputType

    def get_output_type(self):
        return BaseOutputType

    def run(self, inp: BaseInputType):
        i = inp.inp
        print(f"data: {i**2}")
        return BaseOutputType(out=f"data: {i**2}")