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
    arr = []
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('#reserve'):
            entry = []
            await message.channel.send('Please select a room to reserve (1 - 5).')
            def is_digit(m):
                return m.author == message.author and m.content.isdigit()
            try:
                number = await self.wait_for('message', check=is_digit, timeout=t)
            except asyncio.TimeoutError:
                return await message.channel.send('Reservation cancelled.')
            entry.append(str(number.content))
            await message.channel.send('Please enter a time range.')
            def is_time(m):
                return m.author == message.author
            try:
                time = await self.wait_for('message', check=is_time, timeout=t)
            except asyncio.TimeoutError:
                return await message.channel.send('Reservation cancelled.')
            entry.append(str(time.content))
            entry.append(str(message.author))
            today = date.today()
            entry.append(str(today.strftime("%m/%d/%Y")))
            self.arr.append(entry)
            await message.channel.send('Successfully reserved.')
            
        if message.content.startswith('#remove'):
            if len(self.arr) == 1:
                self.arr = []
            else:
                await message.channel.send('Enter the entry number (1 to ' + str(len(self.arr)) + '):')
            
                def is_valid_remove(m):
                    return m.author == message.author and m.content.isdigit() and int(m.content) >= 1 and int(m.content) < len(self.arr)

                try:
                    number = await self.wait_for('message', check=is_valid_remove, timeout=t)
                except asyncio.TimeoutError:
                    return await message.channel.send('Removal cancelled.')
                del self.arr[int(int(number.content) - 1)]
            await message.channel.send('Successfully removed.')
            
        if message.content.startswith('#help'):
            await message.channel.send('Commands: #reserve, #remove, #queue, #clear')

        if message.content.startswith('#queue'):
            await message.channel.send('Format: [Room Number, Time, Reservee, Date]')
            await message.channel.send('Current reservations: ' + str(self.arr))

        if message.content.startswith('#clear'):
            await message.channel.send('Are you sure you want to clear? y/n')
            def is_yn(m):
                return m.author == message.author and m.content == 'y' or m.content == 'n'
            try:
                yn = await self.wait_for('message', check=is_yn, timeout=t)
            except asyncio.TimeoutError:
                return await message.channel.send('Clearing cancelled.')
            if str(yn.content) == 'y':
                self.arr = []
                await message.channel.send('Queue cleared.')
            else:
                await message.channel.send('Clearing cancelled.')
    
client = MyClient()
client.run('token')
