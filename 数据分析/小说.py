"""
[课      题]：Python实现小说下载器

[主讲老师]: 青灯教育 - 自游老师   [上课时间]: 20:05

[课程亮点]
    1. 系统分析网页性质
    2. 结构化的数据解析
    3. 函数式编程
    4. 下载进度条显示
    5. 打包py程序成exe

[环境介绍]：
    python 3.8
    pycharm

[模块使用]:
    requests  >>> pip install requests 数据请求
    parsel  >>> pip install parsel 数据解析  >>> scrapy 框架里面解析模块  [核心 css 和 xpath ]

    (完善功能) 添加搜索功能 搜索小说名字或者作者名字
    tqdm  >>> pip install tqdm  下载进度条显示模块
    prettytable >>> pip install prettytable 输入的格式好看一些

相对应的安装包/安装教程/激活码/使用教程/学习资料/工具插件 可以加落落老师微信
---------------------------------------------------------------------------------------------------
听课建议:
    1. 对于本节课讲解的内容, 有什么不明白的地方 可以直接在公屏上面提问, 具体哪行代码不清楚 具体那个操作不明白
    2. 不要跟着敲代码, 先听懂思路, 课后找落落老师领取录播, 然后再写代码
    3. 不要进进出出, 早退不仅没有录播, 你还会思路中断
---------------------------------------------------------------------------------------------------
模块安装问题:
    - 如果安装python第三方模块:
        1. win + R 输入 cmd 点击确定, 输入安装命令 pip install 模块名 (pip install requests) 回车
        2. 在pycharm中点击Terminal(终端) 输入安装命令
    - 安装失败原因:
        - 失败一: pip 不是内部命令
            解决方法: 设置环境变量

        - 失败二: 出现大量报红 (read time out)
            解决方法: 因为是网络链接超时,  需要切换镜像源
                清华：https://pypi.tuna.tsinghua.edu.cn/simple
                阿里云：http://mirrors.aliyun.com/pypi/simple/
                中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
                华中理工大学：http://pypi.hustunique.com/
                山东理工大学：http://pypi.sdutlinux.org/
                豆瓣：http://pypi.douban.com/simple/
                例如：pip3 install -i https://pypi.doubanio.com/simple/ 模块名

        - 失败三: cmd里面显示已经安装过了, 或者安装成功了, 但是在pycharm里面还是无法导入
            解决方法: 可能安装了多个python版本 (anaconda 或者 python 安装一个即可) 卸载一个就好
                    或者你pycharm里面python解释器没有设置好
---------------------------------------------------------------------------------------------------
如何配置pycharm里面的python解释器?
    1. 选择file(文件) >>> setting(设置) >>> Project(项目) >>> python interpreter(python解释器)
    2. 点击齿轮, 选择add
    3. 添加python安装路径
---------------------------------------------------------------------------------------------------
pycharm如何安装插件?
    1. 选择file(文件) >>> setting(设置) >>> Plugins(插件)
    2. 点击 Marketplace  输入想要安装的插件名字 比如:翻译插件 输入 translation / 汉化插件 输入 Chinese
    3. 选择相应的插件点击 install(安装) 即可
    4. 安装成功之后 是会弹出 重启pycharm的选项 点击确定, 重启即可生效
---------------------------------------------------------------------------------------------------
零基础 0
有基础 1

先采集一章小说
再采集一本小说
搜索功能


爬虫基本思路流程去走: <通用的>

一. 数据来源分析
    分析 小说标题, 以及 小说内容数据, 可以通过请求那个url地址获取相关数据内容
    如果去抓包分析数据
        I.  F12或者鼠标右键点击检查 打开开发者工具, 并且刷新网页数据
        II. 复制小说标题, 在开发者工具里面进行搜索 <因为网页返回数据内容比较多的>
        III. 看headers <开发者工具里面headers: 包含了请求url地址 请求方式, 以及伪装请求头参数>

二. 代码实现步骤 <>
    1. 发送请求, 对于https://www.xbiquwx.la/10_10837/5164271.html 发送请求
    2. 获取数据, 获取服务器返回响应数据内容
    3. 解析数据, 提取我们想要数据内容
    4. 保存数据, 把数据保存到本地

打包exe pyinstaller


担心老师教学质量服务质量...
    如果是因为我们青灯教育原因 <直接去申请退款> 自游老师说的 签合同...

种树最好的时间, 一个是十年前 一个就是现在...

学习看性价比...
    预定 300 学费, 可以领取 1000学费优惠券 后续需要支付7580...

整个python体系课程 从零基础入门直面就业系列课程 <两年学习权限: 教学直播 + 解答辅导>
    7580 / 12 = 631  每天22的学费 >>>
    按照两年计算 300多

你自己去找一个专业python程序员, 你每个月花1000块钱 找他给你解答辅导, 给你给教学...<两年服务>
    <多个专业的老师给教学辅导....>

100-300左右
    后续有能力接 1000+以上外包

公开课讲解的
    案例为主 主要演示效果, 没有细节知识点
    内容会重复讲解, 基本都简单内容 不会涉及反爬


系统课程 每一个细节知识点都会教授到

"""
import requests  # 数据请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块 第三方模块 pip install parsel
import prettytable as pt  # 制表输出 第三方模块 pip install prettytable
from tqdm import tqdm  # 进度条显示 第三方模块 pip install tqdm


