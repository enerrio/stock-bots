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

echo "Packaging dependencies..."
rm -rf package.zip
cd packages
zip -r ../package.zip .
cd ..

echo "Packaging application code..."
zip -r package.zip bot config .env

echo "Package created: package.zip"
