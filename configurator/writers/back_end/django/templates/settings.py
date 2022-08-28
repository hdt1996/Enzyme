import inspect, re

class ChoiceSettings():
    def __init__(self):
        print('Initialized Choice Settings')
        self.databases = \
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
        self.installed_apps = \
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
        self.rest_framework = \
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
        super().__init__()

