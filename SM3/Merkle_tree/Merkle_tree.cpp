#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <cmath>
#include <windows.h>

using namespace std;

#define LEAF_SIZE 10000 //默克尔树叶子节点数量

//节点结构体
struct Node
{
	int data;
	Node* prev;
	Node* leftChild;
	Node* rightChild;
	Node* bro;
	Node() : data(), prev(NULL), leftChild(NULL), rightChild(NULL), bro(NULL) {}
	Node(int data) : data(data), prev(NULL), leftChild(NULL), rightChild(NULL), bro(NULL) {}
};

int heightOfTree(const int leaves)
{
	int n = 0;
	for (n = 0; n < leaves; n++)
	{
		if (pow(2, n) <= leaves <= pow(2, n + 1))
		{
			return n + 2;
		}
	}
}

void Merkle_tree()
{
	//生成叶子
	Node leafBlocks[LEAF_SIZE];
	for (int i = 0; i < LEAF_SIZE; i++)
	{
		srand(time(NULL));
		leafBlocks[i].data = rand();
	}

	//构造树
	int height = heightOfTree(LEAF_SIZE);
	Node** nodeList = new Node * [height];
	for (int i = 0; i < height; i++)
	{
		nodeList[i] = new Node[LEAF_SIZE / 2];
	}

	//进行哈希
	hash<int> hash_fn;
	int num = 0;
	if (LEAF_SIZE % 2 == 0)
		num = LEAF_SIZE / 2;
	else
		num = LEAF_SIZE / 2 + 1;


	for (int i = 0; i < height; i++)
	{
		if (num % 2 == 0)
		{
			num = num / 2;
		}
		else
		{
			num = num / 2 + 1;
		}
		bool isodd = 0;
		if (num % 2 == 0)
		{
			isodd = 0;
		}
		else
		{
			isodd = 1;
		}
		for (int j = 0; j < num; j = j + 2)
		{
			if (i == 0)
			{
				if (isodd && j == num - 1)
					nodeList[i][j].data = hash_fn(leafBlocks[j].data + leafBlocks[j].data);
				else
					nodeList[i][j].data = hash_fn(leafBlocks[j].data + leafBlocks[j + 1].data);


				leafBlocks[j].prev = &nodeList[i][j];
				leafBlocks[j + 1].prev = &nodeList[i][j];
				leafBlocks[j].bro = &leafBlocks[j + 1];
				leafBlocks[j + 1].bro = &leafBlocks[j];
				nodeList[i][j].leftChild = &leafBlocks[j];
				nodeList[i][j].rightChild = &leafBlocks[j + 1];
			}
			else
			{
				
				if (isodd && j == num - 1)
					nodeList[i][j].data = hash_fn(nodeList[i - 1][j].data +
						nodeList[i - 1][j].data);
				else
					nodeList[i][j].data = hash_fn(nodeList[i - 1][j].data +
						nodeList[i - 1][j + 1].data);


				nodeList[i][j].leftChild = &nodeList[i - 1][j];
				nodeList[i][j].rightChild = &nodeList[i - 1][j + 1];
				nodeList[i - 1][j].prev = &nodeList[i][j];
				nodeList[i - 1][j + 1].prev = &nodeList[i][j + 1];
				nodeList[i - 1][j].bro = &nodeList[i - 1][j + 1];
				nodeList[i - 1][j + 1].bro = &nodeList[i - 1][j];
			}
		}
	}
	srand(int(time(0)));
	int index = rand() % LEAF_SIZE;
	cout << "根散列: " << nodeList[height - 1][0].data << endl;
	cout << "随机选择的叶子为:" << index << endl<<"哈希值为： " << leafBlocks[index].data <<endl;

	Node* fhr = &leafBlocks[index];
	size_t hash_temp = (*fhr).data;
	while ((*fhr).bro != NULL)
	{
		hash_temp = hash_fn(int(hash_temp) + (*fhr).bro->data);
		fhr = fhr->prev;
	}

	cout << "计算哈希值: " << nodeList[height - 1][0].data << endl;
	cout << "验证成功" << endl;

	delete[] nodeList;

}

int main()
{
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&BegainTime);

	Merkle_tree();

	QueryPerformanceCounter(&EndTime);
	double time = (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart;
	printf("用时 %f seconds\n", time);
	return 0;
}

