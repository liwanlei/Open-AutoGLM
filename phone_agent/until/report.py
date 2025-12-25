import os

def add_image_to_html_report(image_paths, output_html="report.html", title="AutoGLM测试报告"):
    """
    将一组本地图片路径写入 HTML 报告中。

    :param image_paths: 图片路径列表（可以是绝对路径或相对路径）
    :param output_html: 输出的 HTML 文件名，默认为 'report.html'
    :param title: HTML 页面标题
    """
    valid_paths = [os.path.join(image_paths, image_path) for image_path in os.listdir(image_paths) if image_path.endswith(".png")]


    # 构建 HTML 内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        img {{ max-width: 100%; height: auto; margin: 10px 0; border: 1px solid #ccc; }}
        .image-container {{ margin-bottom: 30px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
"""

    for img_path in valid_paths:
        # 转换为相对于 HTML 文件的路径（如果需要可跨平台显示）
        # 这里直接使用原路径，浏览器会尝试加载（注意：本地 file:// 协议下路径需正确）
        # 若部署到 Web 服务器，建议使用相对路径或 URL
        html_content += f'    <div class="image-container">\n'
        html_content += f'        <img src="{img_path}" alt="Image">\n'
        html_content += f'    </div>\n'

    html_content += """</body>
</html>"""

    # 写入文件
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML 报告已生成：{os.path.abspath(output_html)}")