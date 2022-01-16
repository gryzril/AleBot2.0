import random
import pickle


class MyClass():
    def __init__(self, param):
        self.param = param
    
def save_object(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
        
def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

def generate_board():
    nums = []
    for i in range(50):
        num = random.randint(1, 99)
        if num not in nums: 
            nums.append(num)
    #print(nums)
    
    rows, cols = (5, 5)
    arr=[]
    counter = 0
    for i in range(rows):
        col = []
        for j in range(cols):
            to_add = nums[counter]
            if(to_add < 10):
                to_add = "0" + str(to_add)
            col.append(str(to_add))
            counter+=1
        arr.append(col)
    #print(arr)

    temp = arr[2]
    temp[2] = "-1"

    return arr
    
def print_board(board):
    for x in range(0, 5):
        print(board[x])

def update_board(board, number):
    for i in range(5):
        for j in range(5):
            if(board[i[j]] == number):
                board[i[j]] = "-1"
    #check_board()
    return board

        
#board = generate_board()
#print_board(board)

#obj = MyClass(board)
#save_object(obj)

#obj = load_object("data.pickle")
 
#print(obj.param)
#print(isinstance(obj, MyClass))