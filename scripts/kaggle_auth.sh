#!/usr/bin/env bash
set -e

if [ -z "$KAGGLE_API_TOKEN" ]; then
  echo "KAGGLE_API_TOKEN is not set"
  exit 1
fi

mkdir -p ~/.kaggle

cat > ~/.kaggle/kaggle.json <<EOF
{
  "username": "erickmagyar",
  "key": "${KAGGLE_API_TOKEN}"
}
EOF

chmod 600 ~/.kaggle/kaggle.json