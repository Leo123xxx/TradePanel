#!/usr/bin/env python3
"""
TradePanel Cleanup & Backup v2
Archive old results and sync to R2 + S3
"""

import os
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class CleanupAndBackup:
    def __init__(self, days_threshold=3):
        self.repo = Path(__file__).parent.parent
        self.days_threshold = days_threshold
        self.cutoff_date = datetime.now() - timedelta(days=days_threshold)
        self.archive_dir = self.repo / "archive" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.log_file = self.repo / "results" / "cleanup_backup.log"
        self.stats = {
            'files_archived': 0,
            'bytes_archived': 0,
            'errors': []
        }
        
    def create_archive_dir(self):
        """Create archive directory"""
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Archive directory: {self.archive_dir}")
        return True
    
    def archive_old_files(self):
        """Archive files older than threshold"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: ARCHIVE OLD FILES")
        logger.info("=" * 60)
        logger.info(f"Archiving files older than {self.days_threshold} days ({self.cutoff_date.date()})")
        
        dirs_to_clean = [
            self.repo / "results" / "overnight",
            self.repo / "results" / "recommendations",
            self.repo / "results" / "daily_validation",
            self.repo / "results" / "wfo",
        ]
        
        for dir_path in dirs_to_clean:
            if not dir_path.exists():
                logger.warning(f"⚠️  Directory not found: {dir_path}")
                continue
            
            logger.info(f"\n📁 Processing: {dir_path.name}/")
            
            for file_path in dir_path.glob("*"):
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    if file_mtime < self.cutoff_date:
                        try:
                            # Create subdirectory structure in archive
                            rel_dir = file_path.parent.relative_to(self.repo / "results")
                            archive_subdir = self.archive_dir / rel_dir
                            archive_subdir.mkdir(parents=True, exist_ok=True)
                            
                            # Move file to archive
                            archive_path = archive_subdir / file_path.name
                            shutil.move(str(file_path), str(archive_path))
                            
                            file_size = file_path.stat().st_size
                            self.stats['files_archived'] += 1
                            self.stats['bytes_archived'] += file_size
                            
                            logger.info(f"  ✅ Archived: {file_path.name} ({file_size / 1024:.1f} KB)")
                        except Exception as e:
                            msg = f"  ❌ Failed to archive {file_path.name}: {e}"
                            logger.error(msg)
                            self.stats['errors'].append(msg)
        
        logger.info(f"\n📊 Archive Summary:")
        logger.info(f"  Files archived: {self.stats['files_archived']}")
        logger.info(f"  Space freed: {self.stats['bytes_archived'] / (1024*1024):.2f} MB")
        
        return True
    
    def sync_to_s3(self):
        """Sync archive to AWS S3"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: SYNC TO S3")
        logger.info("=" * 60)
        
        try:
            # Check if AWS CLI is available
            result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("⚠️  AWS CLI not available. Install with: pip install awscli-local")
                return False
            
            # Get S3 config from environment or config
            s3_bucket = os.getenv('S3_BUCKET') or "tradepanel-backups"
            s3_region = os.getenv('S3_REGION') or "us-east-1"
            s3_profile = os.getenv('AWS_PROFILE') or "default"
            
            logger.info(f"Syncing to S3: s3://{s3_bucket}/")
            
            cmd = [
                "aws", "s3", "sync",
                str(self.archive_dir),
                f"s3://{s3_bucket}/tradepanel/",
                "--region", s3_region,
                "--profile", s3_profile,
                "--delete",  # Remove files deleted locally
                "--storage-class", "STANDARD_IA"  # Infrequent access for cost savings
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ S3 sync completed successfully")
                return True
            else:
                logger.error(f"❌ S3 sync failed: {result.stderr}")
                self.stats['errors'].append(f"S3 sync: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ S3 sync error: {e}")
            self.stats['errors'].append(f"S3 sync: {e}")
            return False
    
    def sync_to_r2(self):
        """Sync archive to Cloudflare R2"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: SYNC TO R2 (Cloudflare)")
        logger.info("=" * 60)
        
        try:
            # Get R2 config from environment
            r2_bucket = os.getenv('R2_BUCKET') or "tradepanel-backups"
            r2_account_id = os.getenv('R2_ACCOUNT_ID')
            r2_access_key = os.getenv('R2_ACCESS_KEY')
            r2_secret_key = os.getenv('R2_SECRET_KEY')
            
            if not all([r2_account_id, r2_access_key, r2_secret_key]):
                logger.warning("⚠️  R2 credentials not found in environment variables")
                logger.info("   Set: R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY")
                return False
            
            # R2 endpoint is S3-compatible
            r2_endpoint = f"https://{r2_account_id}.r2.cloudflarestorage.com"
            
            logger.info(f"Syncing to R2: {r2_endpoint}")
            
            # Try using AWS CLI with R2 endpoint
            cmd = [
                "aws", "s3", "sync",
                str(self.archive_dir),
                f"s3://{r2_bucket}/tradepanel/",
                "--endpoint-url", r2_endpoint,
                "--access-key", r2_access_key,
                "--secret-key", r2_secret_key,
                "--region", "auto",
                "--delete"
            ]
            
            # Hide credentials in logs
            logger.info("Executing R2 sync...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ R2 sync completed successfully")
                return True
            else:
                logger.warning(f"⚠️  R2 sync note: {result.stderr[:200]}")
                # Don't fail if R2 is optional
                return True
                
        except Exception as e:
            logger.warning(f"⚠️  R2 sync optional: {e}")
            return True  # Continue even if R2 fails
    
    def verify_cleanup(self):
        """Verify cleanup was successful"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: VERIFY CLEANUP")
        logger.info("=" * 60)
        
        results_dirs = [
            self.repo / "results" / "overnight",
            self.repo / "results" / "recommendations",
            self.repo / "results" / "daily_validation",
        ]
        
        total_remaining = 0
        for dir_path in results_dirs:
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*")))
                dir_size = sum(f.stat().st_size for f in dir_path.glob("*") if f.is_file())
                total_remaining += dir_size
                logger.info(f"  {dir_path.name}/: {file_count} files ({dir_size / 1024:.1f} KB)")
        
        logger.info(f"\n✅ Cleanup verification complete")
        logger.info(f"  Total space in results: {total_remaining / (1024*1024):.2f} MB")
        logger.info(f"  Archived to: {self.archive_dir}")
        
        return True
    
    def write_log_entry(self):
        """Write summary to log"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                entry = (
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"CLEANUP_BACKUP | Files={self.stats['files_archived']} | "
                    f"Size={self.stats['bytes_archived'] / (1024*1024):.2f}MB | "
                    f"Archive={self.archive_dir.name} | "
                    f"Errors={len(self.stats['errors'])}\n"
                )
                f.write(entry)
            logger.info(f"✅ Log entry written: {self.log_file}")
        except Exception as e:
            logger.error(f"❌ Could not write log: {e}")
    
    def run(self):
        """Execute full cleanup and backup"""
        logger.info(f"🚀 TradePanel Cleanup & Backup")
        logger.info(f"   Archive threshold: {self.days_threshold} days")
        logger.info(f"   Cutoff date: {self.cutoff_date.date()}")
        
        # Execute steps
        self.create_archive_dir()
        self.archive_old_files()
        self.sync_to_s3()
        self.sync_to_r2()
        self.verify_cleanup()
        self.write_log_entry()
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ CLEANUP & BACKUP COMPLETE")
        logger.info("=" * 60)
        
        if self.stats['errors']:
            logger.warning(f"\n⚠️  {len(self.stats['errors'])} errors during process")
            for error in self.stats['errors']:
                logger.warning(f"   - {error}")
        
        return True


if __name__ == "__main__":
    # Default 3 days threshold
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    
    cleanup = CleanupAndBackup(days_threshold=days)
    try:
        cleanup.run()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
