## 1_chinamoney
#### url
http://www.chinamoney.com.cn/fe/jsp/CN/chinamoney/market/searchBondDetailInfo.jsp?bondDefinedCode=3405698857
#### 简介
用PhantomJS获取动态加载的页面内容，然后找到里面的pdf文件下载链接，最后下载

## 2_amazon
#### url
https://www.amazon.de/Schn%C3%A4ppchen/bbp/bb/ref=bbp_bb_a77114_tr_w_9ea285
#### 简介
1. 从url中拿到所有的商品分类页面链接
2. 分别进入每个商品分类页面，页面使用js动态加载，所以使用selenium结合js实现滚动页面后再解析页面获取数据，最终拿到所有商品的链接地址
3. 分别进入每个商品的详情页面，从中获取商家信息的链接地址
4. 进入商家信息的页面，从中获取需要的信息

## 3_anjufang
### url
http://zjj.sz.gov.cn/bzflh/lhmcAction.do?method=queryYgbLhmcList
### 简介
深圳安居房申请人名单公示信息