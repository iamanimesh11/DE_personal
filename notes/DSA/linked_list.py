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

    def reverse_ll(self):
      curr=self.head
      prev=None
      print("#############3loop starts#######")
      while curr:
          next=curr.next
          curr.next=prev
          prev=curr
          curr=next
  
      self.head=prev    
    
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
      k=k%length
      print(f"k is {k}")
      steps_to_new_Tail=length-k-1
      print(f"Steps :{steps_to_new_Tail}")
      new_tail=self.head
      for _ in range(steps_to_new_Tail):
        print(f"new tail is :{new_tail.__dict__}")
        new_tail=new_tail.next
        
      new_head=new_tail.next
      new_tail.next=None
      
      return new_head
      
          
      
ll=LinkedList()
ll.print_list()
print("###### new func calling again ###")
ll.insert_end(10)
ll.insert_end(20)
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
ll.reverse_ll()
ll.reverse_ll()

ll.print_list()
# ll.reverse_ll_recursive()
print("#### calling rotate list")
ll.rotate_list_by_k(2)
ll.print_list()
