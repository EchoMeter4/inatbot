from discord.ext import commands, menus
from tools import utility
import discord
import aiohttp
import traceback
from tools.inat import find


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['maverick'])
    async def mavericks(self, ctx, *, username: str, location=None):
        """Gets someone's maverick IDs, separate location using a comma (,)."""
        client = self.client

        async with ctx.channel.typing():
            place_id = None
            try:
                # Get location if given
                if "," in username:
                    split = username.split(",", maxsplit=1)

                    username = split[0].strip().lower()
                    location = split[1].strip().title()

                    async with aiohttp.ClientSession() as session:
                        params = {'q': location,
                                  'order_by': 'area'}

                        async with session.get(url=f"{client.endpoint}/places/autocomplete", params=params) as response:
                            response.raise_for_status()
                            response_json = await response.json()

                            place_id = str(response_json['results'][0]['ancestor_place_ids'][-1])

                # Get mavericks from user
                async with aiohttp.ClientSession() as session:
                    params = {'user_login': username,
                              'category': 'maverick',
                              'per_page': '200',
                              'taxon_id': '47336'}

                    if place_id is not None:
                        params['place_id'] = place_id

                    async with session.get(url=f'{self.client.endpoint}/identifications', params=params) as response:
                        response.raise_for_status()
                        response_json = await response.json()
                        user_info = response_json['results']

            except Exception as e:
                print(traceback.format_exc())
                await ctx.send("Something went wrong " + str(e))

            else:
                if len(user_info) == 0:
                    message = "No maverick IDs found for this user."
                    if place_id is not None:
                        message = message.strip(".") + " in " + location + "."

                    await ctx.send(message)
                    return

                class IdSource(menus.ListPageSource):
                    def __init__(self, data):
                        super().__init__(data, per_page=10)

                    async def format_page(self, menu, entries):
                        offset = menu.current_page * self.per_page
                        embed = discord.Embed(color=client.embed_color)

                        embed.title = f"{entries[0]['user']['login']}'s Maverick IDs ({len(user_info)})"
                        if place_id is not None:
                            embed.title += " in " + location

                        embed.description = "Shows Identification made by the User and the date when it was made.\n\n"
                        embed.description += "\n".join(
                            f"{i}.- [{v['observation']['species_guess']} - "
                            f"{v['created_at'].split('T')[0]}]({v['observation']['uri']})"
                            for i, v in enumerate(entries, start=offset + 1)
                        )

                        if entries[0]['user']['icon_url'] is not None:
                            embed.set_thumbnail(url=entries[0]['user']['icon_url'])

                        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()} "
                                              f"| {ctx.author.display_name}",
                                         icon_url=ctx.author.avatar_url)

                        return embed

                pages = utility.BetterMenu(source=IdSource(user_info))
                await pages.start(ctx)

    @commands.command()
    async def find(self, ctx, *, name):
        if " " not in name:
            await ctx.send(f"``Arugment Missing. The command is {self.client.command_prefix}find <genus> <species>``")
            return

        image_link = find(name)['image_list']
        len_of_list = len(image_link)
        url = f"https://www.inaturalist.org/taxa/{find(name)['id']}-{name.replace(' ', '-')}"

        if len_of_list <= 1:
            page1 = discord.Embed(title=name, url=url, description="(1/1)", color=0xEBC815)
            page1.set_image(url=str(find(name)['image_list'][0]))
            await ctx.send(embed=page1)
            return

        # Else

        class Pictures(menus.ListPageSource):
            def __init__(self, data):
                super().__init__(data, per_page=1)

            async def format_page(self, menu, entries):
                embed = discord.Embed(title=name, url=url,
                                      description=f"({menu.current_page + 1}/{self.get_max_pages()})",
                                      color=0xEBC815)
                embed.set_image(url=entries)
                return embed

        pages = utility.BetterMenu(source=Pictures(image_link))
        await pages.start(ctx)


def setup(client):
    client.add_cog(Search(client))
