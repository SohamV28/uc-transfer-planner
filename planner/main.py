import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === NORMALIZATION MAP ===
NORMALIZED_MAP = {
    "MATH 193": "Calculus I", "MATH 31A": "Calculus I", "MATH 20A": "Calculus I", "MATH 3A": "Calculus I",
    "MATH 194": "Calculus II", "MATH 31B": "Calculus II", "MATH 20B": "Calculus II", "MATH 3B": "Calculus II",
    "MATH 292": "Calculus III", "MATH 32A": "Calculus III", "MATH 20C": "Calculus III",
    "MATH 294": "Multivariable Calculus", "MATH 32B": "Multivariable Calculus", "MATH 33B": "Multivariable Calculus",
    "MATH 142": "Linear Algebra", "MATH 18": "Linear Algebra", "MATH 6A": "Linear Algebra",
    "MATH 142L": "Linear Algebra Lab",
    "STA 035A": "Statistics A", "STAT 10": "Statistics A", "STAT 67": "Statistics A",
    "STA 035B": "Statistics B", "STAT 11": "Statistics B", "STAT 7": "Statistics B",
    "STA 035C": "Statistics C", "STATS 13": "Statistics C",
    "STA 013": "Intro to Stats", "STAT 8": "Intro to Stats",
    "PSYCH 214": "Psych Stats", "PSYCH 215": "Psych Stats",
    "COMSC 140": "CS I", "COMSC 200": "CS II", "COMSC 210": "CS III",
    "CS I": "CS I", "CS II": "CS II", "CS III": "CS III",
    "COMSC 165": "CS II", "COMSC 260": "CS III"
}

UC_IDS = {
    "UC Davis": ("89", "e2aafd38-f1e3-4e7a-137a-08dcbcdb53de"),
    "UCLA": ("117", "2b9a9fa2-5dad-4e64-cc51-08dc9134ea85"),
    "UCSB": ("128", "eda5a4d4-8165-478a-97fe-08dcd6abdbb0"),
    "UCSD": ("7", "da31dba3-8138-4ece-a822-08dca807bc76"),
    "UCR": ("46", "6cd925f5-096e-4c87-a195-08dcf4773cca"),
    "UCI": ("120", "e9652deb-3779-425c-a642-08dc9aca4bac"),
    "UCSC": ("132", "024e76f8-69a2-47c7-fb17-08dca4e7493d"),
}

def build_url(year, cc_id, uc_id, major_id):
    return f"https://assist.org/transfer/results?year={year}&institution={cc_id}&agreement={uc_id}&agreementType=to&viewAgreementsOptions=true&view=agreement&viewBy=major&viewByKey={year}%2F{cc_id}%2Fto%2F{uc_id}%2FMajor%2F{major_id}"

def scrape_dvc_courses(uc_name, uc_id, major_id):
    print(f"\n🌐 Scraping {uc_name}...")
    url = build_url(75, "114", uc_id, major_id)

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    browser.get(url)
    try:
        WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "prefixCourseNumber")))
        time.sleep(1.5)
        elements = browser.find_elements(By.CLASS_NAME, "prefixCourseNumber")
        raw_courses = [el.text.strip() for el in elements if el.text.strip()]
        norm_courses = [NORMALIZED_MAP.get(course, course) for course in raw_courses]
        print(f"✅ {uc_name}: {len(norm_courses)} courses found.")
        return set(norm_courses)
    except Exception as e:
        print(f"❌ Failed to load {uc_name}: {str(e)}")
        return set()
    finally:
        browser.quit()

def main():
    major = input("📘 Enter your major (press Enter to continue): ").strip()
    if not major:
        print("❌ No major entered. Exiting.")
        return

    all_uc_courses = {}
    for uc_name, (uc_id, major_id) in UC_IDS.items():
        courses = scrape_dvc_courses(uc_name, uc_id, major_id)
        all_uc_courses[uc_name] = courses

    if not all_uc_courses:
        print("❌ No UC data found.")
        return

    common_courses = set.intersection(*all_uc_courses.values()) if all_uc_courses else set()

    print("\n✅ COMMON COURSES (DVC courses mapped to shared requirements):")
    if common_courses:
        for c in sorted(common_courses):
            print(f" - {c}")
    else:
        print("None found – check mappings or update course normalization.")

    print("\n📍 UNIQUE COURSES (specific to each UC):")
    for uc_name, courses in all_uc_courses.items():
        unique = sorted(c for c in courses if c not in common_courses)
        print(f"\n{uc_name}:")
        for course in unique:
            print(f" - {course}")

if __name__ == "__main__":
    main()
