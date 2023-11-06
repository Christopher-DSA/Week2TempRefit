# 123 Main St, Springfield, IL 62701
# 456 Oakwood Ave, Oak Park, CA 91377
# 789 Elm St, Elmira, NY 14901
# 321 Willow Rd, Willowbrook, IL 60527
# 555 Pine St, Pineville, LA 71360
# 1010 Maple Ave, Maplewood, NJ 07040
# 777 Cherry St, Cherry Hill, NJ 08002
# 888 Oak St, Oakland, CA 94607
# 666 Birch Rd, Birchwood, WI 54817
# 999 Cedar Ave, Cedar Rapids, IA 52401
# 3200 Mayor Magrath Dr S, Lethbridge, AB T1K 6Y6
# 3201 Mayor Magrath Dr S, Lethbridge, AB T1K 6Y6
# 3300 Mayor Magrath Dr S, Lethbridge, AB T1K 6Y6
# 3200 Mayor St, Lethbridge, AB T1K 6Y6
# 3200 Mayor Magrath Dr SE, Lethbridge, AB T1K 6Y6
# 3200 Mayor Magrath Dr N, Lethbridge, AB T1K 6Y6
# 3210 Mayor Magrath Dr S, Lethbridge, AB T1K 6Y6
# 123 Main St, Lethbridge, AB T1K 6Y6
# 456 Elm St, Lethbridge, AB T1K 6Y6
# 789 Oak St, Lethbridge, AB T1K 6Y6

# from fuzzywuzzy import fuzz

# def find_matching_addresses(substring):
#     matching_addresses = []

#     with open('addresses.txt', 'r') as file:
#         addresses = file.readlines()

#         for address in addresses:
#             # Calculate the similarity score between the substring and the address
#             similarity_score = fuzz.partial_ratio(substring, address)

#             # You can adjust the threshold as needed to control the matching sensitivity
#             if similarity_score >= 100:  # You can adjust this threshold
#                 matching_addresses.append(address.strip())  # Remove newline character

#     return matching_addresses
# substring = "3200 Mayor Magrath Dr S, AB T1K 6Y6"
# matching_addresses = find_matching_addresses(substring)

# for address in matching_addresses:
#     print(address)
