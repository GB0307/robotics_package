import numpy as np 

try:
    from .PositionVector import PositionVector as PV
except:
    # pylint: disable=import-error
    from PositionVector import PositionVector as PV  # nopep8
    

class RotationMatrix:
    def __init__(self, rotation=None, of=None, to = None):
        if rotation is not None and not isinstance(rotation, np.matrix) and not isinstance(rotation, np.ndarray) and not isinstance(rotation, list):
            raise Exception("Rotation must be an array or matrix")

        if isinstance(rotation, list) or isinstance(rotation, np.ndarray):
            rotation = np.asmatrix(rotation)

        self.of = of
        self.to = to
        self.npMatrix = rotation if rotation is not None else np.asmatrix(np.identity(3))

        if self.npMatrix.shape != (3,3):
                raise Exception(f"Wrong format, should be (3,3), found {rotation.shape}")

    @property
    def inverse(self) -> 'RotationMatrix':
        return RotationMatrix(of=self.to, to=self.of, rotation=np.transpose(self.npMatrix))
         

    def __str__(self):
        return f"Rotation Matrix from {self.of} to {self.to}\n{self.npMatrix.__str__()}"


    def __mul__(self, other):
        #print(f"MULTIPLING {self} * {other}")

        # MULTIPLYING 2 TRANSFORM MATRICES
        if isinstance(other, RotationMatrix):
            print("IS MATRIX")
            if self.of != other.to:
                raise Exception("Invalid multiplication, self.of must be equals to other.to")
            return RotationMatrix(self.npMatrix * other.npMatrix, other.of, self.to)
            
        # MULTIPLYING A TRANSFORM MATRIX TO A POSITION VECTOR
        elif isinstance(other, PV):
            if self.of != other.of:
                raise Exception("Invalid multiplication, the rotation matrix and position should be from the same system")
            return PV(position=self.npMatrix*other.position, of=self.to)
        else:
            raise Exception("Rotation can only multiply another rotation or a position vector")




