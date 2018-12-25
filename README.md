# GetUserMsg
get repos user messages by api

## 功能介绍
- 根据项目的仓库地址（github URL 或者 SourceForge URL），获取项目的贡献者或开发者 信息

## 目录结构
GetUserMsg.py : 源代码  
GetUserMsg : 可执行程序

## 运行
1. 选项
- ‘--g’ : 输入github项目地址
- ‘--sf’ : 输入SourceForge项目地址
2. 运行命令
- ./GetUserMsg + 选项 + 项目地址   
  比如：./GetUserMsg --g https://github.com/lz4/lz4 、 ./GetUserMsg --sf https://sourceforge.net/projects/sevenzip
