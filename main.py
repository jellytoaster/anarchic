import disnake
import time
import os
import inspect
import random
import importlib
import classes.ability
import classes.role
import config
import classes.changelog
from classes.contraction import Contraction
from cogs import party, setupManagement, admin, endGame, basic, help, guide
from disnake.ext import commands

bot = commands.AutoShardedInteractionBot(intents=disnake.Intents(32767), shard_count=2)

random.seed(time.time())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print("With an ID of " + str(bot.user.id))
    print("Login time: ", time.time())
    print('------')
    
    game = disnake.Activity(type=disnake.ActivityType.watching, name="chaos | /help")
    await bot.change_presence(activity=game, status=disnake.Status.do_not_disturb)

functionType = type(on_ready)

def main():
    print("Initializing classes/objects")

    # Init roles in /classes/roles
    for file in os.listdir("classes/roles"):
        path = os.path.join("classes/roles", file)

        module = os.path.splitext(os.path.basename(path))[0]

        try:
            module = importlib.import_module("classes.roles." + module)
            for moduleClass in [getattr(module, name) for name in dir(module) if isinstance(getattr(module, name), type) and name.lower() != "faction"]:
                role = moduleClass()

                # Discover abilities of the role

                for roleAbility in [getattr(module, name) for name in dir(module) if isinstance(getattr(module, name), functionType)]:
                    if hasattr(roleAbility, "_metadata"):
                        role.abilities.append(classes.ability.Ability.fromMetadata(roleAbility._metadata, roleAbility))

                classes.role.Role.allRoles.append(role)
                break

        except Exception as e:
            if (config.TEST_MODE):
                raise e
            print(f"Could not initialize role in {path}, skipping: {e}")


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
    bot.add_cog(guide.GuideCog(bot))


    print("Connecting to Discord")
    if config.USEBETA:
        bot.run(config.BETATOKEN)
    else:
        bot.run(config.TOKEN)

if __name__ == "__main__":
    main()