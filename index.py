#!/usr/bin/python3
#coding=utf-8
import requests, json
import time

spkey = '70630e3f0d034dc99febb46e194a635f'          #pushplus
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()               #返回的数据
    english = eed.json()['content']
    zh_CN = eed.json()['note']
    str = '\n【奇怪的知识】\n' + english + '\n' + zh_CN
    return str
print(get_iciba_everyday())

def main(*args):
    api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
    city_code = '101010200'               #进入https://where.heweather.com/index.html查询你的城市代码
    tqurl = api + city_code
    response = requests.get(tqurl)
    d = response.json()         #将数据以json形式返回，这个d就是返回的json数据

    if(d['status'] == 200):     #当返回状态码为200，输出天气状况
        print("城市：",d["cityInfo"]["parent"], d["cityInfo"]["city"])
        print("更新时间：",d["time"])
        print("日期：",d["data"]["forecast"][1]["ymd"])
        print("星期：",d["data"]["forecast"][1]["week"])
        print("天气：",d["data"]["forecast"][1]["type"])
        print("温度：",d["data"]["forecast"][1]["high"],d["data"]["forecast"][0]["low"])
        print("湿度：",d["data"]["shidu"])
        print("PM25:",d["data"]["pm25"])
        print("PM10:",d["data"]["pm10"])
        print("空气质量：",d["data"]["quality"])
        print("风力风向：",d["data"]["forecast"][1]["fx"],d["data"]["forecast"][0]["fl"])
        print("感冒指数：",d["data"]["ganmao"])
        print("温馨提示：",d["data"]["forecast"][1]["notice"],"。")

        cpurl = 'http://www.pushplus.plus/send'        
        content = '【明日份天气】\n城市：'+d['cityInfo']['parent']+' '+d['cityInfo']['city']+'\n日期：'+d["data"]["forecast"][1]["ymd"]+' '+d["data"]["forecast"][1]["week"]+'\n天气：'+d["data"]["forecast"][1]["type"]+'\n温度：'+d["data"]["forecast"][1]["high"]+' '+d["data"]["forecast"][1]["low"]+'\n湿度：'+d["data"]["shidu"]+'\n空气质量：'+d["data"]["quality"]+'\n风力风向：'+d["data"]["forecast"][1]["fx"]+' '+d["data"]["forecast"][1]["fl"]+'\n温馨提示：'+d["data"]["forecast"][1]["notice"]+'。\n[更新时间：'+d["time"]+']\n✁-----------------'+get_iciba_everyday()         #天气提示内容，基本上该有的都做好了，如果要添加信息可以看上面的print，我感觉有用的我都弄进来了。
        payload = {'token': '', 'title': '', 'template ': 'markdown'}
        payload['token'] = spkey
        title = '天气预报' 
        payload['title'] = title
        payload['content']=content.encode('utf-8')
        requests.get(cpurl, params=payload)
    else:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务状态！'
        requests.get(cpurl,error.encode('utf-8'))

def main_handler(event, context):
    return main()

if __name__ == '__main__':
    main()
