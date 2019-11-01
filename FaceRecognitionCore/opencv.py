import cv2
import numpy as np
# import tensorflow as tf
from numpy.lib.stride_tricks import as_strided

def pool2d(A, kernel_size, stride, padding, pool_mode='max'):
    '''
    2D Pooling

    Parameters:
        A: input 2D array
        kernel_size: int, the size of the window
        stride: int, the stride of the window
        padding: int, implicit zero paddings on both sides of the input
        pool_mode: string, 'max' or 'avg'
    '''
    # Padding
    A = np.pad(A, padding, mode='constant')

    # Window view of A
    output_shape = ((A.shape[0] - kernel_size)//stride + 1,
                    (A.shape[1] - kernel_size)//stride + 1)
    kernel_size = (kernel_size, kernel_size)
    A_w = as_strided(A, shape = output_shape + kernel_size,
                        strides = (stride*A.strides[0],
                                   stride*A.strides[1]) + A.strides)
    A_w = A_w.reshape(-1, *kernel_size)

    # Return the result of pooling
    if pool_mode == 'max':
        return A_w.max(axis=(1,2)).reshape(output_shape)
    elif pool_mode == 'avg':
        return A_w.mean(axis=(1,2)).reshape(output_shape)

desktop = 'C:/Users/fang/Desktop/'

num = cv2.imread(desktop + '4.bmp', -1)
print(np.shape(num))

kernel1 = np.array([[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]])

kernel2 = np.array([[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]])

res1 = cv2.filter2D(num, -1, kernel1)
res2 = cv2.filter2D(num, -1, kernel2)

res30 = pool2d(num[:, :, 0], kernel_size=2, stride=2, padding=0, pool_mode='max')
res31 = pool2d(num[:, :, 1], kernel_size=2, stride=2, padding=0, pool_mode='max')
res32 = pool2d(num[:, :, 2], kernel_size=2, stride=2, padding=0, pool_mode='max')
res33 = pool2d(num[:, :, 3], kernel_size=2, stride=2, padding=0, pool_mode='max')

cv2.imwrite(desktop + "1.bmp", res1)
cv2.imwrite(desktop + "2.bmp", res2)
cv2.imwrite(desktop + "3.bmp", cv2.merge([res30, res31, res32, res33]))

cv2.imshow("1", res1)
cv2.imshow("2", res2)
cv2.imshow("3", cv2.merge([res30, res31, res32, res33]))
cv2.waitKey(0)
