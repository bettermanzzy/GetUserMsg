# GetUserMsg
get repos user messages by api

## 功能介绍
根据项目的仓库地址（github URL 或者 SourceForge URL），获取项目的贡献者或开发者信息  
- github项目可获取贡献者的姓名，ID,邮箱，location,company,projects,follower,commits 信息
- SourceForge项目可获取开发者的姓名，ID, 主页url 信息

## 目录结构
1. GetUserMsg.py : 源代码  
2. GetUserMsg : 可执行程序

## 运行
1. 选项
- '-u' : 输入你的github 账号 （可选）
- '-t' : 输入你的auth token 值 (需要输入token进行认证）
- '--g' : 输入github项目地址
- '--sf' : 输入SourceForge项目地址
- '-a' : 输入all, 默认是输出30个contributors,使用该选项可输出所有contributors (可选）
- ‘-h’ : 程序help信息

2. 运行命令
- ./GetUserMsg + 选项't' + 选项'--g'/'--sf' + 项目地址   
  比如：./GetUserMsg -t tokenID --g https://github.com/lz4/lz4 、 ./GetUserMsg --sf https://sourceforge.net/projects/sevenzip
