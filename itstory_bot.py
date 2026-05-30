import discord
from discord.ext import commands
from discord import ui
from itstorybot_token import itstorybot_token

class ITStoryBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.voice_states = False
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        game = discord.Game("IT스토리")
        await self.change_presence(status=discord.Status.online, activity=game)
        await self.tree.sync()
        print(f"Logged in with {self.user}")

bot = ITStoryBot()

class Messagesay(ui.Modal, title="보낼 메시지를 입력해주세요"):
    name = ui.TextInput(label="첫 번째 메시지", placeholder="첫 번째 줄에 띄울 메시지를 작성해주세요", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.name.value}")

@bot.tree.command(name="말하기", description="입력한 내용을 말합니다.")
async def say(interaction: discord.Interaction):
    await interaction.response.send_modal(Messagesay())

class SelectMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="말하기", description="'말하기' 명령어의 설명을 볼 수 있습니다.", emoji="1️⃣"),
            discord.SelectOption(label="공지", description="'공지' 명령어의 설명을 볼 수 있습니다.", emoji="2️⃣")
        ]
        super().__init__(placeholder="여기를 눌러서 명령어를 선택하세요", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        messages = {
            "말하기": "입력한 메시지를 봇이 말할 거에요.",
            "공지": "입력한 내용을 봇이 공지할 거에요.\n제목은 큰 글자로 나타나요."
        }
        await interaction.response.send_message(content=messages.get(self.values[0], "알 수 없는 명령어입니다."), ephemeral=True)

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectMenu())

@bot.tree.command(name="도움말", description="명령어의 도움말을 볼 수 있어요.")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(content="설명을 볼 명령어를 선택해주세요.", view=Select())

class NoticeModal(ui.Modal, title="보낼 메시지를 입력해주세요"):
    title_input = ui.TextInput(label="제목", placeholder="공지의 제목을 작성해주세요", style=discord.TextStyle.short)
    content_input = ui.TextInput(label="내용", placeholder="공지의 내용을 작성해주세요", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"# {self.title_input.value}\n{self.content_input.value}")

@bot.tree.command(name="공지", description="이 채널에 공지를 보냅니다.")
async def announce(interaction: discord.Interaction):
    await interaction.response.send_modal(NoticeModal())

bot.run(itstorybot_token)
