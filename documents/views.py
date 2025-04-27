from django.views.generic import TemplateView

# Create your views here.
class DocumentUploadView(TemplateView):
    template_name = "documents/index.html"