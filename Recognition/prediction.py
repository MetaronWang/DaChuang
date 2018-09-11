# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import cv2
import model
n_classes = 10

MODEL_SAVE_PATH = 'Model/'
weights = {
    'wc1': tf.Variable(tf.random_normal([11, 11, 1, 64])),
    'wc2': tf.Variable(tf.random_normal([5, 5, 64, 192])),
    'wc3': tf.Variable(tf.random_normal([3, 3, 192, 384])),
    'wc4': tf.Variable(tf.random_normal([3, 3, 384, 384])),
    'wc5': tf.Variable(tf.random_normal([3, 3, 384, 256])),
    'wd1': tf.Variable(tf.random_normal([4 * 4 * 256, 4096])),
    'wd2': tf.Variable(tf.random_normal([4096, 4096])),
    'out': tf.Variable(tf.random_normal([4096, 10]))
}
biases = {
    'bc1': tf.Variable(tf.random_normal([64])),
    'bc2': tf.Variable(tf.random_normal([192])),
    'bc3': tf.Variable(tf.random_normal([384])),
    'bc4': tf.Variable(tf.random_normal([384])),
    'bc5': tf.Variable(tf.random_normal([256])),
    'bd1': tf.Variable(tf.random_normal([4096])),
    'bd2': tf.Variable(tf.random_normal([4096])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


def resize_img(img_dir):
    image = Image.open(img_dir)
    plt.imshow(image)
    plt.show()
    image = image.resize([28,28])
    image = np.array(image)
    return image



def evaluate(image):
    image = np.reshape(image, [2, 28, 28, 1])
    img = tf.cast(image, tf.float32)
    img = tf.reshape(img, [2, 28, 28, 1])
    cv2.waitKey(0)
    img = tf.reshape(img, [2, 28, 28, 1])
    logit = model.inference(img, weights, biases, 1)
    x = tf.placeholder(tf.float32, shape=[2, 28, 28, 1])
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session()
    saver = tf.train.Saver()
    print("loading model....")
    ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
        print('model is loaded')
        prediction = sess.run(logit, feed_dict={x: image})
        max_index = np.argmax(prediction, 1)
        print("the number is ", max_index)
        return max_index, prediction
    else:
        print("there is wrong with cpkt !")
    sess.close()




if __name__=='__main__':
    #img = resize_img("test_8.jpg")
    img = cv2.imread("test_8.jpg")
    img = img[:, :, 1]
    cv2.imshow('img', img)
    cv2.waitKey(0)
    evaluate(img)