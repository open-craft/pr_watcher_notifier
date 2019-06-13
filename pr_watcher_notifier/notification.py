"""
Utility functions for sending notifications.
"""

from flask import current_app, render_template
from flask_mail import Message

from . import mail


def send_email(context):
    """
    Send the notification email.
    """
    subject = context['subject'].format(**context)
    body = render_template('email_body.txt', **context)
    msg = Message(
        subject,
        recipients=context['to'],
    )
    msg.body = body
    mail.send(msg)


def send_notifications(data):
    """
    Wrapper method to send out notifications.
    """
    pr_data = data['pull_request']
    repo = data['repository']['full_name']
    context = {
        'repo': repo,
        'number': data['number'],
        'action': data['action'] if data['action'] != 'synchronize' else 'updated',
        'merged': pr_data['merged'],
        'creator': pr_data['user']['login'],
        'to': current_app.config['WATCH_CONFIG'][repo]['recipients'],
        'subject': current_app.config['WATCH_CONFIG'][repo]['subject'],
        'pr_url': pr_data['_links']['html']['href']
    }
    send_email(context)
