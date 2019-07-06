import os
from flask import Flask, jsonify, render_template, request,session,redirect, url_for,flash 
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_socketio import SocketIO, emit,send

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,static_url_path = "/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


messages = {}
channelist=["Work","Nature Lovers","Videogames","Party","Sport Club","Project X","Rock Music","College","Arts and Design","Computer Science","Travel"]
current_channel="Viva"

#allocating space for messages 
for c in channelist:
 messages[c] = []


@app.route("/")
def home():
    return render_template("index.html",clist=channelist)

@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
def channels(channel):
     print(channel)
     #change current chanel
     global current_channel
     current_channel=channel
     return render_template("main.html",channel=channel,channel_msg=messages[current_channel],clist=channelist)

@app.route("/add_message",methods=["POST"])
def add_message():
     print("Message trying to add")   
    	# put data recieved from request inside a dictionary
     my_data={"user":request.form.get("user"),"date":request.form.get("date"),"content":request.form.get("content"),"image":request.form.get("image")}
	# add data to the messages field reserved for requested channel 
     print(my_data)
     print(current_channel)
     messages[current_channel].append(my_data)
	# allow to store only the 100 most recent messages per channel
     if len(messages[current_channel]) > 100:
        messages[current_channel].pop(0)
     print("Message passed on!")
     return None 

@app.route("/del_message",methods=["POST"])
def del_message():
  counter=0
  print(request.form.get("targetcontent"))
  for msg in messages[current_channel]:
   print(msg)
   if msg["content"] == request.form.get("targetcontent"):
    messages[current_channel].pop(counter)
    print(messages)
   counter=counter+1 

@app.route("/create_channel",methods=["POST"])
def create_channel():
     newchannel=request.form.get("new_channel")
	#in case the channel name is already  taken
     print(newchannel)
     if newchannel in channelist:
       print("already in the list")
       return jsonify({"success":False})
     #if not  add channel to the list of channels
     else:
      channelist.append(newchannel)
      #allocate space in 'messages' for the newly created channel
      messages[newchannel] = []
       #creating separate namespace for socket requests, for this channel route
      @socketio.on('message',namespace="/channels/"+newchannel)
      def handleMessage(data):
          emit("message", data, broadcast=True)

      print(channelist)
      return jsonify({"success":True,"ch":newchannel})

#for all existing channels inside 'channelist' array creating separate socket request with it's namespace
#this socket request should return recieved message back to the socket
for x in channelist:
 @socketio.on('message',namespace="/channels/"+x)
 def handleMessage(data):
	 print('Message: ' + data['msg'])
	 emit("message", data, broadcast=True)
     

#HANDLING FILE UPLOADS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
         #if request.method == 'POST':
         #check if the post request has the file part
         #if 'file' not in request.files:
         #   flash('No file part')
          #  return redirect(request.url)
         #file = request.files['file']
        # if user does not select file, browser also
         #submit a empty part without filename
        # if file.filename == '':
       #     flash('No selected file')
        #    return redirect(request.url)
     file = request.files['file']
     if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
          #return when 'file uploaded successfully'
          return redirect(url_for('.channels',channel=current_channel))
       

if __name__ == '__main__':
	socketio.run(app)
     