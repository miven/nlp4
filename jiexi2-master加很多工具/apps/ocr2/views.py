from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.
class PolicyExtractorService(View):
    '''
    扫描营业执照

    '''
    def get(self, request):

        return HttpResponse("GET request from PolicyExtractorService")

    def post(self, request):

        '''
        首先导入一个图片的地址.

        :param request:
        :return:
        '''
        # 首先是pic地址
        pic = request.POST.get('url')  # POST必须大写
        import pytesseract
        import cv2
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use("Agg")
        import dlib#这个windows装很麻烦,需要cmake ,linux直接pip
        import matplotlib.patches as mpatches
        from skimage import io, draw, transform, color #    pip install scikit_image来安装
        import numpy as np
        import pandas as pd
        import re

        pic=cv2.imread(pic,0)#后面加0表示变成1个通道的灰度图.

        '''
        cv2
        里面几个重要函数:
        1.cv2.imread(pic,0)
        2.
        '''









        # gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)  # 灰度处理
        # cv2.imshow('gray', gray)
        #先做二值,加强了鲁棒性. 表示超过50亮度的都算作255.也就是只有足够黑的点才算做字体.

        retval, imagebin = cv2.threshold(pic, 30, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
        ## 将照片去除

        img_bilateralFilter = cv2.bilateralFilter(imagebin, 40, 100, 100)  # 高斯双边滤波

        text = pytesseract.image_to_string(img_bilateralFilter, lang='chi_sim')

        #还是ocr框架识别率不行.

        #opencv文档
        #http://www.opencv.org.cn/opencvdoc/2.3.2/html/search.html?q=imread&check_keywords=yes&area=default










        return HttpResponse("POST request from PolicyExtractorService")










        detector = dlib.get_frontal_face_detector()
        #dlib :https://www.cnblogs.com/as3asddd/p/7257820.html
        # image = io.imread(pic)

        # help(detector)
        # 下面一行的2是一个上采样参数,表示把图片先放大多少倍.越大图片越精细.图片输入过小就需要上采样放大细节.
        # dets = detector(image, 2)  # 使用detector进行人脸检测 dets为返回的结果



        image = cv2.imread(pic)
        dets = detector(image, 2)  # 使用detector进行人脸检测 dets为返回的结果

        for i, face in enumerate(dets):
            # 在图片中标注人脸，并显示
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()
            cv2.rectangle(image, (left, bottom), (right, top), (0, 255, 0), 2)#把矩形画到image这个图片参数上.
            # rect = mpatches.Rectangle((left, bottom), right - left, top - bottom,
            #                           fill=False, edgecolor='red', linewidth=1)
            # rect = mpatches.Rectangle((12, 12), 25, 52,
            #                           fill=False, edgecolor='red', linewidth=1)

        '''
        画图还是认准cv2,matplotlib bug太多.
        '''


        predictor = dlib.shape_predictor("../shape_predictor_5_face_landmarks.dat")
        # 因为代码是在new目录下运行的manager所以这里是.. 表示上级目录里面找.
        # predictor = dlib.shape_predictor("/data/zb/shape_predictor_5_face_landmarks.dat")
        # http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2

        #画关键点

        detected_landmarks = predictor(image, dets[0]).parts()


        landmarks = np.array([[p.x, p.y] for p in detected_landmarks])


        for i in landmarks:
            cv2.circle(image, (i[0],i[1]),1,(0,0,255))
        cv2.imwrite('22!!!!!!!!!!.png', image)

        # '''
        # 写一个for循环,把图片进行旋转,判断,因为dlib识别不了旋转角度大的图片.
        #
        # '''
        # jiaodu=np.arange(0,360,10)

        # imgInfo = image.shape
        # height = imgInfo[0]
        # width = imgInfo[1]
        # deep = imgInfo[2]
        # cv2.imwrite("dsfasdfs.png",image)
        # for i in jiaodu:
        #     matRotate = cv2.getRotationMatrix2D((height * 0.5, width * 0.5), i, 1)  # mat rotate 1 center 2 angle 3 缩放系数
        #
        #     dst = cv2.warpAffine(image, matRotate, (height, width))
        #     #cv2输出的后缀名一定要写.
        #     cv2.imwrite(str(i)+".png",dst)




        #dlib:api http://dlib.net/

        ## 将眼睛位置可视化
        # plt.figure()
        # ax = plt.subplot(111)
        # ax.imshow(image)
        # plt.axis("off")
        # plt.plot(landmarks[0:4,0],landmarks[0:4,1],'ro')
        # for ii in np.arange(4):
        #     plt.text(landmarks[ii,0]-10,landmarks[ii,1]-15,ii)
        # plt.show()

        ## 计算眼睛的倾斜角度,逆时针角度
        import numpy as np

        #注意arctan有2个值.一个jiao一个jiao+180,需要用鼻子位置来判断.
        def twopointcor(point1, point2):
            """point1 = (x1,y1),point2 = (x2,y2)"""
            deltxy = point2 - point1
            corner = np.arctan(deltxy[1] / deltxy[0]) * 180 / np.pi
            return corner

        ## 计算多个角度求均值
        corner10 = twopointcor(landmarks[1, :], landmarks[3, :])
        corner23 = twopointcor(landmarks[1, :], landmarks[2, :])
        # corner20 = twopointcor(landmarks[2, :], landmarks[0, :])
        corner = np.mean([corner10, corner23])






        ## 计算图像的身份证倾斜的角度
        def IDcorner(landmarks):
            """landmarks:检测的人脸5个特征点
               经过测试使用第0个和第2个特征点计算角度较合适
            """
            corner20 = twopointcor(landmarks[2, :], landmarks[0, :])
            corner = np.mean([corner20])
            return corner

        corner = IDcorner(landmarks)



        ## 将照片转正
        def rotateIdcard(image):
            "image :需要处理的图像"
            ## 使用dlib.get_frontal_face_detector识别人脸
            detector = dlib.get_frontal_face_detector()
            dets = detector(image, 2)  # 使用detector进行人脸检测 dets为返回的结果
            ## 检测人脸的眼睛所在位置
            predictor = dlib.shape_predictor("../shape_predictor_5_face_landmarks.dat")
            detected_landmarks = predictor(image, dets[0]).parts()
            landmarks = np.array([[p.x, p.y] for p in detected_landmarks])
            corner = IDcorner(landmarks)
            ## 旋转后的图像
            image2 = transform.rotate(image, corner, clip=False)
            image2 = np.uint8(image2 * 255)
            ## 旋转后人脸位置
            det = detector(image2, 2)
            return image2, det

        ## 转正身份证：
        image = io.imread(pic)
        image2, dets = rotateIdcard(image)



        ## 可视化修正后的结果
        cv2.imwrite("dsfadsf.png",image2)

        # 在图片中标注人脸，并显示
        left = dets[0].left()
        top = dets[0].top()
        right = dets[0].right()
        bottom = dets[0].bottom()
        rect = mpatches.Rectangle((left, bottom), (right - left), (top - bottom),
                                  fill=False, edgecolor='red', linewidth=1)

        ## 照片的位置（不怎么精确）
        width = right - left
        high = top - bottom
        left2 = np.uint(left - 0.5 * width)
        bottom2 = np.uint(bottom + 0.5 * width)
        rect = mpatches.Rectangle((left2, bottom2), 1.8 * width, 2.2 * high,
                                  fill=False, edgecolor='blue', linewidth=1)


        ## 身份证上人的照片
        top2 = np.uint(bottom2 + 2.2 * high)  #稍微把图片放大一点,然后扣除
        right2 = np.uint(left2 + 1.8 * width)
        image3 = image2[top2:bottom2, left2:right2, :]
        import time
        cv2.imwrite("身份证扣出来的图片"+str(time.time())+".png",image3)
        # plt.imshow(image3)



        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)  # 灰度处理
        # cv2.imshow('gray', gray)
        #先做二值,加强了鲁棒性. 表示超过50亮度的都算作255.也就是只有足够黑的点才算做字体.
        retval, imagebin = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
        ## 将照片去除
        imagebin[0:bottom2, left2:-1] = 255
        img_bilateralFilter = cv2.bilateralFilter(imagebin, 40, 100, 100)  # 高斯双边滤波

        '''
        看看图片
        '''
        cv2.imwrite("剩余的"+str(time.time())+".png",img_bilateralFilter)

        text = pytesseract.image_to_string(img_bilateralFilter, lang='chi_sim')















        return HttpResponse("POST request from PolicyExtractorService")
