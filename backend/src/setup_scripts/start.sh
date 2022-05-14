#! /usr/bin/env sh
set -e
echo "Running start.sh script"

DEFAULT_MODULE_NAME=main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

if [ "$DEV" = True ]; then
    echo "Running development version - uvicorn with live reload "
    echo "uvicorn --reload --host "$HOST" --port "$PORT" --log-level info "$APP_MODULE""
    exec uvicorn --reload --host $HOST --port $PORT --log-level info "$APP_MODULE"
else
    echo "Running gunicorn version"

    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
    export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
    export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

    # Start Gunicorn
    echo "gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE""
    exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
fi
