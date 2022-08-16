from django.urls import path, include
from .views import GetCSSProps
from django.views.generic import TemplateView

urlpatterns=[
path('get_css_props',GetCSSProps.as_view())
]
