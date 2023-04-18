import discord
import subprocess
import signal

def command_run():
    subprocess.Popen(['python','manage.py','runserver','0.0.0.0:8000'] , shell=True,cwd='FOLDER_PATH')
    result = subprocess.run('ipconfig', shell=True, capture_output=True , text=True)
    hash_result = result.stdout.split()
    index_num = [n for n, v in enumerate(hash_result) if v.startswith('192')]
    return hash_result[index_num[0]]

def command_down():
    result = subprocess.run(['WMIC','PROCESS','GET','Caption,ProcessId,CommandLine','/FORMAT:LIST'], shell=True, capture_output=True , text=True)
    hash_result = result.stdout.split()
    index_num = [n + 1 for n, v in enumerate(hash_result) if v == '0.0.0.0:8000']
    for i in index_num:
        command = ['taskkill', '/f', '/pid', hash_result[i][10:]]
        subprocess.run(command, shell=True)

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$run'):
        address = command_run()
        await message.channel.send("#successfully build server")
        await message.channel.send(f'#Go http://{address}:8000/')


    if message.content.startswith('$down'):
        command_down()
        await message.channel.send("#server stopping")
        await message.channel.send("#goodbye sigtal")

client.run('DISCORD_TOKEN')
