def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# Example
nums = [7, 3, 9, 1, 5]
print("Before sorting:", nums)
print("After sorting :", selection_sort(nums))


def insertion_sort(arr):
    n=len(arr)
    for i in range(1,n):
        key=arr[i]
        j=i-1 
        print(f"key: {arr[i]} ,arr[j]: {arr[j]}")
        while j>=0 and arr[j]>key:
            arr[j+1]=arr[j]
            j-=1
            print(f"while arr is : {arr}")
        arr[j+1]=key
        print(f"curr arr is : {arr}")
    print(arr)
    
arr=[7,3,9,1,5]
insertion_sort(arr)


def bubbble_sort(arr):
    n=len(arr)
    for i in range(n):
        print(f"🧠 i is {i}-{arr[i]}")
        swapped=False
        for j in range(0,n-i-1):
            print(f"🧩 j is {j}-{arr[j]} and range is 0,{n-i-1}")
            print(arr)
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                print(f"c: {arr}")
                swapped=True
        if not swapped:
            print(f"stopped early at i:{i},array already sorted")
            break
    return arr
    
print(bubbble_sort([1,2]))

def merge_sort(arr):
    if len(arr)>1:
        mid=len(arr)//2
        left_half=arr[:mid]
        right_half=arr[mid:]
        print(f"left_half:{left_half},right_half:{right_half}")
        merge_sort(left_half)
        merge_sort(right_half)
        
        i=j=k=0
        while i<len(left_half) and j<len(right_half):
            if left_half[i]<right_half[j]:
                arr[k]=left_half[i]
                i+=1
            else:
                arr[k]=right_half[j]
                j+=1
            k+=1
        #copy remaining elements:
        while i < len(left_half):
            arr[k]=left_half[i]
            i+=1
            k+=1
        while j < len(right_half):
            arr[k]=right_half[j]
            j+=1
            k+=1
        print(f"arr is {arr}")  
        
    return arr
    
my_array = [5,1,4,2,8]
sorted_array = merge_sort(my_array)
print(f"Original array: {my_array}")
print(f"Sorted array: {sorted_array}")
print("HURRAY!!!!")



def quick_sort(arr):
    if len(arr)<=1:
        return arr
    
    pivot = arr[len(arr) // 2]  # Choosing the middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left)+middle+quick_sort(right)
my_array = [5,1,2,8,4]
sorted_array = quick_sort(my_array)
print(f"Original array: {my_array}")
print(f"Sorted array: {sorted_array}")
print("HURRAY!!!!")


def partition(Arr,low,high):
    pivot=arr[high]
    i=-1
    print(f"i-{i},pivot-{pivot},low-{-1},high-{high}")

    for j in range(0,high):
        if arr[j]<pivot:
            i+=1
            arr[i],arr[j]=arr[j],arr[i]
    arr[i+1],arr[high]=arr[high],arr[i+1]
    print(arr)
    return i+1

def quick_sort(arr,low,high):
    print(f"arr in qs: {arr},low: {low}, high:{high}")
    if low<high:
        pi=partition(arr,low,high)
        quick_sort(arr,low,pi-1)
        quick_sort(arr,pi+1,high)
    
arr=[5,1,2,8,4]
quick_sort(arr,0,len(arr)-1)
print(f"After :",arr)
