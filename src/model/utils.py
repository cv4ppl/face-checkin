import numpy as np


class Utils:

    @staticmethod
    def im2vec(shape, img):
        h, w = shape
        vec = np.empty((w * h))

        for i in range(h):
            for j in range(w):
                vec[i * w + j] = img[i][j]
        return vec, (h, w)

    @staticmethod
    def vec2im(vec, shape):
        h, w = shape
        img = np.empty((h, w), np.uint8)
        for i in range(h):
            for j in range(w):
                img[i][j] = vec[i * w + j]
        return img

    def add_dim(self, vec):
        ret = np.zeros((1, len(vec)))
        ret[0] = vec
        return ret
