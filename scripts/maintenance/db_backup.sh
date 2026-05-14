#!/bin/sh

set -e

# Configuration
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-trading_platform}
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="trading_platform_${TIMESTAMP}.sql.gz"
LOCAL_PATH="${BACKUP_DIR}/${FILENAME}"

# R2 Configuration
R2_BUCKET="webz-maw-apps-01"
R2_PATH="s3://${R2_BUCKET}/tradepanel/backups/db/daily/${FILENAME}"

# S3 Configuration
S3_BUCKET="webz-maw-apps-01"
S3_PATH="s3://${S3_BUCKET}/tradepanel/backups/db/daily/${FILENAME}"

# Notification helper
send_telegram() {
  local MESSAGE=$1
  if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d chat_id="${TELEGRAM_CHAT_ID}" \
      -d text="${MESSAGE}" \
      -d parse_mode="HTML" > /dev/null
  else
    echo "Telegram credentials not set, skipping notification."
  fi
}

echo "[$(date)] Starting database backup..."

# 1. Dump and compress
echo "[$(date)] Dumping database to ${LOCAL_PATH}..."
if PGPASSWORD="${DB_PASSWORD}" pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" | gzip > "${LOCAL_PATH}"; then
  echo "[$(date)] Local backup successful."
else
  ERROR_MSG="🚨 <b>Database Backup Failed</b>%0AStage: Local pg_dump%0ADatabase: ${DB_NAME}"
  echo "[$(date)] Backup failed during pg_dump."
  send_telegram "${ERROR_MSG}"
  exit 1
fi

FILE_SIZE=$(stat -c%s "${LOCAL_PATH}")
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))

UPLOAD_SUCCESS=true
UPLOAD_MESSAGES=""

ORIG_AWS_REGION="${AWS_DEFAULT_REGION}"

# 2. Upload to Cloudflare R2 (Primary)
if [ -n "$R2_ACCESS_KEY_ID" ] && [ -n "$R2_SECRET_ACCESS_KEY" ] && [ -n "$R2_ENDPOINT_URL" ]; then
  echo "[$(date)] Uploading to Cloudflare R2..."
  export AWS_ACCESS_KEY_ID="${R2_ACCESS_KEY_ID}"
  export AWS_SECRET_ACCESS_KEY="${R2_SECRET_ACCESS_KEY}"
  export AWS_DEFAULT_REGION="auto"
  
  # Ensure bucket exists
  aws s3 mb s3://${R2_BUCKET} --endpoint-url "${R2_ENDPOINT_URL}" 2>/dev/null || true
  
  if aws s3 cp "${LOCAL_PATH}" "${R2_PATH}" --endpoint-url "${R2_ENDPOINT_URL}"; then
    echo "[$(date)] R2 upload successful."
    UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A✅ R2 Upload: Success"
  else
    echo "[$(date)] R2 upload failed."
    UPLOAD_SUCCESS=false
    UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A❌ R2 Upload: Failed"
  fi
else
  echo "[$(date)] R2 credentials not fully set, skipping R2 upload."
  UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A⚠️ R2 Upload: Skipped (Missing Credentials)"
fi

# 3. Upload to AWS S3 (Secondary)
# Unset the R2 AWS env vars first
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION="${ORIG_AWS_REGION}"


if [ -n "$AWS_S3_ACCESS_KEY_ID" ] && [ -n "$AWS_S3_SECRET_ACCESS_KEY" ] && [ -n "$AWS_DEFAULT_REGION" ]; then
  echo "[$(date)] Uploading to AWS S3..."
  export AWS_ACCESS_KEY_ID="${AWS_S3_ACCESS_KEY_ID}"
  export AWS_SECRET_ACCESS_KEY="${AWS_S3_SECRET_ACCESS_KEY}"
  export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}"
  
  # Ensure bucket exists
  aws s3 mb s3://${S3_BUCKET} 2>/dev/null || true

  
  if aws s3 cp "${LOCAL_PATH}" "${S3_PATH}"; then
    echo "[$(date)] S3 upload successful."
    UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A✅ S3 Upload: Success"
  else
    echo "[$(date)] S3 upload failed."
    UPLOAD_SUCCESS=false
    UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A❌ S3 Upload: Failed"
  fi
else
  echo "[$(date)] AWS S3 credentials not fully set, skipping S3 upload."
  UPLOAD_MESSAGES="${UPLOAD_MESSAGES}%0A⚠️ S3 Upload: Skipped (Missing Credentials)"
fi

# 4. Clean up old local backups (keep last 7 days)
echo "[$(date)] Cleaning up local backups older than 7 days..."
find "${BACKUP_DIR}" -name "trading_platform_*.sql.gz" -type f -mtime +7 -delete

# 5. Log to DB (if possible)
if [ -n "$DB_PASSWORD" ]; then
  echo "[$(date)] Logging status to DB..."
  JSON_META="{\"filename\":\"${FILENAME}\",\"size_mb\":${FILE_SIZE_MB},\"r2_success\":${UPLOAD_SUCCESS},\"s3_success\":${UPLOAD_SUCCESS}}"
  # Note: UPLOAD_SUCCESS is a boolean in script, but we need to check R2/S3 individually if we want more detail.
  # For now, keeping it simple as per the script's logic.
  PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -c \
    "INSERT INTO bot_health (event_type, status, message, meta_data, timestamp) VALUES ('DB_BACKUP', '$( [ "$UPLOAD_SUCCESS" = true ] && echo "SUCCESS" || echo "WARNING" )', 'Dual-cloud backup completed', '${JSON_META}', NOW());" || echo "DB logging failed."
fi

# 6. Send final notification
if [ "$UPLOAD_SUCCESS" = true ]; then
  SUCCESS_MSG="🟢 <b>Database Backup Complete</b>%0AFile: <code>${FILENAME}</code>%0ASize: ${FILE_SIZE_MB} MB${UPLOAD_MESSAGES}"
  send_telegram "${SUCCESS_MSG}"
  echo "[$(date)] Backup process completed successfully."
else
  ERROR_MSG="🟠 <b>Database Backup Partial Failure</b>%0AFile: <code>${FILENAME}</code>%0ASize: ${FILE_SIZE_MB} MB${UPLOAD_MESSAGES}"
  send_telegram "${ERROR_MSG}"
  echo "[$(date)] Backup process completed with upload errors."
fi
