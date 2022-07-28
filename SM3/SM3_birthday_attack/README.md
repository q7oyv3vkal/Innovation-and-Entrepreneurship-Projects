**由于我初次提交项目时代码中的注释部分较少，且格式不符合助教于7月25日在QQ群中发布的提交作业要求。因此在项目初次提交后于7月28日重新创建文件夹整理项目，并且进行修改文件夹等部分操作可能会影响github网站提交时间的认证，希望老师能理解。**

1.项目简介：使用python实现对于SM3算法简单的生日攻击

2.项目名称：SM3_birthday_attack.py

3.具体代码说明：为了追求更高的效率，本项目利用gmssl库中的相关函数实现对任意字符串加密，并对其进行生日攻击并测量攻击所需要的时间。详情请见SM3_birthday_attack.py项目中注释部分

4.运行指导：函数中为攻击前24位，如果需要修改攻击范围只需要修改代码第23行：

`test_len = 24`  

并直接运行即可得到攻击得到的内容以及所需要的时间。

4.代码运行全过程截图：

截图中，我分别对sm3进行了前8位，前16位，前24位与前30位的攻击并测量其时间，其中对前8位进行攻击时由于时间太短显示为0。攻击结果与对应时间截图如下：

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/8.png)

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/16.png)

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/24.png)

![image](https://github.com/q7oyv3vkal/Innovation-and-Entrepreneurship-Projects/blob/main/image/30.png)


5.个人具体贡献：独立完成该项目编写

