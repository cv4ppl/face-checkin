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

SYS_WIDTH = 96
SYS_HEIGHT = 128


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
                for n in os.listdir(user[3]):
                    filename = os.path.join(user[3], n)
                    user_img = cv2.imread(filename)
                    user_img = cv2.resize(user_img, (SYS_WIDTH, SYS_HEIGHT))
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

        img = cv2.resize(img, (SYS_WIDTH, SYS_HEIGHT))
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

        max_logits = dict()
        for j in range(len(F)):
            if uid[j] in max_logits:
                max_logits[uid[j]] = max(max_logits[uid[j]], -np.log(np.linalg.norm(np.abs(f - F[j]))))
            else:
                max_logits[uid[j]] = -np.linalg.norm(np.abs(f - F[j]))
        s = sum([np.exp(x) for x in max_logits.values()])
        v = []
        k = []
        for key, value in max_logits.items():
            v.append(np.exp(value) / s)
            k.append(key)
        sorted_idx = np.argsort(v)
        ret = []
        for i in reversed(sorted_idx):
            ret.append([k[i], v[i]])
        return ret

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
        K = min(len(sig), 20)

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
    # options.parse_command_line()

    model = SingleFaceModel()
    model.train()

    # acc_count = 0
    # all_count = 0
    # for i in range(1, 4 + 1):
    #     for j in range(1, 2):
    #         print(i, j)
    #         im = cv2.imread(os.path.join(options.options.data_path, "test", "s%d" % i, "%d.jpg" % j))
    #         all_count += 1
    #         acc_count += (str(i) == str(model.get_id_by_image(im, True)))
    #
    # print("Acc: %.6f" % (acc_count / all_count))


if __name__ == "__main__":
    test_acc()
