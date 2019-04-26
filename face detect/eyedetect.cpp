// skindetect.cpp : 定义控制台应用程序的入口点。
//

#include <opencv2\core.hpp>
//OpenCV图形处理头文件
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\highgui\highgui_c.h>
#include <opencv2\imgproc\types_c.h>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <vector>
#pragma comment(lib,"opencv_world410d.lib")

using namespace std;
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

int cvSkinYUV(IplImage* src, IplImage* dst)
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
	int beginh = INT32_MAX;

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
				if (beginh == INT32_MAX) {
					beginh = h;
				}
				
				memcpy(pdst, psrc, 3);
			}
			pycrcb += 3;
			psrc += 3;
			pdst += 3;
		}
	}
	return beginh;
	//cvCopyImage(dst,_dst);  
	//cvReleaseImage(&dst);  
}

int sobel(IplImage* src, IplImage* dst) {
	int l = src->width / 100 * 2 + 1;
	int border = l / 2;
	vector<int> gray;
	vector<int> Scale;
	for (int i = 0; i < l / 2; i++) {
		Scale.push_back(-1);
	}
	Scale.push_back(0);
	for (int i = 0; i < l / 2; i++) {
		Scale.push_back(1);
	}
	int sumsum = 0;
	for (int h = 0; h < src->height / 2; h++)
	{
		sumsum = 0;
		unsigned char* psrc = (unsigned char*)src->imageData + h*src->widthStep;
		unsigned char* pdst = (unsigned char*)dst->imageData + h*dst->widthStep;
		for (int w = border; w<src->width - border; w++)
		{
			
			psrc += border;
			pdst += border;
			int sum = 0;
			for (int k = -border; k <= border; k++)
			{
				sum += Scale[border + k] * psrc[w + k];
			}
			if (sum < 0) {
				sum = 0;
			}
			else if (sum > 255) {
				sum = 255;
			}
			sumsum += sum;
			//cout << sum << endl;
			//memcpy(pdst, psrc, 1);
			psrc += 1;
			pdst += 1;
		}
		gray.push_back(sumsum);
	}
	vector<int>::iterator biggest = std::max_element(gray.begin(), gray.end());
	int eyepos = std::distance(gray.begin(), biggest);
	cout << eyepos << endl;
	return eyepos;
}
//YUV最好
int main()
{
	cv::Mat img1 = cv::imread("./test3.jpg"); //随便放一张jpg图片在D盘或另行设置目录  
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


	int beginh = cvSkinYUV(img, dstRGB);
	//std::cout << beginh << std::endl;

	/*cv::Mat M = cv::cvarrToMat(dstRGB);
	cv::Mat graytmp;

	cv::cvtColor(M, graytmp, CV_BGR2GRAY);

	IplImage* grayresult = &IplImage(graytmp);*/

	IplImage* grayresult = cvCreateImage(size, 8, 1);
	cvCvtColor(dstRGB, grayresult, CV_BGR2GRAY);
	IplImage* sobelresult = cvCreateImage(size, 8, 1);
	int eyeheight = sobel(grayresult, sobelresult);

	/*vector<int> gray;
	for (int i = beginh; i < grayresult->height / 2; i++) {
		int count = 0;
		unsigned char* pgray = (unsigned char*)grayresult->imageData + i*grayresult->widthStep;
		for (int j = 0; j < grayresult->width; j++) {
			count += pgray[0];
			
			pgray += 1;
		}

		gray.push_back(count);
	}

	vector<int>::iterator biggest = std::max_element(gray.begin(), gray.end());
	int eyepos = std::distance(gray.begin(), biggest);
	cout << eyepos << endl;*/
	cv::Point p1(0,eyeheight);
	cv::Point p2(dstRGB->width - 1, eyeheight);
	cv::Mat M = cv::cvarrToMat(dstRGB);
	cv::line(M, p1, p2, cv::Scalar(33, 33, 133), 2);
	IplImage* result = &IplImage(M);

	cv::namedWindow("SkinRGB", CV_WINDOW_AUTOSIZE);
	cvShowImage("SkinRGB", result);
	

	cvWaitKey(0);
	return 0;
}