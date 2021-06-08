'''
cron 表达式翻译成中文可读模式
'''
import re


num_day_dict = {
        '1': '星期天',
        '2': '星期一',
        '3': '星期二',
        '4': '星期三',
        '5': '星期四',
        '6': '星期五',
        '7': '星期六',
    }


def second_parser(second):
    if second == '*':
        return '每秒执行'
    elif '/' in second:
        interval = second.split('/')[1]
        start = second.split('/')[0]
        return '从' + start + '秒' + '每隔' + interval + '秒执行'
    elif '-' in second:
        start = second.split('-')[0]
        end = second.split('-')[1]
        return '从' + start + '秒到' + end + '秒执行'
    else:
        return second + '秒执行'


def minute_parser(minute):
    if minute == '*':
        return '每分钟执行'
    elif '/' in minute:
        interval = minute.split('/')[1]
        start = minute.split('/')[0]
        return '从' + start + '分钟' + '每隔' + interval + '分钟执行'
    elif '-' in minute:
        start = minute.split('-')[0]
        end = minute.split('-')[1]
        return '从' + start + '分钟到' + end + '分钟执行'
    else:
        return minute + '分钟执行'


def hour_parser(hour):
    if hour == '*':
        return '每小时执行'
    elif '/' in hour:
        interval = hour.split('/')[1]
        start = hour.split('/')[0]
        return '从' + start + '时' + '每隔' + interval + '时执行'
    elif '-' in hour:
        start = hour.split('-')[0]
        end = hour.split('-')[1]
        return '从' + start + '时到' + end + '时执行'
    else:
        return hour + '时执行'


def day_parser(day):
    global num_day_dict
    if day == '?':
        return '已按周制定'
    elif day == '*':
        return '每日执行'
    elif '/' in day:
        interval = day.split('/')[1]
        start = day.split('/')[0]
        return '从' + start + '日' + '每隔' + interval + '日执行'
    elif day == 'L':
        return '本月最后一天执行'
    elif day == 'LW':
        return '本月最后一个工作日执行'
    elif len(re.findall(re.compile(r'[1-7]L'), day)) > 0:
        return '在这个月的最后一个' + num_day_dict[day[0]] + '执行'
    elif len(re.findall(re.compile(r'L-\d'), day)) > 0:
        return '在本月底前' + day.split('-')[-1] + '日执行'
    elif len(re.findall(re.compile(r'\dW'), day)) > 0:
        return '最近的工作日（周一至周五)至本月' + re.findall(re.compile(r'\d+'), day)[0] + '日执行'
    else:
        return day + '日执行'
    

def month_parser(month):
    if month == '*':
        return '每月执行'
    elif '/' in month:
        interval = month.split('/')[1]
        start = month.split('/')[0]
        return '从' + start + '月' + '每隔' + interval + '月执行'
    elif '-' in month:
        start = month.split('-')[0]
        end = month.split('-')[1]
        return '从' + start + '月到' + end + '月执行'
    else:
        return month + '月执行'


def week_parser(week):
    global num_day_dict
    if week == '?':
        return '已按天制定' 
    elif '/' in week:
        interval = week.split('/')[1]
        start = week.split('/')[0]
        return '从' + num_day_dict[start] + '开始每隔' + interval + '周执行'
    elif '#' in week:
        interval = week.split('#')[1]
        start = week.split('#')[0]
        return '在这个月的第' + interval + '个' + num_day_dict[start] + '执行'
    else:
        week_dict = {
            'MON': '星期一',
            'TUE': '星期二',
            'WED': '星期三',
            'THU': '星期四',
            'FRI': '星期五',
            'SAT': '星期六',
            'SUN': '星期天',
        }
        for key, value in week_dict.items():
            week = week.replace(key, value)
        return week + '执行'


def year_parser(year):
    if year == '*':
        return '每年执行'
    elif '/' in year:
        interval = year.split('/')[1]
        start = year.split('/')[0]
        return '从' + start + '年' + '每隔' + interval + '年执行'
    elif '-' in year:
        start = year.split('-')[0]
        end = year.split('-')[1]
        return '从' + start + '年到' + end + '年执行'
    else:
        return year + '年执行'



def cron_translator(cron_text):
    cron_list = cron_text.split(' ')
    second = second_parser(cron_list[0])
    minute = minute_parser(cron_list[1])
    hour = hour_parser(cron_list[2])
    day = day_parser(cron_list[3])
    month = month_parser(cron_list[4])
    week = week_parser(cron_list[5])
    year = year_parser(cron_list[6])
    return [
        {'label': '秒', 'interpreter': second},
        {'label': '分钟', 'interpreter': minute},
        {'label': '小时', 'interpreter': hour},
        {'label': '天', 'interpreter': day},
        {'label': '月', 'interpreter': month},
        {'label': '周', 'interpreter': week},
        {'label': '年', 'interpreter': year},
    ]



if __name__ == '__main__':
    cron_translator('1,2,3 3/5 3/5 ? 7,3,5 MON,WED,SUN,TUE,THU,FRI,SAT 2018-2018')