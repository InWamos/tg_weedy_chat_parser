from pyrogram import Client
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

    with open('config.json', 'w') as json_file:
        json_file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))    


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
         *MMMMMh   "MMMMM"   JMMOMMMP                   -g        Set the group id (e.g. -g -643222694)
           MMMMMM   3MMMM.  dMMMMMM            .        {'-' * 3}
            MMMMMM  "MMMM  .MMMMM(        .nnMP"        -i        Get the config info
=..          *MMMMx  MSM"  dMMMM"    .nnMMMMM*          {'-' * 3}
  "MMn...     'MMMMr 'MM   MMM"   .nMMMMMMM*"           -r        Save changes and run programm
   "4MMMMnn..   *MMM  MM  MMP"  .dMMMMMMM""             {'-' * 3}
     ^MMMMMMMMx.  *ML "M .M*  .MMMMMM**"                -e        Close programm
        *PMMMMMMhn. *x > M  .MMMM**""                   {'-' * 3}
           ""**MMMMhx/.h/ .=*"                          
                    .3P"%....                           
                  nP"     "*MMnx       @KillTheRussians

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
                print(e)
                print("Wrong data, cant split!")


        elif initial_input.startswith('-i'):

            print(f'\n[api_id]: {data["api_id"]}\n[api_hash]: {data["api_hash"]}\n[target_chat]: {data["target_chat_id"]}\n')
        
        
        elif initial_input.startswith('-r'):
            print("Saving changes...")
            break
        
        elif initial_input.startswith('-e'):
            sys.exit("Exiting...")

        else: print("Unknown command!")
        


async def parse_chat(chat_id):

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
            
        
def main():
    handle_the_configurator()
    asyncio.run(parse_chat(data["target_chat_id"]))

if __name__ == "__main__":
    main()