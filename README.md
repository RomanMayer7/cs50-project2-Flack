# Project 2
Web Programming with Python and JavaScript
--------------------------------------------------------------------------------------------
#Project Name :Flack:"Chatroom for your Team"
--------------------------------------------------------------------------------------------
#Project Description
--------------------------------------------------------------------------------------------
This Chatroom style Web Application enables multiple users to communicate by joining existing and by creating the new channels.They can send text messages and attach images as well.

#Project Objectives
--------------------------------------------------------------------------------------------
*Build Chat Room Style Multichannel Web Application
*Use JavaScript to run code server-side.
*Building web user interfaces.
*Gain experience with Socket.IO to communicate between clients and servers.

#Project Structure
--------------------------------------------------------------------------------------------
*'flack.py' inside the main folder should be used in order to run the App.It have all ServerSide functionality and Backend Logic
written in the Python and generate HTML content of the page by Rendering the templates,which can be found 
inside the "Templates"  folder. 
*Inside the main folder there is "templates" folder with three HTML files:"index.html","layout.html","main.html"
Their contend of HTML and JavaScript code as well,which is FrontEnd UI/UX of  the Application.The "main.html"
uses AJAX requests as well in order to communicate with a Server
*Inside the main folder there is "static" folder with two subfolders :"static/img" and "static/uploads",which are reserved
for storing images and images uploads for the App.

#Functionalities and their Implementation
--------------------------------------------------------------------------------------------
*Display Name: When a user visits the web application for the first time, they should be prompted to type in a display name that will
eventually be associated with every message the user sends. User can change Display Name anytime  by clicking on 'login section'
inside the Navigation Bar.If a user closes the page and returns later, the display name
will still be remembered.This is Implemented through the  usage of Local Storage.
It possible to clear Browser's Local Storage by Removing the Cookies inside Browser's Advanced Settings Section

*Channel Creation: Any user is able to create a new channel, so long as its name doesn’t conflict with the name of an existing
channel.Channel Creation implemented in the backend by @app.route("/create_channel",methods=["POST"])
And in the Frontend by: $("#create").on('click', function() {...........}) which appends the new channel name to the content of the
unordered list inside the page;

*Channel List: Users are able to see a list of all current channels, and selecting one should allow the user to view the channel
Such List is present in Home Page and Channel Page as well,so user can switch fast  between the channels

*Messages View: Once a channel is selected, the user can see any messages that have already been sent in that channel, up to a
maximum of 100 messages.According to Requirement of this Assignment there is no Database for this App. 
The messages are stored in Flask's Backend Server-Side memory inside 'messages' object.There is 'IF' condition in Backend Logic
which checks the length of messages["channel_name"] array.In case it exceeds 100:it will pop out the old message in order to keep
the constant number of the messages:equals to 100

*Sending Messages: Once in a channel, users are able to send text messages to others the channel. When a user sends a
message, their display name and the timestamp of the message should be associated with the message.
Timestap is generated inside the FrontEnd's JavaScript function:"getCurrentDate()",declared inside the <script> tag
of the "main.html" file. All users in the channel can see the new message (with display name and timestamp) appear on their channel page. 
Sending and receiving messages is not requiring to reload the page:The App updates the HTML content of the pagethrough JavaScript.
Sending Messages functionality implemented in the BackEnd by @app.route("/add_message",methods=["POST"])
which  actually adds a message's content to Server's Memory,
And the FrontEnd inside: $('#sendbutton').on('click', function() {...} function);
which sends message to the IO Socket for  the particular NameSpace(which corresponds the channel's name)
 by calling socket.emit('message',{'msg': $('#myMessage').val(),'img':ipath}); So the message is transmited to the Backend
and there is handeled and when retransmitted to all sockets,which are listening to this particular namespace by this  code snippet :
 @socketio.on('message',namespace="/channels/"+x)
  def handleMessage(data):  emit("message", data, broadcast=True)
When  in FrontEnd :socket.on('message', function(data) {...}); is listening for message,and when recieving it,it will update
HTML content of the page by generating and appending to it the message representation
In the end all users which are sitting on this particular channel should simultaniosly see the new message appearing on the page 

*Image Attachments:Users can make an image attachment to their Messages.The user need to choose filename and when
press "attach button" By doing this user will initiate File Upload route in the Server:@app.route('/upload_file', methods=['GET', 'POST'])
 and the chosen file will be apploaded  to the "static/upload folder" .When user  can add some text to the message and press "Send"
button to append message+image to the channnel's  page

*Delete User's Own Messages:
User can delete his own messages by clicking on [x] inside the messagebox.The App will perform check and in case the current user
is not actual creator of the message it will drop error message.In other case it will call BackEnd function
 @app.route("/del_message",methods=["POST"])  def del_message(): In order to remove the message from Server's Memory
As well the  message will be removed from HTML content of the page by FrontEnd function:  $(".close").on('click', function() {...});
----------------------------------------------------------------------------------------
by Roman Meyerson @ 2019/Started :Feb 8, 2019-Finished:Feb 13, 2019
