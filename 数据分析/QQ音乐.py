"""
[课程内容]: Python零基础之 QQ音乐爬虫
[授课老师]: 青灯教育-巳月
录播链接：链接: https://pan.baidu.com/s/1n3UmFr8sduDFBIPRIpMA_w?pwd=d6s6 提取码: d6s6
"""
import requests
import json
import prettytable as pt


headers = {
    'Cookie': 'pgv_pvid=4227223875; RK=Y0TkAmcewt; ptcz=3a828bb1418fef564dd446864d5d7e6c7562128b5d68f825b464081becb8864e; fqm_pvqid=36f3d133-a426-438a-83d0-1821e340c527; ts_uid=5469654834; LW_uid=Y1L6P2C7r3S822W8D1s1v5N7n8; eas_sid=61d6w2q7A3f8d2Y8J1W1d5X8z3; Qs_lvt_323937=1627382806%2C1628862589; Qs_pv_323937=1419504452504244200%2C153728413586928030; LW_sid=v156O2D9Z121j1k3e0t2a1J5N4; ied_qq=o3421355804; ptui_loginuin=1321228067; _gcl_au=1.1.1508020928.1629704849; pt_235db4a7=uid=ZQvkc6mgZ/IgqUlIz0-9/A&nid=1&vid=-52PpDj4Jxm4Azg-ojxaMw&vn=1&pvn=1&sact=1629704849033&to_flag=0&pl=0KzaISwJA-wYoyVB1nkjpQ*pt*1629704849033; _ga=GA1.2.129533475.1629704849; tmeLoginType=2; pac_uid=1_321228067; iip=0; tvfe_boss_uuid=bb9075b919981d3a; o_cookie=1321228067; fqm_sessionid=cdf92536-8796-42d8-b3df-a5dd1f7ed779; pgv_info=ssid=s8544727808; ts_refer=ADTAGmyqq; _qpsvr_localtk=0.485361667619747; login_type=1; qm_keyst=Q_H_L_24HXk560eyZgA931iPUTiWoSp_xP9wMRpYW0s8WgQWUrkjK_o_ZV6jE8WdjBBU3; qqmusic_key=Q_H_L_24HXk560eyZgA931iPUTiWoSp_xP9wMRpYW0s8WgQWUrkjK_o_ZV6jE8WdjBBU3; wxunionid=; wxopenid=; psrf_qqunionid=FAEE1B5B10434CF5562642FABE749AB9; psrf_qqrefresh_token=309E71065899568052CD8433ECBED69C; wxrefresh_token=; psrf_musickey_createtime=1634632977; uin=1321228067; euin=oKoAoK-ANens7z**; psrf_qqaccess_token=098E5A5A88BFCFF2513A0D2AC9C09C9F; psrf_qqopenid=4F37937E43ECA9EAB02F9E89BE1860E2; psrf_access_token_expiresAt=1642408977; qm_keyst=Q_H_L_24HXk560eyZgA931iPUTiWoSp_xP9wMRpYW0s8WgQWUrkjK_o_ZV6jE8WdjBBU3; ts_last=y.qq.com/n/ryqq/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}


"""搜索功能"""
music_info_list = []
name = input('请输入歌手或歌曲：')  # input函数 输入 做用户交互 使用的
# 1. 发送请求 向第一个接口发送网络请求
url = f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=10&w={name}'
# print(url)
response = requests.get(url, headers=headers).text  # 获取到的是字符串
# 2. 获取数据 获取所有歌曲信息数据
# 将response切分成json格式 类似字典 但是现在还是字符串
music_json = response[9:-1]
# 字符串转字典
music_data = json.loads(music_json)  # 转换成 字典
# print(music_data)
# 3. 解析数据 提取 '序号', '歌名', '歌手', '专辑', '歌曲mid'
tb = pt.PrettyTable()
tb.field_names = ['序号', '歌名', '歌手', '专辑']
music_list = music_data['data']['song']['list']
count = 0
for music in music_list:
    song_name = music['songname']  # 歌曲的名字
    singer_name = music['singer'][0]['name']  # 歌手的名字
    song_mid = music['songmid']  # 歌曲mid
    album_name = music['albumname']  # 专辑名称
    # 4. 格式化输出
    tb.add_row([count, song_name, singer_name, album_name])
    # 将音乐信息存储在 列表当中
    music_info_list.append([song_name, singer_name, song_mid])
    count += 1
print(tb)


"""下载功能"""
while True:
    input_index = eval(input("请输入要下载歌曲的序号(-1退出): "))
    if input_index == -1:
        break
    download_info = music_info_list[input_index]
    print(download_info[2])
    # 音乐接口
    music_info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch", "filename":"M800","param":{"guid":"8846039534","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","filename":"M800","param":{"guid":"8846039534","songmid":["%s"],"songtype":[0],"uin":"1152921504784213523","loginflag":1,"platform":"20"}},"comm":{"uin":"1152921504784213523","format":"json","ct":24,"cv":0}}' % download_info[2]
    response_1 = requests.get(music_info_url, headers=headers).json()
    purl = response_1['req_0']['data']['midurlinfo'][0]['purl']
    full_media_url = 'http://dl.stream.qqmusic.qq.com/' + purl
    music_data = requests.get(full_media_url, headers=headers).content
    with open(f'歌曲下载/{download_info[0]}-{download_info[1]}.mp3', mode='wb') as f:
        f.write(music_data)
        print(f'{download_info[0]}', '下载完成！！！')