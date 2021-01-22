from LCD1602Driver import LCD_LINE_1,LCD_LINE_2, DEFINED_CHR, CGRAM_C1, CGRAM_C2, lcd_string, \
    lcd_clean, define_character, display_custom_character, curser_return, \
    display_image
import json
import os
import datetime
import requests
import time

Celsius_Mark = ['00010110', '00001001', '00001000', '00001000', '00001000', '00001001', '00000110', '00000000']

define_character(CGRAM_C1, Celsius_Mark)


def main():
    while True:
        Tempfile = open('/sys/class/thermal/thermal_zone0/temp')
        Temp = int(float(Tempfile.read()) / 1000)
        Tempfile.close

        RAMInfo = os.popen('free')
        index = 0
        while True:
            index = index + 1
            Line = RAMInfo.readline()
            if index == 2:
                RAMRemain = int(float(Line.split()[3]) / 1000)
                break
        Current_Time = datetime.datetime.now()
        if Current_Time.minute < 10:
            Current_Time_minute = '0' + str(Current_Time.minute)
        else:
            Current_Time_minute = str(Current_Time.minute)
        if Current_Time.hour < 10:
            Current_Time_hour = '0' + str(Current_Time.hour)
        else:
            Current_Time_hour = str(Current_Time.hour)

        Weather_Report = get_weather_info('三亚')
        if Weather_Report[2] == '晴':
            Weather_Logo = '/home/pi/SystemMonitor/Pics/Sunny.jpg'
        elif Weather_Report[2] == '多云':
            Weather_Logo = '/home/pi/SystemMonitor/Pics/Clouded.jpg'
        elif Weather_Report[2] == '小雨':
            Weather_Logo = '/home/pi/SystemMonitor/Pics/SmallRain.jpg'
        else:
            pass

        lcd_string('CPU:' + str(Temp) + '  ' + 'Mem:' + str(RAMRemain), LCD_LINE_1[0])
        display_custom_character(LCD_LINE_1[6], DEFINED_CHR[0])
        lcd_string('     ' + str(Current_Time_hour) + ':' + str(Current_Time_minute), LCD_LINE_2[0])

        time.sleep(3)

        lcd_string('H:' + Weather_Report[0], LCD_LINE_1[0])
        display_custom_character(LCD_LINE_1[4], DEFINED_CHR[0])
        lcd_string('L:' + Weather_Report[1], LCD_LINE_2[0])
        display_custom_character(LCD_LINE_2[4], DEFINED_CHR[0])
        if Weather_Logo:
            display_image(Weather_Logo, 13)
        else:
            pass

        time.sleep(3)


def get_weather_info(City):
    URL = 'http://wthrcdn.etouch.cn/weather_mini?city=' + City
    Report_File = requests.get(URL)
    Report = json.loads(Report_File.text)
    Weather_Report = [Report['data']['forecast'][0]['high'][3:].strip('℃'),
                      Report['data']['forecast'][0]['low'][3:].strip('℃'), Report['data']['forecast'][0]['type']]
    return Weather_Report


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        curser_return()
        lcd_string('Closing Process', LCD_LINE_1[0])
        lcd_string(' ', LCD_LINE_2[0])
        time.sleep(1)
    finally:
        lcd_clean()
