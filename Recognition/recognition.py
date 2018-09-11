# -*- coding: utf-8 -*-
import numpy as np
import cv2
from PIL import Image
import math
import prediction
import queue
import time
min_area = 1000
max_area = 10000

def deleteArea(img):
    h = np.size(img, 0)
    w = np.size(img, 1)
    v = np.zeros([h, w])
    thre = 255 * h
    if np.sum(img[:, 0]) == thre:
        q = queue.Queue()
        a = [0, 0]
        v[0, 0] = 1
        q.put(a)
        while not q.empty():
            a = q.get()
            y0 = a[0]
            x0 = a[1]
            img[y0, x0] = 0
            x1 = x2 = y1 = y2 = -1
            if a[0] + 1 < h:
                y1 = a[0] + 1
            if a[0] - 1 >= 0:
                y2 = a[0] - 1
            if a[1] + 1 < w:
                x1 = a[1] + 1
            if a[1] - 1 >= 0:
                x2 = a[1] - 1
            if x1 >= 0:
                if v[y0][x1] == 0 and img[y0][x1] == 255:
                    b = [y0, x1]
                    q.put(b)
                    v[y0][x1] = 1
            if x2 >= 0:
                if v[y0][x2] == 0 and img[y0][x2] == 255:
                    b = [y0, x2]
                    q.put(b)
                    v[y0][x2] = 1
            if y1 >= 0:
                if v[y1][x0] == 0 and img[y1][x0] == 255:
                    b = [y1, x0]
                    q.put(b)
                    v[y1][x0] = 1
            if y2 >= 0:
                if v[y2][x0] == 0 and img[y2][x0] == 255:
                    b = [y2, x0]
                    q.put(b)
                    v[y2][x0] = 1
    if np.sum(img[:, w - 1]) == thre:
        q = queue.Queue()
        a = [0, w - 1]
        v[0, 0] = 1
        q.put(a)
        while not q.empty():
            a = q.get()
            y0 = a[0]
            x0 = a[1]
            img[y0, x0] = 0
            x1 = x2 = y1 = y2 = -1
            if a[0] + 1 < h:
                y1 = a[0] + 1
            if a[0] - 1 >= 0:
                y2 = a[0] - 1
            if a[1] + 1 < w:
                x1 = a[1] + 1
            if a[1] - 1 >= 0:
                x2 = a[1] - 1
            if x1 >= 0:
                if v[y0][x1] == 0 and img[y0][x1] == 255:
                    b = [y0, x1]
                    q.put(b)
                    v[y0][x1] = 1
            if x2 >= 0:
                if v[y0][x2] == 0 and img[y0][x2] == 255:
                    b = [y0, x2]
                    q.put(b)
                    v[y0][x2] = 1
            if y1 >= 0:
                if v[y1][x0] == 0 and img[y1][x0] == 255:
                    b = [y1, x0]
                    q.put(b)
                    v[y1][x0] = 1
            if y2 >= 0:
                if v[y2][x0] == 0 and img[y2][x0] == 255:
                    b = [y2, x0]
                    q.put(b)
                    v[y2][x0] = 1
    return img


def getRo(box):
    ro = np.array([box[0][1], box[1][1], box[2][1], box[3][1]])
    flag_1 = False
    for i in range(1, 4):
        for j in range(0, i):
            if box[i][0] > box[j][0]:
                temp = ro[i]
                ro[i] = ro[j]
                ro[j] = temp
            elif box[i][0] == box[j][0]:
                if not flag_1:
                    flag_1 = True
                else:
                    return 2
    print(ro)
    if ro[3] >= ro[2]:
        return 0 # right
    elif ro[3] < ro[2]:
        return 1  # left

def getNum(img):
    h = np.size(img, 0)
    w = np.size(img, 1)
    flag = 0
    flag_1 = False # check the first number
    flag_2 = False # check the second number
    for i in range(w):
        if flag_2:
            print("flag is ", flag)
            if flag < 4:
                img_1 = img[:, flag: i]
            else:
                img_1 = img[:, flag - 2: i]
            img_2 = img[:, i: w]
            return img_1, img_2
        if np.sum(img[:, i]) == 0:
            if flag_1:
                flag_2 = True
        if np.sum(img[:, i]) != 0:
            if not flag_1:
                flag = i
            flag_1 = True
    return img


