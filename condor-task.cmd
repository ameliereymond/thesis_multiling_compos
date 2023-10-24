executable = condor-run.sh
getenv     = true
error      = run.error
log        = run.log
notification = complete
Requirements = (Machine == "patas-gn3.ling.washington.edu")
transfer_executable = false
request_GPUs = 1
queue