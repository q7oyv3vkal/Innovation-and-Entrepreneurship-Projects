**由于我初次提交项目时代码中的注释部分较少，且格式不符合助教于7月25日在QQ群中发布的提交作业要求。因此在作业提交说明后进行二次修改，并且进行修改文件夹等部分操作可能会影响github网站提交时间的认证，希望老师能理解。**

1.项目简介：在CBC模式基础SM4算法的基础上使用项目加密整个文件

2.项目名称：SM4.h（相关定义）

SM4_file.cpp（主要用于读取文件完成加密）

3.具体代码说明：详情请见SM4.h与SM4_file.cpp项目中注释部分

4.运行指导：本项目中直接设定128位的密钥（key[4]）为0x01234567,0x89abcdef,0xfedcba98,0x76543210，明文则在SM4_file.cpp中的第105行中代码中：

`<inFile.open("C:\\test.txt", ios::in);>`  

修改相应路径即可。运行时直接点击进行运行就能得到加密结果与运行时间，如果要更改加密内容只需要修改代码部分内容即可。

4.代码运行全过程截图（由于本项目输出内容较多，因此只提供输出结尾部分代表“成功”与有时间的截图）：

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/Image/SM4_file.png)

5.个人具体贡献：在已有的SM4_basic项目的基础上独立完成本项目

6.其他问题：本项目并未写在ppt中，但是老师在课堂上曾经提及建议同学们实现。

本次实验中我实验使用的test.txt文件也一并上传至github中。
