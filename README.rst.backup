=========
ek_optical
=========

==========
一、开发流程
==========

后端 :

1. 新建目录virtualenvs
2. 进入virtualenvs目录下， 使用命令 Python3 -m venv ek_optical创建虚拟环境
3. source virtualenvs/ek_optical/bin/activate（此处最好给完整路径）激活虚拟环境
4. 进入 ek_optical 项目下，pip install -r requirements.txt 安装项目所需依赖
5. 通过./scripts/manage_dev.sh run 启动后端服务

前端 :

1. 进入到webapp目录下， npm install 安装所需的包
2. 通过npm run dev，启动前端服务

==========
二、部署流程
==========

1. 在webapp目录下运行npm run buildprod，将前端文件进行打包。
2. 在项目ek_optical下运行 python setup.py package ，将项目进行打包。
3. 将打包的项目文件传送到服务器端，使用scp -i wmu.pem optical-dist-0+workingcopy.tgz wmu@eyediseases.bio-data.cn:~/
4. sudo systemctl stop nginx 停止nginx代理
5. tsrunit deploy optical optical-dist-0+workingcopy.tgz 解压到optical用户下
6. tstool ek manage db upgrade 升级当前数据库。
7. tsrunit start ek disco_server 运行当前后端程序（后端部署已完成）
8. lesslog ek disco_server log查看当前后端运行日志 如需退出按q
9. sudo systemctl start nginx 启动nginx代理

=======
三、维护
=======

使用tstool optical manage populate进行项目数据库数据更新，例如: “tstool optical manage populate x19-go -f ~/update/GO/Retinitis/Retinitis.MF.txt -t Ture”；x19-go 为命令名，-f 为需要更新的文件路径，-t为是否清空原有数据表（清空则加 -t True，不清空则不加 -t）
