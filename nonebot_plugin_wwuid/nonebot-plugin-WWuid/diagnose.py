# coding=utf-8
import sys
from pathlib import Path

# 创建标记文件来确认脚本是否运行
marker = Path(__file__).parent / "script_ran.marker"
with open(marker, 'w') as f:
    f.write("Script executed successfully\n")

# 测试基本功能
try:
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (100, 100), (255, 0, 0))
    output = Path(__file__).parent / "test_red.png"
    img.save(output)
    with open(marker, 'a') as f:
        f.write(f"Image created: {output}\n")
except Exception as e:
    with open(marker, 'a') as f:
        f.write(f"Error: {e}\n")

sys.exit(0)
