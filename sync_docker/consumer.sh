
#!/bin/bash
set -x
echo "HUEY CONSUMER"
echo "-------------"
echo "Stop the consumer using Ctrl+C"
PYTHONPATH=.:$PYTHONPATH

python -m huey.bin.huey_consumer app_runner.docker_huey


