from flask import Flask, request, jsonify, send_from_directory
from flask import Response
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Simple response logic
    response = "You said: " + user_message

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
