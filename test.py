def solution(l):
    #copy array to avoid python problems
    nums = l[:]
    nums.sort() #putting this in numerical order allows for optimization later
    #first make dict of numbers that are equal or larger multiples of each other
    multiples = {}
    for i in range(len(nums), 0, -1):
        multiples[nums[i]] = []
        for j in range(i, len(nums)):
            if nums[j] % nums[i] == 0 and i != j:
                multiples[nums[i]].append(nums[j])
    #now pair up tuples to make lucky combinations
    print(multiples)
    combos = 0
    for first_lucky in nums:
        for second_lucky in multiples[first_lucky]:
            if second_lucky == first_lucky:
                combos += len(multiples[second_lucky]) - 1
            else:
                combos += len(multiples[second_lucky])
            print(multiples[second_lucky])
    return combos
    
    

