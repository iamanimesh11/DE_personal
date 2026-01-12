# AWS DMS -database migration service

❌Why?:
  * Enterprises need to migrate db to aws
  * kepe osurce and target in sync
  * move transactional data into analytics system


> DMS is bridge between OLTP and analytics.

### change data capture (CDC)

capture ongoing changes like insert,update,delete) from source DB and applies them to the target.

* keeps target up to date
* enables near real time ingestion
* avoid reloading entire tables

## Migration task types

1. Full load-copy exisiting data ,one time bulk migration
   * use - Initial migration,historical data copy

2. full load + CDC
   > bulk load then continuous replication
   * uses when minimal downtime required,source remains active

3. CDC only
   * no historical data,only new changes
  
> if source db is still being used -> choose full load + cdc


## AWS DMS architecture componenets:

* replication instance -compute
* source endpount
* target endpoint
* migration task

  
