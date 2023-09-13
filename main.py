import disnake
import config
import cogs
from classes.role import Role
from cogs import party, setupManagement, admin, endGame, basic
from disnake.ext import commands

bot = commands.Bot(intents=disnake.Intents(message_content=True,guilds=True),command_prefix=config.PREFIX)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print("With an ID of " + str(bot.user.id))
    print('------')
    game = disnake.Activity(type=disnake.ActivityType.watching, name="chaos | /help")
    await bot.change_presence(activity=game, status=disnake.Status.do_not_disturb)


print("Initializing roles")
Role.init()

print("Loading cogs")
bot.add_cog(cogs.party.PartyCog(bot))
bot.add_cog(cogs.setupManagement.setupManagement(bot))
bot.add_cog(cogs.admin.adminCommands(bot))
bot.add_cog(cogs.endGame.endGame(bot))
bot.add_cog(cogs.basic.basic(bot))

print("Connecting to Discord")
bot.run(config.BETATOKEN)