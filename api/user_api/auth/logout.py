from fastapi import APIRouter, Depends, status, Response

router = APIRouter(
    prefix="/logout",
    tags=["Logout"],
)

@router.post("")
async def revoke_access_token(
        response: Response
    ):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"status": "token revoked"}