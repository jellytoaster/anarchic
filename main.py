import disnake
import time
import os
import importlib
import config
import classes.changelog
from classes.contraction import Contraction
from cogs import party, setupManagement, admin, endGame, basic, help
from disnake.ext import commands

bot = commands.AutoShardedInteractionBot(intents=disnake.Intents(29447), shard_count=2)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print("With an ID of " + str(bot.user.id))
    print("Login time: ", time.time())
    print('------')
    
    game = disnake.Activity(type=disnake.ActivityType.watching, name="chaos | /help")
    await bot.change_presence(activity=game, status=disnake.Status.do_not_disturb)


def main():
    print("Initializing classes/objects")

    # Init roles in /classes/roles
    cwd = os.getcwd()
    for file in os.listdir("classes/roles"):
        path = os.path.join("classes/roles", file)

        module = os.path.splitext(os.path.basename(path))[0]

        try:
            module = importlib.import_module("classes.roles." + module)
            module.init()
        except Exception as e:
            if (config.TEST_MODE):
                raise e
            print(f"Could not initialize role in {path}!: {e}")


    # Init contractions & changelogs
    Contraction.initContractions()
    classes.changelog.Changelog.initChangelogs()

    # Create cogs (for slash commands)
    print("Loading cogs")
    bot.add_cog(party.PartyCog(bot))
    bot.add_cog(setupManagement.setupManagement(bot))
    bot.add_cog(admin.adminCommands(bot))
    bot.add_cog(endGame.endGame(bot))
    bot.add_cog(basic.basic(bot))
    bot.add_cog(help.HelpCog(bot))


    print("Connecting to Discord")
    bot.run(config.BETATOKEN)

if __name__ == "__main__":
    main()