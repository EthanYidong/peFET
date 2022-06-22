from django.test import RequestFactory, TestCase
from django.conf import settings

import bcrypt
import json
import jwt

from ..models import User
from ..views import account


class AccountTestLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

    def test_login_valid(self):
        req = self.factory.post(
            '/api/account/login', {'email': 'test@example.com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])

        self.assertEqual(claims['sub'], self.user.id)

    def test_login_valid_different_email_format(self):
        req = self.factory.post(
            '/api/account/login', {'email': 'test@Example.com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])

        self.assertEqual(claims['sub'], self.user.id)

    def test_login_wrong_user(self):
        req = self.factory.post(
            '/api/account/login', {'email': 'test_nonexistant@example.com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'User with that email does not exist'])

    def test_login_wrong_password(self):
        req = self.factory.post(
            '/api/account/login', {'email': 'test@example.com', 'password': 'wrong_password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Password is incorrect'])

    def test_login_invalid_email(self):
        req = self.factory.post(
            '/api/account/login', {'email': 'test', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])


class AccountTestSignup(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

    def test_signup_valid(self):
        req = self.factory.post('/api/account/signup', {
                                'email': 'test_new@example.com', 'password': 'new_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        new_user = User.objects.get(email='test_new@example.com')

        claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])

        self.assertEqual(claims['sub'], new_user.id)

    def test_signup_existing(self):
        req = self.factory.post(
            '/api/account/signup', {'email': 'test@example.com', 'password': 'new_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['User already exists'])

    def test_signup_invalid_email(self):
        req = self.factory.post('/api/account/signup', {
                                'email': 'test_new', 'password': 'new_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])
