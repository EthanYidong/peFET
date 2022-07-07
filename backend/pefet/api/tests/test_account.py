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
            '/api/account/login', {'email': 'test_nonexistent@example.com', 'password': 'password'}, 'application/json')
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
    
    def test_login_password_case_sensitive(self):
        # The password should be case sensitive. "password" is a different password from "passworD".
        req = self.factory.post(
            '/api/account/login', {'email': 'test@example.com', 'password': 'passworD'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Password is incorrect'])

    def test_login_blank_password(self):
        # A blank password (obviously) shouldn't allow the user to login.
        req = self.factory.post(
            '/api/account/login', {'email': 'test@example.com', 'password': ''}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Password is incorrect'])
    
    def test_login_whitespace_in_password_not_ignored(self):
        # "password " should be regarded as a different password from "password". 
        req = self.factory.post(
            '/api/account/login', {'email': 'test@example.com', 'password': 'password '}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Password is incorrect'])
    
    def test_login_invalid_email_format_at_dot_wrong_order(self):
        # "test.example@com" should be considered an invalid email format.
        req = self.factory.post(
            '/api/account/login', {'email': 'test.example@com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])

    def test_login_email_local_part_case_sensitive(self):
        # "Test@example.com" should be considered different to "test@example.com", because the local part is case sensitive.
        req = self.factory.post(
            '/api/account/login', {'email': 'Test@example.com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'User with that email does not exist'])
    
    def test_login_special_characters(self):
        # special characters can be considered a valid email, resulting in does not exist error instead of invalid email format error
        req = self.factory.post(
            '/api/account/login', {'email': 'test+123@example.com', 'password': 'password'}, 'application/json')
        resp = account.login(req)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'User with that email does not exist'])



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

    def test_signup_valid_symbols_in_email(self):
        # Some symbols are allowed in email addresses.
        req = self.factory.post('/api/account/signup', {
                                'email': 'a.b-c+d+e_f-@example.com', 'password': 'test plus hyphen dot underscore'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        new_user = User.objects.get(email='a.b-c+d+e_f-@example.com')

        claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])

        self.assertEqual(claims['sub'], new_user.id)
    
    def test_signup_valid_64_characters_long_local_part(self):
        # 64 character long local parts in email addresses should be allowed.
        req = self.factory.post('/api/account/signup', {
                                'email': 'this-local-part-is-64-characters-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm@example.com', 'password': '64_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        new_user = User.objects.get(email='this-local-part-is-64-characters-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm@example.com')

        claims = jwt.decode(content['token'], settings.JWT_SECRET, ['HS256'])

        self.assertEqual(claims['sub'], new_user.id)
    
    def test_signup_valid_longest_possible_email(self):
        # longest possible accepted email (64 + 1 + 63 + 1 + 63 = 192 chars)
        req = self.factory.post('/api/account/signup', {
                                'email': '64-characters-local-part-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm@63-characters-before-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm.63-characters-after-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                                'password': '192_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        new_user = User.objects.get(email='64-characters-local-part-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm@63-characters-before-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm.63-characters-after-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')

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
    
    def test_signup_invalid_65_characters_long_local_part(self):
        # 65 character long (or longer) local parts in email addresses should not be allowed.
        req = self.factory.post('/api/account/signup', {
                                'email': 'this-local-part-is-65-characters-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm@example.com', 'password': '65_password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])
    
    def test_signup_invalid_64_characters_long_middle_part(self):
        # If the part between the @ and . is 64 characters long or more, return a HTTP 400 'Invalid email format' error.
        req = self.factory.post('/api/account/signup', {
                                'email': 'test@64-characters-before-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm.com',
                                'password': 'password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])
    
    def test_signup_invalid_64_characters_long_end_part(self):
        # If the part after the . is 64 characters long or more, return a HTTP 400 'Invalid email format' error.
        req = self.factory.post('/api/account/signup', {
                                'email': 'test@example.64-characters-after-dot-mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                                'password': 'password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])
    
    def test_signup_invalid_underscore_in_domain_part(self):
        # Underscore in domain part of email shouldn't be allowed
        req = self.factory.post('/api/account/signup', {
                                'email': 'test@exam_ple.com', 'password': 'password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])
    
    def test_signup_invalid_underscore_in_domain_part_2(self):
        # Underscore in domain part of email shouldn't be allowed
        req = self.factory.post('/api/account/signup', {
                                'email': 'test@example.c_om', 'password': 'password'}, 'application/json')
        resp = account.signup(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Invalid email format'])