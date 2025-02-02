from flask import Flask, request, jsonify
from nltk.chat.eliza import eliza_chat
from nltk.chat.iesha import iesha_chat
from nltk.chat.rude import rude_chat
from nltk.chat.suntsu import suntsu_chat
from nltk.chat.zen import zen_chat
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    if "medical" in user_message or "tourism" in user_message:
        response = eliza_chat() 
    
    elif "MICE" in user_message or "conference" in user_message:
        response = suntsu_chat()  

    elif "wedding" in user_message or "marriage" in user_message:
        response = iesha_chat()  

    elif "angry" in user_message or "bad service" in user_message:
        response = rude_chat() 

    elif "philosophy" in user_message or "business vision" in user_message:
        response = zen_chat()  

    else:
        response = "I'm not sure how to respond. Can you clarify your question?"

    return jsonify({"response": response})

if __name__ == '_main_':
    app.run(debug=True)