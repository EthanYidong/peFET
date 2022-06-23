from datetime import date

from django.test import RequestFactory, TestCase
from django.conf import settings

import bcrypt
import json
import jwt

from ..models import User, Event, Participant
from ..views import event


class ParticipantTestAll(TestCase):
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
        cls.event = Event.objects.create(name='Test Event', date=cls.eventDate, creator=cls.user)

        cls.participant1 = Participant.objects.create(name='Test Participant', email='test_participant@example.com', event=cls.event)

    def test_get_participants(self):
        req = self.factory.get(
            f'/api/event/{self.event.id}/participants', HTTP_AUTHORIZATION=self.authorization)
        
        resp = event.read_participants(req, self.event.id)

        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)

        self.assertEqual(content['participants'], [{
            'id': self.participant1.id,
            'name': self.participant1.name,
            'email': self.participant1.email,
            'status': self.participant1.status,
            'event_id': self.event.id,
            'last_email_sent': None,
        }])

    def test_get_participants_wrong_user(self):
        req = self.factory.get(
            f'/api/event/{self.event.id}/participants', HTTP_AUTHORIZATION=self.authorization2)
        
        resp = event.read_participants(req, self.event.id)

        self.assertEqual(resp.status_code, 401)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['Unauthorized to read from this event'])


    def test_get_participants_no_such_event(self):
        req = self.factory.get(
            f'/api/event/0/participants', HTTP_AUTHORIZATION=self.authorization)
        
        resp = event.read_participants(req, 0)

        self.assertEqual(resp.status_code, 404)
        content = json.loads(resp.content)

        self.assertEqual(content['errors'], ['No such event'])



