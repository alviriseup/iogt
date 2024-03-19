import re
import uuid
from datetime import datetime
from time import sleep
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.core.models import Page
from .services import RapidProApiService
from .models import RapidPro, Interactive
from .forms import CrankySendMessageForm
from .models import RapidPro
from .serializers import RapidProSerializer


class CrankyUncleQuizView(TemplateView):
    template_name = 'cranky_uncle/cranky_uncle_quiz.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs['slug']
        
        # session_uid = request.COOKIES.get('cranky_uid')
        user = RapidProApiService().get_user_identifier(request)
        
        if not user:
            return redirect('/')
        
        referer_lang = request.META.get('HTTP_REFERER').split('/')[3]
        current_lang = self.request.build_absolute_uri().split('/')[3]
        
        if(referer_lang != current_lang):
            core_page_id = Page.objects.filter(slug=slug).first().id
            uncle_page = Interactive.objects.filter(page_ptr_id=core_page_id).first()

            data = {
                'from': user,
                'text': uncle_page.trigger_string + '_' + current_lang
            }
            
            RapidProApiService().send_message(data=data, slug=slug)
        
        context['db_data'] = self.get_message_from_db(user=user)
        context['slug'] = slug
        
        
        return render(request, self.template_name, context)

    def get_message_from_db(self, user):
        # wait a second to receive new message from rapidpro
        sleep(1)

        # Retrieve the latest chat for the user
        chat = RapidPro.objects.filter(to=user).order_by('-created_at').first()

        if not chat:
            return None

        text = chat.text.strip()

        # Check if the message has a next message indicator, then sleep for 3 seconds
        if text.endswith('[CONTINUE]'):
            sleep(3)
            chat = RapidPro.objects.filter(to=user).order_by('-created_at').first()
            text = chat.text.strip()

        # Extract content between [MESSAGE] and [/MESSAGE]
        message_match = re.search(r'\[MESSAGE](.*?)\[\/MESSAGE]', text)
        message_content = message_match.group(1) if message_match else ''

        # Extract content between [POINT] and [/POINT]
        point_match = re.search(r'\[POINT](.*?)\[\/POINT]', text)
        point_content = point_match.group(1) if point_match else ''

        return {
            'message': text,
            'point': point_content,
            'buttons': chat.quick_replies
        }
    
    def post(self, request, slug):
        form = CrankySendMessageForm(request.POST)
        cranky_page_url = request.META.get('HTTP_REFERER')
        
        # session_uid = request.COOKIES.get('cranky_uid', str(uuid.uuid4()))
        
        if form.is_valid():
            user = RapidProApiService().get_user_identifier(request)

            data = {
                'from': user,
                'text': form.cleaned_data['text']
            }
            
            response = RapidProApiService().send_message(data=data, slug=slug)
            response = redirect('cranky:cranky-quiz', slug=slug)
            # response.set_cookie(key='cranky_uid', value=session_uid)
            return response
        else:
            # Handle invalid form
            return redirect(cranky_page_url)


class RapidProMessageHook(APIView):
    queryset = RapidPro.objects.all()
    serializer_class = RapidProSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        '''
            {
                "id": "4796",
                "text": "[POINT] 0 [/POINT] [CONTINUE]",
                "to": "admin@admin.com",
                "to_no_plus": "admin@admin.com",
                "from": "cranky_uncle",
                "from_no_plus": "cranky_uncle",
                "channel": "2d18d133-46b2-4a9c-bc70-35f373c6b445",
                "quick_replies": [
                ]
            }
        '''

        rapidpro_id = data.get('id')
        text = data.get('text')
        to = data.get('to')
        from_field = data.get('from')
        channel = data.get('channel')
        quick_replies = data.get('quick_replies')

        prev_msg = RapidPro.objects.filter(to=to).order_by('-created_at').first()

        if prev_msg:
            prev_msg_text = prev_msg.text.strip()

            if prev_msg_text.endswith('[CONTINUE]'):
                text = prev_msg_text + text
            else:
                text = text

            dic = {'rapidpro_id': rapidpro_id, 'text': text, 'quick_replies': quick_replies}
            RapidPro.objects.filter(rapidpro_id=prev_msg.rapidpro_id).update(**dic)
        else:
            RapidPro.objects.create(
                rapidpro_id=rapidpro_id,
                text=text,
                quick_replies=quick_replies,
                to=to,
                from_field=from_field,
                channel=channel,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

        # return JsonResponse(data)

        return Response('ok', status=status.HTTP_201_CREATED)

        #TODO: add serializer check
        # serializer = self.serializer_class(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response('ok', status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

