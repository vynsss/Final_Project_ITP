# https://media.readthedocs.org/pdf/discordpy/latest/discordpy.pdf

import discord, asyncio
import requests, json

from user_data import user


userdata = {}
file = open("data.txt", "r")
data = file.read().split('\n')
for f in data:
    new = f.split(",")
    userdata[new[0]] = user(new[0], new[1], new[2], new[3], new[4], new[5], new[6])
file.close()


def view(key):
    d = userdata[key]
    return("userID: {}, name: {}, username: {}, usernumber: {}, age: {}, school: {}, major: {}".format(d.userid, d.name,d.username ,d.usernumber, d.age,d.school,d.major))


def write():
    temp = ''
    file = open("data.txt", "w")
    for d in userdata.values():
        temp += d.userid + "," + d.name + "," + d.username + "," + str(d.usernumber) + "," + str(d.age) + "," +d.school+","+ d.major + '\n'
    file.write(temp)
    file.close()



#https://www.youtube.com/watch?v=_0LXIvLDhBM&t=356s // https://github.com/FoggyIO/DiscordPythonBots
class MyClient(discord.Client):


    async def on_ready(self):
        print("Bot is online and connected to Discord!")


    async def send_github_notif(self, content):
        #id from channel id in discord server
        channel = discord.Object(id='508174256920723459')
        await self.send_message(channel, content)
        print('github notif sent')


    #for the bot respond to message
    async def on_message(self, message):


        #for test response message only
        if message.content.lower() == "hello":
            await self.send_message(message.channel, "hi")
        if message.content.lower() == "cookie":
            await self.send_message(message.channel, ":cookie:")


        #.lower() to prevent capital and lower letter differences
        if message.content.lower().startswith('!ping'):

            #userID, store the user id that said !ping / send the message
            userID = message.author.id
            await self.send_message(message.channel, "{} Pong!".format(userID))


        if message.content.lower().startswith('!say'):

            #separate the user input based on the spacing in the message into list
            args = message.content.split(" ")
            #[1:] to avoid including !say in the command
            await self.send_message(message.channel, "%s" % (" ".join(args[1:])))


        #view data from data.txt // only allow in string format
        if message.content.lower() == ".viewdata":

            for d in userdata.keys():
                await self.send_message(message.channel, view(d))


        #search data from data.txt based on the userID
        if message.content.lower().startswith(".searchdata"):

            search_data = message.content.split(" ")
            data = search_data[1]

            if data in userdata:
                await self.send_message(message.channel, view(data))


        #to add or edit data to userdata dictionary
        if message.content.lower().startswith(".editdata"):

            add_data = message.content.split(",")

            userid = add_data[1]
            name = add_data[2]
            username = add_data[3]
            usernumber = add_data[4]
            age = add_data[5]
            school = add_data[6]
            major = add_data[7]

            userdata[userid] = user(userid, name, username, usernumber, age, school, major)
            await self.send_message(message.channel, "The data successfully added or editted!")

            write()


        #to remove data from data.txt
        if message.content.lower().startswith(".remove"):

            remove_data = message.content.split(" ")
            number = str(remove_data[1])

            if number in userdata.keys():
                userdata.pop(number)
                await self.send_message(message.channel, "The data have been removed.")
            else:
                await self.send_message(message.channel, "The data/user number u inputted is not available or an error occured")

            write()


        #the currency converter
        #https://currency-api.appspot.com/
        if message.content.upper().startswith(".CURRENCY"):
            url = "http://www.apilayer.net/api/live?access_key=df1fa21b42994013fed11d8454508658&format=1"

            response = requests.get(url)

            spl = message.content.split(" ")
            # the currency to convert from
            convert_from = str(spl[1]).upper()
            # the currency to convert to
            convert_to = str(spl[2]).upper()
            amount = float(spl[3])

            #only need e.g. IDR as the input, not e.g. USDIDR
            convert_from = "USD" + convert_from
            convert_to = "USD" + convert_to

            #https://stackoverflow.com/questions/44766282/accessing-json-api-with-python?rq=1
            #checking for error
            if response.status_code != 200:
                await self.send_message(message.channel, "error {}".format(response.status_code))
            else:
                data = json.loads(response.text)

                if convert_from and convert_to in data["quotes"]:
                    from_number = float(data["quotes"][convert_from])
                    to_number = float(data["quotes"][convert_to])
                    total1 = "%.2f" % round(to_number / from_number * amount, 2)
                    await self.send_message(message.channel, "total converted amount: {}".format(total1))
                else:
                    await self.send_message(message.channel,"Sorry, the currency you are inputting are false or not available in the library")
