import urllib.request
import xml.etree.ElementTree as ET
import trafilatura
import os
import shutil

# ==================== 你的 GitHub 信息 ====================
GITHUB_USER = "zukuxi"            
GITHUB_REPO = "bbcworldnews"       
# ==========================================================

# BBC RSS 源
url = "http://feeds.bbci.co.uk/news/world/rss.xml"
req = urllib.request.Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    print("正在连接 BBC 获取最新国际新闻...")
    with urllib.request.urlopen(req) as response:
        rss_data = response.read()

    root = ET.fromstring(rss_data)

    # 创建新的 RSS 结构
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "BBC World (kkgithub 纯净版)"
    ET.SubElement(channel, "link").text = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
    ET.SubElement(channel, "description").text = "完全使用 kkgithub 直连，彻底抛弃 ghproxy"

    if os.path.exists("html_articles"):
        shutil.rmtree("html_articles")
    os.makedirs("html_articles", exist_ok=True)

    items = root.findall('.//item')
    print(f"成功获取 {len(items)} 条新闻。开始生成专属 HTML 网页...")

    for i, item_node in enumerate(items):
        title = item_node.find('title').text
        original_link = item_node.find('link').text
        pub_date = item_node.find('pubDate').text if item_node.find('pubDate') is not None else ""

        article_text = ""
        if original_link:
            try:
                downloaded = trafilatura.fetch_url(original_link)
                if downloaded:
                    article_text = trafilatura.extract(downloaded)
            except Exception as e:
                print(f"提取失败: {e}")

        if not article_text:
            article_text = "正文抓取失败。该页面可能是交互式网页、纯视频，或者源网站限制了抓取。"

        html_content = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p><i>原文链接：<a href="{original_link}">{original_link}</a></i></p>
    <hr>
"""
        for para in article_text.split('\n'):
            if para.strip():
                html_content += f"    <p>{para.strip()}</p>\n"
        
        html_content += """</body>
</html>"""

        html_filename = f"news_{i+1}.html"
        with open(f"html_articles/{html_filename}", "w", encoding="utf-8") as f:
            f.write(html_content)

        # ✨ 【关键修改点】：给 x3 提供的每一篇文章链接，也全部使用通畅的 kkgithub！
        proxy_html_url = f"https://raw.kkgithub.com/{GITHUB_USER}/{GITHUB_REPO}/main/html_articles/{html_filename}"

        new_item = ET.SubElement(channel, "item")
        ET.SubElement(new_item, "title").text = title
        ET.SubElement(new_item, "link").text = proxy_html_url
        if pub_date:
            ET.SubElement(new_item, "pubDate").text = pub_date
        ET.SubElement(new_item, "description").text = "请点击标题进入阅读完整文章..."

    tree = ET.ElementTree(rss)
    tree.write("bbc_world.xml", encoding="utf-8", xml_declaration=True)
    print("✨ 大功告成！HTML 网页与 XML 订阅源已全部生成完毕！")

except Exception as e:
    print(f"运行发生崩溃: {e}")
