#!/bin/bash

TEXT=$(cat -)
WEBHOOK_URL="{{ slack_web_hook_url }}"
CHANNEL="{{ slack_channel }}"
ICON="{{ slack_icon }}"
USERNAME="$(hostname)"
TEXT_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S %Z')] "

if [ "${TEXT}" == "" ]; then
    #echo "text is empty."
    exit 0
fi

MESSAGE="{\"channel\": \"#${CHANNEL}\", \"icon_emoji\": \"${ICON}\", \"username\": \"${HOSTNAME}\", \"text\": \"${TEXT_PREFIX}\"}"

RESULT=$(echo $MESSAGE \
| jq ".text += \"${TEXT}\"" \
| curl -s -X POST \
--data-binary @- \
${WEBHOOK_URL})

if [ "${RESULT}" != "ok" ]; then
    echo ${RESULT}
    exit 1
fi
exit 0
