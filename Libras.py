#IMPORTS
import cv2
from ultralytics import YOLO #ultralytics para validar as caixas com os gestos e ajustar os parâmetros.

# Carrega o modelo treinado pelo YOLO 
model = YOLO("/caminho/para/best.pt")

# Abre a webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Faz o YOLO funcionar e pra dar os resultados ou não
    resultados = model.predict(source=frame, conf=0.5, verbose=False)

    # Pega as detecções
    for r in resultados: # Itera sobre os resultados de detecção retornados pelo modelo
        for box in r.boxes:
            # Coordenadas
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            classe_id = int(box.cls[0])
            conf = float(box.conf[0])
            nome_classe = model.names[classe_id]

            # Caixa que aparece as letras 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            texto = f"{nome_classe} ({conf:.2f})"
            cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)
            

    cv2.imshow("Detector de Libras", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
