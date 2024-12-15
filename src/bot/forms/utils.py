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
