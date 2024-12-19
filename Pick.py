import cv2
import pickle

width, height = 15, 30

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# Variabel global tambahan
dragParkir = False
parkirTerpilih = None
offsetX, offsetY = 0, 0
highlighted = []  # Menyimpan indeks kotak yang ditebalkan

def mouseClick(events, x, y, flags, params):
    global posList, dragParkir, parkirTerpilih, offsetX, offsetY, highlighted

    if events == cv2.EVENT_LBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                if i in highlighted:
                    highlighted.remove(i)  # Hilangkan dari daftar jika sudah ada
                else:
                    highlighted.append(i)  # Tambahkan ke daftar jika belum ada
                break

        if not dragParkir:
            posList.append((x, y))

    if events == cv2.EVENT_LBUTTONUP:
        dragParkir = False

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                if i in highlighted:
                    highlighted.remove(i)  # Hapus juga dari daftar highlighted
                break

    if dragParkir and parkirTerpilih is not None:
        posList[parkirTerpilih] = (x - offsetX, y - offsetY)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('Foto/Foto 2.png')
    counter = 1
    for i, pos in enumerate(posList):
        if i in highlighted:
            # Gambar kotak yang ditebalkan
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 3)
        else:
            # Gambar kotak biasa
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 3)
        cv2.putText(img, str(counter), (pos[0] + 5, pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        counter += 1

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    # Tambahkan fitur hapus semua kotak dengan menekan tombol 'x'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        posList.clear()
        highlighted.clear()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
