"""
Model to map the face image to id, where id is provided by database.

If you run this file directly, you can will get the test result.
"""

import os
from copy import deepcopy

import cv2
import numpy as np
from tornado import options

from src.model import utils
from src.server.backend_service import BackendService

class DataProvider:
    def __init__(self):
        self.backend_service = BackendService()

    def get_images(self):
        """
        read database, and get user image, binned with id.
        :return: (list<numpy.array>, list<str>)
        """
        user_ids = self.backend_service.get_user_ids()

        images = []
        ids = []

        for user_id_tuple in user_ids:
            user_id = user_id_tuple[0]
            user = self.backend_service.get_user_by_uid(user_id)[0]

            if user[3]:
                user_img = cv2.imread(user[3])
                # print(user[3])
                user_img = cv2.cvtColor(user_img, cv2.COLOR_BGR2GRAY)
                user_img, _ = utils.Utils.im2vec(user_img.shape, user_img)
                ids.append(user_id)
                images.append(user_img)
        return np.array(images), np.array(ids)


class SingleFaceModel:
    def __init__(self):
        self.data = DataProvider()

    def get_id_by_image(self, img: np.ndarray, show: bool = False):
        """
        Prediction function
        :param img: image to get id
        :param show: to show result image?
        :return: id
        """

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        shape = img.shape
        img, _ = utils.Utils.im2vec(img.shape, img)
        _dif = np.load(os.path.join(options.options.data_path, "mat", "dif.npy"))
        PT = np.load(os.path.join(options.options.data_path, "mat", "pt.npy"))
        F = np.load(os.path.join(options.options.data_path, "mat", "F.npy"))
        avr = np.load(os.path.join(options.options.data_path, "mat", "avr.npy"))
        uid = np.load(os.path.join(options.options.data_path, "mat", "uid.npy"))

        dif = img - avr
        f = np.dot(dif, PT)
        for i in range(len(F)):
            dis = 1e100
            u = -1
            for j in range(len(F)):
                tmp = np.linalg.norm(np.abs(f - F[j]))

                if tmp < dis:
                    dis = tmp
                    u = j

        if show:
            original = utils.Utils.vec2im(img, shape)
            result = utils.Utils.vec2im(_dif[u] + avr, shape)
            v_merge = np.vstack((original, result))
            cv2.imshow("ori + res", v_merge)
            cv2.waitKey(0)
        return uid[u]

    def train(self):
        n_dot = 2

        def diff(raw, avr):
            print("getting dif face")
            dif = np.zeros((len(raw), len(avr)))
            for i in range(len(raw)):
                dif[i] = raw[i] - avr
            return dif

        def add_dim(vec):
            ret = np.zeros((1, len(vec)))
            ret[0] = vec
            return ret

        def get_average_image(images):
            print("getting average face")
            ret = np.copy(images[0])
            for i in range(1, len(images)):
                ret += images[i]
            return ret / len(images)

        input_images, input_labels = self.data.get_images()
        np.save(os.path.join(options.options.data_path, os.path.join("mat", "uid.npy")), input_labels)

        avr = get_average_image(input_images)
        np.save(os.path.join(options.options.data_path, os.path.join("mat", "avr.npy")), avr)

        dif = diff(input_images, avr)
        np.save(os.path.join(
            options.options.data_path, os.path.join("mat", "dif.npy")), dif)

        data = dif
        data = np.mat(data)
        print("calculating svd ...")
        U, sig, VT = np.linalg.svd(data)
        sig = np.diag(sig)
        K = min(len(sig), 10)

        _U = []

        _U = U[:, :K]

        _sig = []

        for row in sig:
            _sig.append(row[:K])

        __sig = deepcopy(_sig)
        _sig = []
        _VT = []

        for i in range(K):
            _sig.append(__sig[i])

        _VT = VT[:K, :]

        _VT = np.array(_VT)
        _sig = np.array(_sig)
        _U = np.array(_U)

        P = np.empty((n_dot, len(avr)))

        for i in range(n_dot):
            P[i] = VT[i]
        PT = P.transpose()

        np.save(os.path.join(options.options.data_path, os.path.join("mat", "pt.npy")), PT)

        F = np.empty((len(dif), n_dot))
        for i in range(len(dif)):
            F[i] = np.dot(add_dim(dif[i]), PT)

        np.save(os.path.join(options.options.data_path, os.path.join("mat", "F.npy")), F)


def test_acc():
    """
    Test acc.
    :return:
    """
    options.define('db_absl_path', 'data/database', type=str, help="database to load")
    options.define('data_path', 'data', type=str, help="database to load")
    options.parse_command_line()

    model = SingleFaceModel()
    model.train()

    acc_count = 0
    all_count = 0
    for i in range(1, 4 + 1):
        for j in range(1, 10 + 1):
            im = cv2.imread(os.path.join(options.options.data_path, "test", "s%d" % i, "%d.pgm" % j))
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            all_count += 1
            acc_count += (str(i) == str(model.get_id_by_image(im, True)))

    print("Acc: %.6f" % (acc_count / all_count))


if __name__ == "__main__":
    test_acc()
