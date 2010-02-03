from django.test import TestCase
from rapidsms import *
from rapidsms.connection import *
from rapidsms.tests.scripted import TestScript
from register.models import *
from reporters.models import PersistantBackend, Reporter
from register.app import App
from poll.models import Phone
import poll.app as poll_app
import register.app as register_app
import reporters.app as reporter_app

class RegistrationTest(TestCase):
    fixtures = ['registration']
    
    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.connection = Connection(backend=self.backend, identity="1000")
        self.pconnection = Phone(backend=self.backend, 
                                 reporter=self.reporter, 
                                 identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        self.reg = Registration()
        message = Message(text='register poll 100 1001', connection=self.connection)
        message.persistant_connection = self.pconnection
        self.reg.parse(message)

    
    def test_parse(self):
        self.assertEquals(self.reg.public_identifier, 'poll')
        self.assertEquals(self.reg.governorate, '100')
        self.assertEquals(self.reg.district, '1001')
        self.assertEquals(self.reg.phone.identity, "1000")

    def test_load_by_mobile_number(self):
        query_result = Registration.objects.filter(phone__identity = '100')
        self.assertEquals(query_result.count(), 0)

        query_result = Registration.objects.filter(phone__identity = '1000')
        self.assertEquals(query_result.count(), 1)
        r = query_result.iterator().next()
        self.assertNotEquals(r, None)

    def test_to_string(self):
        r = Registration()
        r.public_identifier = "Poll"
        r.governorate = "12"
        r.district = "8"
        r.phone = self.pconnection
        self.assertEquals(str(r), "1000 Poll 12 8")