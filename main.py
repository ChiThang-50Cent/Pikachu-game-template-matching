import cv2 as cv
import numpy as np
import argparse

def matching(path):
    img = cv.imread(path)
    img = cv.resize(img, (956, 630))

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    for i in range(1, 37):
        copy = img.copy()

        template = cv.imread(f'./img/pieces{i}.png', cv.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.65

        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv.rectangle(copy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv.imshow('img', copy)
        key = cv.waitKey(0)

        if key == ord('q'):
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', default='./game_play.jpg')

    args = parser.parse_args()

    matching(path=args.img_path)