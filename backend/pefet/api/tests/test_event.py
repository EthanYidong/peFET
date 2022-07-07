from datetime import date, timedelta

from django.test import RequestFactory, TestCase
from django.conf import settings

import bcrypt
import json
import jwt

from ..models import User, Event
from ..views import event


class EventTestAll(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        token = jwt.encode({'sub': self.user.id},
                           settings.JWT_SECRET, algorithm='HS256')
        self.authorization = f'Bearer {token}'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))
        
        cls.user2 = User.objects.create(
            email='test2@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

        cls.eventDate = date.today()

        cls.event = Event.objects.create(
            name='Testing Event', date=cls.eventDate, creator=cls.user)
        cls.event2 = Event.objects.create(
            name='Testing Event 2', date=cls.eventDate, creator=cls.user2)

    def test_get_all_events(self):
        req = self.factory.get(
            '/api/event/all', HTTP_AUTHORIZATION=self.authorization)

        resp = event.all(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        self.assertEqual(content,
                         {
                             'events': [
                                 {
                                     'creator_id': self.user.id,
                                     'date': self.eventDate.isoformat(),
                                     'id': self.event.id,
                                     'name': self.event.name
                                 }
                             ]
                         }
                         )


class EventTestCreate(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        token = jwt.encode({'sub': self.user.id},
                           settings.JWT_SECRET, algorithm='HS256')
        self.authorization = f'Bearer {token}'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

        cls.eventDate = date.today()

    def test_create_event(self):
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': self.eventDate.isoformat()}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        new_event = Event.objects.get(name='New Testing Event')

        self.assertEqual(content['id'], new_event.id)

    def test_create_event_invalid_date(self):
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '01-01-3000'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'01-01-3000\' is not a \'date\''])

    def test_create_event_invalid_date_wrong_order(self):
        # Date should be in YYYY-MM-DD, DD-MM-YYYY is the wrong order
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '01-01-2023'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'01-01-2023\' is not a \'date\''])
    
    def test_create_event_invalid_date_13_month(self):
        # Date should be in YYYY-MM-DD, 13th month doesn't exist
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2023-13-01'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-13-01\' is not a \'date\''])
    
    def test_create_event_invalid_date_31_april(self):
        # Date should be in YYYY-MM-DD, 31 April doesn't exist
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2023-04-31'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-04-31\' is not a \'date\''])
    
    def test_create_event_invalid_date_non_leap_year(self):
        # 29 Feb 2023 doesn't exist because 2023 is not a leap year
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2023-02-29'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-02-29\' is not a \'date\''])
    
    def test_create_event_invalid_date_non_leap_year_2100(self):
        # 29 Feb 2100 doesn't exist because 2100 is not a leap year (divisible by 100 but not 400)
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2100-02-29'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2100-02-29\' is not a \'date\''])
    
    def test_create_event_invalid_date_year_10000(self):
        # Date doesn't exist because it's too far in the future / only 4 year digits allowed
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '10000-01-01'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'10000-01-01\' is not a \'date\''])
    
    def test_create_event_invalid_dd_one_digit(self):
        # Date doesn't exist because DD should be 2 digits
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2023-01-1'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-01-1\' is not a \'date\''])
    
    def test_create_event_invalid_mm_one_digit(self):
        # Date doesn't exist because MM should be 2 digits
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '2023-1-01'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-1-01\' is not a \'date\''])
    
    def test_create_event_invalid_yyyy_two_digits(self):
        # Date doesn't exist because YYYY should be 4 digits
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': '23-01-01'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'23-01-01\' is not a \'date\''])
    
    def test_create_event_invalid_date_blank(self):
        # Blank date is invalid
        req = self.factory.post(
            '/api/event/create', {'name': 'New Testing Event', 'date': ''}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.create(req)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'\' is not a \'date\''])


class EventTestUpdate(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        token = jwt.encode({'sub': self.user.id},
                           settings.JWT_SECRET, algorithm='HS256')
        self.authorization = f'Bearer {token}'

        token2 = jwt.encode({'sub': self.user2.id},
                           settings.JWT_SECRET, algorithm='HS256')
        self.authorization2 = f'Bearer {token2}'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

        cls.user2 = User.objects.create(
            email='test2@example.com', password=bcrypt.hashpw(b'password', bcrypt.gensalt()))

        cls.eventDate = date.today()
        cls.event = Event.objects.create(
            name='Testing Event', date=cls.eventDate, creator=cls.user)

    def test_update_event(self):
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': newEventDate.isoformat()}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 200)
        _content = json.loads(resp.content)

        new_event = Event.objects.get(id=self.event.id)
        self.assertEqual(new_event.name, 'New Testing Event')
        self.assertEqual(new_event.date, newEventDate)

    def test_update_event_wrong_user(self):
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': newEventDate.isoformat()}, 'application/json', HTTP_AUTHORIZATION=self.authorization2)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Unauthorized to update this event'])

    def test_update_event_invalid_date(self):
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': '01-01-3000'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'01-01-3000\' is not a \'date\''])
    
    def test_update_event_invalid_date_DDMMYYYY(self):
        # 01-01-2023 is not a valid date because the format is YYYY-MM-DD
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': '01-01-2023'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'01-01-2023\' is not a \'date\''])
    
    def test_update_event_invalid_date_non_leap_year(self):
        # 2023-02-29 is not a valid date because 2023 is not a leap year
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': '2023-02-29'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'2023-02-29\' is not a \'date\''])

    def test_update_event_invalid_date_year_0000(self):
        # 0000-01-01 is not a valid date (whereas 0001-01-01 is valid)
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': '0000-01-01'}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'0000-01-01\' is not a \'date\''])
    
    def test_update_event_invalid_date_blank(self):
        # blank date is invalid
        newEventDate = self.eventDate + timedelta(days=1)

        req = self.factory.post(
            f'/api/event/{self.event.id}/update', {'name': 'New Testing Event', 'date': ''}, 'application/json', HTTP_AUTHORIZATION=self.authorization)

        resp = event.update(req, self.event.id)

        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], [
                         'Invalid JSON: \'\' is not a \'date\''])