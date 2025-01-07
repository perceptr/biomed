from src.bot.create_bot import bot
from src.bot.utils.utils import get_analysis_photo
from src.schemas import AnalysisSchema


async def send_message_to_user(analysis: AnalysisSchema, text: str):
    photo = await get_analysis_photo(analysis)
    await bot.send_photo(
        analysis.user.telegram_id,
        photo,
        caption=
        f"""
Вот расшифровка вашего анализа "{analysis.name}":
                   
{text}""")


def get_text_for_operator(analysis: AnalysisSchema) -> str:
    extras = ""
    text = "Переведите файл в текст по установленному формату и введите результат в чат."
    if analysis.edit_note:
        extras = (f"Расшифровка отправлена на редактирование. Текущий текст расшфировки:\n\n"
                  f"{analysis.result}\n\n"
                  f"Комментарий пользователя по поводу расшфировки:\n\n"
                  f"{analysis.edit_note}\n\n")
    return f'{extras}{text}'
