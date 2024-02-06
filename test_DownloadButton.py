import unittest
from MongoDBConnection import MongoDBConnection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class DownloadTests(unittest.TestCase):

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
        self.driver.get("https://www.lambdatest.com/selenium-playground/jquery-download-progress-bar-demo")

    def tearDown(self):
        self.driver.quit()

    def click_download_button(self):
        self.driver.find_element(By.ID, "downloadButton").click()

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

    def test_download_progress_1(self):
        try:
            # Clica botão de download
            self.click_download_button()

            complete_message = self.driver.find_element(
                By.XPATH, "//div[@id='dialog']/div[text()='Complete!']").text
            # Verifique se a mensagem é "Complete"
            self.assertEqual("Complete!", complete_message, "\n Expected & Actual Messages Do Not Match \n")
            print("Approved")

            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_download_progress_1", "Approved", content=complete_message, expected="Complete!")
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_download_progress_1", "Failed")
            raise e

    def test_download_progress_2(self):
        try:
            # Clica botão de download
            self.click_download_button()

            # Aguarde até que o elemento esteja visível
            wait = WebDriverWait(self.driver, 10)
            element_to_drag = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]")))

            # Obtenha as coordenadas do elemento antes do movimento
            initial_location = element_to_drag.location

            # Crie uma instância ActionChains
            action_chains = ActionChains(self.driver)

            # Realize o clique no elemento e mantenha pressionado o botão do mouse
            action_chains.click_and_hold(element_to_drag).perform()

            # Mova o mouse para a posição desejada (ajuste conforme necessário)
            action_chains.move_by_offset(300, 100).perform()

            # Obtenha as coordenadas do elemento depois do movimento
            final_location = element_to_drag.location

            # Solte o botão do mouse
            action_chains.release().perform()

            # Verifique se as coordenadas foram alteradas
            self.assertNotEqual(initial_location, final_location, "Element not moved as expected")
            print("Approved")

            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_download_progress_2", "Approved",
                                    comparison_variable={"initial_location": initial_location, "final_location": final_location}
                                    )
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_download_progress_2", "Failed",
                                    comparison_variable={"initial_location": initial_location, "final_location": final_location}
                                    )
            raise e

    def test_download_progress_3(self):
        try:
            # Clica botão de download
            self.click_download_button()

            # Aguarde até que o botão de cancelamento esteja visível e interagível
            wait = WebDriverWait(self.driver, 10)
            cancel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*/text()[normalize-space(.)='Cancel Download']/parent::*")))

            cancel_message = cancel_button.text

            # Execute o clique
            cancel_button.click()

            # Verifique se a mensagem é "Cancel Download" 
            self.assertEqual("Cancel Download", cancel_message, "\n Expected & Actual Messages Do Not Match \n")
            print("Approved")

            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_download_progress_3", "Approved", content=cancel_message, expected="Cancel Download")
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_download_progress_3", "Failed", expected="Cancel Download")
            raise e

if __name__ == "__main__":
    unittest.main()
