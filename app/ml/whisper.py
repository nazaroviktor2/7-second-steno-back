from moviepy.editor import VideoFileClip
import whisperx

from app.core.celery import model, diarize_model


device = "cuda" 
BATCH_SIZE = 16  # reduce if low on GPU mem
COMPUTE_TYPE = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

#
# diarize_model = whisperx.DiarizationPipeline(
#     use_auth_token=HF_TOKEN,
#     device=device
# )
# model = whisperx.load_model(
#     "large-v2",
#     device,
#     compute_type=COMPUTE_TYPE,
#     language='ru'
# )


def mp4_to_mp3_converter(filename):
    video = VideoFileClip(filename)
    video.audio.write_audiofile('./tmp.mp3')
    audio = whisperx.load_audio('./tmp.mp3')

    return audio


def whisper_model_pipeline(filename, file_format, num_speakers=None):
    if file_format == 'mp4':
        audio = mp4_to_mp3_converter(filename)
    else:
        audio = whisperx.load_audio(filename)

    # 1. Transcribe with original whisper (batched)
    result = model.transcribe(audio, batch_size=BATCH_SIZE)
    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False
    )
    # add min/max number of speakers if known
    diarize_segments = diarize_model(
        audio,
        num_speakers=num_speakers
    )
    # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    return result


def format_time_string(time_string):
    # Разделение строки на начальное и конечное время
    start_time, end_time = time_string.split('-')
    
    # Преобразование времени из секунд в формат часы:минуты:секунды
    def seconds_to_hms(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Формирование итоговой строки
    formatted_start_time = seconds_to_hms(float(start_time))
    formatted_end_time = seconds_to_hms(float(end_time))
    formatted_time_string = f"[{formatted_start_time}-{formatted_end_time}]"
    
    return formatted_time_string


def convert_whisper_result_to_text(result):
    result_text = ''
    current_user_text_speech = ''
    last_speaker = result['segments'][0]['speaker']
    speaker_start_time = 0

    for elem in result['segments']:
        if last_speaker == elem['speaker']:
            current_user_text_speech += elem['text'] + ' '
        else:
            # Конвертим время
            time_string = f"{speaker_start_time}-{elem['start']}"
            formatted_time_string = format_time_string(time_string)
            # добавляем время, спикера и текст
            result_text += f"{formatted_time_string} {last_speaker}\n{current_user_text_speech}\n"
            current_user_text_speech = elem['text'] + ' '
            speaker_start_time = elem['start']
            last_speaker = elem['speaker']
    # Конвертим время
    current_user_text_speech = current_user_text_speech[:-1]
    time_string = f"{speaker_start_time}-{elem['end']}"
    formatted_time_string = format_time_string(time_string)
    # добавляем время, спикера и текст
    result_text += f"{formatted_time_string} {elem['speaker']}\n{current_user_text_speech}"
    return result_text

#############################################################
###Сохранение docx
#############################################################
# from docx import Document
#
# def save_docx_file(text_result, file_path):
#     doc = Document()
#     doc.add_paragraph(text_result)
#     doc.save(file_path)