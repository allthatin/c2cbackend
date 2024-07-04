
> c2c Backend

# Features

- [o] 회원
- [o] 상품
- [o] 입찰
- [o] 게시글
- [o] 팀 활동


## Git 다운로드

    git clone https://github.com/allthatin/c2cbackend.git
    백엔드 브랜치로 이동: git checkout main

## Branch 
- `backend`: 백엔드 브랜치입니다.

## Stack
- DJANGO
- POSTGRESQL
- REDIS
- DOCKER
- ALB

## Monitoring
- AWS Cloudwatch
- Sentry

## Create Docker Image
docker build -f deployments/app/Dockerfile -t allthatin/api:latest .

## Run Docker Image 
docker run -d --name api -p 8000:8000 -e DEBUG=false -e DJANGO_SETTINGS_MODULE=config.settings.prod -e REDIS_HOST=redis -e CRONTAB_DJANGO_SETTINGS_MODULE=config.settings.prod -e ECS_ENABLE_AWS_EXEC=true allthatin/api:latest /cmds/start.sh
