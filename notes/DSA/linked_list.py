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

           
        print(f"in class node : {self.__dict__}")
        temp=self.head
        print(f" temp var is {temp.__dict__}")
        while temp.next: 
            print("im in while loop")  
            temp=temp.next
        print(f"temp.next is {temp.next}")
        temp.next=new_node
        print(f"temp.next is {temp.next.__dict__}")
    
   
    def insert_atINDEX(self,index,data):
        new_node=Node(data)
        
        if index==0:
            print("im in index 0")
            print(f"self.head.next is {self.head.next.__dict__}")
            new_node.next=self.head
            self.head=new_node
            return 


        temp=self.head
        print(f"temp is {temp.__dict__}")
        curr_index=0

        while temp is not None and curr_index<index-1:
                    temp=temp.next
                    curr_index+=1
            
        if temp is None:
            raise IndexError("index out of range")

        new_node.next=temp.next
        temp.next=new_node

    def delete_AtINDEX(self,index):
        if self.head is None:
            return IndexError("list is empty")

        if  index==0:
            self.head=self.head.next

        temp=self.head
        curr_index=0

        while temp is not None and curr_index<index-1:
            temp =temp.next
            curr_index+=1

        if temp is  None or temp.next is  None:
            raise IndexError("index out of unbound")

        temp.next=temp.next.next
        
        
    def print_list(self):
        temp=self.head
        while temp:
            print(temp.data,end=" ")
            temp=temp.next
        print()

    def count_nodes(self):
        count=0
        temp=self.head
        while temp:
            count+=1
            temp=temp.next
        print(f"count is {count}")

    def count_node_recursively(self,node):
        if node is None:
               return 0
        return 1+self.count_node_recursively(node.next)
            

    def search(self,target):
        temp=self.head

        while temp:
            if temp.data==target:
                print(f"target {target} exist in LL")
                return
            temp=temp.next
        print(f"target {target} doesnt exist in LL")
        return 
        
    def find_middle(self):
            slow=self.head
            fast=self.head

            while fast and  fast.next:
                slow =slow.next
                fast=fast.next.next
            return slow

    def reverse_ll(self,head):
      curr=head
      prev=None
      while curr:
          next=curr.next
          curr.next=prev
          prev=curr
          curr=next
  
      return prev  
    
    def reverse_ll_recursive(self):
      self.head=self._reverse_Recursive(self.head)
    
    def _reverse_Recursive(self,node):
      if node is None or node.next is None:
        return node
      print(f"node is {node.__dict__}")
      new_head=self._reverse_Recursive(node.next)
      node.next.next =node
      node.next=None
      return new_head
  
    def rotate_list_by_k(self,k):
      
      if not self.head or not self.head.next or k ==0:
        return self.head
      
      length=1
      last=self.head
      while last.next:
        last=last.next
        length+=1
      print(f"length is {length}")
        
      last.next=self.head
      print(f"last next is {last.next.__dict__}")
      k=k%length
      steps_to_new_Tail=length-k-1
      new_tail=self.head
      print(f"k is {steps_to_new_Tail}")
      for _ in range(steps_to_new_Tail): 
        print(f"new tail is :{new_tail.__dict__}")
        new_tail=new_tail.next
      print(f"after loop is new tail is {new_tail.__dict__}")
      new_head=new_tail.next
      print(f"after loop is new head is {new_head.__dict__}")
      new_tail.next=None
      
      self.head=new_head
      return new_head
      
    
    def make_cycle_atINDEX(self,pos):
      if pos<0:
        return
      
      cycle_Start=None
      temp=self.head
      index=0 
      
      while temp and temp.next:
        if index==pos:
          cycle_Start=temp
        temp=temp.next
        index+=1
      
      if cycle_Start:
        temp.next=cycle_Start
    
    
    def detect_cycle(self):

      slow=self.head
      fast=self.head
      
      while fast and fast.next:
        slow =slow.next
        fast=fast.next.next
        if slow==fast:
          print("True")
          return slow
      print(False)
      return None
      
      
    def remove_cycle(self):
        meeting=self.detect_cycle()
        if meeting is None:
          return
        
        slow=self.head
        fast=meeting
        prev=None
        while slow!=fast:
          prev=fast
          slow=slow.next
          fast=fast.next
          
        prev.next=None
            
    def check_palindrome(self):
      print(self.head.next.__dict__)
      middle=self.find_middle()
      
      second_half=self.reverse_ll(middle)
      print(f"second hald is {second_half.__dict__}")
      return self.identical_ll(second_half)
      
    def remvoe_duplicate_sortedLL(self):
      curr=self.head
      while curr and curr.next:
        if curr.data ==curr.next.data:
          curr.next=curr.next.next
        else:
          curr=curr.next
   
    def remvoe_duplicate_un_sortedLL(self):
      print("calling duplicate on unsorted ll3")
      curr=self.head
      seen=set()
      prev=None
      while curr:
        print(f"curr is : {curr.__dict__}")
        if prev is not None :
          print(f"prev is : {prev.__dict__}")
        else:
          print(f"prev is : None")
          
        if curr.data  in seen:
          prev.next=curr.next
        else:
          seen.add(curr.data)
          prev=curr 
        curr=curr.next 
      
      
    def remove_duplicate_un_sortedll_without_set(self):
      # time complexity =o(n2)
      curr=self.head
      while curr:
        runner=curr
        while runner.next:
          if runner.next.data==curr.data:
            runner.next=runner.next.next    
          else:
            runner=runner.next
        curr=curr.next
          
      
ll=LinkedList()
ll.print_list()
print("###### new func calling again ###")
ll.insert_end(10)
ll.insert_end(20)
ll.insert_end(30)
ll.insert_end(30)
ll.insert_end(40)
ll.insert_end(50)

# ll.insert_atINDEX(4,50)
ll.print_list()
count=ll.count_node_recursively(ll.head)
print(f"count is :{count}")
# ll.delete_AtINDEX(1)
ll.print_list()
middle=ll.find_middle()
print(f"middle is : {middle.data}")
# ll.reverse_ll()
# ll.reverse_ll()

ll.print_list()
# ll.reverse_ll_recursive()
print("#### calling rotate list")
ll.rotate_list_by_k(5)
ll.print_list()
ll.detect_cycle()
ll.make_cycle_atINDEX(2)
ll.detect_cycle()
ll.remove_cycle()
ll.detect_cycle()
# ll.check_palindrome()
ll3=LinkedList()

ll3.insert_end(1)
ll3.insert_end(3)
ll3.insert_end(2)
ll3.insert_end(3)
ll3.insert_end(1)
ll3.remove_duplicate_un_sortedll_without_set()
ll3.print_list()


