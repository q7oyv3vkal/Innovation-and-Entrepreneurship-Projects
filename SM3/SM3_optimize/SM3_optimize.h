#pragma once
#include <iostream>
#include <string>
#include <cmath>
#include <windows.h>
#include<immintrin.h> //simd
#pragma GCC optimize(2)
using namespace std;


string BinToHex(string str)
{
	string hex = "";
	int temp = 0;
	while (str.size() % 4 != 0)  //Converts a binary number length to a multiple of 4
	{
		str = "0" + str;     //Add 0 to the highest digit until it's a multiple of length 4
	}
	for (int i = 0; i < str.size(); i += 4)
	{
		temp = (str[i] - '0') * 8 + (str[i + 1] - '0') * 4 + (str[i + 2] - '0') * 2 + (str[i + 3] - '0') * 1;
		if (temp < 10)
			hex += to_string(temp);
		else
			hex += 'A' + (temp - 10);
	}
	return hex;
}

string HexToBin(string str)
{
	string table[16] = { "0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111" };
	//循环展开，内存调用
	for (int i = 0; i < str.size(); i+=2)
	{
		char temp = str[i];
		char temp1 = str[i + 1];
		if (temp >= 'A' && temp <= 'F')
			bin += table[temp - 'A' + 10];
		else
			bin += table[temp - '0'];
		if (temp1 >= 'A' && temp1 <= 'F')
			bin += table[temp1 - 'A' + 10];
		else
			bin += table[temp1 - '0'];
	}
	return bin;
}

int BinToDec(string str)
{
	int dec = 0;
	int temp1 = 0;
	int temp2 = 0;
	//循环展开
	for (int i = 0; i < str.size(); i+=2)
	{
		temp1 += (str[i] - '0') * pow(2, str.size() - i - 1);
		temp2 += (str[i + 1] - '0') * pow(2, str.size() - i);
	}
	dec = temp1 + temp2;
	return dec;
}

string DecToBin(int str)
{
	string bin = "";
	while (str >= 1)
	{
		bin = to_string(str % 2) + bin;
		str = str / 2;
	}
	return bin;
}

int HexToDec(string str)
{
	int dec = 0;
	//循环展开+内存调用
	for (int i = 0; i < str.size(); i+=2)
	{
		char temp = str[i];
		char temp1 = str[i + 1];
		if (str[i] >= 'A' && str[i] <= 'F')
			dec += (temp - 'A' + 10) * pow(16, str.size() - i - 1);
		else
			dec += (temp - '0') * pow(16, str.size() - i - 1);
		if (str[i] >= 'A' && str[i] <= 'F')
			dec += (temp1 - 'A' + 10) * pow(16, str.size() - i);
		else
			dec += (temp1 - '0') * pow(16, str.size() - i);
	}
	return dec;
}

string DecToHex(int str)
{
	string hex = "";
	int temp = 0;
	while (str >= 1)
	{
		temp = str % 16;
		if (temp < 10 && temp >= 0)
			hex = to_string(temp) + hex;
		else
			hex += ('A' + (temp - 10));
		str = str / 16;
	}
	return hex;
}

//Fill in the data
string padding(string str)
{
	string res = "";
	for (int i = 0; i < str.size(); i++)
	{
		res += DecToHex((int)str[i]);
	}
	//cout << "输入消息的ASCII码为：" << endl;
	////内存调用
	//int temp = res.size();
	//for (int i = 0; i < temp; i++)
	//{
	//	cout << res[i];
	//	if ((i + 1) % 8 == 0)
	//		cout << "  ";
	//	if ((i + 1) % 64 == 0 || (i + 1) == res.size())
	//		cout << endl;
	//}
	//cout << endl;
	int res_length = res.size() * 4;       //The length of the string is in bin
	res += "8"; //hex：+8
	//内存调用
	int temp1 = res.size() % 128;
	while (temp1 != 112)
	{
		res += "0";
	}
	string res_len = DecToHex(res_length); //The length of string
	//内存调用
	int temp2 = res_len.size();
	while (temp2 != 16)
	{
		res_len = "0" + res_len;
	}
	res += res_len;
	return res;
}

//Cyclic shift to the left
string LeftShift(string str, int len)
{
	string res = HexToBin(str);
	res = res.substr(len) + res.substr(0, len);
	return BinToHex(res);
}

string XOR(string str1, string str2)
{
	string res1 = HexToBin(str1);
	string res2 = HexToBin(str2);
	string res = "";
	//内存调用
	int temp = res1.size();
	for (int i = 0; i < temp; i++)
	{
		if (res1[i] == res2[i])
			res += "0";
		else
			res += "1";
	}
	return BinToHex(res);
}

string AND(string str1, string str2)
{
	string res1 = HexToBin(str1);
	string res2 = HexToBin(str2);
	string res = "";
	//内存调用
	int temp = res1.size();
	for (int i = 0; i < temp; i++)
	{
		if (res1[i] == '1' && res2[i] == '1')
			res += "1";
		else
			res += "0";
	}
	return BinToHex(res);
}

string OR(string str1, string str2)
{
	string res1 = HexToBin(str1);
	string res2 = HexToBin(str2);
	string res = "";
	//内存调用
	int temp = res1.size();
	for (int i = 0; i < temp; i++)
	{
		if (res1[i] == '0' && res2[i] == '0')
			res += "0";
		else
			res += "1";
	}
	return BinToHex(res);
}

string NOT(string str)
{
	string res1 = HexToBin(str);
	string res = "";
	//内存调用
	int temp = res1.size();
	for (int i = 0; i < temp; i++)
	{
		if (res1[i] == '0')
			res += "1";
		else
			res += "0";
	}
	return BinToHex(res);
}

