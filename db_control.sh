#!/bin/bash
PGDATA="$HOME/pgdata"

case "$1" in
    init)
        echo "[*] Initializing PostgreSQL database cluster..."
        initdb -D "$PGDATA"
        echo "[+] Database cluster initialized!"
        ;;
    start)
        echo "[*] Starting PostgreSQL server..."
        pg_ctl -D "$PGDATA" -l "$PGDATA/postgres.log" start
        echo "[+] PostgreSQL server started in background."
        ;;
    stop)
        echo "[*] Stopping PostgreSQL server..."
        pg_ctl -D "$PGDATA" stop
        echo "[+] Server stopped."
        ;;
    backup)
        echo "[*] Exporting database dump and syncing to Google Drive..."
        mkdir -p "$HOME/aimux_workspace/db_backups"
        pg_dumpall > "$HOME/aimux_workspace/db_backups/pg_backup_$(date +%Y%m%d_%H%M%S).sql"
        rclone sync "$HOME/aimux_workspace/db_backups/" "gdrive:/Aimux_Workspace_Mirror/db_backups/" --progress
        echo "[+] Backup sync complete!"
        ;;
    *)
        echo "Usage: ./aimux_workspace/db_control.sh {init|start|stop|backup}"
        ;;
esac
