# 展示vcenter一天的磁盘的数据增长情况
1.通过vmware提供的pyvmomi模块取得所需数据\
2.通过django呈现数据信息

首页显示lun信息和相对前一天变化值\
![image](https://github.com/276622709/show_vm_lun_info/blob/master/1.jpg)
点击查看lun对应的vm信息和相对前一天的磁盘变化值\
![image](https://github.com/276622709/show_vm_lun_info/blob/master/2.jpg)
-------------------------------------------------------------------------
## 使用教程
### 1.搭建django平台
网上随便找个例子安装基础环境就行，我的环境是django1.10.6，python版本3.5 用的virtualenv 网上有教程
### 2.安装mysql数据库
过程略，启动mysql服务，设置数据库管理员密码，创建数据库名为vm\
安装mysqlclient,用于和mysql数据库交互，安装mysqlclient之前需要安装mysql-devel\
yum install mysql-devel -y\
pip3 install mysqlclient\
安装dateutil模块\
pip3.5 install python-dateutil
### 3.创建项目并初始化数据库表信息
> django-admin startproject test\
cd test

拷贝程序代码到当前目录
> cp 我的目录中的所有文件 ./

初始化数据库
> python manage.py makemigrations\
python manage.py migrate

修改setup.py中对应的root和密码设置
### 4.启动django
> python manager.py runserver 0.0.0.0:9000
### 5.使用getallvms_bak1.py 文件获取所需数据
安装pyvmomi-community-samples 参考http://vmware.github.io/pyvmomi-community-samples/ \
将getallvms_bak1.py 拷贝到 samples目录下
### 6.使用crontab
> 2 0 * * * python /root/pyvmomi-community-samples/samples/getallvms_bak1.py -s "vcenter ip地址" -u "用户名" -p '密码' -S

至此，搭建过程结束\
有很多可以去优化可添加的地方，以后有时间会去修改和添加新功能

