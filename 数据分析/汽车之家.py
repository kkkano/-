"""
[课    题]：Python爬取汽车之家

[授课老师]: 巳月老师    [上课时间]: 20:05

[课程亮点]:
	1、系统分析目标网页
	2、html标签数据解析方法
	3、海量数据一键保存

[环境介绍]:
    python 3.8  anaconda: 自动配置环境变量
    pycharm 2021专业版 >>> 激活码
    requests >>> pip install requests
    parsel >>> pip install parsel

[模块安装]: 按住键盘 win + r, 输入cmd回车 打开命令行窗口, 在里面输入 pip install 模块名

先听一下歌, 等一下后面进来的同学, 20:05开始讲课 有什么喜欢听的歌 也可以发在公屏上

[没听懂?]
课后的回放录播资料找木子老师微信: python10010
+python  安装包 安装教程视频
+pycharm 社区版 专业版 及 激活码免费

python应用:
    爬虫程序:
        批量采集互联网数据(文本, 图片, 视频, 音频)
    本质:
        一次一次请求与响应

一.明确需求
    我们要爬取内容是什么? 在哪里?
        每一辆车信息
        在网页源代码当中

二. 代码实现
    1. 发送请求 https://www.che168.com/china/a0_0msdgscncgpi1ltocsp1exx0/?pvareaid=102179
    2. 获取数据 网页源代码
    3. 解析数据(筛选数据) 工具帮助我们去做数据解析 parsel 第三方模块 需要大家去下载安装
    4. 保存数据
"""
import requests     # 发送请求
import parsel
import csv

# 伪装
headers = {
    'Cookie': 'userarea=0; listuserarea=0; fvlid=1639134728358TfiUoYkPyH86; sessionid=530d5f12-0c83-42b6-8a5a-7260ce6d0507; sessionip=175.0.62.169; area=430103; che_sessionid=652B6AFA-A370-444B-A099-D891A75FB0BD%7C%7C2021-12-10+19%3A12%3A09.393%7C%7C0; Hm_lvt_d381ec2f88158113b9b76f14c497ed48=1639134728,1639137478; ahpvno=4; Hm_lpvt_d381ec2f88158113b9b76f14c497ed48=1639144859; ahuuid=77E92EB7-7EEF-4366-A036-72BD8BDD2500; sessionvisit=b3c4a319-d202-4fb8-871a-5d7e683bf852; sessionvisitInfo=530d5f12-0c83-42b6-8a5a-7260ce6d0507|www.che168.com|102179; showNum=4; v_no=4; visit_info_ad=652B6AFA-A370-444B-A099-D891A75FB0BD||62B11FCC-BC2B-492B-9EB4-98A135366FC6||-1||-1||4; che_ref=0%7C0%7C0%7C0%7C2021-12-10+22%3A00%3A59.875%7C2021-12-10+19%3A12%3A09.393; che_sessionvid=62B11FCC-BC2B-492B-9EB4-98A135366FC6; sessionuid=530d5f12-0c83-42b6-8a5a-7260ce6d0507',
    # 浏览器基本信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
csv_qczj = open('qczj_1.csv', mode='a', encoding='utf-8', newline='')
csv_write = csv.writer(csv_qczj)
# csv_write.writerow(['品牌', '里程(万公里)', '车龄', '城市', '认证', '售价(万元)', '原价(万元)', '链接', '车辆图片'])
for page in range(92, 101):
    print(f'-----------------------正在爬取第{page}页-----------------------')
    # 1. 发送请求
    url = f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/?pvareaid=102179'
    response = requests.get(url=url, headers=headers)
    # 设置编码
    # response.encoding = 'gbk'
    # 2. 获取数据 网页源代码
    # <Response [200]>: 发送请求成功
    data_html = response.text
    # 3. 解析数据(筛选数据)
    selector = parsel.Selector(data_html)
    lis = selector.css('.viewlist_ul li')
    for li in lis:
        try:
            name = li.css('.card-name::text').get()   # 车名
            unit = li.css('.cards-unit::text').get()  # 信息
            kmNumber = unit.split('／')[0]
            years = unit.split('／')[1]
            city = unit.split('／')[2]
            business = unit.split('／')[3]
            price = li.css('.pirce em::text').get()   # 售价
            yprice = li.css('s::text').get()          # 原价
            carinfo = li.css('.carinfo::attr(href)').get()  # 详情页链接
            img = li.css('img::attr(src)').get()      # 车图片链接
            print(name, kmNumber, years, city, business, price, yprice, carinfo, img)
            csv_write.writerow([name, kmNumber, years, city, business, price, yprice, carinfo, img])
        except:
            pass
