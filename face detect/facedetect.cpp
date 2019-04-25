// skindetect.cpp : 定义控制台应用程序的入口点。
//

#include <opencv2\core.hpp>
//OpenCV图形处理头文件
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\highgui\highgui_c.h>
#include <opencv2\imgproc\types_c.h>
#include <opencv2/imgproc.hpp>
#include <iostream>
#pragma comment(lib,"opencv_world410d.lib")
void SkinRGB(IplImage* rgb, IplImage* _dst);

void cvThresholdOtsu(IplImage* src, IplImage* dst)
{
	int height = src->height;
	int width = src->width;

	//histogram  
	float histogram[256] = { 0 };
	for (int i = 0; i<height; i++)
	{
		unsigned char* p = (unsigned char*)src->imageData + src->widthStep*i;
		for (int j = 0; j<width; j++)
		{
			histogram[*p++]++;
		}
	}
	//normalize histogram  
	int size = height*width;
	for (int i = 0; i<256; i++)
	{
		histogram[i] = histogram[i] / size;
	}

	//average pixel value  
	float avgValue = 0;
	for (int i = 0; i<256; i++)
	{
		avgValue += i*histogram[i];
	}

	int threshold;
	float maxVariance = 0;
	float w = 0, u = 0;
	for (int i = 0; i<256; i++)
	{
		w += histogram[i];
		u += i*histogram[i];

		float t = avgValue*w - u;
		float variance = t*t / (w*(1 - w));
		if (variance>maxVariance)
		{
			maxVariance = variance;
			threshold = i;
		}
	}

	cvThreshold(src, dst, threshold, 255, CV_THRESH_BINARY);
}

void cvSkinOtsu(IplImage* src, IplImage* dst)//yCbCr  
{
	assert(dst->nChannels == 1 && src->nChannels == 3);
	CvSize size = cvSize((*src).width, (*src).height);

	IplImage* ycrcb = cvCreateImage(size, 8, 3);
	IplImage* cr = cvCreateImage(size, 8, 1);
	cvCvtColor(src, ycrcb, CV_BGR2YCrCb);
	cvSplit(ycrcb, 0, cr, 0, 0);

	cvThresholdOtsu(cr, cr);
	cvCopy(cr, dst);
	cvReleaseImage(&cr);
	cvReleaseImage(&ycrcb);
}



void SkinRGB(IplImage* rgb, IplImage* _dst)
{
	assert(rgb->nChannels == 3 && _dst->nChannels == 3);

	static const int R = 2;
	static const int G = 1;
	static const int B = 0;
	CvSize size = cvSize((*_dst).width, (*_dst).height);
	IplImage* dst = cvCreateImage(size, 8, 3);
	cvZero(dst);

	for (int h = 0; h<rgb->height; h++)
	{
		unsigned char* prgb = (unsigned char*)rgb->imageData + h*rgb->widthStep;
		unsigned char* pdst = (unsigned char*)dst->imageData + h*dst->widthStep;
		for (int w = 0; w<rgb->width; w++)
		{
			if ((prgb[R]>95 && prgb[G]>40 && prgb[B]>20 &&
				prgb[R] - prgb[B]>15 && prgb[R] - prgb[G]>15) ||//uniform illumination  
				(prgb[R]>200 && prgb[G]>210 && prgb[B]>170 &&
					abs(prgb[R] - prgb[B]) <= 15 && prgb[R]>prgb[B] && prgb[G]>prgb[B])//lateral illumination  
				)
			{
				memcpy(pdst, prgb, 3);
			}
			prgb += 3;
			pdst += 3;
		}
	}
	cvCopy(dst, _dst);

	cvReleaseImage(&dst);
}

void cvSkinYUV(IplImage* src, IplImage* dst)
{
	CvSize size = cvSize((*src).width, (*src).height);
	IplImage* ycrcb = cvCreateImage(size, 8, 3);
	//IplImage* cr=cvCreateImage(cvGetSize(src),8,1);  
	//IplImage* cb=cvCreateImage(cvGetSize(src),8,1);  
	cvCvtColor(src, ycrcb, CV_BGR2YCrCb);
	//cvSplit(ycrcb,0,cr,cb,0);  

	static const int Cb = 2;
	static const int Cr = 1;
	static const int Y = 0;

	//IplImage* dst=cvCreateImage(cvGetSize(_dst),8,3);  
	cvZero(dst);

	for (int h = 0; h<src->height; h++)
	{
		unsigned char* pycrcb = (unsigned char*)ycrcb->imageData + h*ycrcb->widthStep;
		unsigned char* psrc = (unsigned char*)src->imageData + h*src->widthStep;
		unsigned char* pdst = (unsigned char*)dst->imageData + h*dst->widthStep;
		for (int w = 0; w<src->width; w++)
		{
			if (pycrcb[Cr] >= 133 && pycrcb[Cr] <= 183 && pycrcb[Cb] >= 77 && pycrcb[Cb] <= 127)        // origin second 173
			{
				memcpy(pdst, psrc, 3);
			}
			pycrcb += 3;
			psrc += 3;
			pdst += 3;
		}
	}
	//cvCopyImage(dst,_dst);  
	//cvReleaseImage(&dst);  
}


//YUV最好
int main()
{
	cv::Mat img1 = cv::imread("./original.jpg"); //随便放一张jpg图片在D盘或另行设置目录  
	IplImage img2 = img1;
	IplImage* img = &img2;
	CvSize size = cvSize((*img).width, (*img).height);
	IplImage* dstRGB = cvCreateImage(size, 8, 3);
	//IplImage* dst_crotsu = cvCreateImage(size, 8, 1);
	//SkinRGB(img, dstRGB);
	/*int i = 0;
	while (i < 100) {                         // 100times in 2 seconds
		cvSkinYUV(img, dstRGB);
		i++;
	}*/


	cvSkinYUV(img, dstRGB);

	cv::Mat M = cv::cvarrToMat(dstRGB);
	cv::Mat graytmp;

	cv::cvtColor(M, graytmp, CV_BGR2GRAY);

	IplImage* grayresult = &IplImage(graytmp);

	cv::namedWindow("SkinRGB", CV_WINDOW_AUTOSIZE);
	cvShowImage("SkinRGB", grayresult);
	
	cvWaitKey(0);
	return 0;
}