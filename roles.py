import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.reactions = True
intents.members = True  # Enable member intents

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store message IDs based on the channel
bot.messages = {}
roles = [

]
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

    channel = bot.get_channel(CHANNEL_ID)
    

    if channel:
        message = await channel.send(""" **Hii if you want more roles just react with :
💻:devoloper ,🖼️ NFT's  , 🎨:Designer, ♂️ :Male , ♀️ :Female
                                     **""") #add any message you want 
        # Add emojis reactions to the message
        emojis = ['💻', '🖼️', '🎨', '♂️','♀️']
        for emoji in emojis:
            await message.add_reaction(emoji)

        # Store the message ID for later reference
        bot.messages[channel.id] = message.id

@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is on the desired message
    message_id = bot.messages.get(payload.channel_id)
    if message_id == payload.message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        # Get the role based on the emoji
        role_mapping = {
            '💻': '💻 Developer',
            '🖼️': "NFT's",
            '🎨':'Designer',
            '♂️':'Male',
            '♀️':'Female',
        }

        role_name = role_mapping.get(payload.emoji.name)
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)

            # Give the role to the user
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.add_roles(role)
                    print(f"Added role {role.name} to {member.display_name}")
                else:
                    print("Member not found!")
            else:
                print(f"Role {role_name} not found!")
        else:
            print(f"Role not mapped for emoji {payload.emoji.name}!")

@bot.event
async def on_raw_reaction_remove(payload):

    message_id = bot.messages.get(payload.channel_id)
    if message_id == payload.message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        # Get the role based on the emoji
        role_mapping = {
            '💻': '💻 Developer',
            '🖼️': "NFT's",
            '🎨':'Designer',
            '♂️':'♂️ Male',
            '♀️':'♀️ Female',
        }

        role_name = role_mapping.get(payload.emoji.name)
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)

            # Remove the role from the user
            if role:
                member = guild.get_member(payload.user_id)
                if member:
                    await member.remove_roles(role)
                    print(f"Removed role {role.name} from {member.display_name}")
                else:
                    print("Member not found!")
            else:
                print(f"Role {role_name} not found!")
        else:
            print(f"Role not mapped for emoji {payload.emoji.name}!")

# Run the bot with your token
if __name__ == "__main__":
    bot.run(BOT_TOKEN)