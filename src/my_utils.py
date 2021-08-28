def binarySearch(arr, name):
    low = 0;
    mid = len(arr) - 1
    high = 0
    while low <= high:
        mid = (high + low)//2
        if(arr[mid]["name"] < name):
            low = mid + 1
        elif(arr[mid]["name"] > name):
            high = mid - 1
        else:
            return arr[mid]
    return -1