def convertBW(img):
    h = np.size(img, 0)
    w = np.size(img, 1)
    for i in range(h):
        for j in range(w):
            if img[i][j] == 0:
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img
'''旋转图像并剪裁'''
def rotate(
        img,  # 图片
        pt1, pt2, pt3, pt4
):

    withRect = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)  # 矩形框的宽度
    heightRect = math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) **2)

    angle = math.acos((pt4[0] - pt1[0]) / withRect) * (180 / math.pi)  # 矩形框旋转角度

    if pt4[1]<=pt1[1]:
        angle = -angle
    print('angle is  ', angle)
    height = img.shape[0]  # 原始图像高度
    width = img.shape[1]   # 原始图像宽度
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
    widthNew = int(width * math.fabs(math.sin(math.radians(angle))) + height * math.fabs(math.cos(math.radians(angle))))
    heightNew = int(height * math.fabs(math.sin(math.radians(angle))) + width * math.fabs(math.cos(math.radians(angle))))

    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))

    # 旋转后图像的四点坐标
    [[pt1[0]], [pt1[1]]] = np.dot(rotateMat, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(rotateMat, np.array([[pt3[0]], [pt3[1]], [1]]))
    [[pt2[0]], [pt2[1]]] = np.dot(rotateMat, np.array([[pt2[0]], [pt2[1]], [1]]))
    [[pt4[0]], [pt4[1]]] = np.dot(rotateMat, np.array([[pt4[0]], [pt4[1]], [1]]))

    # 处理反转的情况
    if pt2[1]>pt4[1]:
        pt2[1],pt4[1]=pt4[1],pt2[1]
    if pt1[0]>pt3[0]:
        pt1[0],pt3[0]=pt3[0],pt1[0]

    imgOut = imgRotation[int(pt2[1]):int(pt4[1]), int(pt1[0]):int(pt3[0])]
    image = Image.fromarray(np.uint8(imgOut))

    return image  # rotated image


def drawRect(img,pt1,pt2,pt3,pt4,color,lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)

def pointLimit(point):
    if point[0] < 0:
        point[0] = 0
    if point[1] < 0:
        point[1] = 0


def imreadex(filename):
    return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_COLOR)

