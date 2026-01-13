# BLOCK VS FILE VS OBJECT STORAGE


example -airport baggage
1.file storage -: normal traditional storage system like in harddrives or google file sharing
carry own bag - aware of whihc pocket has passport or headphone.
have to remember the complete path to access file
problem is when had 1000 such bag ,cant remember which pocke in which bag had keys,near to impossible to mangage at scale

like personal file on laptop or harddrive

2. block storage: example: engine parts (performance)
engine is multiple of thousand of tiny bold,gear working together.so to fix one part of engine(file),dont have to repalce whole engine .
just swap out one specific key tiny bold(a block)
-incredible fast
- used case in database otap ,where data is constntly changing

3. obhect storage: (checked luggage)
like giving suitcase to agent at check in counter'
"ID" : (barcode) they stick a barcode on bag and give tiny sticker.dont know where in airport bag is,like might be in basement,cart or on plane
"metadata": (the tag) ,barcode contain info who owns it ,whats destination
"flat":(pool) : all bag from all flight are sitting in giant area like aws s3 area. no folder for anything specific just sccan the barcode

so the airport example : technical term

suitcase -the object
barcode sticker - unique identifier (key)
the tag - metadata
warehouse floor -flat namespace
check-in counter - api(restful)
shipping container -bucket


so when w eupload photo to cloud ,say s3 .it doesnr say put this in folder c. it send a commant called put request
system give that photo a unuiqe id called as ,key
system attache dinformation to file (tag) ,user_id,filter_usd,location,so and so
when we want to retrieev photo ,app sen a get request with unique id .system look at flat warehouse ,find the barcode and send the data back

object sorage use hash table

---

Date 13-1-26
```
AWS EBS -elastic book store
AWS OPESEARC
AWS SYSTEM MANAGER
Amazon Elastic File System (EFS) is a managed, scalable, and elastic file storage service for AWS that provides shared file access (using NFS) for Linux-based workloads,

```

