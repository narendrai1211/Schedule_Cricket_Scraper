# -*- coding: utf-8 -*-
import datetime
from datetime import datetime
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
import csv


class RankingsScraperSpider(scrapy.Spider):
    name = 'rankings_scraper'
    start_urls = ['https://www.cricbuzz.com/cricket-stats/icc-rankings/men/teams']
    test_rankings = []
    header = ['rank', 'team_name', 'points']
    odi_rankings = []
    t20i_rankings = []

    def start_requests(self):
        yield SplashRequest(url= self.start_urls[0], callback=self.parse)

    def parse(self, response):
        date_ran = datetime.today()
        required_date = date_ran.date().strftime('%d-%m-%Y')
        print(required_date)
        note = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[1]/div[1]/text()').get()
        print(note.strip('*').strip())
        for i in range(3, 12):
            team_rank = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[1]/div['+format(i)+']/div[1]/text()').get()
            team_name = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[1]/div['+format(i)+']/div[2]/text()').get()
            team_pts = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[1]/div['+format(i)+']/div[3]/text()').get()
            test_json_record = {
                    'id': team_rank,
                    'team_name': team_name,
                    'points': team_pts
            }
            print(test_json_record)
            list_record = [team_rank, team_name, team_pts]
            self.test_rankings.append(list_record)
        self.write_to_file('team_rankings_test.csv', self.test_rankings)
        self.parse_odi(response)
        self.parse_t20i(response)

    def parse_odi(self, response):
        for i in range(2, 12):
            team_rank = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[2]/div['+format(i)+']/div[1]/text()').get()
            team_name = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[2]/div['+format(i)+']/div[2]/text()').get()
            team_pts = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[2]/div['+format(i)+']/div[3]/text()').get()
            test_json_record = {
                    'rank': team_rank,
                    'team_name': team_name,
                    'points': team_pts
            }
            print(test_json_record)
            list_record = [team_rank, team_name, team_pts]
            self.odi_rankings.append(list_record)
        self.write_to_file('team_rankings_odi.csv', self.odi_rankings)

    def parse_t20i(self, response):
        for i in range(2, 12):
            rank = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[3]/div['+format(i)+']/div[1]/text()').get()
            team_name = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[3]/div['+format(i)+']/div[2]/text()').get()
            pts = response.xpath('//*[@id="page-wrapper"]/div[3]/div[2]/div/div/div[3]/div[' + format(i) + ']/div[3]/text()').get()
            json_record = {
                'rank': rank,
                'team_name': team_name,
                'points': pts
            }
            print(json_record)
            list_record = [rank, team_name, pts]
            self.t20i_rankings.append(list_record)
        self.write_to_file('team_rankings_t20i.csv', self.t20i_rankings)

    def write_to_file(self, file_name, data):
        with open(str(file_name), 'w') as f:
            csv_writer = csv.writer(f, csv.QUOTE_NONE, escapechar='')
            csv_writer.writerow(self.header)
            csv_writer.writerows(data)
            print('Witten Data to', file_name)
