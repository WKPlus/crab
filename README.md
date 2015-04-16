# crab

## 项目说明
用来简化web page测试的框架，采用基于twisted的异步模式，支持自动爬取页面子链接进行测试，支持并发数限制。

缺点：不能执行页面的javescript代码，如果有执行页面js的需求，建议和js render service（比如[splash](https://github.com/scrapinghub/splash)或者[prerender](https://github.com/prerender/prerender)）一起使用。



## 使用手册
### 系统要求
 - python 2.6+环境
 - 安装python twisted、lxml、beautifulsoup4扩展库
   - 如果已经安装了pip，直接使用`pip install twisted lxml beautifulsoup4`即可
   - 如果没有安装pip，可以先安装pip，如何安装可以参考[官方文档](https://pypi.python.org/pypi/pip)


### case执行
* git clone https://github.com/WKPlus/crab.git
* cd crab; ./crab -c casename 
* 比如要运行现有的case/test.py中的case，直接执行`./crab -c test`即可


### case编写
以下case在位于case/test.py中

#### sample case 1
----
假设要验证www.baidu.com的http status是200

```python
from lib.base_case import TestCase
from checker.http import HTTPStatusChecker
class TestCase1(TestCase):
    def __init__(self):
        self.urls.append("www.baidu.com")
        self.checkers.append(HTTPStatusChecker(200))
```

1. 保存上述代码至case目录的testcase1.py文件
2. 执行`./crab -c testcase1`


#### sample case 2
----
如果要检查的url很多，且已经列在一个文件中了，那么上述的case如何编写呢？需要如下两个操作:
1. 在`class TestCase1(TestCase)`这一行之前添加`import lib.utils as utils`
2. 把`self.urls.append("www.baidu.com")`这一行替换为`self.urls = utils.read_list_from_file(your_file_name)`


#### sample case 3
----
如果除了检查url的http status还需要检查url对应的页面html标签是否完整

```python
from lib.base_case import TestCase
from checker.http import HTTPStatusChecker
class TestCase1(TestCase):
    def __init__(self):
        self.urls.append("www.baidu.com")
        self.checkers.append(HTTPStatusChecker(200))
        self.checkers.append(HTMLTagChecker())
```

如上代码所示，只需要在case1的基础上增加`self.checkers.append(HTMLTagChecker())`一行代码即可




## 组织结构
----
crab整体分为三个部分：crab框架、检查器(checker)、测试用例


### 检查器
检查器全部位于checker目录，目前有五个检查器：

* HTTPStatusChecker，位于http.py文件，用于检测某url的http status是否符合预期
* HTMLTagChecker，位于html.py文件，用于检测某个url对应的页面中html元素标签是否闭合
* DomainChecker，位于domain.py，用于检查页面上的链接url的domain是否符合黑白名单的要求


### 测试用例
测试用例全部位于case目录，其作用主要是关联url和检查器。
比如，要测试某个url列表中的每个url的http status，只需要写一个case关联这个url列表和HTTPStatusChecker即可。


### crab框架
crab框架的主要功能是根据命令行输入，加载对应的case执行，并格式化输出结果。

在使用crab时，可能需要自己扩展检查器满足特定测试需求，因此定义框架和检查器的接口协议为：

* 检查器实现`check`方法，框架会将一个`Page`对象作为参数来调用`check`方法。`Page`对象中包含了常见测试需要关注的内容：当前页面的url、页面源码及父url（如果该页面是自动爬取得到的）
* 检查器的`check`方法需要返回一个二元组：
   * 二元组第一个元素为True or False，表示页面检查通过与否
   * 第二个元素为error message，如果检查通过可以第二个元素可以为None




