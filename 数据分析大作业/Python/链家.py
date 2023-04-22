

import requests
import parsel
import csv
import time



f = open('数据.xlsx', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '标题',
    '地区',
    '户型',
    '面积',
    '朝向',
    '装修',
    '楼层',
    '建立时间',
    '房子类型',
    '总价',
    '单价',
    '关注人数',
    '发布时间',
    '标签',
    '详情页',
])
csv_writer.writeheader()
for page in range(1, 21):
        time.sleep(1)
        url = f'https://gz.lianjia.com/ershoufang/pg{page}/'
        #print(page)
        headrs = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
        }
        response = requests.get(url=url, headers=headrs)
        # print(response.text)

        selector = parsel.Selector(response.text)
        lis = selector.css('.sellListContent li')
        for li in lis:
                title = li.css('.title a::text').get()  # 标题
                if title:
                    href = li.css('.title a::attr(href)').get()  # 详情页

                    area_list = li.css('.flood a::text').getall()
                    area = '-'.join(area_list)  # 地区
                    house_info = li.css('.houseInfo::text').get().split('|')
                    # print(len(house_info))
                    try:
                        unit_type = house_info[0]  # 户型 几室几厅
                        acreage = house_info[1]  # 面积
                        path = house_info[2]  # 朝向
                        furnish = house_info[3]  # 装修
                        floor = house_info[4]  # 楼层
                        build_time = house_info[5]  # 建立时间
                        house_type = house_info[6]  # 房子类型
                    except:
                        house_type = "暂无数据"

                    # print(house_info)
                    follow_info = li.css('.followInfo::text').get().split('/')  # 关注人数
                    follow_man = follow_info[0]  # 关注人数
                    updated = follow_info[1]  # 发布时间
                    tag_list = li.css('.tag span::text').getall()  # 标签
                    tag = '-'.join(tag_list)
                    total_price = li.css('.totalPrice span::text').get() + '万'  # 总价
                    unit_price = li.css('.unitPrice span::text').get().replace('单价', '')  # 单价
                    dit = {
                        '标题': title,
                        '地区': area,
                        '户型': unit_type,
                        '面积': acreage,
                        '朝向': path,
                        '装修': furnish,
                        '楼层': floor,
                        '建立时间': build_time,
                        '房子类型': house_type,
                        '总价': total_price,
                        '单价': unit_price,
                        '关注人数': follow_man,
                        '发布时间': updated,
                        '标签': tag,
                        '详情页': href,
                    }
                    csv_writer.writerow(dit)
                    print(title, area, unit_type, acreage, path, furnish, floor, build_time, house_type, follow_info, follow_man, updated,
                          tag, total_price, unit_price, sep='|')
                    # li.css
                    # print(house_info)
                    # print(title)

