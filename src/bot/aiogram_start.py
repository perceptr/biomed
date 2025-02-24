import asyncio

from src.bot.forms.upload_document import upload_document_router
from src.bot.forms.user_form import user_info_router
from src.bot.handlers.edit_docuents import edit_documents_router
from src.bot.handlers.list_documents import list_documents_router
from create_bot import bot, dp
from handlers.start import start_router
# from work_time.time_func import send_time_msg


async def main():
    dp.include_router(start_router)
    dp.include_router(user_info_router)
    dp.include_router(upload_document_router)
    dp.include_router(list_documents_router)
    dp.include_router(edit_documents_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
