
async def media_processing(problem_description, album, message, bot):
    files_id = []
    caption = problem_description

    if album:
        for element in album:
            if element.photo:
                file_id = element.photo[-1].file_id
                if element.caption:
                    caption = element.caption
                files_id.append(file_id)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, f"../media/{file.file_id}.png")
            else:
                return await message.answer("Этот тип медиафайлов не поддерживается!")
    else:
        if message.photo:
            await bot.download(
                message.photo[-1],
                destination=f"../media/{message.photo[-1].file_id}.png"
            )
            files_id.append(message.photo[-1].file_id)

    return files_id, caption
