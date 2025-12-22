import os
from phone_agent.commconfig import step,stepfilename
base=os.getcwd()
file_base=os.path.join(base,step)
if not os.path.exists(file_base):
    os.makedirs(file_base)
filename=os.path.join(file_base,stepfilename)
def create_txt_file(content=""):
    """创建一个 txt 文件并写入内容（如果文件已存在，会被覆盖）"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 文件 '{filename}' 创建成功。")
    except Exception as e:
        print(f"❌ 创建文件失败: {e}")

def append_to_txt_file( content):
    """向指定 txt 文件末尾追加内容（如果文件不存在，会自动创建）"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(str(content)+"\n")
        print(f"✅ 内容已追加到 '{filename}'。")
    except Exception as e:
        print(f"❌ 追加内容失败: {e}")

def delete_txt_file():
    """删除指定的 txt 文件"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✅ 文件 '{filename}' 已删除。")
        else:
            print(f"⚠️ 文件 '{filename}' 不存在，无法删除。")
    except Exception as e:
        print(f"❌ 删除文件失败: {e}")
def read_txt_without_newline():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return []