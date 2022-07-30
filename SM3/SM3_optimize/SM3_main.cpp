#include "SM3_basic.h"
//#include "SM3_optimize.h"

int main()
{
	string str[2];
	str[0] = "abc";
	str[1] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";
	for (int num = 0; num < 2; num++)
	{
		LARGE_INTEGER BegainTime;
		LARGE_INTEGER EndTime;
		LARGE_INTEGER Frequency;
		QueryPerformanceFrequency(&Frequency);
		QueryPerformanceCounter(&BegainTime);
		cout << "示例 " + to_string(num + 1) + " ：输入消息为字符串: " + str[num] << endl;
		cout << endl;
		string paddingValue = padding(str[num]);
		//cout << "填充后的消息为：" << endl;
		//for (int i = 0; i < paddingValue.size() / 64; i++)
		//{
		//	for (int j = 0; j < 8; j++)
		//	{
		//		cout << paddingValue.substr(i * 64 + j * 8, 8) << "  ";
		//	}
		//	cout << endl;
		//}
		//cout << endl;
		string result = iteration(paddingValue);
		QueryPerformanceCounter(&EndTime);
		cout << "杂凑值：" << endl;
		for (int i = 0; i < 8; i++)
		{
			cout << result.substr(i * 8, 8) << "  ";
		}
		cout << endl;
		double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
		printf("用时 %f seconds\n", time);
	}
}
