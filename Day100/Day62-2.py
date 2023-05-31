from lxml import etree
import requests

import bs4
import requests

if __name__ == '__main__':
    # 练习一：通过xpath获取豆瓣电影数据
    # for page in range(1, 11):
    #     resp = requests.get(
    #         url=f'https://movie.douban.com/top250?start={(page - 1) * 25}',
    #         headers={'User-Agent': 'BaiduSpider'}
    #     )
    #     tree = etree.HTML(resp.text)
    #     # 通过XPath语法从页面中提取电影标题
    #     title_spans = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]')
    #     # 通过XPath语法从页面中提取电影评分
    #     rank_spans = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]')
    #     for title_span, rank_span in zip(title_spans, rank_spans):
    #         print(title_span.text, rank_span.text)
    # 练习二、通过CSS选择器获取豆瓣电影数据
    for page in range(1, 11):
        resp = requests.get(
            url=f'https://movie.douban.com/top250?start={(page - 1) * 25}',
            headers={'User-Agent': 'BaiduSpider'}
        )
        # 创建BeautifulSoup对象
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        # 通过CSS选择器从页面中提取包含电影标题的span标签
        title_spans = soup.select('div.info > div.hd > a > span:nth-child(1)')
        # 通过CSS选择器从页面中提取包含电影评分的span标签
        rank_spans = soup.select('div.info > div.bd > div > span.rating_num')
        for title_span, rank_span in zip(title_spans, rank_spans):
            print(title_span.text, rank_span.text)
