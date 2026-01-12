# AWS LAKE FORMATION '

❓why exist?
becasue anyone with s3+glue permissions could see all data

> It provide centralized ,fine grained access control for data lakes build on Amazon S3 using Glue data catalog

👉Lake formation= Security layer

## componenets

 * data lake location -like S3 bucket ,registered with lake formation,LF takes control of access
 * Glue data catalog (backbone) -DB,tABLE,COLUMN,PARTITION
 * Permissions : DB level,table level,column level,row level permisssion

Who get access? IAM users,IAM roles,AWS accounts

IAM isn't enough:
* IAM contorls who can call servcies,cannot restrict which columns in a table

**lAKE formation permission overrides IAM permissions for data access.

IAM-who can call  or access

Lake formation- what data they see


### who grants permisson ?
Only:
* data lake admin
* or prinicipal with grant permissions

⚡Imp - `IAMALLOWEDPRINCIPALS`

special permission that means anyone who has IAM permissions can access this data,

* appears when LF is first enabled
* legacy glue setups
* due to this user can acccess table even without lake formation grants.so must be removed


## ROW LEVEL SECURITY & TAG BASED ACCESS CONTROL (LF-TBAC)

column level security not enough when same columns,different rows,diferent teams

like AWS loves Sales team -only their region
 ,HR-only their department


LF enforce row level access using data filters( a rule that restrict rows,columns and applied at query time

example: table sales_order (region,orderid,amount)

so can see spcifci region only by row level filters .

Its enforce when querying vi ,athena ,glue,redshift spctrum


### tag ased access control : -advanced governance

basically grant access based on matching tags (tag data resorueces,prinicipal)

-its scalable ,dynamic solution


#### note:

column level is for hide sensitive fields, 
row level is for restrict data subsets
Lt-TBAC is for scale permissions

> column hide fields,rows hide records,tag hide complexity


## crosw account data sharing

AWS architecture:
* central acocunt owns by s3,glue catallog,lake froamtion permissions
* query data using athena,redshift spectrum

  so in lake formation permsisions ,db or table can be share dwith external AWS accoutns.

  > only permission ,not data moves
