import numpy as np

class PositionVector:
    def __init__(self, x=None, y=None, z=None, position:np.ndarray=None, of=None):
        self.of = of

        if isinstance(position, list):
            position = np.array(position)
        if position is not None and position.shape == (3,):
            position = np.reshape(position, (3,1))

        if position is not None:
            if position.shape != (3,1):
                raise Exception(f"Wrong position shape, should be (3,1), found {position.shape}")
            self.position = position
        else:
            x = x if x is not None else 0
            y = y if y is not None else 0
            z = z if z is not None else 0

            self.position = np.array([[x],[y],[z]])
    
    def __str__(self):
        return f"Position in system {self.of}\n{self.position.__str__()}"
    
    def __mul__(self, other):
        if type(other) != int or float:
            raise Exception("Positions can only be multiplied to numbers")
        return PositionVector(position=self.position*other, of=self.of)
        

