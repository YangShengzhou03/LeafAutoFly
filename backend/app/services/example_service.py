from app.config import Config
from app.models.example import Example
from app.utils.helpers import read_json_file, write_json_file, generate_id, get_current_timestamp

def get_examples():
    """获取所有示例数据"""
    examples_data = read_json_file(Config.EXAMPLES_JSON_PATH)
    return [Example.from_dict(data) for data in examples_data]

def get_example_by_id(example_id):
    """通过ID获取示例数据"""
    examples = get_examples()
    for example in examples:
        if example.id == example_id:
            return example
    return None

def get_examples_by_author(author_id):
    """通过作者ID获取示例数据"""
    examples = get_examples()
    return [e for e in examples if e.author_id == author_id]

def create_example(title, content, author_id):
    """创建新示例数据"""
    # 创建新示例
    example = Example(
        id=generate_id(),
        title=title,
        content=content,
        author_id=author_id
    )
    
    # 设置时间戳
    timestamp = get_current_timestamp()
    example.created_at = timestamp
    example.updated_at = timestamp
    
    # 保存到JSON文件
    examples = get_examples()
    examples.append(example)
    write_json_file(Config.EXAMPLES_JSON_PATH, [e.to_dict() for e in examples])
    
    return example

def update_example(example_id,** kwargs):
    """更新示例数据"""
    examples = get_examples()
    for i, example in enumerate(examples):
        if example.id == example_id:
            # 更新字段
            if 'title' in kwargs:
                example.title = kwargs['title']
            if 'content' in kwargs:
                example.content = kwargs['content']
            
            # 更新时间戳
            example.updated_at = get_current_timestamp()
            
            # 保存更改
            examples[i] = example
            write_json_file(Config.EXAMPLES_JSON_PATH, [e.to_dict() for e in examples])
            return example
    
    return None

def delete_example(example_id):
    """删除示例数据"""
    examples = get_examples()
    examples = [e for e in examples if e.id != example_id]
    write_json_file(Config.EXAMPLES_JSON_PATH, [e.to_dict() for e in examples])
    return True
