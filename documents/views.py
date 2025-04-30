from django.shortcuts import redirect, render
from django.views.generic import View

# from core.ai.chromadb import chroma, openai_ef

from .models import Document
from .tasks import process_document


# Create your views here.
class DocumentUploadView(View):
    def get(self, request):
        return render(request, template_name='documents/index.html')
    
    def post(self, request):
        file = request.FILES.get("file")

        try:
            document = Document.objects.create(file=file, name=file.name)

            process_document(document)
        except Exception as e:
            print(e)

        return redirect("documents")
    
# class QueryView(View):
#     def get(self, request):
#         return render(request, template_name='documents/query.html')
    
#     def post(self, request):
#         query = request.POST.get("query")

#         collection = chroma.get_collection(name="6810f05055ef861d1baaf883", embedding_function=openai_ef)
#         data = collection.query(
#             query_texts=[query],
#             n_results=3
#         )

#         print(data)

#         return redirect("documents")