def get_response(html_url):
    """
    发送请求:
        1. url地址
        2. 请求方式<get post>
    <Response [200]>  响应对象, 200状态码 表示请求成功

    通过requests这个模块里面get请求方式对于html_url发送请求, 最后用自定义变量response接收返回数据
    response = requests.get(url=html_url)
    headers: 请求头, 作用伪装python代码, 为了防止被反爬
        User-Agent: 用户代理 表示浏览器基本身份标识
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)
    response.encoding = response.apparent_encoding  # 自动识别编码
    # <Response [200]>
    return response


def get_content(html_url):
    """
    获取小说内容
    :param html_url: 传入小说详情页url地址
    :return: 小说内容
    response.text 获取响应对象文本数据
    提取数据, 解析数据
        parsel 使用里面css选择器去解析提取数据
        css选择器 根据标签属性内容提取数据

        h1::text 取h1标签里面文本数据 get() 获取第一个h1标签数据返回字符串数据
        getall获取所有内容 返回列表
    '\n'.join(content_list) 以换行符把列表里面每一个元素拼接起来
    """
    response = get_response(html_url)
    # print(response.text)
    selector = parsel.Selector(response.text)  # 把获取到response.text文本数据转成selector对象
    # title = selector.css('#wrapper > div.content_read > div > div.bookname > h1::text').get()
    content_list = selector.css('#content::text').getall()
    content = '\n'.join(content_list)

    # novel_content >>> ['标题', '小说内容']
    return content


def save(name, title, content):
    """
    保存数据
    :param title:  小说标题
    :param content: 小说内容
    :return:

    a 保存方式 a 追加保存 不会覆盖数据
    utf-8 编码格式, 保存文字 指定编码
    """
    with open(name + '.txt', mode='a', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(content)
        f.write('\n')


def get_novel_url(list_url):
    """
    获取小说章节url地址 以及标题
    :param list_url: 小说目录页url
    :return:
    a::attr(href) 获取这个a标签里面href属性
    """
    html_data = get_response(html_url=list_url).text  # 调用发送请求函数
    selector_1 = parsel.Selector(html_data)
    href = selector_1.css('#list > dl > dd > a::attr(href)').getall()
    title_list = selector_1.css('#list > dl > dd > a::attr(title)').getall()
    zip_data = zip(href, title_list)  # zip函数把两个列表打包放一起 返回可迭代对象
    return zip_data


def search(world):
    """
    搜索功能
    :param world: 书名或者作者名
    :return:
    """
    search_url = f'https://www.xbiquwx.la/modules/article/search.php?searchkey={world}'
    html_data = get_response(html_url=search_url).text
    selector_2 = parsel.Selector(html_data)
    # 第一次提取获取所有tr标签内容
    trs = selector_2.css('.grid tr')
    tb = pt.PrettyTable()
    tb.field_names = ['序号', '书ID', '书名', '作者']
    page = 0
    lis = []
    for tr in trs[1:]:
        # 自定义变量 可以随意取, 但是不能以数字开头, 不建议使用关键字作为变量名
        name = tr.css('.odd a::text').get()
        novel_id = tr.css('.odd a::attr(href)').get().split('/')[1]
        author = tr.css('td:nth-child(3)::text').get()
        dit = {
            '书名': name,
            '书ID': novel_id,
            '作者': author,
        }
        tb.add_row([page, novel_id, name, author])
        lis.append(dit)
        # print(name, novel_id, author)
        page += 1
    print(tb)
    num = input('请输入你想要下载小说的序号: ')
    novel_uid = lis[int(num)]['书ID']
    novel_name = lis[int(num)]['书名']
    # print('你选择下载小说书名以及ID是:', novel_uid, novel_name)
    novel_info = [novel_uid, novel_name]
    return novel_info


def main():
    """
    主函数
        整合上面所有函数功能块
    """
    while True:
        key_word = input('请输入你想要下载小说(输入0即可退出):')
        if key_word == '0':
            break
        novel_info = search(key_word)
        html_url = f'https://www.xbiquwx.la/{novel_info[0]}/'
        zip_data = get_novel_url(list_url=html_url)  # 获取小说章节url地址
        for index, title in tqdm(list(zip_data)):  # 通过for循环遍历
            # print(index, title)
            # 小说章节详情页
            index_url = f'https://www.xbiquwx.la/{novel_info[0]}/{index}'  # 使用的字符串格式化方法, 把index传入字符串里面
            novel_content = get_content(html_url=index_url)  # 调用前面定义好的获取小说内容函数
            save(name=novel_info[1], title=title, content=novel_content)


if __name__ == '__main__':
    # 函数入口
    """
    当你这个文件被当做模块去调用的时候, 下面的代码不会被执行
    """
    # main(html_url='https://www.xbiquwx.la/10_10837/')  # 调用函数
    main()
