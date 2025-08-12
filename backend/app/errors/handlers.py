from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'message': '请求参数错误'}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'message': '未授权访问'}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'message': '禁止访问'}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'message': '资源不存在'}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'message': '请求方法不允许'}), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'message': '服务器内部错误'}), 500
