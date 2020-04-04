from django.test import RequestFactory

client = RequestFactory()
response = client.get('http://127.0.0.1:8000/store/packages/sold-store-package-phase-detail-list/?object_id=&content_type=soldstorepaidpackagephase')
print(response)