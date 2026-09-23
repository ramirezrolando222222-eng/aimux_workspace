#!/usr/bin/env bash
set -euo pipefail

ITERATION_COUNT=2
OPTIMIZATION_LEVEL=2
SYSTEM_DELAY=0
TOTAL_COMMITS_PUSHED=1
FREE_QUOTA_REMAINING=49

AIMUX_DIR="${HOME}/.config/aimux"
LOG_FILE="${AIMUX_DIR}/session.log"
SELF_PATH="$(readlink -f "$0")"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

log_status() {
    local type="$1"
    local message="$2"
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] [${type}] ${message}" | tee -a "$LOG_FILE"
}

execute_vibe_cycle() {
    log_status "WORKLOAD" "Executing Aimux Autonomous Vibe-Coding Cycle #${ITERATION_COUNT}..."
    local free_mem
    free_mem=$(free -m 2>/dev/null | awk '/Mem:/ {print $4}' || echo "N/A")
    log_status "METRICS" "Free Memory: ${free_mem}MB | Quota Cycles Remaining: ${FREE_QUOTA_REMAINING}"
    sleep "$SYSTEM_DELAY"

    if command -v termux-notification >/dev/null 2>&1; then
        termux-notification --title "Aimux AI Terminal" \
            --content "Cycle #${ITERATION_COUNT} complete. Quota remaining: ${FREE_QUOTA_REMAINING}" \
            --id "aimux_vibe" || true
    fi
}

self_optimize() {
    local duration_ms="$1"
    local next_iter=$(( ITERATION_COUNT + 1 ))
    local next_opt=$OPTIMIZATION_LEVEL
    local next_delay=$SYSTEM_DELAY
    local next_quota=$(( FREE_QUOTA_REMAINING - 1 ))

    if [ "$duration_ms" -gt 1500 ] && [ "$SYSTEM_DELAY" -gt 0 ]; then
        next_delay=$(( SYSTEM_DELAY - 1 ))
        next_opt=$(( OPTIMIZATION_LEVEL + 1 ))
    elif [ "$duration_ms" -lt 800 ]; then
        next_opt=$(( OPTIMIZATION_LEVEL + 1 ))
    fi

    log_status "EVOLVER" "${GREEN}Rewriting state: Iter -> ${next_iter}, Opt -> ${next_opt}, Quota -> ${next_quota}${NC}"

    sed -i "s/ITERATION_COUNT=${ITERATION_COUNT}/ITERATION_COUNT=${next_iter}/" "$SELF_PATH"
    sed -i "s/OPTIMIZATION_LEVEL=${OPTIMIZATION_LEVEL}/OPTIMIZATION_LEVEL=${next_opt}/" "$SELF_PATH"
    sed -i "s/SYSTEM_DELAY=${SYSTEM_DELAY}/SYSTEM_DELAY=${next_delay}/" "$SELF_PATH"
    sed -i "s/FREE_QUOTA_REMAINING=${FREE_QUOTA_REMAINING}/FREE_QUOTA_REMAINING=${next_quota}/" "$SELF_PATH"
}

sync_git() {
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        log_status "GIT" "${CYAN}Syncing workspace state to Git...${NC}"
        git add "$SELF_PATH" || true
        git commit -m "Aimux Autonomous Optimization Cycle #${ITERATION_COUNT}" || true
        local commits=$(( TOTAL_COMMITS_PUSHED + 1 ))
        sed -i "s/TOTAL_COMMITS_PUSHED=${TOTAL_COMMITS_PUSHED}/TOTAL_COMMITS_PUSHED=${commits}/" "$SELF_PATH"
    fi
}

main() {
    clear
    echo -e "${CYAN}========================================================================${NC}"
    echo -e "${GREEN}  AIMUX AI DEVELOPER TERMINAL v7.0.0-PROD                              ${NC}"
    echo -e "${GREEN}  Copyright (c) 2026 Rolando H Ramirez Jr.                             ${NC}"
    echo -e "${CYAN}========================================================================${NC}"

    local start_ns end_ns elapsed_ms
    start_ns=$(date +%s%N 2>/dev/null || echo "0")
    
    execute_vibe_cycle
    
    end_ns=$(date +%s%N 2>/dev/null || echo "0")
    if [ "$start_ns" -ne 0 ] && [ "$end_ns" -ne 0 ]; then
        elapsed_ms=$(( (end_ns - start_ns) / 1000000 ))
    else
        elapsed_ms=1000
    fi

    self_optimize "$elapsed_ms"
    sync_git
    log_status "SYSTEM" "${GREEN}Aimux cycle completed successfully.${NC}"
}

main "$@"
