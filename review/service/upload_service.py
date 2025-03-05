import boto3
import os
from datetime import datetime

from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 AWS 설정 가져오기
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

# S3 클라이언트 생성
class S3Client:
    def __init__(self):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                               region_name=AWS_S3_REGION_NAME)
        self.bucket_name = AWS_STORAGE_BUCKET_NAME

    def upload_review_image(self,file):
        save_dir = 'media/review/' # 저장 경로
        now = datetime.now()
        date_prefix = now.strftime("%Y%m%d_%H%M%S")
        new_file_name = f"{date_prefix}_{file.name}"
        extra_args = {'ContentType':file.content_type}

        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                f'{save_dir}{new_file_name}',
                ExtraArgs=extra_args,
            )
            return f'https://{self.bucket_name}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{save_dir}{new_file_name}'
        except NoCredentialsError:
            print("Credentials not available")

