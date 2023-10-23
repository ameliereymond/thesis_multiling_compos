executable = condor-run.sh
getenv     = true
error      = run.error
log        = run.log
notification = complete
transfer_executable = false
request_GPUs = 1
queue