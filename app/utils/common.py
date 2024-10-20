import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# ID와 비밀번호 설정
SECURITY_ID = os.getenv('SECURITY_ID')
SECURITY_PASSWORD = os.getenv('SECURITY_PASSWORD')


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != SECURITY_ID or credentials.password != SECURITY_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# /docs 페이지에 인증 적용
