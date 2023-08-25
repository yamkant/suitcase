mkdir -p /var/log/nginx/logs/

# nginx 실행 전 템플릿 파일의 변수를 환경 변수 값으로 변경해주는 구문입니다.
if [ "$INITIAL_START" -eq '1' ]; then
    bash /docker-entrypoint.d/20-envsubst-on-templates.sh
    INITIAL_START="0"
fi
nginx -g "daemon off;"