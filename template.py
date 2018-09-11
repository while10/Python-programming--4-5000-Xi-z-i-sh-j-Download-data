import requests
import btc_close_2017
import json


json_url='https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
req = requests.get(json_url)

#将数据写入文件
with open ('123.json', 'w') as fp:
    fp.write(req.text)
file_requests = req.json()
print(file_requests)
print(req.text)
print(req.text == file_requests)
print(btc_close_2017.file_urllib == file_requests)

filename = 'btc_close_2017.json'
with open(filename, 'r') as fp:
    bct_data = json.load(fp)
for bct_dict in bct_data:
    date = bct_dict['date']
    month = bct_dict['month']
    week = bct_dict['week']
    weekday = bct_dict['weekday']
    close = bct_dict['close']
    print("{} is month {} week {},{}, the close price is {} RMB".format(date, month,week, weekday, close))

dates, months, weeks, weekdays, close = [], [], [], [], []
for bct_dict in bct_data:
    dates.append(bct_dict['date'])
    months.append(int(bct_dict['month']))
    weeks.append(int(bct_dict['week']))
    weekdays.append(bct_dict['weekday'])
    close.append(int(float(bct_dict['close'])))

import pygal
import math

line_chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False) # x轴的标签旋转20度  不全展示
line_chart.title = '收盘价（¥）'
line_chart.x_labels = dates # x轴用dates作为标签
N = 20 # x轴坐标每20天显示一次
line_chart.x_labels_major = dates[::N]

close_log = [math.log10(x) for x in close]

line_chart.add('log收盘价', close_log)
line_chart.render_to_file('收盘价对数变换折线图.svg')


from itertools import groupby

def draw_line(x_data, y_data, title, y_legend):
    xy_map = []
    for x, y in groupby(sorted(zip(x_data, y_data)), key=lambda _: _[0]):  # 2
        y_list = [v for _, v in y]
        xy_map.append([x, sum(y_list) / len(y_list)])  # 3
    x_unique, y_mean = [*zip(*xy_map)]  # 4
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_unique
    line_chart.add(y_legend, y_mean)
    line_chart.render_to_file(title + '.svg')
    return line_chart

idx_month = dates.index('2017-12-01')
print(idx_month)
line_chart_month = draw_line(months[:idx_month], close[:idx_month], '收盘价月日均值', '月日均值')
idx_week = dates.index('2017-12-01')
print(idx_week)
line_chart_week = draw_line(weeks[1:idx_week], close[1:idx_week], '收盘价周日均值', '周日均值')



idx_week = dates.index('2017-12-11')
wd = ['Monday', 'Tuesday', 'Wednesday',
      'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdays_int = [wd.index(w) + 1 for w in weekdays[1:idx_week]]
#print(weekdays_int)
line_chart_weekday = draw_line(
    weekdays_int, close[1:idx_week], '收盘价星期均值（¥）', '星期均值')
line_chart_weekday.x_labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
line_chart_weekday.render_to_file('收盘价星期均值（¥）-final.svg')

with open('收盘价DASHBOARD.html', 'w', encoding='utf8') as html_file:
    html_file.write('<html><head><title>收盘价dashboard</title><matecharset="utf8"></head><body>\n')
    for svg in ['收盘价对数变换折线图.svg','收盘价月日均值.svg','收盘价周日均值.svg',
                '收盘价星期均值（¥）.svg','收盘价星期均值（¥）-final.svg']:
        html_file.write('   <object type="image/svg+xml" data="{0}" height=500></object>\n'.format(svg))
    html_file.write('</body></html>')

