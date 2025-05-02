from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = "chats/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = self.kwargs.get("document_id")
        context["document_id"] = document
        return context
