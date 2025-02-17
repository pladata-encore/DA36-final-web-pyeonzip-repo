from .settings import *
import socket

DEBUG = False

ALLOWED_HOSTS = [
    'Eb-pyeonzip-app-env.eba-skazjekk.ap-northeast-2.elasticbeanstalk.com',
    'pyeonzip.store'
]

# 내부 ip추가
try:
    internal_ip = socket.gethostbyname(socket.gethostname())
    ALLOWED_HOSTS.append(internal_ip)
except Exception as e:
    print(str(e))

# DB 관련 세팅
