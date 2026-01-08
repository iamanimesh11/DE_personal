# STEP FUNCTIONS

without it
  * glue job run independently
  *  no central retry logic ,conditional branching,hard to track end to end pipeline state

with it:
  * one state machine contorl everything
  * native reties,error handling,graph based execution,event driven orchestration

> Execute steps sequentially/parallel

## State machine
* json based definition,describe flow not code
* deployed once executed many times

##  states

TASK- > calls AWS service 
CHOICE -> conditional logic
PARALLEL  -> run steps simulatenously
WAIT-> pause execution
succeed -> successfully end
fail -> controlled failrue

> step func is used with glue,lambda,emr,s3,sns
> handles retires easiy,catch exceptions


## execution models

* Standard workflow
  * long running upto 1 yr
  * exactly once exectution
  * detailed execution hisotry

> ETL .BATCH PIPELINES -> STANDARD

* express workflows
   * at lease once execution
   * cheaper faster
   * high vol short duration
  
> for streaming /event bursts

## Sync/Async 

* ASYNC -> fire and forget,step continues immediately
* SYNC -> step wait for job completion ,used with GLUE jobs and emr steps

### step func is aws service while state machine is workflow definition and execution is one run of a state machine

State Machine runs on **Step functions**

