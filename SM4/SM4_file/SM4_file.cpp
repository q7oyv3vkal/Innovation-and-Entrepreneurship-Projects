#include "SM4.h" //头文件
using namespace std;

int main()
{
	uint32_t key[4] = {
	   0x01234567,0x89abcdef,
	   0xfedcba98,0x76543210
	};
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&BegainTime);
	ifstream inFile;       //创建处理文件输入的对象
	inFile.open("E:\\test.txt", ios::in);  
	if (!inFile.is_open())
	{
		cout << "文件打开失败" << endl;
		return 0;
	}
	uint32_t plain[4] = { 0,0,0,0 };
	while (inFile.peek() != EOF)
	{
		int flag = 0;
		for (int i = 0; i < 4; i++)
		{
			string temp = " ";
			for (int j = 0; j < 8; j++)
			{
				char val;
				inFile.read((char*)&val, 1);//获取文件第一个字节的内容
				if (val == ' ')
				{
					j--;
				}
				else
				{
					temp = temp + val;           //拼接
				}
				if (j == 7)
				{
					ClearAllSpace(temp);
					//string 转化成char* 再转化成uint32_t
					char* p3 = NULL;
					p3 = (char*)malloc(temp.length() * sizeof(char));
					temp.copy(p3, temp.length(), 0);
					plain[flag] = strtol(p3, NULL, 16);
					flag++;
				}
			}
		}
		SM4(plain, key);
	}
	inFile.close();
	QueryPerformanceCounter(&EndTime);
	double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
	printf("用时 %f seconds\n", time);
	return 0;
}
