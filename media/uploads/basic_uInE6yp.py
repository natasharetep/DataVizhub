# num = [1,4,6,2,3,7,8]

# for i in range(len(num)):
#     min_index = i
#     for j in range(i+1, len(num)):
#         if num[j] < num[min_index]:
#             min_index = j
#     num[i], num[min_index] = num[min_index], num[i]

# for n in num:
#     print(n)


num = [1,4,6,2,3,7,8]

n = max(num)
print(n)

formula = n * (n+1) // 2

print(formula)
num2 = sum(num)
missing_num = formula-num2
num.append(missing_num)
print(num)  




