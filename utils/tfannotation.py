"""

** coded by shibinmak on 7/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""

import tensorflow as tf

from object_detection.utils.dataset_util import int64_feature
from object_detection.utils.dataset_util import int64_list_feature
from object_detection.utils.dataset_util import bytes_feature
from object_detection.utils.dataset_util import float_list_feature
from object_detection.utils.dataset_util import bytes_list_feature 


class tfAnnotation:

    def __init__(self):
        self.filename = None
        self.encoding = None
        self.image = None
        self.height = None
        self.width = None
        self.xmins = []
        self.xmaxs = []
        self.ymins = []
        self.ymaxs = []
        self.classes = []
        self.textLabels = []

    def build(self):
        w = int64_feature(self.width)
        h = int64_feature(self.height)
        filename = bytes_feature(self.filename.encode('utf8'))
        encoding = bytes_feature(self.encoding.encode('utf8'))
        image = bytes_feature(self.image)
        xmins = float_list_feature(self.xmins)
        xmaxs = float_list_feature(self.xmaxs)
        ymins = float_list_feature(self.ymins)
        ymaxs = float_list_feature(self.ymaxs)
        classes = int64_list_feature(self.classes)
        textLabels = bytes_list_feature(self.textLabels)

        data = {
            'image/height': h,
            'image/width': w,
            'image/filename': filename,
            'image/source_id': filename,
            'image/encoded': image,
            'image/format': encoding,
            'image/object/bbox/xmin': xmins,
            'image/object/bbox/xmax': xmaxs,
            'image/object/bbox/ymin': ymins,
            'image/object/bbox/ymax': ymaxs,
            'image/object/class/text': textLabels,
            'image/object/class/label': classes, }

        return data

