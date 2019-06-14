"""
Utility functions for interacting with the GitHub API.
"""
import hashlib
import hmac
from fnmatch import fnmatch

from flask import current_app
from github import Github


def is_signature_valid(request_obj):
    """
    Check the HMAC signature and return if it is valid or not.
    """
    signature = request_obj.headers.get('X-Hub-Signature')
    if signature is not None:
        secret = current_app.config['GITHUB_WEBHOOK_SECRET'].encode('utf-8')
        mac = hmac.new(secret, msg=request_obj.data, digestmod=hashlib.sha1)
        return hmac.compare_digest('sha1={}'.format(mac.hexdigest()), signature)
    return False


def get_client():
    """
    Return the GitHub client.
    """
    return Github(current_app.config['GITHUB_ACCESS_TOKEN'])


def get_pr(repo, pr_number):
    """
    Return the pull request object for the given repository and pull request number.
    """
    try:
        return get_client().get_repo(repo).get_pull(pr_number)
    except Exception:
        current_app.logger.error('Failed to retrieve the details of {}: #{}'.format(repo, pr_number))
        raise


def get_file_names(files):
    """
    Returns a list of file names from an iterable containing the 'File' object.
    """
    return [f.filename for f in files]


def get_comparison_file_names(repo, base, head):
    """
    Return the file names of the file names modified in the given comparison.
    """
    return get_file_names(get_client().get_repo(repo).compare(base, head).files)


def get_target_branch(pr):
    """
    Return the target branch name of a pull request.
    """
    return pr.base.ref


def should_send_notification(data):
    """
    Return whether the notification should be sent for the given request data or not.
    """
    action = data['action']
    notify = False
    if action in ('opened', 'closed', 'synchronize', 'reopened'):
        repo = data['repository']['full_name']
        pr_number = data['number']
        pr = get_pr(repo, pr_number)
        matched = False
        for modified_file in pr.get_files():
            config = current_app.config['WATCH_CONFIG'].get(repo)
            if config:
                for pattern in config['patterns']:
                    if fnmatch(modified_file.filename, pattern):
                        matched = True
                        break
                if matched:
                    break
        if matched:
            notify = True
            if action == 'synchronize':
                target = get_target_branch(pr)
                previous_head = data['before']
                for modified_file in get_comparison_file_names(repo, target, previous_head):
                    if fnmatch(modified_file, 'docs/*'):
                        notify = False
                        break
    return notify
