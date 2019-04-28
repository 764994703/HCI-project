#include <iostream>
#include <vector>
#include<algorithm>
using namespace std;

//get the average of open eyes
int debug = 1;

int findaverage(vector<float> input) {
	sort(input.begin(), input.end());
	return input[input.size() / 2];
}

float linearinter(float average, float persent, float now, float last, int i) {
	float result;
	result = (average * persent - last) / (now - last) + i - 1;
	return result;
}
int perclos(vector<float> input) {
	if (debug) {
		input = { 20,20,20,20,20,5,4,2,1,4,5,20,20,20,20,20,4,2,2,20 };
	}
	int average = findaverage(input);
	int flag = INT_MAX;
	int border = 20;       // avoid begin at eyes closing and at the begin of vector
	int i = border;
	for (; i < input.size(); i++) {
		if (input[i] < average * 0.8) {
			flag = i;
			break;
		}
	}
	if (flag == INT_MAX) {
		return -1;         //-1 : no close eyes in this piece of time
	}
	float timepoint1, timepoint2, timepoint3, timepoint4;
	timepoint1 = linearinter(average, 0.8, input[i], input[i - 1], i);
	for (; i < input.size(); i++) {
		if (input[i] < average * 0.2) {
			flag = i;
			break;
		}
	}
	timepoint2 = linearinter(average, 0.2, input[i], input[i - 1], i);
	for (; i < input.size(); i++) {
		if (input[i] > average * 0.2) {
			flag = i;
			break;
		}
	}
	timepoint3 = linearinter(average, 0.2, input[i], input[i - 1], i);
	for (; i < input.size(); i++) {
		if (input[i] > average * 0.8) {
			flag = i;
			break;
		}
	}
	timepoint4 = linearinter(average, 0.8, input[i], input[i - 1], i);
	float result = (timepoint3 - timepoint2) / (timepoint4 - timepoint1);
	if (result > 0.15) {
		return 1;                      //1 : tiring
	}
	else {
		return 0;                      //0 : not tiring
	}
}