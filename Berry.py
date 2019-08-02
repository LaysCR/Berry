import time
import math
import numpy as np
from gpiozero import Motor
from gpiozero import DistanceSensor
from Berry_compass import Compass
from Berry_movement import Movement
from Berry_acceleration import Accelerometer


# Segue em frente e detecta obstáculos
def straight(angle):

    speedLeft = 0.6     # Porcentagem inicial da rotação do motor esquerdo
    speedRight = 0.4    # Porcentagem inicial da rotação do motor direito
    DeltaS = 0          # Deslocamento total inicial igual a 0
    minDistance = 15    # Distância mínima aceitada até um obstáculo
    A0 = 0              # Aceleração inicial igual a 0
    V0 = 0              # Velocidade inicial igual a 0

    distance = ultrasonicSensor.distance*100
    while distance > minDistance:

        start = time.time()
        # Movimenta o robô para frente de acordo com a porcentagem de rotação
        (speedLeft, speedRight) = motors.moveForward(angle, speedLeft, speedRight)
        end = time.time()

        # Lê a nova distância até o obstáculo a frente
        distance = ultrasonicSensor.distance*100

        # Mede e a aceleração resultante entre o ponto anterior e o atual
        (Ax, Ay) = accelerationSensor.getAcceleration()
        A = math.sqrt(Ax * Ax + Ay * Ay)

        t = end - start      # Calcula o tempo de locomoção para frente
        # Calcula a velocidade e o deslocamento entre o ponto atual e o anterior
        V = (A0 + A) * t / 2
        S = (V + V0) * t / 2

        A0 = A          # Atualiza o valor inicial da aceleração
        V0 = V          # Atualiza o valor inicial da velocidade
        DeltaS += S*100 # Soma o deslocamento atual com os anteriores convertendo para cm

    motors.stop()   # Para a rotação das rodas

    # Retorna a direção do movimento (angle) e o deslocamento total(DeltaS)
    return angle, round(DeltaS, 2)


# Seleciona um lado para virar (esquerda ou direita)
def selectSide():

    # Verifica a distância para o possível obstáculo na esquerda
    motors.turnLeft(0.6)            # Vira para esquerda
    angleLeft = compass.getAngle()  # Lê a direção atual
    #Lê a distância até o obstáculo na esquerda
    distanceLeft = ultrasonicSensor.distance*100

    # Retorna para a direção inicial
    motors.turnRight(0.5)

    # Verifica a distância para o possível obstáculo na direita
    motors.turnRight(0.5)           # Vira para a direita
    angleRight = compass.getAngle() # Lê a direção atual
    #Lê a distância até o obstáculo na direita
    distanceRight = ultrasonicSensor.distance*100

    # Retorna para a direção inicial
    motors.turnLeft(0.6)

    # Seleciona o lado de maior distância
    if distanceLeft > distanceRight:
        motors.turnLeft(0.6)    # Vira para esquerda
        # Retorna o ângulo da esquerda (angleLeft) e o lado escolhido (Left)
        return angleLeft, 'Left'
    else:
        motors.turnRight(0.5)   # Vira para direita
        # Retorna o ângulo da direita (angleRight) e o lado escolhido (Right)
        return angleRight, 'Right'


