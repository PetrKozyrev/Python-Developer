from abc import ABCMeta, abstractmethod
import os

import pickle
import json

class ParamHandlerException(BaseException):
    raise Exception

class ParamHandler(metaclass=ABCMeta):
    types = {}

    def __init__(self, source):
        self.source = source
        self.params = {}

    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ParamHandlerException('Type must have a name!')
        if not issubclass(klass, ParamHandler):
            raise ParamHandlerException(
                'Class "{}" is not ParamHandler!'.format(klass)
            )
        cls.types[name] = klass

    @classmethod
    def get_instance(cls, source, *args, **kwargs):
        # Шаблон "Factory Method"
        _, ext = os.path.splitext(str(source).lower())
        ext = ext.lstrip('.')
        klass = cls.types.get(ext)
        if klass is None:
            raise ParamHandlerException(
                'Type "{}" not found!'.format(ext)
            )
        return klass(source, *args, **kwargs)

    def add_param(self, key, value):
        self.params[key] = value

    def get_all_params(self):
        return self.params

    @abstractmethod
    def read(self, file):
        pass

    @abstractmethod
    def write(self, file):
        pass


class JsonParamHandler(ParamHandler):
    def read(self, file):
        with open(file) as f:
            json_data = json.load(f)
            for el in json_data:
                self.params[el] = json_data[el]

    def write(self, file):
        with open(file, 'w') as f:
            json.dump(self.params, f)


class PickleParamHandler(ParamHandler):
    def read(self, file):
        with open(file, 'rb') as f:
            pickle_data = pickle.load(f)
            for el in pickle_data:
                self.params[el] = pickle_data[el]

    def write(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.params, f)
        """
        Запись в формате XML параметров self.params
        """