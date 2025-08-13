from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/auto-info')
def auto_info():
    return render_template('auto_info.html')


@app.route('/ai-takeover')
def ai_takeover():
    return render_template('ai_takeover.html')


@app.route('/second-page')
def second_page():
    return render_template('second_page.html')


@app.route('/task-list')
def task_list():
    return render_template('task_list.html')


if __name__ == '__main__':
    app.run(debug=True)
