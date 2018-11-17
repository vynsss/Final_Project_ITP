import discord
import asyncio
from message_content import MyClient
from flask import Flask, request
import threading


client = MyClient()
token = "secret token"

#loop every events that is happening in my github repository
loop = asyncio.get_event_loop()

#https://www.youtube.com/watch?v=YMBzb_RBDAA
def flask_app():
    app = Flask(__name__)

    @app.route('/github', methods=['POST'])
    def github_webhook():
        jmsg = request.json
        msg_send = jmsg['sender']['login'] + ' pushed to github'
        loop.create_task(client.send_github_notif(msg_send))
        print(jmsg)
        return 'Successful'

    print('Flask App Starting')
    app.run()


t = threading.Thread(target=flask_app)
t.start()

client.run(token)
