from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.core.files.base import ContentFile


class UserListCreateTestCase(APITestCase):

    def setUp(self):
        self.url_user = reverse('api_user:user-list')
        self.image = ContentFile(b"foo", "volunteer_image.jpg")
        self.id = ""

    def authenticate(self):
        response = self.client.post(
            reverse("api_auth:register_user"),
            {
                "email": "bangpham+test@gmail.com",
                "password": "123456",
                "username": "bangpham",
                "full_name": "bang pham",
                "study_at": "DH BKDN"
            },
        )
        self.id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            reverse("api_auth:login"),
            {
                "email": "bangpham+test@gmail.com",
                "password": "123456",
            },
        )

        token = response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_retrieve_user(self):
        self.authenticate()
        retrieve_url = reverse('api_user:user-detail', kwargs={'pk': self.id})
        response = self.client.get(path=retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.authenticate()
        url_user_update = reverse('api_user:user-detail', kwargs={'pk': self.id})
        response = self.client.put(path=url_user_update,
                                    data={
                                            "full_name": "bang update"
                                        }
                                    )
        self.assertEqual(response.data['full_name'], "bang update")

    def test_update_user_avatar(self):
        self.authenticate()
        url_user_update = reverse('api_user:user-detail', kwargs={'pk': self.id})
        response = self.client.put(path=url_user_update,
                                   data=encode_multipart(
                                       data=dict(avatar=self.image),
                                       boundary=BOUNDARY),
                                   content_type=MULTIPART_CONTENT
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
