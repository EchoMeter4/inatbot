from bot import iNatBot

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

    client.run("ODM4NTU1MzQ0MzE3MDU0OTk3.YI8zhQ.khJmbW2rQNsHAv6KcDgixzIeboI")
