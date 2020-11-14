import numpy as np
from ..transform import TransformMatrix as TM

    

class DHParameters:
    def __init__(self, parameters, inDegrees=True):
        self.__degree__ = inDegrees

        # Convert parameters into a numpy array
        if isinstance(parameters, list):
            parameters = np.array(parameters)
        elif not isinstance(parameters, np.ndarray):
            raise Exception("Parameters shoud be a list or a numpy array")
        
        
        # Check if parameters is a multiple of 4 and guarantee a shape of (*, 4)
        if len(parameters.shape) == 1:
            if parameters.shape[0] != 4:
                raise Exception("A Denavit-Hartenberg row must have 4 parameters")
            parameters = np.reshape(parameters, (1,4))

        elif len(parameters.shape) != 2 or parameters.shape[-1] != 4:
            raise Exception("Denavit-Hartenberg parameters must be a unidimentional array or an array of shape (*, 4)")

        self.parameters = parameters
    
    def append(self, a, alpha, d, omega):
        self.parameters = np.concatenate((self.parameters, [[a, alpha, d, omega]]))

    def get_transform(self, of:int, to:int=None) -> TM:
        to = to if to is not None else of-1

        # IF TO==OF, THE TRANSFORM WILL ALWAY BE A IDENTITY MATRIX
        if to == of:
            return TM(transform=np.asmatrix(np.identity(4)), of=of, to=to)

        # HANDLE INVERSE REQUESTS
        inv = False
        if to > of:
            inv = True
            of, to = to, of

        T = self.__row_to_transform__(of)

        for i in range(1, of-to):
            T2 = self.__row_to_transform__(of-i)
            T = T2 * T
        return T if not inv else T.inverse
        

    def __str__(self):
        return f"Denavit Hartenbert table with {len(self.parameters)} systems\n{np.concatenate(([['a', 'α', 'd', 'θ']], self.parameters)).__str__()}"

    def __row_to_transform__(self, of: int) -> TM:
        if of <= 0 or of > len(self.parameters):
            raise Exception(f"System out of range, should be in [{1}, {len(self.parameters)}] range but found {of}")

        row = self.parameters[of-1]

        a, alpha = row[0], np.deg2rad(row[1]) if self.__degree__ else row[1]
        d, omega = row[2], np.deg2rad(row[3]) if self.__degree__ else row[3]

        T = [
            [np.cos(omega)              ,  -np.sin(omega)             ,   0            ,     a              ],
            [np.sin(omega)*np.cos(alpha),  np.cos(omega)*np.cos(alpha),  -np.sin(alpha),    -d*np.sin(alpha)],
            [np.sin(omega)*np.sin(alpha),  np.cos(omega)*np.sin(alpha),   np.cos(alpha),     d*np.cos(alpha)],
            [0                          ,  0                          ,   0            ,     1              ]
            ]

        return TM(transform=T, of=of, to=(of-1))

