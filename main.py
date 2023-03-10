from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import openai
from flask_socketio import SocketIO, send, emit


openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

# sqlite database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='sqlite:///database'
db = SQLAlchemy(app)
socketio = SocketIO(app)
class HumanChats(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_sent = db.Column(db.DateTime)
  content = db.Column(db.Text)
  # chat_img = db.Column(db.String(100))
  #foreign key to link to other tables
  chater_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  response_content = db.relationship('ChatGptChats', backref='gpt')

  
class ChatGptChats(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_sent = db.Column(db.DateTime)
  gpt_response = db.Column(db.Text)
  # chat_img = db.Column(db.String(100))
  #foreign key to link to other tables
  human_chat_id = db.Column(db.Integer, db.ForeignKey('human_chats.id'))
  
#define the Users table
class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(250))
  email = db.Column(db.String(250))
  password = db.Column(db.String(256))
  #profile_pic = db.Column(db.String(250), default='user.png')
  #pic_file_path = db.Column(db.String(256))
  date_joined = db.Column(db.DateTime)
  #user can have many chats
  chat = db.relationship('HumanChats', backref='chater')
    
  
@app.route('/')
def index():
  start_sequence = "\nAI:"
  restart_sequence = "\nHuman: "
  #user = Users(username='john', email='john@gmail.com', password='12345678', date_joined=datetime.now())
  #db.create_all()
  #db.session.add(user)
  #db.session.commit()

  human_chats = HumanChats.query.all()
  back_gpt = ChatGptChats.query.all()
  
  return render_template("index.html", human_chats=human_chats, back_gpt=back_gpt)

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
  
  gpt_chats = ChatGptChats(date_sent=datetime.now(), gpt_response=response["choices"][0]["text"])
  print('response@ ',response["choices"][0]["text"])
  db.create_all()
  db.session.add(gpt_chats)
  db.session.commit()
  
  emit('gpt-response', response["choices"][0]["text"])
  send({'msg':data['msg']})
  
  human_chats = HumanChats(date_sent=datetime.now(), content=data["msg"])
  db.create_all()
  db.session.add(human_chats)
  db.session.commit()
  
  return data
  #sends the message to event called message


if __name__ == "__main__":
  socketio.run(app, debug=True)
