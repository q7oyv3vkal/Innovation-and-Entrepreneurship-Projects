**由于我初次提交项目时代码中的注释部分较少，且格式不符合助教于7月25日在QQ群中发布的提交作业要求。因此在项目初次提交后于7月28日重新创建文件夹整理项目，并且进行修改文件夹等部分操作可能会影响github网站提交时间的认证，希望老师能理解。**

1.项目简介：使用python实现对于SM3算法的长度扩展攻击

2.项目名称：

SM3_length_extention_attack.py（长度扩展攻击核心代码）

Mysm3.py（修改gmssl库中部分函数方便进行长度扩展攻击）

3.具体代码说明：

为了追求更高的效率，本项目修改了gmssl库中的相关函数实现对任意字符串加密，并对其进行长度扩展攻击并测量攻击所需要的时间。

实验的主要思想为计算SM3(IV, salt+data+padding+append)与SM3(SM3(IV, salt+data), append)是否相等，如果相等则可以证明长度扩展攻击成功。

在这个过程中首先需要对明文进行填充，随后将填充过后的明文进行分块运算，并对其进行加密。
那么如果攻击者知道SM3(salt+data)的值并可控制data的值，攻击者可以设定data为与data+padding+append等长的任意字符串，
然后计算SM3(str+append)。因为加密过程需要先填充再运算，攻击者可以在程序计算append所在块之前，将SM3(salt+data)的值直接替换掉初始的链变量，
就能够算出SM3(salt+data+padding+append)的值了。设SM3(CV,data)表示以链变量CV计算data的SM3值，也就是计算SM3(IV, salt+data+padding+append)与SM3(SM3(IV, salt+data), append)是否相等


详情请见SM3_length_extention_attack.py项目中注释部分

4.运行指导：本次实验中，我将附加消息定为“202000460066”，即是我的学号，如果需要修改只需要修改项目第13行对应的参数即可

`append_m = "202000460066"`  

随后直接运行，可以根据提示过程参数，能否攻击成功以及所需时间。

4.代码运行全过程截图：

附加消息为”202000460066“。直接运行即可得到随机生成的消息、消息长度、添加的附加消息、加入附加消息后的消息的hash值，以及生成的indeed消息以及其哈希函数，并且测算是否能够攻击成功并得到所需总时间。

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/SM3_length.png)


5.个人具体贡献：独立完成该项目编写

