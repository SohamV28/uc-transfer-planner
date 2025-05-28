# UC Transfer Planner - Starting Point

print("📚 Welcome to the UC Transfer Planner!")
print("-------------------------------------")

cc = input("Enter your Community College (e.g., Diablo Valley College): ")
uc = input("Enter your target UC campus (e.g., UC Davis): ")
major = input("Enter your intended major (e.g., Computer Science): ")


sample_courses = [
    "MATH 192 - Calculus I",
    "MATH 193 - Calculus II",
    "PHYS 130 - Physics I",
    "COMSC 110 - Intro to Programming",
    "COMSC 165 - Data Structures"
]


print(f"\n📍 Community College: {cc}")
print(f"🎯 UC Campus: {uc}")
print(f"🎓 Major: {major}\n")

print("✅ Recommended major preparation courses:")
for course in sample_courses:
    print(" -", course)



print("\n✅ NOTE: This is just a sample. Real data will come from ASSIST.org later.")
