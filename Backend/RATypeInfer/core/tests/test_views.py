from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
import os
from django.conf import settings
import pandas as pd
import json
from django.urls import reverse
import shutil


TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, "test_media")

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FileUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("upload")
        os.makedirs(TEST_MEDIA_ROOT, exist_ok=True)

    def test_upload_successful(self):
        file_path = os.path.join(TEST_MEDIA_ROOT, "test.csv")
        with open(file_path, "w") as f:
            f.write("header1,header2\n1,2\n3,4")
        with open(file_path, "rb") as file:
            response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("file_url", response.json())

    def tearDown(self):
        # Clean up any files created during tests
        if os.path.exists(TEST_MEDIA_ROOT):
            shutil.rmtree(TEST_MEDIA_ROOT)

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FileProcessTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("process")
        self.test_file_path = os.path.join(TEST_MEDIA_ROOT, "test.csv")
        os.makedirs(TEST_MEDIA_ROOT, exist_ok=True)

        # Create a sample CSV file
        pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]}).to_csv(self.test_file_path, index=False)

    def test_process_csv_file_successful(self):
        data = {"fileUrl": "test.csv"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())
        self.assertIn("types", response.json())

    def tearDown(self):
        # Clean up any files created during tests
        if os.path.exists(TEST_MEDIA_ROOT):
            shutil.rmtree(TEST_MEDIA_ROOT)
