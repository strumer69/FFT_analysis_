#!/bin/bash

# ---------- INPUT ----------
START_TIME="$1"
END_TIME="$2"

# ---------- BASE OUTPUT (REMOTE SAFE PATH) ----------
BASE_OUTPUT="/home/di97qid/sl/FFT"

# Create folder name from start date
DATE_TAG=$(date -d "$START_TIME" +"%Y-%m-%d_%H-%M-%S")

OUTPUT_BASE="${BASE_OUTPUT}/dcdb_${DATE_TAG}"

# ---------- SETTINGS ----------
BASE_SENSOR="/qic/coldlab/magnetometer"
AXES=("X" "Y" "Z")

STEP=70
WINDOW=10

# ---------- TIME CONVERSION ----------
start_ts=$(date -d "$START_TIME" +%s)
end_ts=$(date -d "$END_TIME" +%s)

echo "Creating base directory: $OUTPUT_BASE"
mkdir -p "$OUTPUT_BASE"

for axis in "${AXES[@]}"
do
    SENSOR="$BASE_SENSOR/$axis"
    OUTPUT_DIR="${OUTPUT_BASE}/${axis}"

    mkdir -p "$OUTPUT_DIR"

    current_ts=$start_ts

    while [ $current_ts -le $end_ts ]
    do
        start_time=$(date -d "@$current_ts" +"%Y-%m-%dT%H:%M:%S")
        end_time=$(date -d "@$((current_ts + WINDOW))" +"%Y-%m-%dT%H:%M:%S")

        filename=$(date -d "@$current_ts" +"data_%Y-%m-%d_%H-%M.csv")

        dcdbquery "$SENSOR" "$start_time" "$end_time" > "$OUTPUT_DIR/$filename"

        current_ts=$((current_ts + STEP))
    done
done

echo "DONE:$OUTPUT_BASE"
