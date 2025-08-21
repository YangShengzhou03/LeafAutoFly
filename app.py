from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

from data_manager import (
    load_tasks, load_ai_data, load_home_data, add_task, delete_task, update_task_status, clear_tasks, import_tasks,
    save_ai_settings, add_ai_history, reply_history, get_ai_stats
)


app = Flask(__name__)
CORS(app)

load_tasks()
load_ai_data()


@app.route('/')
def home():
    return redirect('http://localhost:8080')


@app.route('/auto-info')
def auto_info():
    return redirect('http://localhost:8080/auto_info')


@app.route('/ai-takeover')
def ai_takeover():
    return redirect('http://localhost:8080/ai_takeover')

@app.route('/other_box')
def other_box():
    return redirect('http://localhost:8080/other_box')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(load_tasks().values()))


@app.route('/api/tasks', methods=['POST'])
def add_task_route():
    task_data = request.json
    new_task = add_task(task_data)
    return jsonify(new_task), 201


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)
    if success:
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status_route(task_id):
    data = request.json
    if 'status' not in data:
        return jsonify({'error': 'Status field is required'}), 400

    updated_task = update_task_status(task_id, data['status'])
    if updated_task:
        return jsonify(updated_task), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks', methods=['DELETE'])
def clear_tasks_route():
    clear_tasks()
    return jsonify({'success': True}), 200


@app.route('/api/tasks/import', methods=['POST'])
def import_tasks_route():
    try:
        tasks_data = request.json
        if not isinstance(tasks_data, list):
            return jsonify({'error': '请求数据必须是一个任务列表'}), 400

        success_count, total_count = import_tasks(tasks_data)
        return jsonify({
            'success': True,
            'imported': success_count,
            'total': total_count,
            'message': f'成功导入 {success_count}/{total_count} 个任务'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai-settings', methods=['GET'])
def get_ai_settings():
    return jsonify(load_ai_data())


@app.route('/api/ai-settings', methods=['POST'])
def save_ai_settings_route():
    settings_data = request.json
    saved_settings = save_ai_settings(settings_data)
    return jsonify(saved_settings), 200


@app.route('/api/ai-history', methods=['GET'])
def get_ai_history():
    return jsonify(reply_history)


@app.route('/api/ai-history', methods=['POST'])
def add_ai_history_route():
    history_data = request.json
    new_history = add_ai_history(history_data)
    return jsonify(new_history), 201


@app.route('/api/home-data', methods=['GET'])
def get_home_data():
    return jsonify(load_home_data())


@app.route('/api/ai-stats', methods=['GET'])
def get_ai_stats_route():
    stats = get_ai_stats()
    return jsonify(stats)


@app.route('/api/stats/<range>', methods=['GET'])
def get_chart_data(range):
    if range == '7d':
        return jsonify({
            "stats": {
                "replyRate": 10,
                "averageTime": 80,
                "satisfactionRate": 70
            },
            "chartData": {
                "dates": ["2023-09-01", "2023-09-02", "2023-09-03", "2023-09-04"],
                "counts": [30, 90, 30, 15]
            }
        })
    elif range == '30d':
        return jsonify({
            "stats": {
                "replyRate": 100,
                "averageTime": 50,
                "satisfactionRate": 50
            },
            "chartData": {
                "dates": ["2023-09-01", "2023-09-02", "2023-09-03", "2023-09-04"],
                "counts": [10, 90, 30, 15]
            }
        })
    else:
        return jsonify({
            "stats": {
                "replyRate": 100,
                "averageTime": 10,
                "satisfactionRate": 20
            },
            "chartData": {
                "dates": ["2023-09-01", "2023-09-02", "2023-09-03", "2023-09-04"],
                "counts": [10, 60, 23, 15]
            }
        })


if __name__ == '__main__':
    print('正在仅启动Flask后端服务器...')
    app.run(debug=True)
