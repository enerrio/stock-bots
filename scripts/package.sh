#!/bin/bash
set -e

echo "Exporting dependencies..."
uv export --frozen --no-dev --no-editable -o requirements.txt

echo "Installing dependencies into packages folder..."
rm -rf packages
mkdir packages
uv pip install \
    --no-installer-metadata \
    --no-compile-bytecode \
    --python-platform x86_64-manylinux2014 \
    --python 3.13 \
    --target packages \
    -r requirements.txt

# Define array of market bots
BOTS=("domestic" "international" "futures")

for BOT in "${BOTS[@]}"; do
    TMP_DIR="package_${BOT}"
    ZIPFILE="package_${BOT}.zip"
    rm -rf "${TMP_DIR}"
    mkdir -p "${TMP_DIR}"

    echo "Copying common dependencies to ${TMP_DIR}..."
    cp -r packages/* "${TMP_DIR}/"

    echo "Adding shared code..."
    # Copy common bot code
    mkdir -p "${TMP_DIR}/bot"
    cp -r bot/common "${TMP_DIR}/bot/"
    cp -r bot/__init__.py "${TMP_DIR}/bot/"

    echo "Adding ${BOT} specific code..."
    cp -r "bot/${BOT}" "${TMP_DIR}/bot/"

    if [ -d "config/${BOT}" ]; then
        echo "Adding config for ${BOT}..."
        mkdir -p "${TMP_DIR}/config"
        cp -r "config/${BOT}" "${TMP_DIR}/config/"
    fi

    if [ -f ".env.${BOT}" ]; then
        echo "Adding .env file for ${BOT}..."
        cp ".env.${BOT}" "${TMP_DIR}/"
    fi

    echo "Creating zip package ${ZIPFILE}..."
    (cd "${TMP_DIR}" && zip -r "../${ZIPFILE}" .)
    rm -rf "${TMP_DIR}"
    echo "Package created: ${ZIPFILE}"

done

rm -rf packages

echo "All packages created successfully."
