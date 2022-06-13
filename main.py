import cv2
import numpy as np
path = "gambar.png"

img = cv2.imread(path)


def is_putih(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    flt = cv2.inRange(hsv, np.array(
        [0.2, 0.01, 0.50]), np.array([0.7, 0.3, 0.9]))

    cnts = cv2.findContours(flt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    return len(cnts) > 0


def is_bersih(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    flt = cv2.inRange(hsv, np.array([0, 0, 0.55]), np.array([1, 0.4, 1]))

    cnts = cv2.findContours(flt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    return len(cnts) > 0


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# convert to binary
th, threshed = cv2.threshold(gray, 100, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# mencari contours
cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]

# print(len(cnts))
# filter by area
s1 = 10
xcnts = []
standard = 361.45
i = 1

beras_baik = 0
beras_kurang = 0
beras_buruk = 0

for cnt in cnts:
    # untuk setiap contour yang dideteksi, hitung area, dan dibandingkan
    if s1 < cv2.contourArea(cnt):
        xcnts.append(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [approx], -1, (1, 1, 1), -1)
        cropped = img * mask

        putih = is_putih(cropped)
        bersih = is_bersih(cropped)
        utuh = cv2.contourArea(cnt) > standard

        # kondisi 1
        if (bersih == True) and (putih == True) and (utuh == True):
            beras_baik = beras_baik + 1
            print("Beras ke ", i, " berada di kondisi 1 nomor 1")
        elif (bersih == True) and (putih == True) and (utuh == False):
            beras_baik = beras_baik + 1
            print("Beras ke ", i, " berada di kondisi 1 nomor 2")

        # kondisi 2
        elif (bersih == True) and (putih == False) and (utuh == True):
            beras_baik = beras_baik + 1
            print("Beras ke ", i, " berada di kondisi 2 nomor 1")

        # kondisi 3
        elif (bersih == True) and (putih == False) and (utuh == False):
            beras_kurang = beras_kurang + 1
            print("Beras ke ", i, " berada di kondisi 3 nomor 1")

        # kondisi 4
        elif (bersih == False) and (putih == True) and (utuh == True):
            beras_kurang = beras_kurang + 1
            print("Beras ke ", i, " berada di kondisi 4 nomor 1")
        elif (bersih == False) and (putih == True) and (utuh == False):
            beras_kurang = beras_kurang + 1
            print("Beras ke ", i, "berada di kondisi 4 nomor 2")

        # Kondisi 5
        elif (bersih == False) and (putih == False) and (utuh == True):
            beras_buruk = beras_buruk + 1
            print("Beras ke ", i, " berada di kondisi 5 nomor 1")
        elif (bersih == False) and (putih == True) and (utuh == False):
            beras_buruk = beras_buruk + 1
            print("Beras ke ", i, " berada di kondisi 5 nomor 2")

    i = i + 1

print("Jumlah Beras Baik : ", beras_baik)
print("Jumlah Beras Kurang : ", beras_kurang)
print("Jumlah Beras Buruk : ", beras_buruk)
