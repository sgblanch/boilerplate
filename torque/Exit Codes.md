# Possible exit codes from cluster jobs

- Completed jobs report this in the output of `qstat -f <JOB_ID>` as `exit_status`.
    - **This is only visible for 5 minutes after job completes**
- Configure prologue and eplilogue scripts to create a permant record of your jobs' exit statuses

## Torque Exit Codes
Exit Code | Reason
----------|-------
-1, -2, -3 | Job execution failed
-4, -5, -6 | Abort on MOM initialization
-7 | Job restart failed
-8 | exec() of user command failed
-9 | Could not create/open STDOUT/STDERR files
-10 | Job exceeded a memory limit
-11 | Job exceeded a walltime limit
-12 | Job exceeded a CPU time limit

## Linux Exit Codes
Exit Code | Reason
----------|-------
0 | Execution succeeded
0-127 | Exit of last command run in submit script
128-173 | Command exited on signal; `signal = exit - 121`; See `man 7 signal`
256+ | Command exited on signal; `signal = exit - 255`; See `man 7 signal`
254 | Could not execute command
255 | Command not found