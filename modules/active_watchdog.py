import time
import sqlite3
from datetime import datetime

class ActiveWatchdog:
    def __init__(self, db_path="database/socmint.db"):
        self.db_path = db_path

    def orchestrate_state_snapshot(self):
        """
        Creates an immutable, timestamped structural clone of the target 
        network status to track data alterations across temporal boundaries.
        """
        # Create a unique name using the current timestamp
        timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_table_name = f"comparisons_snapshot_{timestamp_suffix}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if the primary comparisons table exists before copying
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='comparisons';")
            if not cursor.fetchone():
                print("[WATCHDOG WARN] Primary comparisons table not found yet. Skipping snapshot.")
                return

            # Dynamically duplicate the schema and rows of the operational table
            cursor.execute(f"CREATE TABLE {snapshot_table_name} AS SELECT * FROM comparisons;")
            conn.commit()
            print(f"[WATCHDOG SUCCESS] State snapshot persisted into table: {snapshot_table_name}")
        except Exception as e:
            print(f"[WATCHDOG FAULT] Execution halted during state migration: {e}")
        finally:
            conn.close()

    def deploy_monitor_loop(self, check_interval_seconds=3600):
        """
        Launches a persistent background monitoring loop.
        """
        print(f"[WATCHDOG] Initializing automated collection loop. Interval: {check_interval_seconds}s")
        try:
            while True:
                self.orchestrate_state_snapshot()
                time.sleep(check_interval_seconds)
        except KeyboardInterrupt:
            print("[WATCHDOG] Monitoring loop gracefully terminated by user.")