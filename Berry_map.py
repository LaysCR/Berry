import matplotlib.pyplot as pplot
import numpy as np

distanceVector = np.loadtxt('distanceVector.npy')
sideSelected = np.genfromtxt('sideSelected.npy', dtype='str')
blockSize = 30


class Map:
    def __init__(self):
        pass

    def generateMap(self):

        m = 1   # Índice atual na linha
        n = 1   # Índice atual na coluna
        # Inicia matriz de zeros 3x3
        blueprint = np.zeros((3, 3))

        for i in range(0, len(sideSelected)):

            # Calcula o número de blocos a ser percorrido
            steps = round(int(distanceVector[i]) / blockSize)

            # Redimenciona a matriz caso necessário
            if m - steps - 1 < 0:
                # Calcula quantas linhas e colunas serão adicionadas
                increase = abs(m - steps - 1)
                # Aumenta o tamanho da matriz
                blueprint = np.pad(blueprint, pad_width=increase,
                                   mode='constant', constant_values=0)
                m += increase   # Atualiza o índice atual da linha
                n += increase   # Atualiza o índice atual da coluna

            # Mede o tamanho da matriz
            (mSize, nSize) = np.shape(blueprint)
            indexRange = mSize - 1

            # Rotaciona as matrizes
            if sideSelected[i] == 'Left':
                # Rotaciona a matriz para direita
                blueprint = np.rot90(blueprint, 3)
                # Atualiza a posição atual na matriz
                aux = m
                m = n
                n = indexRange - aux
            elif sideSelected[i] == 'Right':
                # Rotaciona a matriz para a esquerda
                blueprint = np.rot90(blueprint)
                # Atualiza a posição atual na matriz
                aux = m
                m = indexRange - n
                n = aux
            else:
                # Rotaciona a matriz duas vezes para a esquerda
                blueprint = np.rot90(blueprint, 2)
                # Atualiza a posição atual na matriz
                m = indexRange - m
                n = indexRange - n
                # Percorre os blocos
                m -= steps
                continue
            # Percorre os blocos
            m -= steps
            # Marca os obstáculos na matriz
            blueprint[m - 1, n] = 1

        # Gera uma imagem do mapa criado
        fig, ax = pplot.subplots(1)
        pplot.imshow(blueprint, cmap="binary")
        pplot.suptitle('Mapa Gerado')
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        # Salva a imagem como um arquivo .png
        fig.savefig('Blueprint.png')
        pplot.show()

map = Map()
map.generateMap()