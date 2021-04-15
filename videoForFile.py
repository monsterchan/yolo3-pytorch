
import time

import cv2
import numpy as np
from PIL import Image

from yolo import YOLO

yolo = YOLO()


# capture=cv2.VideoCapture("video/input.mp4")
capture=cv2.VideoCapture("video/highway.mp4")

fps = capture.get(cv2.CAP_PROP_FPS)
size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("size:{}".format(size))

# 定义编码格式
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
VideoWriter = cv2.VideoWriter('logs/output.mp4', fourcc, fps, size)

while(capture.isOpened()):
    startTime = time.time()
    # 读取某一帧
    ref, frame = capture.read()
    print('ref:{}'.format(ref))
    if ref is False:
        break
    if ref:
        #如果读完了结束循环
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))

        # 进行检测
        frame = np.array(yolo.detect_image(frame))

        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        #保存每一帧图片
        # path = "logs/" + str(time.time()) + ".jpg"
        # print(path)
        # image = Image.fromarray(frame)
        # image.save(path)


        print("fps= %.2f"%(fps))
        frame = cv2.putText(frame,"fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

        # frame = cv2.flip(frame, 2)
        # cv2.imshow("video",frame)

        #查看frame大小
        size = (frame.shape[1], frame.shape[0])
        print('fps:{}\n size:{}\n'.format(fps, size))
        #向视频写入一帧
        VideoWriter.write(frame)

        time.sleep(25/1000)

    #调取摄像头时，使用esc进行退出
    # c= cv2.waitKey(1) & 0xff
    # if c==27:
    #     capture.release()
    #     break
capture.release()