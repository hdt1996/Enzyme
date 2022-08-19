import inspect, re

class ChoiceSettings():
    def __init__(self):
        self.db = \
            inspect.cleandoc(
            """
            DATABASES = {{
                'default': {{
                    'ENGINE': '{dbengine}',
                    'NAME': '{dbname}',
                    'USER': '{dbuser}',
                    'PASSWORD': '{dbpassword}',
                    'HOST': '{dbhost}',
                    'PORT': '{dbport}',
                }}
            }}
            """)
        self.apps = \
            [
                "\n    'django.contrib.admin'",
                "'django.contrib.auth'",
                "'django.contrib.contenttypes'",
                "'django.contrib.sessions'",
                "'django.contrib.messages'",
                "'django.contrib.staticfiles'",
            ]
        self.middleware = \
            [
                "\n\t'django.middleware.security.SecurityMiddleware'",
                "'django.contrib.sessions.middleware.SessionMiddleware'",
                "'django.middleware.common.CommonMiddleware'",
                "'django.middleware.csrf.CsrfViewMiddleware'",
                "'django.contrib.auth.middleware.AuthenticationMiddleware'",
                "'django.contrib.messages.middleware.MessageMiddleware'",
                "'django.middleware.clickjacking.XFrameOptionsMiddleware'",
            ]
        self.oauth = \
            inspect.cleandoc(
            """
                REST_FRAMEWORK = {{
                    'DEFAULT_PERMISSION_CLASSES':[
                        {permissions}
                    ],
                    'DEFAULT_AUTHENTICATION_CLASSES':[
                        {authentication}
                    ]
                }}      
            """)

    def matchDBSetting(self,txt:str):
        match = re.findall("""(DATABASES[ ]*\=[ ]*\{([ a-zA-Z\'\.\n\,\/\:\{\d\_\#\@]*[ ]*\})[\n ]*\})""",txt)
        if len(match) > 0:
            match = match[0][0]
        else: 
            return False
        return match
    def matchAuthSetting(self,txt:str):
        match = re.findall("""(REST_FRAMEWORK[ ]*\=[ ]*(\{[ a-zA-Z\'\.\n\,\t\/\:\{\d\_\#\[\]]*[ ]*[\n ]*\}))""",txt)
        if len(match) > 0:
            match = match[0][0]
        else: 
            return False
        return match