from flask import Flask, request, render_template, redirect

from datetime import datetime
import os
import openai
from flask_socketio import SocketIO, send, emit


openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)
socketio = SocketIO(app)

  
@app.route('/')
def index():
  start_sequence = "\nAI:"
  restart_sequence = "\nHuman: "
  
  return render_template("index.html")

#events handles
@socketio.on('message')
def message(data):
  print(data['msg'])
  #response from gpt
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=data["msg"],
    temperature=0.9,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
        )
  
  emit('gpt-response', response["choices"][0]["text"])
  send({'msg':data['msg']})
  #sends the message to event called message


if __name__ == "__main__":
  socketio.run(app, debug=True)
