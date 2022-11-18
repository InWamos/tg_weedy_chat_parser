from pyrogram import Client, filters
import asyncio
import json
import os
import sys

# Checks the packages   
if "config.json" in os.listdir():

    with open("config.json", 'r') as json_file:
        data = json.loads(json_file.read())

else:
    with open("config.json", 'x') as json_file:
        json_file.write('{}')
    
    with open("config.json", 'r') as json_file:
        data = json.loads(json_file.read())

    data["api_hash"] = None
    data["api_id"] = None
    data["target_chat_id"] = None
    data["run_as_admin"] = False

    with open('config.json', 'w') as json_file:
        json_file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))    

if "goyim_data.json" not in os.listdir():

    with open("goyim_data.json", 'x') as json_file:
        json_file.write('{}')

else:
    with open("goyim_data.json", 'w') as json_file:
        json_file.write('{}')


if "text.txt" not in os.listdir():

    with open('text.txt', 'x') as text_file:
        pass

else:
    rewrite_txt_input = input("ATTENTION! This will rewrite your previous text.txt!(-e to exit)")
    if rewrite_txt_input == '-e': sys.exit("Program stopped")

    with open('text.txt', 'w') as text_file:
        text_file.write('')


# Prints out the art, info about config and commands

print(f"""

                     .                          
                     M                          
                    dM                          
                    MMr                         
                   4MMMI                  .     
                   MMMMM.                xf             [API_ID]: {data["api_id"]}
   .              "MMMMM               .MM-             [API_HASH]: {data["api_hash"]}
    Mh..          +MMMMMM            .MMMM              [TARGET_CHAT]: {data["target_chat_id"]}
    .MNM.         .MMMMML.          MMMMMh              
     )MMMh.        MMWMMM         MMMMMMM               [COMMANDS]:
      3MMMMx.     'MMMMMMf      xnMMMMMM"               
      '*MMMMM      MMMMMM.     nMMMAMMP"                -c        Change api id and hash (e.g. -c 12345354 hash)
        *MMMMMx    "MMMMM\    .MMMMMMM=                 {'-' * 3}
         *MMMMMh   "MMMMM"   JMMOMMMP                   -g        Set the chat id (e.g. -g -643222694)
           MMMMMM   3MMMM.  dMMMMMM            .        {'-' * 3}
            MMMMMM  "MMMM  .MMMMM(        .nnMP"        -i        Get the config info
=..          *MMMMx  MSM"  dMMMM"    .nnMMMMM*          {'-' * 3}
  "MMn...     'MMMMr 'MM   MMM"   .nMMMMMMM*"           -r        Save changes and run programm (-r a for admin)
   "4MMMMnn..   *MMM  MM  MMP"  .dMMMMMMM""             {'-' * 3}
     ^MMMMMMMMx.  *ML "M .M*  .MMMMMM**"                -e        Close programm
        *PMMMMMMhn. *x > M  .MMMM**""                   {'-' * 3}
           ""**MMMMhx/.h/ .=*"                          
                    .3P"%....                           
                  nP"     "*MMnx   By: seniornamedw@proton.me

""")


def handle_the_configurator():

    while True:

        initial_input = input("Enter command: ")

        if initial_input.startswith('-c'):

            try:

                data["api_id"] = initial_input.split(' ')[1]
                data["api_hash"] = initial_input.split(' ')[2]

                with open('config.json', 'w') as json_file:
                    json_file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

                print(f"[api_id]: {initial_input.split(' ')[1]}\n[api_hash]: {initial_input.split(' ')[2]}")


            except Exception as e:

                print("Wrong data, cant split!")


        elif initial_input.startswith('-g'):

            try:

                data["target_chat_id"] = int(initial_input.split('-')[2]) * -1

                with open('config.json', 'w') as json_file:
                    json_file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

                print("Target chat id:" + str(data["target_chat_id"]))
            except Exception as e:
                print("Wrong data, cant split!")


        elif initial_input.startswith('-i'):

            print(f'\n[api_id]: {data["api_id"]}\n[api_hash]: {data["api_hash"]}\n[target_chat]: {data["target_chat_id"]}\n')
        

        elif initial_input.startswith('-r'):
            with open("config.json", 'r') as json_file:
                data = json.loads(json_file.read())

            if data["api_id"] == None or data["api_hash"] == None or data["target_chat_id"] == None:

                print("Api id, api hash and chat_id are required!") 
                continue

            print("Changes saved!")

            if initial_input == '-r a':
                data["run_as_admin"] = True
                print("Admin mode activated")
            else:
                data["run_as_admin"] = False
                

            with open('config.json', 'w') as json_file:
                json_file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

            break
        
        elif initial_input.startswith('-e'):
            sys.exit("Exiting...")

        else: print("Unknown command!")
        
def parse_chat_if_member(chat_id):

    app = Client("my_account", data['api_id'], data['api_hash'])

    @app.on_message(filters.group)
    async def hello(client, message):

        with open('goyim_data.json', 'r', encoding='utf-8') as json_file:
            data = json.loads(json_file.read())

        if (message.chat.id == chat_id) and (message.from_user.username != None):

            if str(message.from_user.id) not in data:
                data[str(message.from_user.id)] = {
                    "goy_messages_count": 1,
                    "goy_nickname": f'@{message.from_user.username}'
                }

            else:
                data[str(message.from_user.id)]["goy_messages_count"] += 1

                if f'@{message.from_user.username}' != data[str(message.from_user.id)]["goy_nickname"]:
                    data[str(message.from_user.id)]["goy_nickname"] = f'@{message.from_user.username}'


            with open('goyim_data.json', 'w') as json_file:
                json_file.write(json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False))

    try:
        app.run()
    except:
        app.stop()
        print(f'\nStopped!{Exception}')


async def parse_chat_if_admin(chat_id):

    NUMBER_OF_MESSAGES = 0
    MEMBERS_PARSED = 0

    async with Client("my_account", data['api_id'], data['api_hash']) as app:

        async for member in app.get_chat_members(chat_id):

            async for i in app.search_messages(chat_id, from_user=member.user.id):

                NUMBER_OF_MESSAGES += 1


            if NUMBER_OF_MESSAGES > 0 and member.user.username:
                MEMBERS_PARSED += 1

                with open('text.txt', 'a', encoding='utf-8') as text_file:
                    text_file.write(f'[NICKNAME]: @{member.user.username}\n[MESSAGES SENT]: {NUMBER_OF_MESSAGES}\n\n')

            NUMBER_OF_MESSAGES = 0
        
        print(f'Members parsed: {MEMBERS_PARSED}, data saved to text.txt')
            
def json_to_txt():

    MEMBERS_PARSED = 0

    with open('goyim_data.json', 'r') as json_file:
        data = json.loads(json_file.read())         
    
    for i in data:

        MEMBERS_PARSED += 1

        with open('text.txt', 'a') as text_file:
            text_file.write(f'[MEMBER]: {data[i]["goy_nickname"]}\n[MESSAGE_SENT]: {data[i]["goy_messages_count"]}\n\n\n')
    
    print(f'{MEMBERS_PARSED} members parsed. Result in text.txt')

        

if __name__ == "__main__":
    handle_the_configurator()

    if data["run_as_admin"] == True:
        asyncio.run(parse_chat_if_admin(data["target_chat_id"]))
    elif data["run_as_admin"] == False:
        parse_chat_if_member(data["target_chat_id"])
        json_to_txt()