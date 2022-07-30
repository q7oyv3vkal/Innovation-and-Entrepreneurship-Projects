**由于我初次提交项目时代码中的注释部分较少，且格式不符合助教于7月25日在QQ群中发布的提交作业要求。因此在项目初次提交后于7月30日重新创建文件夹整理项目，并且进行修改文件夹等部分操作可能会影响github网站提交时间的认证，希望老师能理解。**

1.项目简介：使用c++实现初始SM3，并使用软件方法进行优化，提升运行速度

2.项目名称：

SM3_main.cpp（测试文件）

SM3_basic.h（初始的实现SM3的文件，用于加速对照）

SM3_optimize.h（代码实现加速后的文件）

3.具体代码说明：

实验在使用SM3进行基础加密的基础上，通过消除不必要的函数调用与内存调用，使用循环展开，SIMD等方式对项目进行软件加速，实现目的。

对于消除不必要的函数调用与内存调用，除不必要的工作（函数调用、条件测试、内存引用）和利用处理
器提供的指令级并行。大多数编译器已经实现了通过优化级别的选择来实现不同程度的
性能提升，但是对于内存别名使用、修改全局程序状态的函数调用等操作，编译器很难
做出进一步的优化。没有任何编译器能用一个好的算法或数据结构代替低效率的算法或
数据结构，因此，编写使编译器能高效的产生代码的程序极具意义。

例如可以将

`for (int i = 0; i < str.size(); i++)`

`{`

`	if (str[i] >= 'A' && str[i] <= 'F')`

`		bin += table[str[i] - 'A' + 10];`

`	else`

`		bin += table[str[i] - '0'];`

`}`

修改为

`for (int i = 0; i < str.size(); i++)`

`{`

`	char temp = str[i];`

`	if (temp >= 'A' && temp <= 'F')`

`		bin += table[temp - 'A' + 10];`

`	else`

`		bin += table[temp - '0'];`

`}`
  
  
 即将str[i]在进入if循环语句之前首先修改为temp，并且将'A'与'F'分别赋值，减小内存调用从而提高效率。

对于循环展开，它可以从两方面提高程序的性能，分别是减少无助于程序结果的操作的数量（循环索
引计算、条件分支等），提供一些进一步变化代码的方法、减少计算中关键路径（提供
程序所需周期数的下界）上的操作数量。

例如

`for (int i = 0; i < str.size(); i++)`

`{`

`	if (str[i] >= 'A' && str[i] <= 'F')`

`		bin += table[str[i] - 'A' + 10];`

`	else`

`		bin += table[str[i] - '0'];`

`}`

可以修改为

`for (int i = 0; i < str.size(); i+=2)`

`{`

`	char temp = str[i];`

`	char temp1 = str[i + 1];`

`	if (temp >= 'A' && temp <= 'F')`

`		bin += table[temp - 'A' + 10];`

`	else`

`		bin += table[temp - '0'];`

`	if (temp1 >= 'A' && temp1 <= 'F')`

`		bin += table[temp1 - 'A' + 10];`

`	else`

`		bin += table[temp1 - '0'];`

`}`

对于SIMD 指令集，一个寄存器可以储存多个过程变量，从而实现加速。

4.运行指导：本次实验中，只需要修改SM3_main.cpp文件中的第一行，
修改需要引用的头文件即可。对于验证函数，
本项目分别对“abc”以及"abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
进行加密验证，如果需要修改相应的验证内容，只需要修改SM3_main.cpp文件中第7行与第8行即可：

`	str[0] = "abc";`  
`	str[1] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";`  


4.代码运行全过程截图：

首先验证能否加密：

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/SM3_chushi.png)

由于单次运行时间较短，在测量时间时重复加密20次进行测量：
进行基础加密时的截图为：

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/SM3_opbasic.png)

对SM3进行软件加速后加密的截图为：

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/SM3_opop.png)

5.个人具体贡献：独立完成该项目编写
