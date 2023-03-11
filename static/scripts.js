

document.addEventListener('DOMContentLoaded', () =>{
  var socket = io.connect('https://' + document.domain + ':'+ location.port);
  
  // socket.on('connect', function(){
  //   socket.send({'msg': 'successfully connected'})
  //   console.log('connected')
  // }
    //)
  //sends the message to the server
  var messageButton = document.querySelector('#send-btn');
  var messageInput = document.querySelector('#message-input');
  messageButton.onclick = function(e){
    
    socket.send({'msg': messageInput.value});
    messageInput.value = ''
  };
  let directMessage = document.querySelector('.direct-chat-messages');
  //reciece message from the server
  socket.on('message', function(data){
      const div = document.createElement('div');
      div.setAttribute('class', 'direct-chat-text')
      const p = document.createElement('p');
      //const span_timestamp = document.createElement('small');
      const br = document.createElement('br');
      const hr = document.createElement('hr');
      //span_timestamp.innerHTML = data.time_stamp;
      //span_timestamp.class = "msg_time";
      p.innerHTML =  data.msg ;
      div.innerHTML = p.outerHTML
      var messageDisplay = document.querySelector('#message-display');
      var timeDisplay = document.querySelector('.direct-chat-timestamp');
      //messageDisplay.append(p);
      directMessage.append(div)
      
    }
  );
  //recv gpt response
  socket.on('gpt-response', (data)=>{
    const div = document.createElement('div');
    
    const right = document.createElement('div');
    right.setAttribute('class', 'right','direct-chat-msg')
    
    const info = document.createElement('div');        
    info.setAttribute('class', 'direct-chat-info clearfix')
    
    const name = document.createElement('span')
    name.setAttribute('class', 'direct-chat-name', 'pull-right')
    
    const time = document.createElement('span')
    time.setAttribute('class', 'direct-chat-timestamp', 'pull-left')
    
    const text = document.createElement('div')
    text.setAttribute('class', 'direct-chat-text')

    div.setAttribute('class', 'direct-chat-text')
    const p = document.createElement('p');
    //const span_timestamp = document.createElement('small');
    const br = document.createElement('br');
    const hr = document.createElement('hr');
    //span_timestamp.innerHTML = data.time_stamp;
    //span_timestamp.class = "msg_time";
    p.innerHTML =  data;
    text.innerHTML = p.outerHTML
    
    info.innerHTML= name.outerHTML + time.outerHTML
    right.innerHTML = info.outerHTML + text.outerHTML

    var gptMessageDisplay = document.querySelector('#gpt-message-display');
    var gptTimeDisplay = document.querySelector('#gpt-timestamp');
    //gptMessageDisplay.append(p);
    directMessage.append(right)
  })

  });


//const right = document.createElement('div');        
//right.setAttribute('class', 'right','direct-chat-msg')

