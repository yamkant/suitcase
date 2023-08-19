from django.conf import settings
from PIL import Image
from io import BytesIO
import boto3

class S3ImageUploader():
    def __init__(self) -> None:
        self.aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        self.aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        self.aws_region = getattr(settings, 'AWS_REGION', None)
        self.aws_storage_bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)

    def upload_pil(self, img_src: Image, filename):
        s3_transport_buffer = BytesIO()
        img_src.save(s3_transport_buffer, format="PNG")
        s3_resource = boto3.resource( 
            's3', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        s3_resource.Bucket(self.aws_storage_bucket_name).put_object(Body=BytesIO(s3_transport_buffer.getvalue()), Key=filename)


# class S3ImgUploader:
#     def __init__(self, file):
#         self.file = file

#     def upload(self):
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
#         )
#         url = 'img'+'/'+uuid.uuid1().hex
        
#         s3_client.upload_fileobj(
#             self.file, 
#             "bucket_name", 
#             url, 
#             ExtraArgs={
#                 "ContentType": self.file.content_type
#             }
#         )
#         return url