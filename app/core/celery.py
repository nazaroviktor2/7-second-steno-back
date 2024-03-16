from celery import Celery
from celery.signals import worker_process_init
from celery.utils.log import LoggingProxy
import whisperx

from app.core.config import config
from transformers import pipeline


app_celery = Celery(
    "worker",
    broker=config.CELERY_BROKER_URL,
    include=["app.worker.tasks"],
    debug=True,
)
# для patoolib
setattr(LoggingProxy, "encoding", "UTF-8")

global diarize_model
global model
global summarizer_model

@worker_process_init.connect
def init_worker(**kwargs):
    global diarize_model, model, summarizer_model
    HF_TOKEN = 'your_hf_token'
    device = "cuda"
    COMPUTE_TYPE = "float16"

    diarize_model = whisperx.DiarizationPipeline(
        use_auth_token=HF_TOKEN,
        device=device
    )
    model = whisperx.load_model(
        "large-v2",
        device,
        compute_type=COMPUTE_TYPE,
        language='ru'
    )

    # Суммаризация для всего текста
    summarizer_model = pipeline(
        "summarization",
        model="basic-go/FRED-T5-large-habr-summarizer",
        device=device
    )

    print("Model and other resources initialized.")

