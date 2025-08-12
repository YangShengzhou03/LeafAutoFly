class Example:
    def __init__(self, id, title, content, author_id, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """转换为字典用于JSON序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建Example实例"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            content=data.get('content'),
            author_id=data.get('author_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
