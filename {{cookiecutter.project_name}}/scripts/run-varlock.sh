#!/bin/bash
# Wrapper script to run commands with varlock
# Usage: ./scripts/run-varlock.sh [load|run] -- <command>

set -e

ACTION=${1:-run}
shift

case "$ACTION" in
    load)
        echo "📦 Loading secrets..."
        varlock load
        ;;
    run)
        # Check if varlock needs to decrypt first
        if [ -f ".env.locked" ] && [ ! -f ".env" ]; then
            echo "📦 Loading secrets first..."
            varlock load
        fi

        # Run the command passed after --
        if [ "$1" == "--" ]; then
            shift
            exec "$@"
        else
            echo "Usage: ./scripts/run-varlock.sh run -- <command>"
            exit 1
        fi
        ;;
    *)
        echo "Usage: ./scripts/run-varlock.sh [load|run] -- <command>"
        exit 1
        ;;
esac
