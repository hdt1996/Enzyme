from django.contrib import admin
from .models import *
# Register your models here.

for m in [CssAnimatable,CssBrowserSupport,CssDefaultValues,CssEntities,CssFallbackFonts,CssFunctions,
        CssPxEmConverter,CssReference,CssReferenceAural,CssSelectors,CssUnits,CssProperties]:
    admin.site.register(m)

