import cv2
import numpy as np
import time
import os
import mediapipe as mp

# Inicializando o detector de mãos do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85
)
mp_draw = mp.solutions.drawing_utils

# Configurações da Tela e Cores (BGR)
brush_thickness = 8
eraser_thickness = 40
colors = [
    (255, 0, 0),     # Azul
    (0, 255, 0),     # Verde
    (0, 0, 255),     # Vermelho
    (0, 255, 255)    # Amarelo / Borracha (quando selecionado no topo)
]
current_color_idx = 0

# Inicialização da Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Largura
cap.set(4, 720)  # Altura

# Canvas (Tela de pintura) inicial vazio
paint_canvas = None

xp, yp = 0, 0 # Coordenadas anteriores

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Erro ao acessar a webcam.")
        break

    # Espelha a imagem para uma experiência mais natural (como um espelho)
    img = cv2.flip(img, 1)
    h, w, c = img.shape

    if paint_canvas is None:
        paint_canvas = np.zeros((h, w, 3), np.uint8)

    # Converte a imagem de BGR para RGB (exigido pelo MediaPipe)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extrai as coordenadas dos pontos da mão (landmarks)
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if len(lm_list) != 0:
                # Pontas dos dedos: Indicador (8) e Médio (12)
                x1, y1 = lm_list[8][1], lm_list[8][2]
                x2, y2 = lm_list[12][1], lm_list[12][2]

                # Verifica quais dedos esticados (comparação simples com a articulação inferior)
                # Dedo indicador levantado se a ponta (8) estiver acima da articulação (6)
                finger_index_up = lm_list[8][2] < lm_list[6][2]
                finger_middle_up = lm_list[12][2] < lm_list[10][2]

                # ---------------------------------------------------------
                # 1. MODO SELEÇÃO (Dois dedos levantados: Indicador + Médio)
                # ---------------------------------------------------------
                if finger_index_up and finger_middle_up:
                    xp, yp = 0, 0 # Reseta o ponto anterior para evitar linhas retas indesejadas
                    
                    # Desenha indicador visual na tela de seleção
                    cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), colors[current_color_idx], cv2.FILLED)

                    # Seleção de ferramentas por faixa na parte superior da tela (Y < 100)
                    if y1 < 100:
                        if 150 < x1 < 300:
                            current_color_idx = 0 # Azul
                        elif 400 < x1 < 550:
                            current_color_idx = 1 # Verde
                        elif 650 < x1 < 800:
                            current_color_idx = 2 # Vermelho
                        elif 900 < x1 < 1050:
                            # Limpar Tela / Borracha total
                            paint_canvas = np.zeros((h, w, 3), np.uint8)

                # ---------------------------------------------------------
                # 2. MODO DESENHO (Apenas o dedo indicador levantado)
                # ---------------------------------------------------------
                elif finger_index_up and not finger_middle_up:
                    # Desenha o indicador na ponta para guiar o usuário
                    cv2.circle(img, (x1, y1), 10, colors[current_color_idx], cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    # Desenha no Canvas virtual
                    if current_color_idx == 3: # Se quiser implementar borracha por toque
                        cv2.line(paint_canvas, (xp, yp), (x1, y1), (0, 0, 0), eraser_thickness)
                    else:
                        cv2.line(paint_canvas, (xp, yp), (x1, y1), colors[current_color_idx], brush_thickness)

                    xp, yp = x1, y1

                else:
                    xp, yp = 0, 0

            # Opcional: Desenha os esqueletos da mão de forma limpa
            # mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Processamento para fundir o Canvas na imagem da Webcam
    img_gray = cv2.cvtColor(paint_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, paint_canvas)

    # -------------------------------------------------------------
    # Interface Gráfica Superior (Menu de Cores)
    # -------------------------------------------------------------
    cv2.rectangle(img, (150, 10), (300, 80), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, "Azul", (175, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.rectangle(img, (400, 10), (550, 80), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, "Verde", (425, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.rectangle(img, (650, 10), (800, 80), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "Vermelho", (660, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.rectangle(img, (900, 10), (1050, 80), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, "Limpar", (925, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Exibe a janela final
    cv2.imshow("Air Canvas - Portfolio Project", img)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()