from flask import Flask, jsonify, request, render_template, Response
import json

app = Flask(__name__)

tasks = [
    # {'id': 1, 'text': '買牛奶', 'done': False},
    # {'id': 2, 'text': '寫作業', 'done': False}
]
task_id_counter = 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods = ['GET']) #取得
def get_tasks():
    print("🟢 任務清單被讀取！目前任務數：", len(tasks))    #len(tasks) 計算陣列剩餘數量
    response = json.dumps(tasks)    #jsonify寫法：return jsonify(tasks)
    return Response(response, status=200, mimetype='application/json') # mimetype (只有flask用) 會自動變成 Content-Type (js只能用這個)

@app.route('/tasks', methods = ['POST'])    #新增
def add_task():
    global task_id_counter  # 如果不寫 global，Python 預設你是想在函式裡自己用一個新的變數，不會去動到外面的那個。
    data = request.get_json() #把前端送過來的資料（通常是 JSON 格式）讀出來，存進 data 這個變數。
    task_id_counter += 1  #把任務編號 task_id_counter 加 1
    new_task = {
        'id': task_id_counter,  # 任務 ID 為當前的 task_id_counter
        'text': data['text'],    # 從前端傳來的資料（data）中取出 'text' 欄位，作為任務的描述
        'finish': False
    }
    tasks.append(new_task)  #剛剛新建好的這個任務，加到 tasks 這個列表（list）裡 (tasks = [])
    print(f'➕ 加入了{new_task["text"]}任務')
    return jsonify(new_task),201 #把 Python 的字典（像 { "id": 1, "text": "買牛奶" }）轉成 JSON 格式，這樣前端才能懂你回什麼。

@app.route('/tasks/<int:task_id>/toggle', methods = ['POST'])   #更新
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['finish'] = not task['finish'] #預設是 False
            print(f'✔️  完成了{task['text']}任務')
            return jsonify(task),200 
    # return jsonify({"error": "Task not found"}), 404    #js刪除按鈕沒阻止冒泡，如果按過完成再刪除會顯示沒有任務

@app.route('/tasks/<int:task_id>', methods = ['DELETE'])    #刪除
def delete_task(task_id):   #task_id 是傳進來的參數，代表「要刪掉哪個任務的id」
    global tasks    #要用外面那個全域的 tasks 變數 要改 tasks 的內容（把不要的任務刪掉）
    new_tasks = []      #推導式寫法：tasks = [task for task in tasks if task["id"] != task_id]
    for task in tasks:
        if task['id'] != task_id:  #不等於 task_id 
            new_tasks.append(task)
    tasks = new_tasks
    response = {    #jsonify寫法：return jsonify({'message': 'deleted'}),200
        task['text']: 'deleted'    #字典 # 買牛奶 : "deleted"
    }
    json_response = json.dumps(response)    #使用 dumps 將 Python 字典轉換成 JSON 字串
    print(f'🔴 {task['text']}結束了')
    return Response(json_response,status=200, mimetype='application/json') 

if __name__ == '__main__':  #確保只有當這個檔案是直接執行時，才會執行後面的 
    app.run(debug=True)     #啟動 app.py 檔案會開啟 debug 模式，讓開發者能更方便地調試程式碼。
    # python app.py 會執行 Debug mode 
    # flask run 不會執行 Debug mode