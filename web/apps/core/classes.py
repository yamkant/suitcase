from django.conf import settings
from PIL import Image
from io import BytesIO
import boto3
import uuid

import requests
from io import BytesIO
from rembg import remove

class ImageHandler():
    def __init__(self, img_url) -> None:
        # TODO: Exception 추가
        self._image = self.get_image_object(img_url)
    
    def get_image_object(self, img_url):
        response = requests.get(img_url)
        img_data = BytesIO(response.content)
        return Image.open(img_data)
    
    def get_removed_background_image(self):
        return remove(self._image)
    
    def get_resized_image(self, image, w_ratio: float, h_ratio: float):
        return image.resize((
            image._size[0] * w_ratio,
            image._size[1] * h_ratio
        ))

class S3ImageUploader():
    def __init__(self) -> None:
        self.aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        self.aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        self.aws_region = getattr(settings, 'AWS_REGION', None)
        self.aws_storage_bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
        self.aws_s3_custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    @staticmethod
    def get_file_name(file_path):
        file_id = str(uuid.uuid4())
        return f'{file_path}/{file_id}'

    def upload_pil(self, img_src: Image, filename):
        s3_transport_buffer = BytesIO()
        img_src.save(s3_transport_buffer, format="PNG")
        s3_resource = boto3.resource( 
            's3', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        s3_resource.Bucket(self.aws_storage_bucket_name).put_object(Body=BytesIO(s3_transport_buffer.getvalue()), Key=filename)

        return f'https://{self.aws_s3_custom_domain}/{filename}'