## 私募基金管理人综合查询——python爬虫

> 爬取 [私募基金管理人综合查询](https://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html) 中基金数据的如下字段：
> * 基金管理人全称(中文)  
> * 登记时间
> * 是否为符合提供投资建议条件的第三方机构
> * 管理规模区间

### 使用技术
**python3.8 + selenium + pickle + xlwt**

### 爬取逻辑
1. 使用selenium模拟用户浏览界面，点击进入每一页的每一个基金详情页，用正则解析基金基本信息，并写入字典；
2. 利用pickle序列化；
3. 利用pickle反序列化，处理数据写入excel；
> 2和3步是为了减少爬取次数

### 程序入口
1. `python data_to_catch_async.py` -> *爬取数据，并序列化*
   > 如果失败可以使用 `python data_to_catch.py` 重试 （*慢50%*）
2. `python catch_to_data.py` -> *将序列化的数据写入excel*

**config文件设置程序参数**

**别忘了配置selenium哦**
