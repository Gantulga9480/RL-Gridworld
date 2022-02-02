import numpy as np
import cv2
import pygame


class Image:

    # class imports
    import cv2
    import os
    import pygame

    def __init__(self):
        pass

    def load(self, img_path):
        return pygame.image.load(img_path)

    def save(self, img, path):
        cv2.imwrite(path, img)

    def process(self, img_path, dim=None, save=False, save_path=None):
        try:
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            re_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            if save:
                cv2.imwrite(save_path, re_img)
                img = pygame.image.load(save_path)
            else:
                cv2.imwrite("img\\temp.jpg", re_img)
                img = pygame.image.load("img\\temp.jpg")
                os.remove("img\\temp.jpg")
            return img
        except FileNotFoundError:
            return None
