import os, discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")
ROLE_ID = int(os.environ.get("ROLE_ID"))

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()

@tree.command(name="btn_getinaction")
async def command_setup_channel(interaction: discord.Interaction):
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="参加",
            custom_id="set_inaction",
            style=discord.ButtonStyle.red
        )
    )
    view.add_item(
        discord.ui.Button(
            label="解除",
            custom_id="del_inaction",
            style=discord.ButtonStyle.blurple
        )
    )
    content = f"""参加する方は参加を押してください
<@&{ROLE_ID}> ロールを付与します"""
    await interaction.response.send_message(content=content, view=view)

@client.event
async def on_interaction(interaction: discord.Interaction):
        if interaction.data['component_type'] == 2:
            await on_button_click(interaction)

async def on_button_click(interaction: discord.Interaction):
    custom_id = interaction.data["custom_id"]
    
    if custom_id == "set_inaction":
        await interaction.user.add_roles(interaction.guild.get_role(ROLE_ID))
        await interaction.response.send_message(content=f"<@&{ROLE_ID}> を付与しました", ephemeral=True)
    elif custom_id == "del_inaction":
        await interaction.user.remove_roles(interaction.guild.get_role(ROLE_ID))
        await interaction.response.send_message(content=f"<@&{ROLE_ID}> を解除しました", ephemeral=True)

def run():
    client.run(TOKEN)

if __name__ == "__main__":
    run()
