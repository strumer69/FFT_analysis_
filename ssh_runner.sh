#!/bin/bash

REMOTE_USER="di97qid"
REMOTE_HOST="login.beast.lrz.de"
REMOTE_SCRIPT="/home/di97qid/sl/FFT/dcdb_logger.sh"

START_TIME="$1"
END_TIME="$2"
LOCAL_DIR="$3"
LABEL="$4"

# Run remote script and capture output
REMOTE_OUTPUT=$(ssh ${REMOTE_USER}@${REMOTE_HOST} \
"bash ${REMOTE_SCRIPT} \"$START_TIME\" \"$END_TIME\"")

echo "$REMOTE_OUTPUT"

# Extract output directory
REMOTE_DIR=$(echo "$REMOTE_OUTPUT" | grep "DONE:" | cut -d':' -f2)

echo "Remote directory: $REMOTE_DIR"

# Copy to local machine
scp -r ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR} "${LOCAL_DIR}"
mv "${LOCAL_DIR}/$(basename $REMOTE_DIR)" "${LOCAL_DIR}/${LABEL}"