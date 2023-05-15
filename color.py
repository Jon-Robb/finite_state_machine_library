class Color:
    def __init__(self, r_value:int = 0, g_value:int = 0, b_value:int = 0):
        if r_value> 255 or g_value > 255 or b_value > 255 or r_value < 0 or g_value < 0 or b_value < 0:
            raise ValueError("Color values must be between 0 and 255")
        self.__color_tuple = (r_value, g_value, b_value)
        
    @property
    def color_tuple(self):
        return self.__color_tuple
    
    @color_tuple.setter
    def color_tuple(self, r_value:int, g_value:int, b_value:int):
        if r_value> 255 or g_value > 255 or b_value > 255 or r_value < 0 or g_value < 0 or b_value < 0:
            raise ValueError("Color values must be between 0 and 255")
        self.__color_tuple = (r_value, g_value, b_value)