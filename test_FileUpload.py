import unittest
from MongoDBConnection import MongoDBConnection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
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
        self.driver.get("https://www.lambdatest.com/selenium-playground/upload-file-demo")

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

    def test_file_upload_1(self):
        try:
            # Caminho do arquivo a ser enviado
            upload_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "assets", "Frame 3.png"))
            
             # Esperar pelo botão de upload
            upload_file = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "file"))
            )

            # Enviar o caminho do arquivo
            upload_file.send_keys(upload_path)
            
            complete_message = self.driver.find_element(
                By.XPATH, "//div[@id='error']").text
           
            # Verifique se a mensagem é "File Successfully Uploaded"
            if self.assertEqual("File Successfully Uploaded", complete_message, "\n Expected & Actual Messages Do Not Match \n"):
                print("Approved")            
           
            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_file_upload_1", "Approved", content=complete_message, expected="File Successfully Uploaded")
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_file_upload_1", "Failed")
            raise e

    def test_file_upload_2(self):
        try:
            # Caminho do arquivo a ser enviado
            upload_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "assets", "test.exe"))
              
             # Esperar pelo botão de upload
            upload_file = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "file"))
            )

            # Enviar o caminho do arquivoo
            upload_file.send_keys(upload_path)
            
            complete_message = self.driver.find_element(
                By.XPATH, "//div[@id='error']").text
            # Verifique se a mensagem é "File type should be pdf, png, jpeg or jpg"
            self.assertEqual("File type should be pdf, png, jpeg or jpg", complete_message, "\n Expected & Actual Messages Do Not Match \n"):
            print("Approved")

            # Registrar o resultado do teste no MongoDB
            self.record_test_result("test_file_upload_2", "Approved", content=complete_message, expected="File type should be pdf, png, jpeg or jpg")
        except Exception as e:
            # Se houver uma exceção, registrar que o teste falhou
            self.record_test_result("test_file_upload_2", "Failed")
            raise e

if __name__ == "__main__":
    unittest.main()
