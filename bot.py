from twitchio.ext import commands
import os
import json
import xml.dom.minidom


class Bot(commands.Bot):

    users = {}

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ['ACCESS_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)
        await self.iterate_message_count(message.author.name)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def iterate_message_count(self, name):
        print(name)
        if not self.users.get(name):
            self.users.update({name: 1})
            return

        self.users[name] = self.users.get(name)+1

        print("")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def stream(self, ctx: commands.Context):
        await ctx.send(f'Stream tego zawodnika {ctx.channel.name}, dzięki za wpisanie komendy {ctx.author.name}')


    @commands.command()
    async def messages(self, ctx: commands.Context):
        await ctx.send(f'@{ctx.author.name} wysłałeś {self.users.get(ctx.author.name)} wiadomości!')
        print(self.users)




if __name__ == "__main__":
    bot = Bot()
    bot.run()
