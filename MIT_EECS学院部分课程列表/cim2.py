from bs4 import BeautifulSoup


# 提取打印课程信息的函数
def print_course_info(course_tag):
    # 旧课程代码
    old_tag = course_tag.find('old')

    annotation_div = course_tag.find('div', class_='annotation')

    # 课程介绍
    if annotation_div:
        course_name = annotation_div.find('b')
        course_introduce = annotation_div.find('p')

        # 打印课程名称
        print(f"课程名称：{course_name.text if course_name else '无'}")

        # 打印旧课程代码
        print(f"旧课程代码：{old_tag.text if old_tag else '无'}")

        # 打印先修要求
        prereqs_text = annotation_div.find(string=lambda text: text and 'Prereqs:' in text)
        print(f"{prereqs_text if prereqs_text else '无'}")

        # 打印学时要求
        units_text = annotation_div.find(string=lambda text: text and 'Units:' in text)
        print(f"{units_text if units_text else '无'}")

        # 打印课程简介
        print(f"{course_introduce.text if course_introduce else '无'}")

    print("-" * 50 + "\n")


# 打开本地 HTML 文件
try:
    with open("E:\\Desktop\\roadmap\\roadmap.html", "r", encoding="utf-8") as file:  # 指定文件路径和编码
        content = file.read()  # 读取文件内容
except FileNotFoundError:
    print("HTML文件未找到，请检查文件路径")
    exit()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(content, "html.parser")

# 查找所有带有 name="AUS2" 的 <a> 标签
aus_tag = soup.find_all('a', attrs={'name': 'CIM2'})

all_courses_count = 0
# 遍历每个 <a> 标签
for aus in aus_tag:
    # 找到下一个同级的 <div> 标签
    next_div = aus.find_next_sibling('div')

    # 如果找到下一个 <div> 标签，打印其内容
    if next_div:
        table_tag = next_div.find('table')
        if table_tag:
            course_tags = table_tag.find_all('a')
            course_count = len(course_tags)
            all_courses_count += course_count

            # 遍历每个课程标签
            for course_tag in course_tags:
                print_course_info(course_tag)  # 打印课程信息

    print("共有" + str(all_courses_count) + "门课")
