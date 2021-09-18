import os, discord, json
from colorama import Fore, init

client = discord.Client()
init()

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())


class Console():
    def main(self, username, id):
        os.system('cls && title Discord Message Searcher - Made By Kaneki Web')
        print(center(f"""

    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
    ███████╗█████╗  ███████║██████╔╝██║     ███████║█████╗  ██████╔╝  
    ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  ██╔══██╗
    ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║███████╗██║  ██║  
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝


            Login as: {Fore.CYAN + username + Fore.RESET} ({Fore.CYAN + id + Fore.RESET})

        """).replace('█', Fore.RED+"█"+Fore.RESET))


with open('config.json', 'r') as f:
    config = json.load(f)

@client.event
async def on_ready():
    Console().main(str(client.user), str(client.user.id))
    serveur_count = 0
    channels_count = 0
    messages_count = 0
    dm_count = 0

    for guild in client.guilds:
        print(f"[{Fore.RED}SERVER{Fore.RESET}] Scan du serveur: " + guild.name+ " "*30)
        serveur_count += 1
        for channel in guild.text_channels:
            print(f"[{Fore.CYAN}CHANNEL{Fore.RESET}] Scan du salon: " + channel.name + " "*30, end="\r")
            channels_count += 1
            try:
                channel = client.get_channel(channel.id)
                async for message in channel.history(limit=99999):
                    messages_count += 1
                    if config['message'] in message.content:
                        print(f"[{Fore.GREEN}MESSAGE{Fore.RESET}] Message Found: " + message.content)
                        open('found.txt', 'a+').write(f"{message.author.name}: {message.content}")
            except:
                pass
    
    for prv_channel in client.private_channels:
        channels_count += 1
        dm_count += 1
        username = str(prv_channel).replace('Direct Message with ', '')
        print(f"[{Fore.CYAN}CHANNEL{Fore.RESET}] Scan du DM: {username}" + " "*30, end="\r")
        channel = client.get_channel(prv_channel.id)
        async for message in channel.history(limit=99999):
            messages_count += 1
            if config['message'] in message.content:
                print(f"[{Fore.GREEN}MESSAGE{Fore.RESET}] Message Found: " + message.content)
                open('found.txt', 'a+').write(f"{message.author.name}: {message.content}")

    input(f"{Fore.RED+str(messages_count)+Fore.RESET} Messages on été scanné depuis {Fore.RED+str(channels_count)+Fore.RESET} Salons ({Fore.RED+str(serveur_count)+Fore.RESET} Serveurs, {Fore.RED+str(dm_count)+Fore.RESET} DMs)")


client.run(config["token"], bot=False)