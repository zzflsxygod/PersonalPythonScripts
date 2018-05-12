'''
超絶かわいい~~ななせ~~
Create by zzflsxygod
'''
import requests
from bs4 import BeautifulSoup
import os


class NogiSpider(object):
    '''
    乃木坂46官方博客图片下载脚本
    '''

    __blog_url = 'http://blog.nogizaka46.com/nanase.nishino/?p=1'
    __target_folder = 'E:\\Pictures'
    __header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    def __init__(self, member_url=__blog_url, target_folder=__target_folder):
        '''基本参数设定:
        member_url -->成员博客首页地址
        target_folder -->图片存放目标文件夹
        '''
        self.member_url = member_url
        self.target_folder = target_folder

    def GetPage(self, url=__blog_url):
        '''请求并处理页面:
        url -->需要处理的页面地址
        return: 返回页面内容
        return Type: BeautifulSoup
        '''
        rq = requests.get(url, headers=self.__header)
        soup = BeautifulSoup(rq.text, 'html.parser')

        return soup

    def GetContents(self, soup):
        '''解析页面获得博客本体
        soup -->页面的BeautifulSoup实例
        return: 返回当前页面所有的博客主体信息
        return Type: List
        '''
        return soup.find_all('div', class_='entrybody')

    def GetDates(self, soup):
        '''解析页面获得博客发布时间
        soup -->页面的BeautifulSoup实例
        return: 返回当前页面所有博客发布日期
        return Type: List
        '''
        return soup.find_all('span', class_='date')

    def ParseDate(self, soup_date):
        '''解析发布时间
        soup_date -->发布时间的BeatifulSoup实例
        return: 返回解析后的发布日期
        return Type: string
        '''
        return soup_date.find(
            'span', class_='yearmonth').text + '_' + soup_date.find(
                'span', class_='dd1').text

    def ParseImage(self, soup_content):
        '''解析内容获得图片
        soup_content -->博客主体的BeautifulSoup实例
        return: 返回解析后的图片URL
        return Type: List
        '''
        imgs = soup_content.find_all('img')
        urls = []
        for e in imgs:
            urls.append(e['src'])
        return urls

    def MakeFolder(self, date):
        '''根据发布时间创建文件夹
        date -->发布时间的字符串
        return: 返回创建的文件及地址
        return Type: string
        '''
        path = os.path.join(self.target_folder, date.replace('/', '\\'))
        os.makedirs(path, exist_ok=True)
        return path

    def DownLoadImage(self, img_url, path, name):
        '''通过图片地址下载图片
        imag_url -->图片的下载地址
        path -->保存路径
        name -->保存文件名
        '''
        r = requests.get(img_url, headers=self.__header)
        with open(path + '\\' + name + '.jpg', 'wb') as f:
            f.write(r.content)


def Main():
    '''
    主函数
    '''
    spider = NogiSpider()
    page = spider.GetPage()
    dates = spider.GetDates(page)
    contents = spider.GetContents(page)

    count = 0
    for e in dates:
        date = spider.ParseDate(e)
        path = spider.MakeFolder(date)
        img_urls = spider.ParseImage(contents[count])
        name = 0
        for url in img_urls:
            spider.DownLoadImage(url, path, str(name))
            name = name + 1
        count = count + 1


if __name__ == '__main__':
    Main()
