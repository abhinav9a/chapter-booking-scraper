from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located, presence_of_element_located
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import time
import os


url = "https://www.chapter-living.com/booking/"
residence = "CHAPTER KINGS CROSS"  # 1127644
booking_period = "SEP 24 - AUG 25 (51 WEEKS)"
property_type = "Ensuite"
space_option = "Bronze"


def get_data():
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920, 1080")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    results = []
    try:
        fake = Faker()
        driver.get(url)

        residence_dropdown = Select(driver.find_element(By.ID, "BookingAvailabilityForm_Residence"))
        residence_dropdown.select_by_visible_text(residence)
        time.sleep(1)
        booking_period_dropdown = Select(driver.find_element(By.ID, "BookingAvailabilityForm_BookingPeriod"))
        booking_period_dropdown.select_by_visible_text(booking_period)

        room_links = [element.get_attribute("href") for element in driver.find_elements(By.CLASS_NAME, "room-list-selection")]

        for link in room_links:
            # Generate Fake Data
            fake_first_name = fake.first_name()
            fake_last_name = fake.last_name()
            fake_email = fake.email()
            fake_phone_number = fake.phone_number()
            fake_password = fake.password()

            print(f"Link: {link}")
            driver.get(link)

            # Fill out the form
            driver.find_element(By.ID, "applicant_first_name").send_keys(fake_first_name)
            driver.find_element(By.ID, "applicant_last_name").send_keys(fake_last_name)
            country_code = (driver.find_element(By.CSS_SELECTOR, "input.country-code"))
            country_code.clear()
            country_code.send_keys("+91")
            driver.find_element(By.ID, "phone_numbers[0][phone_number]-base").send_keys(fake_phone_number)
            driver.find_element(By.ID, "applicant_username").send_keys(fake_email)
            driver.find_element(By.ID, "applicant_password").send_keys(fake_password)
            driver.find_element(By.ID, "applicant_password_confirm").send_keys(fake_password)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            checkbox = driver.find_element(By.ID, "agrees_to_terms")
            submit_btn = driver.find_element(By.ID, "create-app-btn")
            driver.execute_script("arguments[0].click();", checkbox)
            driver.execute_script("arguments[0].click();", submit_btn)  # Submit the form

            # Wait for the pop-up dialog to appear
            dialog = WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, "btn-bar")))

            # Click the "I agree to the terms" button
            dialog.find_element(By.CLASS_NAME, "js-confirm").click()
            time.sleep(2)

            # Application Form Page
            # Filter
            # TERM SELECTION
            term_select = Select(driver.find_element(By.CLASS_NAME, "student_units_filter.lease_start_window.first-value"))
            term_select.select_by_visible_text("Sep 24 - Jul 25 (44 Weeks) (07/09/2024 - 11/07/2025)")
            WebDriverWait(driver, 10).until(invisibility_of_element_located((By.CLASS_NAME, "app-loader-overlay.is-hidden.js-loader-overlay")))

            # FLOOR PLANS
            driver.find_element(By.CLASS_NAME, "property_floorplans").click()
            driver.find_element(By.CSS_SELECTOR, "a[data-value='1166878']").click()
            WebDriverWait(driver, 10).until(invisibility_of_element_located((By.CLASS_NAME, "app-loader-overlay.is-hidden.js-loader-overlay")))

            # SPACE OPTION
            driver.find_element(By.CSS_SELECTOR, "select[data-filter-name='space_configuration_ids'").click()
            driver.find_element(By.CSS_SELECTOR, "a[data-value='454']").click()
            WebDriverWait(driver, 10).until(invisibility_of_element_located((By.CLASS_NAME, "app-loader-overlay.is-hidden.js-loader-overlay")))

            view_details_btn = driver.find_element(By.CSS_SELECTOR, 'input[value="View Details"]')
            driver.execute_script("arguments[0].click();", view_details_btn)
            WebDriverWait(driver, 10).until( invisibility_of_element_located((By.CLASS_NAME, "app-loader-overlay.is-hidden.js-loader-overlay")))

            # Unit Info Page
            unit_lists = driver.find_elements(By.CLASS_NAME, "sus-unit-space-details")

            for i, unit in enumerate(unit_lists):
                data = {}
                # Extract details from the left side
                left_side = unit.find_element(By.CLASS_NAME, "sus-col-40.left").find_elements(By.CSS_SELECTOR, "dd.value")
                data["Building"] = left_side[0].text.strip()
                data["Rent"] = left_side[1].text.strip()
                data["Deposit"] = left_side[2].text.strip()
                data["Amenities"] = left_side[3].text.strip()

                # Extract unit space details from the right side
                unit_spaces = unit.find_element(By.CLASS_NAME, "unit-space-table")

                data["Spaces"] = []
                for row in unit_spaces.find_elements(By.CSS_SELECTOR, "tbody tr"):
                    space_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
                    status = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
                    data["Spaces"].append({"Name": space_name, "Status": status})

                results.append(data)
        return results
    except Exception as e:
        print("Error: ", e)
    finally:
        driver.close()


def save_data(data):
    try:
        client = MongoClient(os.getenv('CONNECTION_STRING'))
        db = client.get_database()[os.getenv('COLLECTION_NAME')]
        db.insert_many(data)
    except Exception as e:
        print("Error: ", e)
    finally:
        client.close()


if __name__ == "__main__":
    load_dotenv()
    data = get_data()
    save_data(data)