# Retorna uma posição seguindo em frente por
# uma distância (distance) na angulação (angle)
def goBack(distance, angle):

    speedLeft = 0.6     # Porcentagem inicial da rotação do motor esquerdo
    speedRight = 0.4    # Porcentagem inicial da rotação do motor direito
    DeltaS = 0          # Deslocamento total inicial igual a 0
    A0 = 0              # Aceleração inicial igual a 0
    V0 = 0              # Velocidade inicial igual a 0

    # Segue em frente enquanto o deslocamento atual for menor que a distância determinada
    while distance > DeltaS:

        start = time.time()
        # Movimenta o robô para frente de acordo com a porcentagem de rotação
        (speedLeft, speedRight) = motors.moveForward(angle, speedLeft, speedRight)
        end = time.time()

        # Mede e a aceleração resultante entre o ponto anterior e o atual
        (Ax, Ay) = accelerationSensor.getAcceleration()
        A = math.sqrt(Ax * Ax + Ay * Ay)

        t = end - start         # Calcula o tempo de locomoção para frente
        # Calcula a velocidade e o deslocamento entre o ponto atual e o anterior
        V = (A0 + A) * t / 2
        S = (V + V0) * t / 2

        A0 = A  # Atualiza o valor inicial da aceleração
        V0 = V  # Atualiza o valor inicial da velocidade
        DeltaS += S * 100  # Soma os deslocamentos e converte para cm

    motors.stop()   # Para a rotação das rodas
    # Adiciona o deslocamento à lista de todos os deslocamentos efetuados
    fulldistanceVector.append(round(DeltaS, 2))


# Inicia a exploração do ambiente
def findPath():
    i = 0
    while i < 10:
        i += 1      # Contador de iterações

        # Chama o método de seleção de lado e recebe o ângulo e lado escolhido
        (angle, side) = selectSide()

        # Verifica se o lado escolhido tem um obstáculo a menos de 30cm
        if ultrasonicSensor.distance * 100 < 30:
            break

        # Insere o lado escolhido em uma pilha
        sideSelected.append(side)
        # Insere o lado escolhido na lista de todos os lados
        # escolhidos durante a exploração do local
        fullsideSelected.append(side)

        (direction, distance) = straight(angle) # Segue em frente na angulação dada

        # Insere o ângulo atual em uma pilha
        directionVector.append(direction)
        # Insere a distância percorrida em uma pilha
        distanceVector.append(distance)
        # Insere o deslocamento na lista de todos deslocamentos
        # efetuados durante a exploração do local
        fulldistanceVector.append(distance)


try:

    # Instancia os objetos utilizados
    compass = Compass()                     # Controle do magnetômetro
    motors = Movement()                     # Controle dos motores
    accelerationSensor = Accelerometer()    # Controle do acelerômetro
    # Controle do sensor ultrassônico
    ultrasonicSensor = DistanceSensor(echo=6, trigger=5, queue_len=1)

    distanceVector = []         # Pilha de deslocamentos
    fulldistanceVector = []     # Lista de deslocamentos
    directionVector = []        # Pilha de angulações
    sideSelected = []           # Pilha de lados escolhidos
    fullsideSelected = []       # Lista de lados escolhidos
    iterations = 0              # Contador de iterações

    while iterations < 5:

        iterations += 1
        # Explora o ambiente
        findPath()

        # Retorna um bloco
        lastDistance = distanceVector[-1]       # Recebe o último deslocamento efetuado
        lastDirection = directionVector[-1]     # Recebe a última direção caminhada

        oppositeAngle = motors.turnBack(lastDirection)  # Rotaciona o robô para trás
        # Adiciona o movimento à lista de todos os lados selecionados
        fullsideSelected.append('Back')
        # Adiciona deslocamento nulo à lista de deslocamentos
        fulldistanceVector.append(0)

        goBack(lastDistance, oppositeAngle)     # Segue para a posição anterior
        distanceVector.pop(-1)                  # Remove o último deslocamento efetuado da pilha
        directionVector.pop(-1)                 # Remove a última direção caminhada da pilha

        # Vai para o lado ainda não explorado
        unusedAngle = motors.turnBack(lastDirection)
        fullsideSelected.append('Back')
        fulldistanceVector.append(0)
        if len(sideSelected) > 0:
            if sideSelected[-1] == 'Left':
                motors.turnRight(0.5)
                straight(compass.getAngle())
            else:
                motors.turnRight(0.5)
                straight(compass.getAngle())
            sideSelected.pop(-1)
        else:
            break

    np.savetxt('distanceVector.npy', fulldistanceVector)
    np.savetxt('sideSelected.npy', fullsideSelected, fmt='%s')

# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
