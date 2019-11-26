#!{{ mail2slack_python_path }}

import os
import sys
import configparser
import json
import requests
import re
import email


def get_subject_from_email(message):
    subject = get_header_from_email(message, 'Subject')
    subject = re.sub(r'^Subject:\s', '', subject)
    return subject


def get_datetime_from_email(message):
    body = get_body_from_email(message).split("\n")
    datetime = [line for line in body if line.startswith('-Datetime')][0]
    datetime = re.sub(r'^-Datetime\s*:\s*', '', datetime)
    return datetime


def get_event_from_email(message):
    body = get_body_from_email(message).split("\n")
    event = [line for line in body if line.startswith('-Event')][0]
    event = re.sub(r'^-Event\s*:\s*', '', event)

    return event


def get_header_from_email(message, name):
    header = ''
    if message[name]:
        for tup in email.header.decode_header(str(message[name])):
            if type(tup[0]) is bytes:
                charset = tup[1]
                if charset:
                    header += tup[0].decode(tup[1])
                else:
                    header += tup[0].decode()
            elif type(tup[0]) is str:
                header += tup[0]
    return header


def get_body_from_email(message):
    charset = message.get_content_charset()
    payload = message.get_payload(decode=True)
    try:
        if payload:
            if charset:
                return payload.decode(charset)
            else:
                return payload.decode()
        else:
            return ""

    except:
        return payload


def parse_email(data):
    message = email.message_from_string(data)

    subject = get_subject_from_email(message)
    # datetime = get_datetime_from_email(message)
    body = get_body_from_email(message).split("\n")
    # event = get_event_from_email(message)
    # if body:
    #     if len(body) > 10:
    #         body = "文字数：" + len(body) + "本文：" + str(body)
    #     else:
    #         body = data
    # else:
    body = data

    return {
        "subject": subject,
        # "datetime": datetime,
        "body": body,
        # "event": event
    }


def is_alert_fail(event):
    if event in json.loads(config_file['alert']['FAIL_ALERTS']):
        return True

    return False


def is_alert_ok(event):
    if event in json.loads(config_file['alert']['OK_ALERTS']):
        return True

    return False


def post_to_slack(data):
    webhook_url = config_file['slack']['WEBHOOK_URL']
    username = config_file['slack']['USERNAME']
    channel = config_file['slack']['CHANNEL']
    icon = config_file['slack']['ICON']
    color = config_file['slack']['COLOR_DEFAULT']

    # event = data['event']
    #
    # if is_alert_fail(data['event']):
    #     color = config_file['slack']['COLOR_FAIL']
    #     event = event + " :x:"
    #
    # if is_alert_ok(data['event']):
    #     color = config_file['slack']['COLOR_OK']
    #     event = event + " :heavy_check_mark:"

    requests.post(webhook_url, data=json.dumps({
        'channel': channel,
        'username': username,
        'icon_emoji': icon,
        'text': data['subject'],
        'attachments': [{
            "text": data['body'],
            # "color": color,
            # "fields": [
            #     {
            #         "type": "mrkdwn",
            #         "value": "*" +  + "*",
            #         "short": False
            #     },
            # {
            #     "type": "mrkdwn",
            #     "value": "*DateTime:*\n" + data['datetime'],
            #     "short": True
            # },
            # {
            #     "type": "mrkdwn",
            #     "value": "*Event:*\n" + event,
            #     "short": True
            # }
            # ]
        }],
    }))


if __name__ == '__main__':
    # Load configuration from file`1
    config_file = configparser.ConfigParser()
    config_file.read('{{ mail2slack_config_file_path }}')

    # Load mail from stdin
    input_stdin = sys.stdin.read()
    alert_data = parse_email(input_stdin)

    post_to_slack(alert_data)
