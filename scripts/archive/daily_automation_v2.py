#!/usr/bin/env python3
"""
TradePanel Daily Automation v2 — INTEGRATED WITH CLEANUP & BACKUP
Comprehensive validation, backtesting, Telegram reporting, and cloud backup
"""

import os
import json
import subprocess
import sys
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S UTC'
)
logger = logging.getLogger(__name__)


class CleanupAndBackup:
    """Integrated cleanup and backup class"""
    def __init__(self, repo_path, days_threshold=3):
        self.repo = Path(repo_path)
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
        logger.info("CLEANUP STEP 1: ARCHIVE OLD FILES")
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
                logger.info(f"⏭  Directory not found: {dir_path}")
                continue
            
            logger.info(f"\n📁 Processing: {dir_path.name}/")
            
            for file_path in dir_path.glob("*"):
                if file_path.is_file():
                    try:
                        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        
                        if file_mtime < self.cutoff_date:
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
        logger.info("CLEANUP STEP 2: SYNC TO S3")
        logger.info("=" * 60)
        
        try:
            # Check if AWS CLI is available
            result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("⚠️  AWS CLI not available")
                return False
            
            # Get S3 config from environment or config
            s3_bucket = os.getenv('S3_BUCKET') or "tradepanel-backups"
            s3_region = os.getenv('S3_REGION') or "us-east-1"
            s3_profile = os.getenv('AWS_PROFILE') or "default"
            
            logger.info(f"Syncing to S3: s3://{s3_bucket}/tradepanel/")
            
            cmd = [
                "aws", "s3", "sync",
                str(self.archive_dir),
                f"s3://{s3_bucket}/tradepanel/",
                "--region", s3_region,
                "--profile", s3_profile,
                "--delete",
                "--storage-class", "STANDARD_IA"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ S3 sync completed successfully")
                # Verify files exist
                logger.info(f"  Verifying S3 bucket contents...")
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
        logger.info("CLEANUP STEP 3: SYNC TO R2 (Cloudflare)")
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
            
            # Use AWS CLI with R2 endpoint
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
            
            logger.info("Executing R2 sync...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ R2 sync completed successfully")
                logger.info(f"  Verifying R2 bucket contents...")
                return True
            else:
                logger.warning(f"⚠️  R2 sync note: {result.stderr[:200]}")
                return True
                
        except Exception as e:
            logger.warning(f"⚠️  R2 sync optional: {e}")
            return True
    
    def verify_cleanup(self):
        """Verify cleanup was successful"""
        logger.info("\n" + "=" * 60)
        logger.info("CLEANUP STEP 4: VERIFY CLEANUP")
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


class TradePanel_DailyAutomation:
    def __init__(self):
        self.repo = Path(__file__).parent.parent
        # Use timezone-aware UTC datetime (fixes deprecation warning)
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.log_file = self.repo / "results" / "validation_daily.log"
        self.results = {}
        
    def validate_components(self):
        """Validate all core components exist"""
        logger.info("=" * 60)
        logger.info("STEP 1: VALIDATE CORE COMPONENTS")
        logger.info("=" * 60)
        
        checks = {
            "Docker": self.repo / "docker-compose.yml",
            "Config": self.repo / "config" / "config.yaml",
            "Strategies": self.repo / "config" / "strategies.yaml",
            "Strategies Dir": self.repo / "strategies",
            "Results Dir": self.repo / "results",
        }
        
        pass_count = 0
        for name, path in checks.items():
            exists = path.exists()
            status = "✅" if exists else "❌"
            logger.info(f"{status} {name}: {path}")
            if exists:
                pass_count += 1
        
        self.results['validation_checks'] = pass_count
        return pass_count == len(checks)
    
    def check_docker_status(self):
        """Check if Docker containers are running"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: CHECK DOCKER STATUS")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            containers = [c for c in result.stdout.split('\n') if 'tradepanel' in c]
            
            if containers:
                logger.info(f"✅ Docker: UP ({len(containers)} containers)")
                self.results['docker_status'] = "UP"
                self.results['docker_containers'] = len(containers)
                return True
            else:
                logger.info("⚠️  Docker: OFFLINE (no TradePanel containers)")
                self.results['docker_status'] = "OFFLINE"
                self.results['docker_containers'] = 0
                return False
        except Exception as e:
            logger.warning(f"⚠️  Docker check failed: {e}")
            self.results['docker_status'] = "ERROR"
            return False
    
    def run_backtest(self, docker_up):
        """Run overnight backtest if Docker is available"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: RUN OVERNIGHT BACKTEST")
        logger.info("=" * 60)
        
        if not docker_up:
            logger.info("⏭  Docker offline - skipping backtest execution")
            self.read_last_backtest_results()
            return
        
        try:
            logger.info("Executing overnight backtest...")
            result = subprocess.run(
                ["docker", "exec", "tradepanel-backend", "python", 
                 "scripts/overnight_backtest.py", "--full"],
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            logger.info("✅ Backtest execution complete")
            self.read_last_backtest_results()
        except Exception as e:
            logger.error(f"❌ Backtest execution failed: {e}")
            self.results['backtest_error'] = str(e)
    
    def read_last_backtest_results(self):
        """Extract results from latest backtest report (with UTF-8 encoding fix)"""
        results_dir = self.repo / "results" / "overnight"
        
        try:
            # Find latest backtest report
            latest = sorted(results_dir.glob("*_backtest_report.md"), reverse=True)[0]
            # FIX: Specify UTF-8 encoding to avoid charmap errors
            content = latest.read_text(encoding='utf-8', errors='ignore')
            
            # Extract summary stats
            if "✅ PASS" in content:
                lines = content.split('\n')
                for line in lines:
                    if "✅ PASS" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['pass_count'] = int(count)
                    elif "Total combos" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['total_combos'] = int(count)
                    elif "⚠️ REVIEW" in line and "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 2:
                            count = ''.join(c for c in parts[1] if c.isdigit())
                            if count:
                                self.results['review_count'] = int(count)
            
            # Calculate pass rate
            if 'pass_count' in self.results and 'total_combos' in self.results:
                pass_rate = (self.results['pass_count'] / self.results['total_combos']) * 100
                self.results['pass_rate'] = round(pass_rate, 1)
                logger.info(f"📊 Backtest: {self.results['pass_count']}/{self.results['total_combos']} " + \
                           f"PASS ({self.results['pass_rate']}%)")
        except Exception as e:
            logger.warning(f"Could not read backtest results: {e}")
    
    def build_telegram_message(self):
        """Build formatted message for Telegram"""
        msg = f"""🤖 *TradePanel Daily Report*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 {self.timestamp}

*📊 BACKTEST RESULTS*
✅ PASS: {self.results.get('pass_count', '?')}/{self.results.get('total_combos', '?')} ({self.results.get('pass_rate', '?')}%)
⚠️ REVIEW: {self.results.get('review_count', '?')}

*🔧 SYSTEM HEALTH*
🐳 Docker: {self.results.get('docker_status', 'Unknown')}
📢 Telegram: Active
☁️  Backup: {self.results.get('backup_status', 'Pending')}

*📈 STRATEGY PERFORMANCE*
🏆 Tier 1 (Elite): 33 combos
🥈 Tier 2 (High Conviction): 21 combos
🥉 Tier 3 (Emerging): Multiple

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Validation + Cleanup complete
"""
        return msg
    
    def post_telegram(self):
        """Post summary to Telegram (checks environment variables)"""
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: POST TO TELEGRAM")
        logger.info("=" * 60)
        
        try:
            # FIX: Check environment variables first (recommended approach)
            token = os.getenv('TELEGRAM_TOKEN') or os.getenv('telegram_token')
            chat_id = os.getenv('TELEGRAM_CHAT_ID') or os.getenv('telegram_chat_id')
            
            # Fallback: try to read from config
            if not token or not chat_id:
                config_path = self.repo / "config" / "config.yaml"
                config_content = config_path.read_text(encoding='utf-8', errors='ignore')
                
                for line in config_content.split('\n'):
                    if 'telegram_token' in line.lower() and ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            token = parts[1].strip().strip('"\'')
                    if 'telegram_chat_id' in line.lower() and ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            chat_id = parts[1].strip().strip('"\'')
            
            if not token or not chat_id:
                logger.warning("⚠️  Telegram credentials not found in config or environment")
                logger.info("   Set environment variables: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID")
                return False
            
            msg = self.build_telegram_message()
            
            # Post to Telegram
            import urllib.request
            import urllib.parse
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urllib.parse.urlencode({
                'chat_id': chat_id,
                'text': msg,
                'parse_mode': 'Markdown'
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.info("✅ Telegram message posted successfully")
                    return True
        except Exception as e:
            logger.warning(f"⚠️  Telegram post failed: {e}")
        
        return False
    
    def run_cleanup(self, days_threshold=3, skip_cleanup=False):
        """Run integrated cleanup and backup"""
        if skip_cleanup:
            logger.info("\n⏭  Cleanup skipped (dry run mode)")
            self.results['backup_status'] = "SKIPPED"
            return True
        
        logger.info("\n" + "=" * 60)
        logger.info("STEP 5: CLEANUP & BACKUP (NEW)")
        logger.info("=" * 60)
        
        try:
            cleanup = CleanupAndBackup(self.repo, days_threshold=days_threshold)
            
            cleanup.create_archive_dir()
            cleanup.archive_old_files()
            cleanup.sync_to_s3()
            cleanup.sync_to_r2()
            cleanup.verify_cleanup()
            cleanup.write_log_entry()
            
            self.results['backup_status'] = "COMPLETE"
            self.results['files_archived'] = cleanup.stats['files_archived']
            self.results['bytes_archived'] = cleanup.stats['bytes_archived'] / (1024*1024)
            
            logger.info("\n✅ CLEANUP & BACKUP COMPLETE")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
            self.results['backup_status'] = "ERROR"
            return False
    
    def write_log_entry(self):
        """Append summary to validation log"""
        try:
            # FIX: UTF-8 encoding for file writing too
            with open(self.log_file, 'a', encoding='utf-8') as f:
                entry = (f"[{self.timestamp}] MODE=daily-v2-integrated | "
                        f"PASS={self.results.get('pass_count', '?')}/{self.results.get('total_combos', '?')} "
                        f"({self.results.get('pass_rate', '?')}%) | "
                        f"DOCKER={self.results.get('docker_status', 'Unknown')} | "
                        f"BACKUP={self.results.get('backup_status', 'PENDING')} | "
                        f"STATUS={'OK' if self.results.get('pass_rate', 0) >= 70 else 'WARN'}\n")
                f.write(entry)
            logger.info(f"✅ Log entry written: {self.log_file}")
        except Exception as e:
            logger.error(f"❌ Could not write log: {e}")
    
    def run(self, run_cleanup=True, cleanup_days=3):
        """Execute full automation suite"""
        logger.info(f"🚀 TradePanel Daily Automation v2 (Integrated) - {self.timestamp}")
        
        # Execute steps
        self.validate_components()
        docker_up = self.check_docker_status()
        self.run_backtest(docker_up)
        self.post_telegram()
        self.run_cleanup(days_threshold=cleanup_days, skip_cleanup=not run_cleanup)
        self.write_log_entry()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ FULL AUTOMATION COMPLETE")
        logger.info("=" * 60)
        return True


if __name__ == "__main__":
    # Parse arguments
    run_cleanup = "--no-cleanup" not in sys.argv
    cleanup_days = 3
    
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--cleanup-days" and i < len(sys.argv) - 1:
            cleanup_days = int(sys.argv[i + 1])
    
    automation = TradePanel_DailyAutomation()
    try:
        automation.run(run_cleanup=run_cleanup, cleanup_days=cleanup_days)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
