# TensorFlow

## 概念

1. tensor:张量

2. flow:流

3. Graph

4. constant

5. variable

6. operator

7. session

8. initializer

9. optimizer

10. placeholder

11. device

12. tf.nn

    提供神经网络相关操作的支持，包括卷积操作、池化操作、归一化、loss、分类操作、embedding、RNN、Evaluation

13. tf.layers

    主要提供高层神经网络，主要和卷积相关的

14. tf.train

15. tf.summary

## 常用方法

* tf.truncated_normal(shape, mean, stddev)

  shape表示生成张量的维度，mean是均值，stddev是标准差。这个函数产生正态分布，均值和标准差自己设定。

  ```python
  import tensorflow as tf
  
  normal = tf.truncated_normal([5, 5], 0, 1)
  with tf.Session() as sess:
      print(sess.run(normal))
  ```

  输出如下：

  ```
  [[ 0.82804805 -1.3059485  -0.5262774   0.06381077  1.1498088 ]
   [-1.601566   -1.3835682  -0.81245834 -0.87032413 -0.25759754]
   [ 1.8594772  -0.24139118 -0.8689264  -0.8653782   0.05525788]
   [-0.4526268   1.6639057   0.8100824  -0.01094603  0.57145065]
   [-0.27275634 -0.59797066 -0.35638377  0.47363234 -0.6935873 ]]
  ```

  

  