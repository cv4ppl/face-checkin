from __future__ import print_function

import argparse
import os

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from layers.functions.prior_box import PriorBox
from models.retinaface import RetinaFace
from utils.box_utils import decode
from utils.nms.py_cpu_nms import py_cpu_nms

from data import cfg_mnet

parser = argparse.ArgumentParser(description='Retinaface')
parser.add_argument('-s', '--save_image', action="store_true", default=True, help='show detection results')


def check_keys(model, pretrained_state_dict):
    ckpt_keys = set(pretrained_state_dict.keys())
    model_keys = set(model.state_dict().keys())
    used_pretrained_keys = model_keys & ckpt_keys
    unused_pretrained_keys = ckpt_keys - model_keys
    missing_keys = model_keys - ckpt_keys
    print('Missing keys:{}'.format(len(missing_keys)))
    print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
    print('Used keys:{}'.format(len(used_pretrained_keys)))
    assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
    return True


def remove_prefix(state_dict, prefix):
    ''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
    f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
    return {f(key): value for key, value in state_dict.items()}


def load_model(model, pretrained_path, load_to_cpu):
    print('Loading pretrained model from {}'.format(pretrained_path))
    if load_to_cpu:
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
    else:
        device = torch.cuda.current_device()
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
    if "state_dict" in pretrained_dict.keys():
        pretrained_dict = remove_prefix(pretrained_dict['state_dict'], 'module.')
    else:
        pretrained_dict = remove_prefix(pretrained_dict, 'module.')
    check_keys(model, pretrained_dict)
    model.load_state_dict(pretrained_dict, strict=False)
    return model


torch.set_grad_enabled(False)
cfg = cfg_mnet
net = RetinaFace(cfg=cfg, phase='test')
net = load_model(net, "src/model/retain_face/weights/mobilenet0.25_Final.pth", True)
net.eval()
cudnn.benchmark = True
device = torch.device("cpu")
net = net.to(device)


def predict_by_filename(filename: str):
    resize = 1
    # testing begin
    image_path = filename
    img_raw = cv2.imread(image_path, cv2.IMREAD_COLOR)
    scale = max(img_raw.shape[1] / 384.0, img_raw.shape[0] / 512.0)
    new_size = (int(img_raw.shape[1] / scale), int(img_raw.shape[0] / scale))
    img_raw = cv2.resize(img_raw, new_size)
    img = np.float32(img_raw)

    im_height, im_width, _ = img.shape
    scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
    img -= (104, 117, 123)
    img = img.transpose(2, 0, 1)
    img = torch.from_numpy(img).unsqueeze(0)
    img = img.to(device)
    scale = scale.to(device)

    loc, conf, _ = net(img)  # forward pass

    priorbox = PriorBox(cfg, image_size=(im_height, im_width))
    priors = priorbox.forward()
    priors = priors.to(device)
    prior_data = priors.data
    boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
    boxes = boxes * scale / resize
    boxes = boxes.cpu().numpy()
    scores = conf.squeeze(0).data.cpu().numpy()[:, 1]

    # ignore low scores
    inds = np.where(scores > 0.02)[0]
    boxes = boxes[inds]
    scores = scores[inds]

    # keep top-K before NMS
    order = scores.argsort()[::-1][:5000]
    boxes = boxes[order]
    scores = scores[order]

    # do NMS
    dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    keep = py_cpu_nms(dets, 0.4)
    dets = dets[keep, :]

    dets = dets[:750, :]

    ret = []
    for b in dets:
        if b[4] < 0.9:
            continue

        b = list(map(int, b))

        x0, y0 = b[0], b[1]
        x1, y1 = b[2], b[3]

        half_x = abs(x1 - x0) // 2
        half_y = abs(y1 - y0) // 2

        y1 = min(img_raw.shape[0], y1 - half_y // 4)

        while (x1 - x0) % 3:
            x1 += 1
        len_x = x1 - x0
        len_y = len_x // 3 * 4

        turn = True
        while (y1 - y0) > len_y:
            if turn:
                y1 -= 1
            else:
                y0 += 1
            turn = not turn

        while (y1 - y0) < len_y:
            if turn:
                y1 += 1
            else:
                y0 -= 1
            turn = not turn
        ret.append(img_raw[y0:y1, x0:x1])
        continue

        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        if x1 - x0 < 10 or y1 - y0 < 10:
            continue

        half_x = abs(x1 - x0) // 2
        half_y = abs(y1 - y0) // 2

        x0 = max(0, x0 - half_x // 2)
        x1 = min(img_raw.shape[1], x1 + half_x // 2)
        y0 = max(0, y0 - half_y)
        y1 = min(img_raw.shape[0], y1 + half_y // 4)

        while (x1 - x0) % 3:
            x1 += 1
        len_x = x1 - x0
        len_y = len_x // 3 * 4

        turn = True
        while (y1 - y0) > len_y:
            if turn:
                y1 -= 1
            else:
                y0 += 1
            turn = not turn

        while (y1 - y0) < len_y:
            if turn:
                y1 += 1
            else:
                y0 -= 1
            turn = not turn

        ret.append(img_raw[y0:y1, x0:x1])
    return ret


if __name__ == "__main__":
    for i in range(1, 5):
        count = 0
        for pic in os.listdir("data/raw/%d/" % i):
            count += 1
            filename = os.path.join("data/raw/%d" % i, pic)
            for img in predict_by_filename(filename):
                cv2.imwrite("data/train/%d/%d.jpg" % (i, count), img)
