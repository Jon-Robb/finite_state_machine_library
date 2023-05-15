class Color:
    def __init__(self, rgb_value:tuple):
        if rgb_value[0]> 255 or rgb_value[1] > 255 or rgb_value[2] > 255 or rgb_value[0] < 0 or rgb_value[1] < 0 or rgb_value[2] < 0:
            raise ValueError("Color values must be between 0 and 255")
        self.__color_tuple = rgb_value
        
    @property
    def color_tuple(self):
        return self.__color_tuple
    
    @color_tuple.setter
    def color_tuple(self, rgb_value:tuple):
        if rgb_value[0]> 255 or rgb_value[1] > 255 or rgb_value[2] > 255 or rgb_value[0] < 0 or rgb_value[1] < 0 or rgb_value[2] < 0:
            raise ValueError("Color values must be between 0 and 255")
        self.__color_tuple = rgb_value