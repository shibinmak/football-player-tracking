"""

** coded by shibinmak on 7/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
from config import config
from tfannotation import tfAnnotation
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from xml_to_csv import xml2csv


def main(_):
    xml2csv()

    f = open(config.CLASSES_FILE, 'w')

    for (k, v) in config.CLASSES.items():
        item = ("item{\n""\t id: " + str(v) + "\n"
                                              "\tname: '" + k + "'\n""}\n")
        f.write(item)

    f.close()

    D = {}
    rows = open(config.ANNOT_PATH).read().strip().split('\n')

    for row in rows[1:]:
        row = (row.split(','))
        (imagepath, width, height, label, xmin, ymin, xmax, ymax) = row
        (xmin, ymin) = (float(xmin), float(ymin))
        (xmax, ymax) = (float(xmax), float(ymax))
        (width, height) = (int(width), int(height))

        b = D.get(imagepath, [])
        b.append((label, (width, height), (xmin, ymin, xmax, ymax)))
        D[imagepath] = b
    (trainKeys, testKeys) = train_test_split(list(D.keys()), test_size=config.TEST_SIZE)

    dataset = [('train', trainKeys, config.TRAIN_RECORD),
               ('test', testKeys, config.TEST_RECORD)]

    for (dtype, keys, output) in dataset:
        print('[INFO] processing {}'.format(dtype))

        writer = tf.python_io.TFRecordWriter(output)
        total = 0
        for k in keys:
            encoded = tf.gfile.GFile(k, 'rb').read()
            encoded = bytes(encoded)
            tfAnnot = tfAnnotation()
            filename = os.path.basename(k)
            encoding = filename[filename.rfind('.') + 1:]
            (width, height) = D[k][0][1]
            tfAnnot.filename = filename
            tfAnnot.image = encoded
            tfAnnot.encoding = encoding

            tfAnnot.width = width
            tfAnnot.height = height
            for (label, (w, h), (xmin, ymin, xmax, ymax)) in D[k]:
                xmin /= w
                xmax /= w
                ymin /= h
                ymax /= h

                tfAnnot.xmins.append(xmin)
                tfAnnot.ymins.append(ymin)
                tfAnnot.xmaxs.append(xmax)
                tfAnnot.ymaxs.append(ymax)
                tfAnnot.textLabels.append(label.encode('utf8'))
                tfAnnot.classes.append(config.CLASSES[label])

                total += 1
            features = tf.train.Features(feature=tfAnnot.build())
            example = tf.train.Example(features=features)

            writer.write(example.SerializeToString())
        writer.close()
        print('[INFO] {} examples saved for {}'.format(total, dtype))


if __name__ == '__main__':
    tf.app.run()
