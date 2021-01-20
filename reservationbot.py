import discord
import asyncio
from datetime import date

class MyClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity=discord.Game('#help'))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    t = 30.0
    queue = {}
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('#reserve'):
            entry = []
            await message.channel.send('Please select a room to reserve (1 - 5).')
            def is_digit(m):
                return m.author == message.author and m.content.isdigit() and int(m.content) >= 1 and int(m.content) <= 5
            try:
                number = await self.wait_for('message', check=is_digit, timeout=self.t)
            except asyncio.TimeoutError:
                return await message.channel.send('Reservation cancelled.')
            
            await message.channel.send('Please enter a time range.')
            def is_time(m):
                return m.author == message.author
            try:
                time = await self.wait_for('message', check=is_time, timeout=self.t)
            except asyncio.TimeoutError:
                return await message.channel.send('Reservation cancelled.')
            
            if int(number.content) not in self.queue:
                self.queue[int(number.content)] = []
            today = date.today()
            self.queue[int(number.content)].append([str(time.content),str(message.author),str(today.strftime("%m/%d/%Y"))])
            await message.channel.send('Successfully reserved.')
            
        if message.content.startswith('#remove'):
            await message.channel.send('Enter valid room number:')
            def queue_remove(m):
                return m.author == message.author and m.content.isdigit() and int(m.content) in self.queue
            try:
                room = await self.wait_for('message', check=queue_remove, timeout=self.t)
            except asyncio.TimeoutError:
                return await message.channel.send('Removal cancelled.')
            if len(self.queue[int(room.content)]) == 1:
                self.queue = {}
            else:
                await message.channel.send('Enter the entry number (1 to ' + str(len(self.queue[int(room.content)])) + '):')
                def is_valid_remove(m):
                    return m.author == message.author and m.content.isdigit() and int(m.content) >= 1 and int(m.content) < len(self.queue[int(room.content)])
                try:
                    number = await self.wait_for('message', check=is_valid_remove, timeout=self.t)
                except asyncio.TimeoutError:
                    return await message.channel.send('Removal cancelled.')
                del self.queue[int(room.content)][int(number.content)]
            await message.channel.send('Successfully removed.')
            
        if message.content.startswith('#help'):
            await message.channel.send('Commands: #reserve, #remove, #queue, #clear')

        if message.content.startswith('#queue'):
            await message.channel.send('Current reservations: ')
            for key in self.queue:
                await message.channel.send(str(key) + ': ' + str(self.queue[key]))

        if message.content.startswith('#clear'):
            await message.channel.send('Are you sure you want to clear? y/n')
            def is_yn(m):
                return m.author == message.author and m.content == 'y' or m.content == 'n'
            try:
                yn = await self.wait_for('message', check=is_yn, timeout=self.t)
            except asyncio.TimeoutError:
                return await message.channel.send('Clearing cancelled.')
            if str(yn.content) == 'y':
                self.queue = {}
                await message.channel.send('Queue cleared.')
            else:
                await message.channel.send('Clearing cancelled.')
    
client = MyClient()
client.run('ODAxMjA2OTMwMjY5NjY3Mzk5.YAdUGQ.3H4YMRa35ZzMuDOOdDC_xBKL03Q')
