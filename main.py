import cv2 as cv
import numpy as np
import argparse
import os

from PIL import ImageGrab
from collections import deque

clear = lambda: os.system('cls')

def eculid_dis(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.linalg.norm(p1 - p2)

def is_one_path(p1, p2):
    x1 = bool(p1[0] - p2[0])
    x2 = bool(p1[1] - p2[1])

    return not (x1 and x2) 

class Pikachu_guide():
    def __init__(self, path) -> None:
        self.w = 40
        self.h = 50
        self.path = path
        self.img = self.read_img()
        self.coors, self.x, self.y = self.find_coordinates()
        self.map = self.convert_into_array()

    def read_img(self):

        screen = cv.cvtColor(np.array(ImageGrab.grab()), cv.COLOR_RGB2BGR)
        screen = screen[226:1014,351:1547,:]
        img = cv.resize(screen, (956, 630))

        return img
    def remove_dup_coors(self, loc):
        temp_list = list(zip(*loc[::-1]))

        list_point = []
        
        while(len(temp_list)):
            temp = temp_list[0]
            temp_list.remove(temp)

            i = 0
            while(i < len(temp_list)):
                dis = eculid_dis(temp, temp_list[i])
                if dis < self.w:
                    temp_list.remove(temp_list[i])
                    i = i - 1
                i = i + 1
            
            list_point.append(temp)
        return list_point

    def find_coordinates(self):

        img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

        coors = []
        x = []
        y = []

        for i in range(1, 37):
            template = cv.imread(f'./img/pieces{i}.png', cv.IMREAD_GRAYSCALE)

            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.65
            loc = np.where(res >= threshold)

            x.extend(loc[1])
            y.extend(loc[0])
            coors.append(self.remove_dup_coors(loc))
            
        return coors, (min(x), max(x)), (min(y), max(y))
    
    def coor_to_index(self, point):
        x_coor = (point[0] - self.x[0]) // (self.w)
        y_coor = (point[1] - self.y[0]) // (self.h)
        return int(x_coor) + 1, int(y_coor) + 1
    
    def convert_into_array(self):
        map_ = np.zeros((11, 18), np.int8)

        for i, piece in enumerate(self.coors):
            for point in piece:   
                x_coor, y_coor = self.coor_to_index(point)
                map_[y_coor][x_coor] = i + 1
        
        return map_

    def find_path(self, start, end):
        queue = deque()
        visited = set()
        parent = {}

        queue.append(start)
        visited.add(start)
        parent[start] = None

        while queue:
            current = queue.popleft()

            if current == end:
                # Đã tìm thấy đích, bạn có thể truy ngược lại từ end sử dụng parent
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            row, col = current
            neighbors = [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]

            for neighbor in neighbors:
                n_row, n_col = neighbor

                if 0 <= n_row < len(self.map) and 0 <= n_col < len(self.map[0])\
                    and ((self.map[n_row][n_col] == 0 and neighbor not in visited) or neighbor == end): 

                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        return None
    
    def count_straight(self, path):
        count = 0
        for i in range(len(path) - 2):
            if not is_one_path(path[i], path[i+2]):
                count += 1
        
        return count
    
    def get_matching(self, piece):
        for i in range(len(piece)):
            p1 = self.coor_to_index(piece[i])
            for j in range(i + 1, len(piece)):
                p2 = self.coor_to_index(piece[j])
                
                path = self.find_path((p1[1], p1[0]), (p2[1], p2[0]))
                if path and self.count_straight(path) <= 2:
                    return (piece[i], piece[j]), path
        
        return tuple()

    def guide(self):
        print('----- Start -------')

        for i, piece in enumerate(self.coors):
            copy = self.img.copy()
            pair = self.get_matching(piece)

            if pair:
                pair, _ = pair
                for pt in list(pair):
                    # print(pt, _)
                    cv.rectangle(copy, pt, (pt[0] + self.w, pt[1] + self.h), (0,0,255), 2)

                cv.imshow('img', copy)
                key = cv.waitKey(0)

                clear()
                if key == ord('q'):
                    break
    
    def display(self):
        for piece in self.coors:
            copy = self.img.copy()
            for pt in piece:
                cv.rectangle(copy, pt, (pt[0] + self.w, pt[1] + self.h), (0,0,255), 2)

            if piece:
                cv.imshow('img', copy)
                key = cv.waitKey(0)

                clear()
                if key == ord('q'):
                    break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', default='./game_play.jpg')
    parser.add_argument('--type', type=int, default=0)
    args = parser.parse_args()

    game = Pikachu_guide(path=args.img_path)

    # path = game.find_path((3, 14), (9, 4))
    # count = game.count_straight(path)
    # print(game.map[(9, 4)], game.map[(3, 14)], path, count)
    # print(game.map)

    if args.type == 0:
        game.guide()
    else:
        game.display()