def getResult(img):
    img_h, img_w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    (_, thresh) = cv2.threshold(gradient, 220, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    (imgs, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for cnt in cnts:
        rect = cv2.minAreaRect(cnt)
        h, w = rect[1]
        if w < h:
            h, w = w, h
        ratio = w / h
        s = w * h
        print(s)
        if 0.5 < ratio < 2 and  min_area <= s <= max_area:
            areas.append(rect)
            global box
            box = cv2.boxPoints((rect[0], (rect[1][0]+5, rect[1][1]+5), rect[2]))
            box = np.int0(box)
            #oldimg = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            oldimg = img
            print("box is ", box)
            corners = []
            corners.append(box[2])
            corners.append(box[3])
            corners.append(box[0])
            corners.append(box[1])
            corners = np.array(corners)
            print("ratio is  ", ratio)
            print("area is  ", s)
    flag = getRo(box)
    print(flag)
    global imgRotation
    if flag == 0:
        imgRotation = rotate(img, box[2], box[1], box[0], box[3])
        imgRotation = np.array(imgRotation)
    if flag == 1:
        imgRotation = rotate(img, box[0], box[1], box[2], box[3])
        imgRotation = np.array(imgRotation)
    if flag == 2:
        imgRotation = np.array(img)
        print(box[2][1])
        imgRotation = imgRotation[box[2][1]: box[0][1], box[0][0]: box[3][0], :]
        #card_imgs = []
    # 矩形区域可能是倾斜的矩形，需要矫正，以便使用颜色定位
    '''for rect in areas:
        if rect[2] > -1 and rect[2] < 1:  # 创造角度，使得左、高、右、低拿到正确的值
            angle = 1
        else:
            angle = rect[2]
        rect = (rect[0], (rect[1][0] + 5, rect[1][1] + 5), angle)  # 扩大范围，避免车牌边缘被排除

        box = cv2.boxPoints(rect)
        heigth_point = right_point = [0, 0]
        left_point = low_point = [img_w, img_h]
        for point in box:
            if left_point[0] > point[0]:
                left_point = point
            if low_point[1] > point[1]:
                low_point = point
            if heigth_point[1] < point[1]:
                heigth_point = point
            if right_point[0] < point[0]:
                right_point = point

        if left_point[1] <= right_point[1]:  # 正角度
            new_right_point = [right_point[0], heigth_point[1]]
            pts2 = np.float32([left_point, heigth_point, new_right_point])  # 字符只是高度需要改变
            pts1 = np.float32([left_point, heigth_point, right_point])
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(oldimg, M, (img_w, img_h))
            point_limit(new_right_point)
            point_limit(heigth_point)
            point_limit(left_point)
            card_img = dst[int(left_point[1]):int(heigth_point[1]), int(left_point[0]):int(new_right_point[0])]
            card_imgs.append(card_img)
        # cv2.imshow("card", card_img)
        # cv2.waitKey(0)
        elif left_point[1] > right_point[1]:  # 负角度

            new_left_point = [left_point[0], heigth_point[1]]
            pts2 = np.float32([new_left_point, heigth_point, right_point])  # 字符只是高度需要改变
            pts1 = np.float32([left_point, heigth_point, right_point])
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(oldimg, M, (img_w, img_h))
            point_limit(right_point)
            point_limit(heigth_point)
            point_limit(new_left_point)
            card_img = dst[int(right_point[1]):int(heigth_point[1]), int(new_left_point[0]):int(right_point[0])]
            card_imgs.append(card_img)
    imgRotation = card_imgs[0]
        # cv2.imshow("card", card_img)
        # cv2.waitKey(0)
    w = imgRotation.shape[1]
    h = imgRotation.shape[1]
    img1 = imgRotation[:, 0:int(w/2)]
    img2 = imgRotation[:, int(w/2): w]
    img2 = Image.fromarray(img2)
    img1 = Image.fromarray(img1)
    plt.imshow(img1)
    pylab.show()
    plt.imshow(img2)
    pylab.show()'''
    img_gray = cv2.cvtColor(imgRotation, cv2.COLOR_BGR2GRAY)
    img_thre = img_gray
    cv2.threshold(img_gray, 220, 255, cv2.THRESH_BINARY_INV, img_thre)
    #img_thre = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 2)
    '''T = mahotas.thresholding.otsu(img_gray)
    img_thre[img_thre > T] = 255
    img_thre[img_thre < T] = 0
    img_thre = cv2.bitwise_not(img_thre)'''
    new_img = deleteArea(img_thre)
    img1, img2 = getNum(new_img)
    img1 = Image.fromarray(np.uint8(img1))
    img1 = img1.resize((28, 28), Image.BILINEAR)
    img1 = np.array(img1)

    img2 = Image.fromarray(np.uint8(img2))
    img2 = img2.resize((28, 28), Image.BILINEAR)
    img2 = np.array(img2)
    img1 = convertBW(img1)
    img2 = convertBW(img2)
    img1 = cv2.GaussianBlur(img1, (3, 3), 0)
    img2 = cv2.GaussianBlur(img2, (3, 3), 0)
    img = [img1, img2]
    max_index, logit = prediction.evaluate(img)
    num_1 = max_index[0]
    num_2 = max_index[1]
    result = num_1 * 10 + num_2
    print(logit)
    print(max_index)
    print("Final Result is ",result)


start = time.time()

if __name__ == '__main__':
    imgs = imreadex('1.jpg')
    getResult(imgs)

    end = time.time()

    print(end - start)
