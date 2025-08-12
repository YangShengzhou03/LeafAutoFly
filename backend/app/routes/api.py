from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.example_service import (
    get_examples, get_example_by_id, get_examples_by_author,
    create_example, update_example, delete_example
)

api = Blueprint('api', __name__)

@api.route('/examples', methods=['GET'])
def get_all_examples():
    """获取所有示例数据"""
    examples = get_examples()
    return jsonify([e.to_dict() for e in examples])

@api.route('/examples/<example_id>', methods=['GET'])
def get_single_example(example_id):
    """获取单个示例数据"""
    example = get_example_by_id(example_id)
    if not example:
        return jsonify({'message': '示例数据不存在'}), 404
    return jsonify(example.to_dict())

@api.route('/examples/my', methods=['GET'])
@login_required
def get_my_examples():
    """获取当前用户创建的示例数据"""
    examples = get_examples_by_author(current_user.id)
    return jsonify([e.to_dict() for e in examples])

@api.route('/examples', methods=['POST'])
@login_required
def create_new_example():
    """创建新的示例数据"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': '请提供标题和内容'}), 400
    
    example = create_example(
        title=data['title'],
        content=data['content'],
        author_id=current_user.id
    )
    
    return jsonify({
        'message': '示例数据创建成功',
        'example': example.to_dict()
    }), 201

@api.route('/examples/<example_id>', methods=['PUT'])
@login_required
def update_single_example(example_id):
    """更新示例数据"""
    example = get_example_by_id(example_id)
    
    if not example:
        return jsonify({'message': '示例数据不存在'}), 404
    
    # 检查权限
    if example.author_id != current_user.id:
        return jsonify({'message': '没有权限修改此数据'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'message': '请提供更新的信息'}), 400
    
    updated_example = update_example(example_id, **data)
    
    return jsonify({
        'message': '示例数据更新成功',
        'example': updated_example.to_dict()
    })

@api.route('/examples/<example_id>', methods=['DELETE'])
@login_required
def delete_single_example(example_id):
    """删除示例数据"""
    example = get_example_by_id(example_id)
    
    if not example:
        return jsonify({'message': '示例数据不存在'}), 404
    
    # 检查权限
    if example.author_id != current_user.id:
        return jsonify({'message': '没有权限删除此数据'}), 403
    
    delete_example(example_id)
    return jsonify({'message': '示例数据删除成功'})
