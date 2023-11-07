from typing import Type, List, Union
from django.urls import URLResolver, URLPattern

APIUrlPatternsType = List[URLPattern]
UrlPatternsType = List[URLResolver]
UrlCompositePatternsType = List[Union[URLResolver, URLPattern]]