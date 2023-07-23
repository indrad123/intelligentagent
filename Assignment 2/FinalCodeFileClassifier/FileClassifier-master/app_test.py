import os
import shutil
import unittest
from flask import Flask
from app import app, UploadAgent, ClassifierAgent, MoveFileAgent
from werkzeug.datastructures import FileStorage, FileMultiDict
from flask.testing import FlaskClient

# Extend FlaskClient for multipart file upload
class FlaskClientWithFileUpload(FlaskClient):
    def open(self, *args, **kwargs):
        if 'data' in kwargs and isinstance(kwargs['data'], dict):
            data = kwargs.pop('data')
            kwargs['data'] = FileMultiDict(data)
        return super().open(*args, **kwargs)

# Replace test client class in Flask app
app.test_client_class = FlaskClientWithFileUpload

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        app.config['TESTING'] = True

   # Test if the endpoint handles upload without any file
    def test_upload_no_files(self):
        response = self.client.post('/upload', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check for a part of the HTML that's always returned
        self.assertIn(b'<!DOCTYPE html>', response.data)

    # Test if the endpoint can upload a single file correctly
    def test_upload_single_file(self):
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')

        with open('test_file.txt', 'rb') as f:
            data = {
                'files[]': f
            }
            response = self.client.post('/upload', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_file.txt', response.data)

    # Test if the endpoint can handle multiple file upload correctly
    def test_upload_multiple_files(self):
        with open('test_file1.txt', 'w') as f:
            f.write('This is a test file.')
        with open('test_file2.txt', 'w') as f:
            f.write('This is another test file.')

        with open('test_file1.txt', 'rb') as f1, open('test_file2.txt', 'rb') as f2:
            data = {
                'files[]': [f1, f2]
            }
            response = self.client.post('/upload', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_file1.txt', response.data)
        self.assertIn(b'test_file2.txt', response.data)

    # Test if the UploadAgent works as expected
    def test_UploadAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        with open('uploads/test_file.txt', 'r') as f:
            file = FileStorage(stream=f, filename='test_file.txt')
            UploadAgent(file)
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    # Test if the ClassifierAgent can classify files correctly
    def test_ClassifierAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        ClassifierAgent('test_file.txt')
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    # Test if the MoveFileAgent can move files to the specified location correctly
    def test_MoveFileAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        MoveFileAgent('test_file.txt', 'safe')
        self.assertTrue(os.path.exists('safe/test_file.txt'))

    # Test if the endpoint for viewing files returns the correct response
    def test_view_files(self):
        response = self.client.get('/view')
        self.assertEqual(response.status_code, 200)

    # Clean up files and directories after each test
    def tearDown(self):
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
        if os.path.exists('test_file1.txt'):
            os.remove('test_file1.txt')
        if os.path.exists('test_file2.txt'):
            os.remove('test_file2.txt')
        if os.path.exists('uploads/test_file.txt'):
            os.remove('uploads/test_file.txt')
        if os.path.exists('safe/test_file.txt'):
            os.remove('safe/test_file.txt')
        if os.path.exists('suspicious/test_file.txt'):
            os.remove('suspicious/test_file.txt')
        if os.path.exists('safe'):
            shutil.rmtree('safe')
        if os.path.exists('suspicious'):
            shutil.rmtree('suspicious')
        if os.path.exists('uploads'):
            shutil.rmtree('uploads')

if __name__ == "__main__":
    unittest.main()
