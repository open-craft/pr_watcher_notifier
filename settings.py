import os

GITHUB_WEBHOOK_SECRET = os.environ['GITHUB_WEBHOOK_SECRET']
GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']

WATCH_CONFIG = {
    'edx/edx-platform': {
        'patterns': ['doc/*', ],
        'recipients': ['nobody@example.com', ],
        'subject': '[ADR] Pull request: {repo} #{number} {action}',
    },
}
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
