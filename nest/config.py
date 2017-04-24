import os


class BaseConfiguration:
    BOTO3_SERVICES = ['s3']
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'JPSv9Ha0sNOurExAICuF0Pq1W9t9OV'
    AUTHOMATIC = {
        'google': {
            'class_': 'authomatic.providers.oauth2.Google',

            # Provider type specific keyword arguments:
            'short_name': 2,
            'consumer_key': os.environ['GOOGLE_CLIENT_ID'],
            'consumer_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'scope': ['https://www.googleapis.com/auth/userinfo.profile',
                      'https://www.googleapis.com/auth/userinfo.email']
        }
    }


class DevelopmentConfiguration(BaseConfiguration):
    DEBUG = True
    S3_BUCKET = "nest.pygillier.me"
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class TestingConfiguration(BaseConfiguration):
    TESTING = True


class ProductionConfiguration(BaseConfiguration):
    pass
