from bot import iNatBot
import os

cogs = ['apicommands.search']

if __name__ == '__main__':
    client = iNatBot()

    for cog in cogs:
        try:
            client.load_extension("cogs." + cog)
        except Exception as e:
            print("Failed to load extension " + cog + " due to:")
            print(e)
        else:
            print("Successfully loaded " + cog)

    # Put your bot token as an environment variable
    client.run(os.environ.get("TOKEN"))
