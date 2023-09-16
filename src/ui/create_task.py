import discord

from src.instance import bot, cache
from src.ui.dm import DMView
from src.database.models import TicketStatus

class CreateTaskView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Создать заказ", style=discord.ButtonStyle.green)
    async def create_task(self, interaction: discord.Interaction, _: discord.ui.Button) -> None: 
        user_data = await cache.get_info_about_user(interaction.user)

        if user_data is not None and user_data.ticket_status != TicketStatus.NOT_CREATED:
            return await interaction.response.send_message(
                content="Вы уже создали заказ, ожидайте ответа от художника.",
                ephemeral=True
            )

        await interaction.user.create_dm()
        
        message = discord.Embed(
            title="Форма подачи заказа:",
            description="1. Ник.\n2. Подробное тз.\n3. Референсы (если имеются)\n4. Дедлайн.\n\nКарта для оплаты скина - 50162",
            colour=discord.Colour.dark_purple()
        )
        message.set_footer(text="ВАЖНО! Отправляйте сообщение строго по форме, иначе заказ будет отклонён")

        await interaction.user.send(embed=message)

        view = DMView(interaction.user.dm_channel)
        
        await cache.write_info_about_user(interaction.user, TicketStatus.PROCCESS_WRITING)

        await interaction.response.send_message(
            'Напишите ваше ТЗ по скину в личные сообщения бота, и оно будет рассмотренно в ближайше время', 
            ephemeral=True, view=view
        )

