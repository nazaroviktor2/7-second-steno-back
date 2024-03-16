import torch
import re

from app.core.celery import summarizer_model

device = 'cuda' if torch.cuda.is_available() else 'cpu'

summarizer_clean_expr = re.compile(r"[\xa0\x1a\x16\x1b\x17\x15\u2004]")
summarizer_spaces_expr = re.compile(r"\s{2,}")


def summarizer_process_text(text: str) -> str:
    """Осуществляет пред- и постобработку текста."""
    text = summarizer_clean_expr.sub(" ", text)
    text = summarizer_spaces_expr.sub(" ", text)

    if "." in text:
        index = text.rindex(".")
        text = text[:index + 1]

    return text


def run_summarize_text(text_to_summarize, max_new_tokens=80):
    response = summarizer_model(
        text_to_summarize,
        max_new_tokens=max_new_tokens,
        num_beams=2,
        do_sample=True,
        top_k=100,
        repetition_penalty=2.5,
        length_penalty=1.0
    )
    summary = summarizer_process_text(
        response[0]["summary_text"]
    )
    return summary




# Суммаризация для определенного спикера

def get_speaker_text(text, speaker_name):
    # Регулярное выражение для поиска спикеров и их текста
    pattern = r'\[.*?\] (SPEAKER_\d+)\n(.*?)\n(?=\[|$)'
    # Поиск всех совпадений с регулярным выражением
    matches = re.findall(pattern, text, re.DOTALL)
    speaker_text = ''

    for match in matches:
        speaker, tmp_text = match
        if speaker == speaker_name:
            if speaker_text:
                speaker_text += tmp_text
            else:
                speaker_text += ' ' + tmp_text
    return speaker_text


def summarize_person_text(text_to_summarize, speaker_name, max_new_tokens=30):
    return run_summarize_text(
        text_to_summarize=get_speaker_text(
            text_to_summarize,
            speaker_name=speaker_name
        ),
        max_new_tokens=max_new_tokens
    )


# summarize_person_text(text_to_summarize, speaker_name='SPEAKER_01')
