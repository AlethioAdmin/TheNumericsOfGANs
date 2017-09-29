import tensorflow as tf
from tensorflow.contrib import slim
import logging
from consensus_gan.ops import lrelu

logger = logging.getLogger(__name__)


def generator(z, f_dim, output_size, c_dim, is_training=True):
    # Network
    net = slim.fully_connected(z, 512, activation_fn=lrelu)
    net = slim.fully_connected(net, output_size//16 * output_size//16 * f_dim, activation_fn=lrelu)
    net = tf.reshape(net, [-1, output_size//16, output_size//16, f_dim])

    conv2dtrp_argscope = slim.arg_scope(
        [slim.conv2d_transpose], kernel_size=[5, 5], stride=[2, 2], activation_fn=lrelu)

    with conv2dtrp_argscope:
        net = slim.conv2d_transpose(net, f_dim)
        net = slim.conv2d_transpose(net, f_dim)
        net = slim.conv2d_transpose(net, f_dim)
        net = slim.conv2d_transpose(net, c_dim, activation_fn=None)

    out = tf.nn.tanh(net)

    return out


def discriminator(x, f_dim, output_size, c_dim, is_training=True):
    # Network
    net = x
    with slim.arg_scope([slim.conv2d], kernel_size=[5, 5], stride=[2, 2], activation_fn=lrelu):
        net = slim.conv2d(net, f_dim)
        net = slim.conv2d(net, f_dim)
        net = slim.conv2d(net, f_dim)
        net = slim.conv2d(net, f_dim)

    net = tf.reshape(net, [-1, output_size//16 * output_size//16 * f_dim])
    net = slim.fully_connected(net, 512, activation_fn=lrelu)
    logits = slim.fully_connected(net, 1, activation_fn=None)
    logits = tf.squeeze(logits, -1)

    return logits
