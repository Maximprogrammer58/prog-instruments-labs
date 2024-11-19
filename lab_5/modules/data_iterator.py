import modules.add_functions as ef


class DataIterator:
    """Iterator for data from dataset
     Attribute:
       data: weather data by day
       index: number of day
     """
    def __init__(self, path: str):
        self.__data = ef.read_data(path)
        self.__index = -1

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        self.__index = value

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        if self.__index < len(self.__data) - 1:
            self.__index += 1
            return tuple(self.__data[self.__index])
        else:
            raise StopIteration