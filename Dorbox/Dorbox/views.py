from django.views.generic import TemplateView

class ThanksPage(TemplateView):
    template_name ='thanks.html'

class LandingPage(TemplateView):
    template_name = 'index.html'

class UserHome(TemplateView):
    template_name = 'user_home.html'

class HelpPage(TemplateView):
    template_name = 'help.html'
