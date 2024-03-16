import uuid

from fastapi import APIRouter, status, Depends

from app.api.v1.endpoints.auth import get_current_user
from app.schemas.file_schemas import UploadFileOut, UploadFileIn
from app.services.exceptions import handle_domain_error

from app.services.use_case.file import service_file_upload

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadFileOut,
)
@handle_domain_error
async def upload_file(payload: UploadFileIn = Depends(), user=Depends(get_current_user)) -> UploadFileOut:
    """Создает заказ на обработку файла."""
    order_id = await service_file_upload(payload)

    # order_id = str(uuid.uuid4())
    return UploadFileOut(
        message="File upload task has been started",
        order=order_id,
    )
