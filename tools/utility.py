from discord.ext import menus


class BetterMenu(menus.MenuPages):
    def __init__(self, source):
        super().__init__(source=source, timeout=3600, clear_reactions_after=True)

    # Makes it so the bot removes the reaction after reacting.
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                message = self.bot.get_channel(payload.channel_id).get_partial_message(
                    payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)

    def reaction_check(self, payload):
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in {self.bot.owner_id, self._author_id, *self.bot.owner_ids}:
            return False

        return payload.emoji in self.buttons
