import discord

from src.instance import (
    bot, logger, cache
)

from src.utils import create_ticket, create_feedback
from src.database.models import TicketStatus


@bot.event
async def on_message(message: discord.Message) -> None:
    if not isinstance(message.channel, discord.DMChannel):
        return None

    sender = message.author
    sender_data = await cache.get_info_about_user(sender)

    logger.info(f"User {sender.display_name}#{sender.discriminator} sent message: {message.content}")

    if sender_data is None:
        return None

    if sender_data.ticket_status == TicketStatus.NOT_CREATED:
        return None

    if sender_data.ticket_status == TicketStatus.PROCCESS_WRITING:
        await sender.send("Ваше ТЗ переданно к художникам, ожидайте ответа.")
        await create_ticket(sender, message.content)        
        await cache.write_info_about_user(sender, TicketStatus.WRITTEN)

    if sender_data.ticket_status == TicketStatus.WRITTEN:
        await sender.send("Пожалуйста, ожидайте принятия вашего заказа.")

    if sender_data.ticket_status == TicketStatus.ACCEPTED:
        await sender.send(
            "Пожалуйста, ожидайте когда ваш заказ будет завершён, "
            "либо перейдите в личный диалог с вашим художником."
        )

    if sender_data.ticket_status == TicketStatus.SEND_FEEDBACK:
        await sender.send("Спасибо за предоставленный отзыв! Приятной вам игры!)")
        await create_feedback(sender, message.content)        
        await cache.write_info_about_user(sender, TicketStatus.NOT_CREATED)

