import sys
# Множества
# A + B = X
# def a(n, x):
#     prev = set()
#     for nums in n:
#         if x - nums in prev:
#             return nums, x - nums
#         prev.add(nums)
#     return 0,0
# a([1,3,5,8,9,3,4,5], 12) 
# Task A
#def main():
    #array = list(map(int, input().split))
    #array = 1,2,3,4,5,1,2,1,2,7,3
    # 1
    #print(len(set(input().split())))
    # 2
    # prev = set()
    # for i in array:
    #     if i not in prev:
    #         prev.add(i)
    # print(prev)
    # print(len(prev))

# Task B
#def main():
    #array_1 = set(map(int, input().split()))
    #array_2 = set(map(int, input().split()))
    # array_1 = [1, 4, 6, 2, 5, 7]
    # array_2 = [10, 4, 2, 3, 8,2,2,2]
    #print(set.intersection(array_1, array_2))
    # input_file = open("D:\Generator_Exel\lessons\input.txt", "r")
    # output_file = open("D:\Generator_Exel\lessons\output.txt", "w")

    # array_1 = input_file.readline().split()
    # array_2 = input_file.readline().split()
    # a = []
    # for i in array_1:
    #     if i in array_2:
    #         a.append(i)
    # a = sorted(a)
    # output_file.write(str(a))
    # print(list(set.intersection(array_1, array_2)))
    # array_1 = set([1, 0,3, 2, 2,3])
    # array_2 = set([4, 0,3, 2, 2,3])
    # 1
    # b = []
    # for i in array_1:
    #     if i in array_2:
    #         b.append(i)
    # print(b)
    # output_file.write(str(b) + "\n")
    #for x in sorted(b): print(output_file.write(str(b)), end=' ')
    # 2
    # a = []
    # [a.append(i) for i in set(array_1) if i in set(array_2)]
    # 3
    #for x in array_1 & array_2: print(x, end=' ')

# Task C
# def main():
#     def intersection(a, b):
#         inters = set()
#         not_inters = []
#         not_inters_1 = []
#         for i in a:
#             if i in b:
#                 inters.add(i)
#             else:
#                 not_inters.append(i)
        
#         for i in b:
#             if i not in a:
#                 not_inters_1.append(i)
#         print(inters, sorted(not_inters), sorted(not_inters_1))
#         return(inters, sorted(not_inters), sorted(not_inters_1))

#     #a, b = map(int, input().split())
#     #array = list(map(int, input().split()))
#     a, b = 0, 0
#     array = [0,1,10,9,1,3,0]
#     a = array[:a]
#     b = array[-b:]
#     print(a, b)
#     inters, not_inters, not_inters_1 = intersection(a, b)
#     print(len(inters))
#     for x in inters: print(x, end=' ')
#     print()
#     print(len(not_inters))
#     for x in not_inters: print(x, end=' ')
#     print()
#     print(len(not_inters_1))
#     for x in not_inters_1: print(x, end=' ')

#Task D
def main():
    #text = sys.stdin.readline()
    text = "She sells sea shells on the sea shore;\nThe shells that she sells are sea shells I'm sure.\nSo if she sells sea shells on the sea shore,\nI'm sure that the shells are sea shore shells."

    a = []
    for i in text.split('\n'):
        print(i)
        a += i.split()
        print(a)
    print(len(set(a)))
            

    #sys.stdout.write('YES')

if __name__ == '__main__':
	main()

