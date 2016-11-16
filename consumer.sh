
#!/bin/bash
echo "HUEY CONSUMER"
echo "-------------"
echo "Stop the consumer using Ctrl+C"
PYTHONPATH=.:$PYTHONPATH
export WORKER_CLASS=${1:-thread}
python -m huey.bin.huey_consumer sync_docker.app_runner.docker_huey


