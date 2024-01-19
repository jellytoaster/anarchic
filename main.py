import disnake
import time
import os
import config
import cogs
from classes.role import Role
from cogs import party, setupManagement, admin, endGame, basic, help
from disnake.ext import commands

bot = commands.AutoShardedInteractionBot(intents=disnake.Intents(presences=True,members=True, guilds=True), shard_count=2)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print("With an ID of " + str(bot.user.id))
    print('------')
    print("Login time in epoch: ", time.time())
    game = disnake.Activity(type=disnake.ActivityType.watching, name="chaos | /help")
    await bot.change_presence(activity=game, status=disnake.Status.do_not_disturb)

os.system("cls")

print("Initializing roles")
Role.init()

print("Loading cogs")
bot.add_cog(cogs.party.PartyCog(bot))
bot.add_cog(cogs.setupManagement.setupManagement(bot))
bot.add_cog(cogs.admin.adminCommands(bot))
bot.add_cog(cogs.endGame.endGame(bot))
bot.add_cog(cogs.basic.basic(bot))
bot.add_cog(cogs.help.HelpCog(bot))

print("Connecting to Discord")
bot.run(config.BETATOKEN)
