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
class TransformMatrix:
    def __init__(self, rotation= None, position= None, transform: np.ndarray = None, of=None, to=None):
        self.of = of
        self.to = to

        #TODO : REMAKE TO BE MORE INTUITIVE, ALLOW FOR 1-dimensional lists and ndarrays in position, check PV of compatibility

        self.position = None
        self.rotation = None

        if transform is not None:
            if isinstance(transform, list):
                transform = np.asmatrix(transform)
            if transform.shape != (4,4):
                raise Exception("Wrong Transform Matrix Shape!")

            self.transform = transform
            self.rotation = RM(rotation=transform[0:3, 0:3], of=of, to=to)
            self.position = PV(position=transform[:3,3:], of=to)


        else:
            position = position if position is not None else np.zeros((3,1))
            rotation = rotation if rotation is not None else np.identity(3)

            position = np.array(position) if isinstance(position, list) else position
            rotation = np.array(rotation) if isinstance(rotation, list) else rotation
            
            if isinstance(position, PV):
                self.position = position
            elif position.shape != (3,1):
                raise Exception(f"Wrong position shape, should be (3,1), found {position.shape}")

            if isinstance(rotation, RM):
                self.rotation = rotation
            elif rotation.shape != (3,3):
                print(rotation)
                raise Exception(f"Wrong rotation shape, should be (3,3), found {rotation.shape}")

            self.position =  self.position if self.position is not None else PV(position=position, of=to)
            self.rotation = self.rotation if self.rotation is not None else RM(rotation=self.rotation, of=of, to=to)
            self.transform = np.concatenate((np.concatenate((self.rotation, self.position), axis=1), np.array([[0,0,0,1]]))) 

        if not isinstance(self.transform, np.matrix):
            self.transform = np.asmatrix(self.transform)       
    
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

        print(r, '\n', p)
        return TransformMatrix(rotation=r, position=p, of=self.to, to=self.of)