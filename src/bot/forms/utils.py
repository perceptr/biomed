from src.bot.utils import generate_tmp_filename, download_image_from_s3
from src.schemas import AnalysisSchema


async def get_analysis_photo(user_id : int, analysis: AnalysisSchema):
    tmp_file_name = generate_tmp_filename(user_id)
    photo = await download_image_from_s3(analysis.s3_address, tmp_file_name)
    return photo