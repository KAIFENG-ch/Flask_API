from flask import Flask, request, jsonify, abort

app = Flask(__name__)


tasks = []


@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        if not request.json or 'title' not in request.json:
            abort(400)
        task = {
            'id': len(tasks) + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False,
        }
        tasks.append(task)
        return jsonify({
            "status": 200,
            "message": "OK",
            "data": task,
        }), 201
    return jsonify({
        "status": 200,
        "message": "OK",
        "data": tasks,
    })


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    task[0]['done'] = not task[0]['done']
    return jsonify({
        "status": 200,
        "message": "OK",
        "data": tasks[task_id - 1],
    })


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({
        "status": 200,
        "message": "ok",
        "data": tasks,
    })


@app.route('/todo/api/v1.0/tasks/delete_all', methods=['DELETE'])
def delete_all_task():
    if len(tasks) == 0:
        abort(404)
    tasks.clear()
    return jsonify({
        "status": 200,
        "message": "ok",
        "data": tasks,
    })


@app.route('/todo/api/v1.0/tasks/status', methods=['DELETE'])
def delete_finish():
    status = bool(int(request.args.get("status")))
    task = list(filter(lambda f: f['done'] == bool(status), tasks))
    if len(task) == 0:
        abort(404)
    for items in task:
        tasks.remove(items)
    return jsonify({
        "status": 200,
        "message": "ok",
        "data": task
    })


@app.route('/todo/api/v1.0/tasks/<int:page>', methods=['GET'])
def find_all(page):
    max_size = 20
    page_num = int(len(tasks) / max_size + 1)
    task = []
    if page > page_num:
        abort(404)
    elif page <= 0:
        abort(404)
    elif page == page_num:
        for i in range((page - 1) * max_size, len(tasks)):
            task.append(tasks[i])
    else:
        for j in range((page - 1) * max_size, page * max_size):
            task.append(tasks[j])
    return jsonify({
        "status": 200,
        "message": 'ok',
        "data": tasks,
    })


@app.route('/todo/api/v1.0/tasks/status/<int:page>', methods=['GET'])
def find_status(page):
    max_size = 20
    status = bool(int(request.args.get('status')))
    task = list(filter(lambda f: f['done'] == status, tasks))
    page_num = int(len(task) / max_size + 1)
    if len(task) == 0:
        abort(404)
    task_ = []
    if page <= 0:
        abort(404)
    elif page > page_num:
        abort(404)
    elif page == page_num:
        for items in range((page - 1) * max_size, len(task)):
            task_.append(task[items])
    else:
        for j in range((page - 1) * max_size, page * max_size):
            task_.append(task[j])
    return jsonify({
        "status": 200,
        "message": "ok",
        "data": task,
    })


@app.route('/todo/api/v1.0/tasks/query', methods=["GET"])
def find():
    query = request.args.get('keyword')
    task = list(filter(lambda f: query in f['description'], tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({
        "status": 200,
        "message": "ok",
        "data": task,
    })


if __name__ == '__main__':
    app.run(port=8000, debug=True)
