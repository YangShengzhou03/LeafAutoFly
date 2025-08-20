import os
import re

# 定义不同文件类型的注释模式
COMMENT_PATTERNS = {
    # Python 注释: # 开头的行注释
    '.py': [
        (re.compile(r'#.*$'), ''),  # 单行注释
    ],
    # JavaScript 注释: // 单行注释和 /* */ 多行注释
    '.js': [
        (re.compile(r'//.*$'), ''),  # 单行注释
        (re.compile(r'/(\*[\s\S]*?\*/)', re.DOTALL), ''),  # 多行注释
    ],
    # CSS 注释: /* */
    '.css': [
        (re.compile(r'/(\*[\s\S]*?\*/)', re.DOTALL), ''),  # 多行注释
    ],
    # Vue 文件: 包含 HTML、JS 和 CSS 注释
    '.vue': [
        (re.compile(r'<!--[\s\S]*?-->'), ''),  # HTML 注释
        (re.compile(r'//.*$'), ''),  # JS 单行注释
        (re.compile(r'/(\*[\s\S]*?\*/)', re.DOTALL), ''),  # JS/CSS 多行注释
    ],
    # XML 注释
    '.xml': [
        (re.compile(r'<!--[\s\S]*?-->'), ''),  # XML 注释
    ],
    # JSON 通常没有注释，但有时会有
    '.json': [
        (re.compile(r'//.*$'), ''),  # 单行注释
        (re.compile(r'/(\*[\s\S]*?\*/)', re.DOTALL), ''),  # 多行注释
    ],
}

# 不需要处理的文件类型
IGNORE_EXTENSIONS = [
    '.pyc', '.svg', '.bat', '.iml', '.md', '.txt', '.json',
    '.gitignore', '.lock', '.license',
]

# 不需要处理的目录
IGNORE_DIRS = [
    '__pycache__', 'venv', '.idea',
]


def remove_comments(file_path):
    """移除文件中的注释"""
    # 获取文件扩展名
    ext = os.path.splitext(file_path)[1].lower()

    # 检查是否需要忽略该文件
    if ext in IGNORE_EXTENSIONS:
        return False

    # 检查是否有对应的注释模式
    if ext not in COMMENT_PATTERNS:
        return False

    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 应用注释移除模式
        original_content = content
        for pattern, replacement in COMMENT_PATTERNS[ext]:
            content = pattern.sub(replacement, content)

        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False


def process_directory(dir_path):
    """处理目录下的所有文件"""
    modified_files = 0

    for root, dirs, files in os.walk(dir_path):
        # 过滤掉不需要处理的目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            file_path = os.path.join(root, file)
            if remove_comments(file_path):
                modified_files += 1
                print(f"已移除注释: {file_path}")

    return modified_files


if __name__ == '__main__':
    # 指定要处理的目录
    target_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"开始处理目录: {target_dir}")

    # 处理目录
    modified_count = process_directory(target_dir)

    print(f"处理完成! 共修改了 {modified_count} 个文件。")