import numpy as np
try:
    from .PositionVector import PositionVector as PV
    from .RotationMatrix import RotationMatrix as RM  # nopep8
except:
    # pylint: disable=import-error
    from PositionVector import PositionVector as PV  # nopep8
    from RotationMatrix import RotationMatrix as RM  # nopep8

np.set_printoptions(suppress=True)

#TODO: make a check function to know if the matrix is correct (0001 on bottom and unitary rotation vectors)
#TODO: RAISE ERROR IF THE VECTOR AND ROTATION OF/TO IS NOT NONE AND NOT EQUAL TO SELF.OF/SELF.TO
class TransformMatrix:
    def __init__(self, rotation= None, position= None, transform: np.ndarray = None, of=None, to=None):
        self.of = of
        self.to = to

        if transform is not None:
            if isinstance(transform, list):
                transform = np.asmatrix(transform)
            if transform.shape != (4,4):
                raise Exception("Wrong Transform Matrix Shape!")

            self.transform = transform
            self.rotation = RM(rotation=transform[0:3, 0:3], of=of, to=to)
            self.position = PV(position=transform[:3,3:], of=to)


        else:
            if position is None:
                position = PV(of=to)
            elif isinstance(position, list) or isinstance(position, np.ndarray):
                position = PV(position=np.array(position), of=to)
            elif not isinstance(position, PV):
                raise Exception("Unsuported type, Position must be an np.ndarray, list or PositionVector")

            if rotation is None:
                rotation = RM(of=of, to=to)
            elif isinstance(rotation, list) or isinstance(rotation, np.ndarray) or isinstance(rotation, np.matrix):
                rotation = RM(rotation=np.asmatrix(rotation), of=of, to=to)
            elif not isinstance(rotation, RM):
                raise Exception("Unsuported type, Rotation must be an np.ndarray, list or RotationMatrix")


            self.position = position
            self.rotation = rotation
            self.transform = np.concatenate((np.concatenate((rotation.npMatrix, position.position), axis=1), np.array([[0,0,0,1]])))
            
    
    def __str__(self):
        return f"Transform matrix from {self.of} to {self.to}\n{np.around(self.transform, decimals=4).__str__()}"
    
    def __mul__(self, other):
        if isinstance(other, TransformMatrix):
            if self.of != other.to:
                raise Exception("Incompatible Transform Matrices")
            else: 
                return TransformMatrix(transform=self.transform*other.transform, of=other.of, to=self.to)
        
        elif isinstance(other, PV):
            if self.of != other.of:
                raise Exception("Position Vector of another system")
            else:
                return PV(position=(self.transform * np.concatenate((other.position, [[1]])))[:3], of=self.to)

    @property
    def inverse(self) -> 'TransformMatrix':
        r = self.rotation.inverse
        p = -(r.npMatrix*self.position.position)
        return TransformMatrix(rotation=r, position=p, of=self.to, to=self.of)