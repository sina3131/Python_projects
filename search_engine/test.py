
import subprocess

# API_KEY="AIzaSyDQn6JZeJIL_WJdUfpCnCntK3eQgRlJZCc"
# CX="844f37d6d23414f54"
# QUERY="lego"
# START="0"
# COUNTRY="sv"



# command = [
#     "curl",
#     f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={QUERY}&start={START}&gl={COUNTRY}",
# ]

# result = subprocess.run(command, capture_output=True, text=True)
# print(result.stdout)

list = [1,2,3]
new_copy = list.copy()

print(list)
print(new_copy)

list.append(4)

print(list)
print(new_copy)