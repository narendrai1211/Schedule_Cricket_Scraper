# -*- coding: utf-8 -*-
import csv
import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime


class ScheduleIndiaSpider(scrapy.Spider):
    name = 'Schedule_India'
    # allowed_domains = ['cricbuzz.com']
    start_urls = ['https://www.cricbuzz.com/cricket-team/india/2/schedule']
    script = """
                function main(splash)
                  splash:init_cookies(splash.args.cookies)
                  assert(splash:go{
                    splash.args.url,
                    headers=splash.args.headers,
                    http_method=splash.args.http_method,
                    body=splash.args.body,
                    })
                  assert(splash:wait(0.5))
                  local entries = splash:history()
                  local last_response = entries[#entries].response
                  return {
                    url = splash:url(),
                    headers = last_response.headers,
                    http_status = last_response.status,
                    cookies = splash:get_cookies(),
                    html = splash:html(),
                  }
                end
                """
    main_list = []
    list_header = ['date', 'series_name', 'series_match_type', 'match', 'venue']

    def start_requests(self):
        header = {
            'user-agent': self.settings['USER_AGENT']
        }
        yield SplashRequest(url=self.start_urls[0],
                            headers=header,
                            endpoint='render.html',
                            args={'wait': 5},
                            callback=self.parse)

    def get_date(self, timestamp):
        final_timestamp = timestamp.split('|')[0].strip()
        conv = (int(final_timestamp) / 1000)
        date_time = datetime.fromtimestamp(conv)
        print(date_time)
        datetime_str = date_time.strftime('%d/%m/%Y, %H:%M:%S')
        return datetime_str

    def parse(self, response):
        print('Parsing Current URL', response.url)
        try:
            for i in range(3, 31):
                timestamp = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[1]/span/@ng-bind').get()
                date_time_str = self.get_date(timestamp)
                match = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[3]/div[1]/a/span/text()').get()
                series_match = match.split(',')
                series_match_type = series_match[1].strip()
                match = series_match[0].strip()
                venue = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[3]/div[1]/div[2]/text()').get()
                series_name = response.xpath('//*[@id="series-matches"]/div/div[' + format(i) + ']/div[3]/div[1]/div[1]/text()').get()
                list_data = [date_time_str, series_name, series_match_type, match, venue]
                print(list_data)
                self.main_list.append(list_data)
        except AttributeError:
            print('End')
        self.write_to_file('schedule_ind.csv')

    def write_to_file(self, file_name):
        with open(file_name, 'w') as file:
            csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, escapechar=' ')
            csv_writer.writerow(self.list_header)
            csv_writer.writerows(self.main_list)
