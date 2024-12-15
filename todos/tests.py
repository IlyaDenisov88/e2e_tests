#to run this you first need "pip install selenium"
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class TodoAppTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)  # Ждем загруженности элементов

    def test_main_page_elements(self):
        self.browser.get('http://localhost:8000/todos/')
        
        # Проверяем заголовок страницы
        title = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(title.text.strip(), 'Todo List')

        # Проверяем форму добавления задачи
        input_box = self.browser.find_element(By.CLASS_NAME, 'form-control')
        self.assertIn('Do laundry', input_box.get_attribute('placeholder'))

        # Проверяем список дефолтных задач
        todo_list = self.browser.find_elements(By.CLASS_NAME, 'list-group-item ')
        self.assertEqual(len(todo_list), 2)

        # Проверяем кнопку "Add"
        add_button = self.browser.find_element(By.NAME, 'submit')
        self.assertEqual(add_button.text.strip(), 'Add')

        
    def test_add_todo_item(self):
        self.browser.get('http://localhost:8000/todos/')

        # Находим поле ввода для добавления нового элемента
        input_box = self.browser.find_element(By.CLASS_NAME, 'form-control')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Do laundry'
        )

        input_box.send_keys('Buy milk')
        add_btn = self.browser.find_element(By.NAME, 'submit')
        add_btn.click()

        time.sleep(1)

        todo_list = self.browser.find_element(By.CLASS_NAME, 'list-group-item')
        self.assertIn('Buy milk', todo_list.text)

    def test_complete_todo_item(self):
        self.browser.get('http://localhost:8000/todos/')

        checkboxes = self.browser.find_elements(By.CSS_SELECTOR, ".todo-status-checkbox")
        if checkboxes:
        # Нажимаем на первый чекбокс
            before_click = checkboxes[0].is_selected()
            checkboxes[0].click()
            
            time.sleep(1)

            checkboxes = self.browser.find_elements(By.CSS_SELECTOR, ".todo-status-checkbox")
            after_click = checkboxes[0].is_selected()
            if after_click:
                print("Checkbox is checked: True")
            else:
                print("Checkbox is checked: False")
            self.assertEqual(not before_click, after_click)

    def test_delete_item(self):
        
        self.browser.get('http://localhost:8000/todos/')
        before_del_count = len(self.browser.find_elements(By.CSS_SELECTOR, ".todo-status-checkbox"))

        time.sleep(5)
            # Ожидаем, пока иконка удаления станет видимой
        delete_icon = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "i.far.fa-trash-alt"))
        )


        delete_icon.click()

        time.sleep(1)
        after_del_count = len(self.browser.find_elements(By.CSS_SELECTOR, ".todo-status-checkbox"))
        self.assertEqual(before_del_count, after_del_count + 1)

    
    def tearDown(self):
        self.browser.quit()  # Закрываем браузер после тестов
