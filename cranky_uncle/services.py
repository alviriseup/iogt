import logging, requests
import uuid
from cranky_uncle.models import Interactive
from wagtail.core.models import Page
from django.contrib.auth import get_user_model



class RapidProApiService(object):
    ACCESS_TOKEN = 'Token 3599dfede6caf725712581703f8ff5928f3fd1c9'
    RAPID_URL = 'https://rapidpro.rultest2.com'

    def __init__(self):
        pass

    def test(self):
        return str(uuid.uuid4())

    def get_current_contact(self, user: object = None):
        response = requests.get(
            f'{self.RAPID_URL}/api/v2/flows.json',
            params={'urn': f'ext:{user}'},
            headers={'Authorization': self.ACCESS_TOKEN},
        )

        if len(response.json().get('results')) < 1:
            data = {
                "name": "Cranky User",
                "urns": [f"ext:{user}"]
            }
            response = requests.post(
                f'{self.RAPID_URL}/api/v2/flows.json',
                headers={'Authorization': self.ACCESS_TOKEN},
                json=data,
            )
        return response.json().get('results')[0] if response.json().get('results') else None

    def send_message(self, data=None, slug=None):
        # url = f'{self.RAPID_URL}/c/ex/7db731d2-dadd-49b6-98a5-63a635b180e8/receive'
        headers = {'Authorization': self.ACCESS_TOKEN}
        
        # TODO: optimize dynamic url allocation............
        core_page_id = Page.objects.filter(slug=slug).first().id
        uncle_page = Interactive.objects.filter(page_ptr_id=core_page_id).first()
        url = uncle_page.channel.request_url

        try:
            response = requests.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            logging.info(f'Send message: {response.text}')
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f'Error sending message: {e}')
            return None


    def get_user_identifier(self, request):
        if not request.session.session_key:
            request.session.save()

        session_uid = request.session.setdefault('cranky_uuid', str(uuid.uuid4()))
        # session_uid = request.COOKIES.get('cranky_uid', str(uuid.uuid4()))
        
        # Get the authenticated user
        user = request.user

        # If the user is authenticated and has no 'cranky_uuid' set, update it
        if user.is_authenticated and not user.cranky_uuid:
            user_model = get_user_model()
            user.cranky_uuid = session_uid
            user_model.objects.filter(pk=user.pk).update(cranky_uuid=session_uid)

        return session_uid
    
    def get_session_uid(self, request):
        return request.COOKIES.get('cranky_uid', str(uuid.uuid4()))