import unittest
from MongoDBConnection import MongoDBConnection
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

class RadioButtonTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mongo_connection = MongoDBConnection("mongodb+srv://---") # Sua URL de conexão 

    @classmethod
    def tearDownClass(cls):
        # Fechar conexão com o MongoDB
        cls.mongo_connection.close_connection()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get("https://www.lambdatest.com/selenium-playground/radiobutton-demo")

    def tearDown(self):
        self.driver.quit()

    def record_test_result(self, test_name, status, comparison_variable=None, content=None, expected=None):
        date_time = datetime.now()
        # Registrar o resultado do teste no MongoDB
        result_data = {
            "test_name": test_name,
            "status": status,
            "datetime": date_time,
            "content": content,
            "comparison_variable": comparison_variable,
            "expected": expected,
        }

        self.mongo_connection.collection.insert_one(result_data)

    def test_selected_radio_button_message(self):
        try:
            self.driver.find_element(
                By.XPATH, "//input[@value='Female' and @name='optradio']").click()
            self.driver.find_element(By.ID, "buttoncheck").click()
            actual_message = self.driver.find_element(
                By.XPATH, "//button[@id='buttoncheck']/following-sibling::p").text
            expected_message = "Radio button 'Female' is checked"
            self.assertEqual(expected_message, actual_message,
                             "\n Actual & Expected Messages Do Not Match")
            print("Approved")
            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_selected_radio_button_message", "Approved", content=actual_message, expected=expected_message)
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_selected_radio_button_message", "Failed")
            raise e

    def test_disabled_radio_button(self):
        try:
            actual_label = self.driver.find_element(
                By.XPATH, "//label[text()='Disabled Radio Button']").text
            self.assertTrue("Disabled" in actual_label,
                            "\n Actual Label Does Not Contain Disabled")
            print("Approved")
            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_disabled_radio_button", "Approved", content=actual_label, expected="Disabled Radio Button")
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_disabled_radio_button", "Failed")
            raise e

if __name__ == "__main__":
    unittest.main()
