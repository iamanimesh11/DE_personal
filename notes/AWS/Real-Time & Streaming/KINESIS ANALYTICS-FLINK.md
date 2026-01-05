#  Apache FLINK (open source stream processing framework

❌ flink is not aws service
✅ AWS provide a managed flink service (like hosting,scaling,integration)

> Querying streaming data means ,query= continously running computations not one time request (**Continous query**)

streaminf engine never try to sort the entire stream.
Do:
* Process event immediately
* group data into time windows
* maintain state

so basically on every new event just update the state ,no sorting,no scanning past data again

### Windowing

basically engine cut time into buckets,
> engine only compare data inside same window ,not whole stream


#### Apache flink called as stateful stream processor,engine maintain state table internally.On new event arrival engine find the right window,updted the strored state 


## concept of watermark

basically a point to delcare that assume no mor eold event before time x will arrive. so late event can be dropped or merged (within allowed lateness)

> so streaming querie work by windowing + state not by sorting data

final emmited result when passes by window time or point


Basically we deifne window type,time attribute,lateness rule 
```sql
TUMBLE(event_time,1 minute)
```
it make pre define the boundary


# cases where must use time window

1. aggregations -sum,count,avg ,group by
2. Last N min type question

# cases when dont need window

1. stateless information -pre event logic only example filter ,map.projection
  
  stateless means each event is handled alone,intedependetly and forgotten immediately . so no memory,past event ,future waiting

ex for every order,add 18% tax and output it 

so for each event engine transofmr the value like 100x1.18 =118 and output it then forget event forever

so here query is like rule not a question basically whenevr data arrives,apply this rule

Ex - filtering - pass only orders greater than 1000

so no aggegation kinda thats is stateless

2 .keyed state-track latet order per user (this use state not windows)



## allowed latenss =extra grace time after window closes so late events can be allowed,accepted and update results
so basicll its designed for correctned ,event time processing ,real world system

 as in relaity of streeam can be netwrok delay,retries,IOT latency,partition lag