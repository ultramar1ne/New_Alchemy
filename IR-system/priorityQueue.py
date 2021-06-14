class PriorityQueue(object):
    def __init__(self):
        self.queue = [] # a list of tuple 
  
    def __str__(self):
        return '\n'.join([i[0] for i in self.queue])
  
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
    
    # for 
    def hasDuplicate(self, data:tuple):
       return data in [i[0] for i in self.queue]
  
    # for inserting an element in the queue
    def insert(self, data:tuple): # tuple(data, priority)
        self.queue.append(data)
  
    # for popping an element based on Priority
    def dequeue(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i][1] > self.queue[max][1]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()
  
if __name__ == '__main__':
    myQueue = PriorityQueue()
    myQueue.insert(('a', 12))
    myQueue.insert(('b',1))
    myQueue.insert(('c',14))
    myQueue.insert(('d',7))

    print(myQueue)         
    while not myQueue.isEmpty():
        print(myQueue.dequeue())
        print(myQueue)