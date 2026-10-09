#!/usr/bin/env python3
"""Fix bbcworldnews RSS links to use jsDelivr instead of ghproxy."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent
xml_path = root / "bbc_world.xml"
readme_path = root / "README.md"

if not xml_path.exists():
    raise SystemExit("请把本脚本放到仓库根目录，与 bbc_world.xml 放在同一目录。")

xml = xml_path.read_text(encoding="utf-8")
fixed = re.sub(
    r"https://ghproxy\.net/https://raw\.githubusercontent\.com/([^/<]+/[^/<]+)/main/",
    r"https://cdn.jsdelivr.net/gh/\1@main/",
    xml,
)
fixed = re.sub(
    r"https://raw\.githubusercontent\.com/([^/<]+/[^/<]+)/main/",
    r"https://cdn.jsdelivr.net/gh/\1@main/",
    fixed,
)
xml_path.write_text(fixed, encoding="utf-8")

if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
    readme = readme.replace(
        "https://ghproxy.net/https://raw.githubusercontent.com/zukuxi/bbcworldnews/main/bbc_world.xml",
        "https://cdn.jsdelivr.net/gh/zukuxi/bbcworldnews@main/bbc_world.xml",
    )
    readme = readme.replace(
        "https://raw.githubusercontent.com/zukuxi/bbcworldnews/main/bbc_world.xml",
        "https://cdn.jsdelivr.net/gh/zukuxi/bbcworldnews@main/bbc_world.xml",
    )
    readme_path.write_text(readme, encoding="utf-8")

print("已处理 bbc_world.xml 和 README.md。")
print("RSS 订阅地址：https://cdn.jsdelivr.net/gh/zukuxi/bbcworldnews@main/bbc_world.xml")
print("注意：本脚本只修改现有文件；如果项目有自动生成 RSS 的脚本，还需要在生成脚本中同步改链接，避免下次更新被覆盖。")
