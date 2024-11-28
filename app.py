from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/proxy": {"origins": "http://maiiiiin-lxnm5lopl-uglstphns-projects.vercel.app"}})


@app.route('/', methods=['OPTIONS'])
def options():
    return '', 200  # Возвращаем статус 200 для OPTIONS запроса


@app.route('/hello')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Простое Flask приложение</title>
    </head>
    <body>
        <h1>Добро пожаловать в Flask!</h1>
        <p>Это простое приложение, отображающее HTML-страницу.</p>
    </body>
    </html>
    '''


@app.route("/proxy", methods=["POST"])
@cross_origin()
def proxy():
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Проверяем обязательные параметры
    if "url" not in data or "type" not in data:
        return jsonify({"error": "Missing required parameters: url and type"}), 400

    url = data["url"]
    request_type = data["type"].upper()
    params = {key: value for key, value in data.items() if key in ["id", "dateBegin", "dateEnd"]}

    if request_type not in ["GET", "POST"]:
        return jsonify({"error": "Invalid request type. Supported types are GET and POST"}), 400

    try:
        # Выполняем запрос в зависимости от типа
        if request_type == "GET":
            response = requests.get(url, params=params)
        elif request_type == "POST":
            response = requests.post(url, json=params)
        
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

#if __name__ == "__main__":
#    app.run(debug=True)
