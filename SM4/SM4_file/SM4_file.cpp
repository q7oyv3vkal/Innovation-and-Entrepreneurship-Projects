#include "SM4.h"//头文件
#include <stdio.h>
#include <string.h>
#include <stdint.h>
using namespace std;



void dump_buf_32(uint32_t* buf, uint32_t len)
{
	int i;
	printf(":");

	for (i = 0; i < len; i++) {
		printf("%s%02x%s", i % 16 == 0 ? "\r\n\t" : " ",
			buf[i],
			i == len - 1 ? "\r\n" : "");
	}
}

uint32_t move(uint32_t data, int length)		//移位运算
{
	uint32_t result = 0;
	result = (data << length) ^ (data >> (32 - length));
	return result;
}


uint32_t T(uint32_t input)		//T置换
{
	uint8_t b[4] = { input >> 24,input >> 16,input >> 8,input };
	for (int i = 0; i < 4; i++)
	{
		b[i] = s_box[(int)b[i]];
	}
	uint32_t c = (b[0] << 24) ^ (b[1] << 16) ^ (b[2] << 8) ^ b[3];
	c = c ^ move(c, 2) ^ move(c, 10) ^ move(c, 18) ^ move(c, 24);
	return c;
}

void T_1(uint32_t input[4], uint32_t rk[32])		//T'置换
{
	uint32_t k[50];
	for (int i = 0; i < 4; i++)
	{
		k[i] = input[i] ^ fk[i];
	}

	for (int i = 0; i < 32; i++)
	{
		uint32_t t = k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ ck[i];
		uint8_t b[4] = { t >> 24,t >> 16,t >> 8,t };
		for (int i = 0; i < 4; i++)
		{
			b[i] = s_box[(int)b[i]];
		}
		t = (b[0] << 24) ^ (b[1] << 16) ^ (b[2] << 8) ^ b[3];
		t = t ^ move(t, 13) ^ move(t, 23);
		rk[i] = k[i] ^ t;
		k[i + 4] = rk[i];

	}
}

void F(uint32_t input[4], uint32_t rk, uint32_t output[4])	//轮函数
{
	output[0] = input[1];
	output[1] = input[2];
	output[2] = input[3];
	output[3] = input[0] ^ T(input[1] ^ input[2] ^ input[3] ^ rk);
}



void SM4(uint32_t plain[4], uint32_t key[4])
{
	uint32_t output[4];
	uint32_t result[4];
	uint32_t rk[32];
	uint32_t temp[4];
	T_1(key, rk);
	F(plain, rk[0], output);
	for (int i = 1; i < 32; i++)
	{
		for (int i = 0; i < 4; i++)
		{
			temp[i] = output[i];
		}
		F(temp, rk[i], output);
	}
	result[0] = output[3];
	result[1] = output[2];
	result[2] = output[1];
	result[3] = output[0];
	dump_buf_32(result, 4);
}


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
	ifstream inFile; //创建处理文件输入的对象
	inFile.open("C:\\test.txt", ios::in);
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
					//ClearAllSpace(temp);
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
