from fastapi import APIRouter

router = APIRouter()


# @router.get(
#     "/{order_id}",
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=UploadFileOut,
# )
# def get_order