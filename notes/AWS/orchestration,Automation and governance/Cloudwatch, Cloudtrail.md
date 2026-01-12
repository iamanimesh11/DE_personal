# cloudwatch =what's happening
# cloudtrail = who did what

basically cloudwatch maintains logs of operatiornal health o services like GLUE,Athena,kinesis,redshift,lambda

## cloudwatch componsnents

1. Metrics : numerical vlaue over time
   * ex like glue job duration,failed job count,redshift cpu usage

2. Logs. -SERVCIE LOGS:
   * ex glue job logs,lambda logs,so and so
  
3. alarms - trigger actions when metrics breach threshold like notification alert
   * actions like send sns ,auto scale,notif ops team


## cloudtrail -account activity and security
 * like who accessed data,changed permissions,deleted resource so .....


---

Cloudtrail records: 

* API CALLS
* console actions
* sdk/cli action

ex:
* `PutObject` on s3
* `DeleteTable` in Glue
* `GrantPermissions` in Lake formation
* IAM role changes
  
