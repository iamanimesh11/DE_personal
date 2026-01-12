# IAM

## Componenents :

1. Policy :
    purpose -> what action are allwoed/denied
    exam keywords -> json,permissions

2.  Role:
    * who assume permissions
    * `st:AssumeRole`

3. Trust Policy:
     * purpose -> who can assume the role
     * services/account

> services NEVER get policies direclty -> they assume roles


## Example

if glue ETL job need to read raw data from S3 and write procese data back to another s3 bucket,then 
* IAM role must be atached to glue job and role has policcy allowing GET and PUT object

ex:
* GLUE -> S3 ,POLICY trusted by `glue.amazonaws.com`
* athena -> s3,read/write permission
* redshift -> s3 , - role attaches to redshift cluster


# TRUST POLICY 

Policy attaches only to IAM rols and defines who is allowed to assume the role

Trust policy ->who is allows to assume the role
```json
{
"Effect":"Allow",
"Principal":{
"Services":"ec2.amazonaws.com"
},
"Actions":"sts:AssumeRole"
}

means trust ec2 to asssume the role
```
Permission policy -> what can they do after assuming the role
