from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define chatbot pairs for New Businesses (Medical Tourism, MICE, Weddings)
pairs = [
    [r"(.)medical tourism(.)", 
     ["Medical tourism involves traveling to another country for medical treatment. At TBO, we offer digital solutions to streamline the booking process and enhance patient experiences."]],
    
    [r"(.)MICE(.)", 
     ["MICE (Meetings, Incentives, Conferences, Exhibitions) is a rapidly growing industry. TBO helps digitize and simplify event planning with customized tools."]],
    
    [r"(.)weddings(.)", 
     ["Destination weddings require extensive planning. TBO provides personalized wedding service databases, booking management, and end-to-end event coordination."]],
    
    [r"(.)how can TBO help(.)", 
     ["TBO offers digital innovations to streamline processes in medical tourism, MICE, and weddings, making bookings and management more efficient."]],
    
    [r"hi|hello|hey", 
     ["Hello! How can I assist you in medical tourism, MICE, or weddings?"]],
    
    [r"quit", 
     ["Goodbye! Feel free to return if you have more queries."]]
]

chatbot = Chat(pairs, reflections)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Please provide a message."})
    
    response = chatbot.respond(user_message)
    return jsonify({"response": response})

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