//Xor bit by bit
char binXor(char str1, char str2)
{
	return str1 == str2 ? '0' : '1';
}

//And bit by bit
char binAnd(char str1, char str2)
{
	return (str1 == '1' && str2 == '1') ? '1' : '0';
}

//mod 2^32
string ModAdd(string str1, string str2)
{
	string res1 = HexToBin(str1);
	string res2 = HexToBin(str2);
	char temp = '0';
	string res = "";
	//内存调用
	int i = res1.size() - 1;
	for (i; i >= 0; i--)
	{
		res = binXor(binXor(res1[i], res2[i]), temp) + res;
		if (binAnd(res1[i], res2[i]) == '1')
			temp = '1';
		else {
			if (binXor(res1[i], res2[i]) == '1')
				temp = binAnd('1', temp);
			else
				temp = '0';
		}
	}
	return BinToHex(res);
}

string P1(string str)
{
	return XOR(XOR(str, LeftShift(str, 15)), LeftShift(str, 23));
}

string P0(string str)
{
	return XOR(XOR(str, LeftShift(str, 9)), LeftShift(str, 17));
}

string T(int j)
{
	if (0 <= j && j <= 15)
		return "79CC4519";
	else
		return "7A879D8A";
}

string FF(string str1, string str2, string str3, int j)
{
	if (0 <= j && j <= 15)
		return XOR(XOR(str1, str2), str3);
	else
		return OR(OR(AND(str1, str2), AND(str1, str3)), AND(str2, str3));
}

string GG(string str1, string str2, string str3, int j)
{
	if (0 <= j && j <= 15)
		return XOR(XOR(str1, str2), str3);
	else
		return OR(AND(str1, str2), AND(NOT(str1), str3));
}

//Message spread
string extension(string str)
{
	string res = str;
	//循环展开
	for (int i = 16; i < 68; i+=2)   //16-68
	{
		res += XOR(XOR(P1(XOR(XOR(res.substr((i - 16) * 8, 8), res.substr((i - 9) * 8, 8)), LeftShift(res.substr((i - 3) * 8, 8), 15))), LeftShift(res.substr((i - 13) * 8, 8), 7)), res.substr((i - 6) * 8, 8));
		res += XOR(XOR(P1(XOR(XOR(res.substr((i - 15) * 8, 8), res.substr((i - 8) * 8, 8)), LeftShift(res.substr((i - 2) * 8, 8), 15))), LeftShift(res.substr((i - 12) * 8, 8), 7)), res.substr((i - 5) * 8, 8));
	}
	//cout << "The extended message is：" << endl;
	//cout << "W0,W1,……,W67：" << endl;
	//for (int i = 0; i < 8; i++)
	//{
	//	for (int j = 0; j < 8; j++)
	//	{
	//		cout << res.substr(i * 64 + j * 8, 8) << "  ";
	//	}
	//	cout << endl;
	//}
	//cout << res.substr(512, 8) << "  " << res.substr(520, 8) << "  " << res.substr(528, 8) << "  " << res.substr(536, 8) << endl;
	//cout << endl;
	for (int i = 0; i < 64; i++)         //W'
	{
		res += XOR(res.substr(i * 8, 8), res.substr((i + 4) * 8, 8));
	}
	//cout << "W0',W1',……,W63'" << endl;
	//for (int i = 0; i < 8; i++)
	//{
	//	for (int j = 0; j < 8; j++)
	//	{
	//		cout << res.substr(544 + i * 64 + j * 8, 8) << "  ";
	//	}
	//	cout << endl;
	//}
	//cout << endl;
	return res;
}

//Message compression
string compress(string str1, string str2)
{
	string IV = str2;
	string A = IV.substr(0, 8), B = IV.substr(8, 8), C = IV.substr(16, 8), D = IV.substr(24, 8), E = IV.substr(32, 8), F = IV.substr(40, 8), G = IV.substr(48, 8), H = IV.substr(56, 8);
	string SS1 = "", SS2 = "", TT1 = "", TT2 = "";
	//cout << "Intermediate value of iterative compression: " << endl;
	//cout << "    A         B         C         D         E         F        G         H " << endl;
	//cout << A << "  " << B << "  " << C << "  " << D << "  " << E << "  " << F << "  " << G << "  " << H << endl;
	for (int j = 0; j < 64; j++)
	{
		SS1 = LeftShift(ModAdd(ModAdd(LeftShift(A, 12), E), LeftShift(T(j), (j % 32))), 7);
		SS2 = XOR(SS1, LeftShift(A, 12));
		TT1 = ModAdd(ModAdd(ModAdd(FF(A, B, C, j), D), SS2), str1.substr((j + 68) * 8, 8));
		TT2 = ModAdd(ModAdd(ModAdd(GG(E, F, G, j), H), SS1), str1.substr(j * 8, 8));
		D = C;
		C = LeftShift(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = LeftShift(F, 19);
		F = E;
		E = P0(TT2);
		//cout << A << "  " << B << "  " << C << "  " << D << "  " << E << "  " << F << "  " << G << "  " << H << endl;
	}
	string res = (A + B + C + D + E + F + G + H);
	//cout << endl;
	return res;
}

//Iterative compression function
string iteration(string str)
{
	int num = str.size() / 128;
	//cout << "Number of packets after message filling：" << to_string(num) << endl;
	//cout << endl;
	string V = "7380166F4914B2B9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E";
	string B = "", extensionB = "", compressB = "";
	for (int i = 0; i < num; i++)
	{
		//cout << "Group number " << to_string(i + 1) << endl;
		B = str.substr(i * 128, 128);
		extensionB = extension(B);
		compressB = compress(extensionB, V);
		V = XOR(V, compressB);
	}
	return V;
}
