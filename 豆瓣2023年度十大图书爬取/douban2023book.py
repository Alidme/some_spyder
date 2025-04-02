import datetime
import random
import re
import requests
import time
from bs4 import BeautifulSoup

"""
访问https://book.douban.com/annual/2023/?fullscreen=1&source=navigation
爬取《豆瓣2023年度书籍》的书籍信息
获取每本书籍的书名、作者、出版社、出版年、页数、定价、豆瓣评分、内容简介等数据
"""


# 作业目标url: 'https://book.douban.com/annual/2023/?fullscreen=1&source=navigation'

# --------------------------------------函数部分--------------------------------------

# 建立书籍url列表
def build_url_list(data, put_list):
    # url = data["widgets"][1]["source_data"]["subject_collection_items"][i]["url"]
    # 循环遍历建立url列表
    for i in range(0, len(data["widgets"][1]["source_data"]["subject_collection_items"])):
        get_url = data["widgets"][1]["source_data"]["subject_collection_items"][i]["url"]
        # print(url)
        put_list.append(get_url)
    # print(put_list)
    return put_list


# 获取url下的书籍信息
def get_book_data(put_url, rank, put_file):
    # 对于书籍的url有不一样的headers请求
    func_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/130.0.0.0 Safari/537.36',
                    'Content-Type': 'application/json, charset=UTF-8'
                    }

    response = requests.get(put_url, headers=func_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    # print(soup.find(id="wrapper"))    # 该id下包含所需的所有信息

    book_name = (soup.find('h1')).get_text().strip()  # 书名

    # info = (soup.find(id="info")).get_text()  # 该id下包含有作者、出版社、出版年、页数、定价

    # book_author = soup.find("span", class_="pl", string=" 作者").find_next("a").get_text().strip()  # 只能获取单个作者
    # 获取每个作者的名字并存储为列表
    authors = soup.find(id="info").find("span").find_all("a")
    book_author = [author.get_text().strip() for author in authors]

    # 出版社、出版年、页数
    book_publisher = soup.find("span", class_="pl", string="出版社:").find_next("a").get_text().strip()
    book_publication_year = soup.find("span", class_="pl", string="出版年:").next_sibling.get_text().strip()
    book_pages = soup.find("span", class_="pl", string="页数:").next_sibling.get_text().strip()

    # 定价
    book_price = soup.find("span", class_="pl", string="定价:").next_sibling.get_text().strip()
    price_match = re.search(r"\d+(\.\d{1,2})?", book_price)
    price = float(price_match.group())
    formatted_price = f"{price:.2f}"    # 格式化定价数字

    # 豆瓣评分
    douban_rating = soup.find('strong').get_text().strip()

    # 内容简介
    intro_out = soup.find(class_="indent", id="link-report")
    intro = intro_out.find_all(class_="intro")
    if len(intro) > 1:
        intro = intro[1]
    else:
        intro = intro[0]

    # print(intro.get_text())
    book_intro_list = []

    for p in intro.find_all("p"):
        book_intro_list.append(p.get_text() + "\n")

    book_intro = '\n'.join(book_intro_list)

    # 打印部分，取消注释可知控制台看到输出
    # print("————————————————————No." + str(rank) + "————————————————————")
    # print("书籍网址: " + put_url)
    # print("书名: 《" + book_name + "》")
    # print("作者: " + ' '.join(book_author))
    # print("出版社: " + book_publisher)
    # print("出版年: " + book_publication_year)
    # print("页数: " + book_pages)
    # print("价格: " + formatted_price + "元")
    # print("豆瓣评分: " + douban_rating)
    # print("内容简介:" + "\n\n" + book_intro + "\n")

    # 打开文件，使用'a'模式进行追加
    with open(put_file, 'a', encoding='utf-8') as f:
        f.write("————————————————————No." + str(rank) + "————————————————————\n")
        f.write("书籍网址: " + put_url + "\n")
        f.write("书名: 《" + book_name + "》\n")
        f.write("作者: " + ' '.join(book_author) + "\n")
        f.write("出版社: " + book_publisher + "\n")
        f.write("出版年: " + book_publication_year + "\n")
        f.write("页数: " + book_pages + "\n")
        f.write("价格: " + formatted_price + "元\n")
        f.write("豆瓣评分: " + douban_rating + "\n")
        f.write("内容简介:\n\n" + book_intro + "\n\n")

    print("已写入" + str(rank) + "条数据")

    # 防止请求过于频繁
    time.sleep(random.randint(2, 5))


# --------------------------------------主体部分--------------------------------------

# 根据作业要求，通过检查网页开发者工具获取到的数据请求地址
book_2023_url = 'https://book.douban.com/j/neu/page/21/'

# google地址栏输入chrome://version或网页开发者工具检查Network获得，用于伪装客户端发送请求
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/130.0.0.0 Safari/537.36'
           }

try:

    book_2023 = requests.get(book_2023_url, headers=headers)

    if book_2023.status_code == 200:
        print("状态码: " + str(book_2023.status_code) + "\n" + "连接成功\n")
        data_book_2023 = book_2023.json()
        # print(data_book_2023)

        # 建立url列表
        book_url_list = []
        build_url_list(data_book_2023, book_url_list)

        # 获取当前时间，格式化为字符串，创建一个以时间戳为文件名的新文件
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = "output_" + current_time + ".txt"

        # 打开文件并写入
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write("x-x-x-x-x-x-x-x-x-x-x-x 豆瓣2023年度图书 x-x-x-x-x-x-x-x-x-x-x-x\n")

        # 遍历列表访问各个url的书籍信息
        number = 1
        for url in book_url_list:
            get_book_data(url, number, file_name)
            number = number + 1
        print("数据写入已完成:" + file_name)
        number = 1
    else:
        print("状态码: " + str(book_2023.status_code) + "\n" + "连接失败")

except requests.exceptions.RequestException as e:
    print("请求错误" + "\n" + str(e))
