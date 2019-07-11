# DockerMonitor
打造属于Deep Learning / Computer Vision Researcher 自己的Cluster
* [AI集群门户网站(校园网)](http://10.15.89.41:8899)
* [AI集官方文档(校园网)](http://10.15.89.41:8898)
* [讨论区](https://github.com/piaozhx/DockerMonitor/issues)

### Overview
门户网站:
![](show/show.png)

GPU监控系统:
![](show/gpu_page.png)

官方文档:
![](show/doc_page.png)




### Docker 管理相比于传统的权限管理的优势
* 环境隔离, 不需要传统模式禁止sudo来维持环境
* 每个人在container中都是root, 想干什么干什么
* 可以通过container灵活移植自己的环境
* 使用deepo 深度学习开发环境, 内置常见所有环境, 无需为装库烦恼


### 已完成功能
* 添加 / 删除计算节点权限
* 删除某个User的账户
* 节点权限情况可视化
* compute节点使用代理联网
* admin节点使用ssh -Y 打开远程窗口
* 使用markdown维护doc与index页面
* 简单的管理页面
* 讨论区
* 使用文档
* 科学上网


### 未完成功能
* 创建临时用户并到期自动删除
* 两个人共用一个home目录
* 加入课题组功能


### Feature Request
* 在container中配置opengl可视化环境