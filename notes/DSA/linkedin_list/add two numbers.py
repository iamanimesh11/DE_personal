# Creating an object
# Setting the threshold of logger to DEBUG
import  logging 

class Node:
    def __init__(self,data):
        self.data=data
        self.next=None

class LinkedList:
    def __init__(self):
        self.head=None
        
    def insert_end(self,data):
        new_node=Node(data)
        
        if self.head is None:
            print("yes self.head is none")
            self.head=new_node
            return

        temp=self.head
        while temp.next: 
            temp=temp.next
        temp.next=new_node


    def print_list(self):
        temp=self.head
        while temp:
            print(temp.data,end=" ")
            temp=temp.next
        print
    
    def add_two_numbers(self,ll2):
      dummy=Node(0)
      print(dummy.__dict__)
      curr=dummy
      print(curr.__dict__)
      
      carry=0 
      l1=self.head 
      l2=ll2.head
      
      while l1 or  l2 or carry:
        val1=l1.data if l1 else 0
        val2=l2.data if l2 else 0
        
        total=val1+val2+carry
        carry=total//10
        new_Digit=total%10
        curr.next= Node(new_Digit)
        curr=curr.next
        if l1 :
          l1=l1.next
        if l2:
          l2=l2.next
      
      print(f"return : {dummy.next.__dict__}")
      return dummy
      
        
      
      

ll3=LinkedList()

ll3.insert_end(2)
ll3.insert_end(4)
ll3.insert_end(3)


ll4=LinkedList()

ll4.insert_end(5)
ll4.insert_end(6)
ll4.insert_end(4)

dummy=ll3.add_two_numbers(ll4)
dummy.print_list()
