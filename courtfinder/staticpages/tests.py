from mock import Mock, patch

from django.test import TestCase, Client, RequestFactory
from django.conf import settings
from django.utils import translation

from .forms import FeedbackForm
from django.core import management, mail
from django.core.management.commands import loaddata
from .views import feedback_submit


class SearchTestCase(TestCase):

    def setUp(self):
        test_data_dir = settings.PROJECT_ROOT +  '/data/test_data/'
        management.call_command('loaddata', test_data_dir + 'test_data.yaml', verbosity=0)

    def test_top_page_returns_correct_content(self):
        c = Client()
        response = c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/index.jinja')

    def test_feedback_page_returns_correct_content(self):
        c = Client()
        response = c.get('/feedback')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staticpages/feedback.jinja')

    def test_feedback_sent_page_returns_correct_content(self):
        with patch('django.core.mail.send_mail', Mock(return_value=2)):
            c = Client()
            settings.FEEDBACK_EMAIL_SENDER="sender@b.com"
            settings.FEEDBACK_EMAIL_RECEIVER="receiver@b.com"
            response = c.post('/feedback_submit',
                              {
                                  'feedback_text': 'I like it',
                                  'feedback_email': 'a@b.com',
                                  'feedback_referer': 'http://example.org',
                              },
                              follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'staticpages/feedback_sent.jinja')
            self.assertContains(response, '<h1>Thank you for your feedback</h1>')
            response = c.post('/feedback_submit',
                              {
                                  'feedback_text': 'I like it',
                                  'feedback_referer': 'http://example.org',
                              },
                              follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'staticpages/feedback_sent.jinja')
            self.assertContains(response, '<h1>Thank you for your feedback</h1>')

    def test_court_id_redirect(self):
        c = Client()
        r = c.get('/courts/accrington-magistrates-court')
        r = c.get('/?court_id=7')
        self.assertRedirects(r, '/courts/accrington-magistrates-court', 302)
        r = c.get('/?court_id=2038')
        self.assertEqual(r.status_code, 404)


class FeedbackFormTestCase(TestCase):

    def setUp(self):
        self.post_data = {
            "feedback_text": "ra ra ra",
            "feedback_referer": "www.a.url.com",
            "feedback_email": "",
            "feedback_name": ""
        }
        self.factory = RequestFactory()

    def test_form_honeypot_field_invalid_if_not_empty(self):

        self.post_data["feedback_name"] = "should be empty"

        form = FeedbackForm(self.post_data)

        self.assertFalse(form.is_valid())

    def test_form_honeypot_field_valid_if_empty(self):

        form = FeedbackForm(self.post_data)

        self.assertTrue(form.is_valid())

    @patch('staticpages.views.get_language_from_request', return_value='cy')
    def test_correct_welsh_to_addresses(self, get_language_from_request):
        mail.outbox = []
        request = self.factory.post('/feedback_submit', self.post_data,
                                        follow=True)
        feedback_submit(request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'welsh_receive@b.com')

    @patch('staticpages.views.get_language_from_request', return_value='en')
    def test_correct_english_to_addresses(self, get_language_from_request):
        mail.outbox = []
        request = self.factory.post('/feedback_submit', self.post_data,
                                        follow=True)
        feedback_submit(request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'eng_receive@a.com')