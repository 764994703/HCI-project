# TensorFlow CNN 表情识别模块

基于[ZiJiaW/CNN-Face-Expression-Recognition](https://github.com/ZiJiaW/CNN-Face-Expression-Recognition)编写。

## FER.py

包含模型训练和测试。在同目录下生成训练过的表情识别模型，即saved_model.xxx文件。

## CNN_MODEL.py
包含调用表情识别模块的API。

使用方法：

```py
import CNN_MODEL as cnn
sess = cnn.Initialize()
cnn.Predict(image_pixels, sess)
sess.close()
```

其中image_pixels为48*48的灰度像素值组成的numpy数组，模型文件必须在同目录下。

## TestModel.py
对同目录下训练过的模型进行测试，输出准确率。

## face.py
调用opencv和CNN_MODEL，对摄像头图像进行人脸分割和情绪识别。
