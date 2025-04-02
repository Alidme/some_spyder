import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 主页面 URL
base_url = ("https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages"
            "/material-by-lecture/")

# 本地存储目录（你可以设置一个根目录）
root_download_dir = "E:\\Desktop\\mit6.100L\\MIT_Course_Resources"
os.makedirs(root_download_dir, exist_ok=True)


def get_soup(url):
    """获取页面内容并解析为 BeautifulSoup 对象"""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"无法访问页面：{url}")
        return None


def sanitize_filename(title):
    """清理文件夹和文件名中的无效字符"""
    invalid_chars = [",", " ", "\\", "/", ":"]
    for char in invalid_chars:
        title = title.replace(char, "_")
    return title


def download_file(lecture_dir, title, pdf_url):
    """下载文件并保存到指定目录"""
    try:
        print(f"正在下载：{title} - {pdf_url}")
        response = requests.get(pdf_url)
        if response.status_code == 200:
            # 使用 lecture_dir 作为目录
            filename = os.path.join(lecture_dir, sanitize_filename(title))
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"已保存：{filename}")
        else:
            print(f"无法下载文件：{pdf_url}")
    except Exception as e:
        print(f"下载失败：{pdf_url} 错误：{e}")


def process_resource_page(lecture_dir, resource_url):
    """进入资源页面并提取 PDF 文件"""
    soup = get_soup(resource_url)
    if not soup:
        return
    # 查找 class="download-file" 的元素
    download_link = soup.find("a", class_="download-file")
    if download_link and download_link.get("href"):
        pdf_relative_url = download_link["href"]  # 获取相对链接
        pdf_url = "https://ocw.mit.edu" + pdf_relative_url  # 拼接成完整的URL
        file_title = pdf_relative_url.split("/")[-1] or "Unnamed_File"  # 如果无标题，用默认值
        print(f'file title: {file_title}')
        download_file(lecture_dir, file_title, pdf_url)


def process_lecture_page(lecture_url):
    """处理每个二级页面，提取目标资源链接并访问资源页面"""
    soup = get_soup(lecture_url)
    if not soup:
        return
    # 获取页面中的所有 h2 标签，选择第二个 h2 标签作为 Lecture 标题
    h2_tags = soup.find_all("h2")
    lecture_title = h2_tags[1].text.strip() if len(h2_tags) > 1 else "Unknown_Lecture"
    lecture_title = sanitize_filename(lecture_title)  # 清理无效字符
    lecture_dir = os.path.join(root_download_dir, lecture_title)
    os.makedirs(lecture_dir, exist_ok=True)  # 为该 Lecture 创建一个文件夹

    # 查找包含目标关键字的标题
    sections = soup.find_all("h3")  # 假设资源部分用 h3 标记
    for section in sections:
        section_title = section.text.strip()
        if any(keyword in section_title for keyword in
               ["Lecture Notes", "Finger Exercise", "Problem Set", "Recitation"]):
            # 使用 find_next 查找该部分后续的内容，包括链接
            next_section = section.find_next()
            while next_section:
                # 如果下一个元素是a标签并且href属性存在，说明是资源链接
                if next_section.name == "a" and next_section.get("href"):
                    resource_title = next_section.text.strip()
                    resource_url = urljoin(lecture_url, next_section["href"])
                    if "mit6_100l_f22" in resource_url:
                        print(f"处理资源页面：{resource_title} - {resource_url}")
                        process_resource_page(lecture_dir, resource_url)
                    else:
                        break

                # 继续查找下一个兄弟节点
                next_section = next_section.find_next()


def fix_directory_names(root_dir):
    """修复路径下所有目录名称中连续的下划线"""
    # 获取所有目录（忽略文件）
    directories = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for directory in directories:
        # 如果目录名包含连续的下划线（如“__”），则替换成单个下划线
        new_directory_name = directory.replace("__", "_")

        # 如果名称有变化，重命名目录
        if new_directory_name != directory:
            old_dir_path = os.path.join(root_dir, directory)
            new_dir_path = os.path.join(root_dir, new_directory_name)
            os.rename(old_dir_path, new_dir_path)
            print(f"目录名称已更改：{old_dir_path} -> {new_dir_path}")


# 第一步：抓取主页面中的二级链接
soup = get_soup(base_url)
if not soup:
    exit()

lecture_links = []
soup1 = soup.find(id="course-content-section")
for link in soup1.find_all("a", href=True):
    if "lecture" in link["href"]:  # 选择包含“lecture”的链接
        lecture_links.append(urljoin(base_url, link["href"]))

# 第二步：处理每个二级链接
for lecture_url in lecture_links:
    print(f"处理页面：{lecture_url}")
    process_lecture_page(lecture_url)

print("所有资源下载完成！")

# 示例：在下载完资源后，调用修复目录名称的函数
fix_directory_names(root_download_dir)

print("所有目录名称已修复！")