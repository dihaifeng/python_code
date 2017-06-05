## Python学习网站
* python-cookbook http://python3-cookbook.readthedocs.io/zh_CN/latest/preface.html#
* [foo]: http://python3-cookbook.readthedocs.io/zh_CN/latest/preface.html#  "python-cookbook"


## 代码部署：
* 获取代码：使用公司gitlab统一管理,指定提交代码的规范
* 编译：根据环境不同,考虑是否使用静态库或在docker中创建不同的编译环境
- 目录名：SuperFans
- 文件名：SuperFans_King_v1.0_2017-03-21-1010
* 匹配环境配置文件,测试环境,灰度,线上环境
* 打包：使用tar命令进行打包,命名规则Super_Fans_King_v1.0_2017-03-21-1010
* 使用SaltStack根据业务分组统一将代码推到目标服务器
* 将待部署节点移除集群,是否可以通过接口的方式移除,动态管理节点
* 解压代码包
* 创建软链接,目的为了秒级回滚,实际代码根路径为/home/w,所有代码存放在/data1	目录下，/home/w/webservice -> /data1/webservice_v1.0_2017-03-21-1010/
* COPY差异文件(可选):因为同一集群中配置文件不同
* 重启服务
* 自动化测试验证:如果有验证接口最好,没有写脚本验证
* 接入集群提供服务
## 代码回滚：
* 列出回滚版本
* 目标服务器移除集群
* 执行回滚:删除旧的软链接,创建到指定版本的软连接
* 重启服务
* 自动化验证
* 加入集群
