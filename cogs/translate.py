import discord
from discord.ext import commands
from discord import app_commands
import config
import providers
from utils.permissions import has_command_permission

class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="translate", description="Translate text to a target language")
    @app_commands.describe(
        text="The text to translate",
        target_language="The language you want to translate to (e.g. Spanish, Japanese, Tagalog)"
    )
    @has_command_permission()
    async def translate_slash(self, interaction: discord.Interaction, text: str, target_language: str):
        if not config.TRANSLATE_ENABLED:
            await interaction.response.send_message("Translation feature is currently disabled.", ephemeral=True)
            return

        await interaction.response.defer()
        
        try:
            # We pass the target prompt directly
            system_prompt = (
                "You are a professional translator. "
                f"Translate the provided text into {target_language}. "
                "Maintain the original tone and context. "
                "Respond ONLY with the translated text."
            )
            
            response, provider = await ask_ai(
                interaction.channel_id,
                interaction.user.display_name,
                text,
                system_prompt=system_prompt,
                category="translation",
                guild_id=interaction.guild_id,
                user_id=interaction.user.id
            )
            await interaction.followup.send(response)
        except Exception as e:
            print(f"[TRANSLATE] Error: {e}")
            await interaction.followup.send("Sorry, I encountered an error while translating.")

    @commands.command(name="translate")
    async def translate_text(self, ctx: commands.Context, target_language: str, *, text: str):
        """Text command version: !translate <language> <text>"""
        if not config.TRANSLATE_ENABLED:
            return

        try:
            async with ctx.typing():
                system_prompt = (
                    "You are a professional translator. "
                    f"Translate the provided text into {target_language}. "
                    "Maintain the original tone and context. "
                    "Respond ONLY with the translated text."
                )
                
                response, provider = await ask_ai(
                    ctx.channel.id,
                    ctx.author.display_name,
                    text,
                    system_prompt=system_prompt,
                    category="translation",
                    guild_id=ctx.guild.id if ctx.guild else None,
                    user_id=ctx.author.id
                )
                await ctx.reply(response)
        except Exception as e:
            print(f"[TRANSLATE] Error: {e}")
            await ctx.send("Sorry, I encountered an error while translating.")

    # Removed do_translate as it's now integrated via ask_ai

async def setup(bot):
    await bot.add_cog(TranslateCog(bot))
