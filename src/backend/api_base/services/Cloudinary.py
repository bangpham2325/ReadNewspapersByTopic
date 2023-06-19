import cloudinary
import cloudinary.api
import cloudinary.uploader

import os
from dotenv import load_dotenv

load_dotenv()


class CloudinaryService:
    @classmethod
    def upload_avatar_user_image(cls, image):
        return cloudinary.uploader.upload(image, folder=os.getenv('CLOUDINARY_AVATAR_USER_FOLDER'))

    @classmethod
    def upload_thumb_post_image(cls, image):
        return cloudinary.uploader.upload(image, folder=os.getenv('CLOUDINARY_THUMB_POST_FOLDER'))

    @classmethod
    def delete_image(cls, pub_id):
        return cloudinary.uploader.destroy(pub_id, folder=os.getenv('CLOUDINARY_AVATAR_USER_FOLDER'))
