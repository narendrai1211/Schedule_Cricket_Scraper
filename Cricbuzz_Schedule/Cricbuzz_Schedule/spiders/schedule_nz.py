# -*- coding: utf-8 -*-
import csv
from datetime import datetime
import scrapy
from scrapy_splash import SplashRequest


class ScheduleNzSpider(scrapy.Spider):
    name = 'schedule_nz'
    allowed_domains = ['cricbuzz.com']
    start_urls = ['https://www.cricbuzz.com/cricket-team/new-zealand/13/schedule']
    main_list = []

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
        list_data = []
        for i in range(3, 28):
            try:
                timestamp = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[1]/span/@ng-bind').get()
                date_time_str = self.get_date(timestamp)
                match = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[3]/div[1]/a/span/text()').get()
                series_match = match.split(',')
                series_match_type = series_match[1].strip()
                # print(series_match_type)
                match = series_match[0].strip()
                # print(match)
                venue = response.xpath('//*[@id="series-matches"]/div/div['+format(i)+']/div[3]/div[1]/div[2]/text()').get()
                series_name = response.xpath(
                    '//*[@id="series-matches"]/div/div[' + format(i) + ']/div[3]/div[1]/div[1]/text()').get()
                list_data = [date_time_str, series_name, series_match_type, match, venue]
                if None in list_data:
                    break
                else:
                    self.main_list.append(list_data)
            except AttributeError as e:
                print(e)
        list_header = ['date', 'series_name', 'series_match_type', 'match', 'venue']

        with open('schedule_nz.csv', 'w') as file:
            csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, escapechar=' ')
            csv_writer.writerow(list_header)
            csv_writer.writerows(self.main_list)
