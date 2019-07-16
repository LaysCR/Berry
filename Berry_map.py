import matplotlib.pyplot as pplot
import numpy as np

# blueprint = np.matrix('1 0 1 0 1 0;'
#                       '1 0 0 0 0 0;'
#                       '1 0 0 0 1 1;'
#                       '1 1 1 0 0 0;'
#                       '0 0 0 0 0 0')

blockSize = 30


class Map:
    def __init__(self):
        pass

    def generateMap(self, distanceVector, sideSelected):
        # Initialize matrix
        m = 1
        n = 1
        blueprint = np.zeros((3, 3))
        blueprint[m, n] = 1
        # Start mapping
        for i in range(0, len(sideSelected)):
            steps = round(distanceVector[i] / blockSize)
            # Resize matrix
            if m - steps - 1 < 0:
                increase = abs(m - steps - 1)
                blueprint = np.pad(blueprint, pad_width=increase, mode='constant', constant_values=0)
                m += increase
                n += increase
            # Calculate size
            (mSize, nSize) = np.shape(blueprint)
            indexRange = mSize - 1
            # Rotate and adjust indexes
            if sideSelected[i] == 'Left':
                blueprint = np.rot90(blueprint, 3)
                aux = m
                m = n
                n = indexRange - aux
            elif sideSelected[i] == 'Right':
                blueprint = np.rot90(blueprint)
                aux = m
                m = indexRange - n
                n = aux
            else:
                blueprint = np.rot90(blueprint, 2)
                m = indexRange - m
                n = indexRange - n
                # Walk blocks
                m -= steps
                continue
            # Walk blocks
            m -= steps
            # Mark obstacle
            blueprint[m - 1, n] = 1

        fig = pplot.figure()
        pplot.imshow(blueprint, cmap="binary")
        fig.savefig('Blueprint.png')
        # pplot.show()
