from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementNotVisibleException
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import tkinter as tk
import requests
from PIL import Image
from io import BytesIO
import os
from tkinter import simpledialog
from tkinter import messagebox
from IPython.display import display
import pdb

def next_image(driver):
    next = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[1]/div/div[2]/div[1]/div/button[2]")
    next.click()

def get_image_url(driver):
    el = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]")
    return el.get_attribute("src")

def get_image_urls_by_query(style, num_images):
    driver = webdriver.Chrome()
    image_urls = []
    driver.get("https://www.google.com/advanced_image_search")

    all_these_words = driver.find_element(By.NAME, "as_q")
    any_of_these_words = driver.find_element(By.NAME, "as_oq")

    all_these_words.send_keys(style)
    any_of_these_words.send_keys("building facade architecture")

    driver.find_element(By.ID, "imgsz_button").click()

    driver.find_element(By.ID, ":76").click()

    driver.find_element(By.ID, "imgtype_button").click()

    driver.find_element(By.ID, ":7s").click()

    driver.find_element(By.ID, "as_filetype_button").click()
    driver.find_element(By.ID, ":6s").click()

    time.sleep(1)
    all_these_words = driver.find_element(By.CLASS_NAME, "jfk-button-action").click()

    driver.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button").click()

    time.sleep(1)

    menu = driver.find_element(By.CLASS_NAME, "islrc")
    first_image = menu.find_element(By.TAG_NAME, "img")
    first_image.click()
    time.sleep(1)

    while len(image_urls) < num_images:
        time.sleep(1)
        url = get_image_url(driver)
        image_urls.append(url)
        next_image(driver) 

    driver.quit()
    return image_urls

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size
    
def save_image_links(download_directory, urls):
    for url in urls:
        try: 
            response = requests.get(url)

            if response.status_code == 200:
                file_name = url.split("/")[-1]
                file_path = f"{download_directory}/{file_name}.jpg"

                with open(file_path, "wb") as file:
                    file.write(response.content)

                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {url}")
        except requests.exceptions.InvalidSchema as e:
            print("Couldn't download the image:", e)
            next
    True

def view_and_delete_image(image_path, df):
    desired_size = (800, 600)
    image = Image.open(image_path)
    image.show()


    file_name = os.path.basename(image_path)
    width, height = image.size()

    response = simpledialog.askstring(f"Delete Image {width}x{height}", f"Do you want to delete '{file_name}'? (y/n):", parent=root)
    if response and response.lower() == 'q':
        image.close()
        return df, False, True

    if response and response.lower() == 'y':
        os.remove(image_path)
        messagebox.showinfo("Deleted", f"Deleted '{file_name}'")

        index = df[df['File Name'] == file_name].index
        df = df.drop(index)
        image.close()
        return df, True, False

    return df, False, False

def delete_small_images(folder_path, width_threshold, height_threshold):
    files = os.listdir(folder_path)
    deleted_count = 0

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with Image.open(file_path) as img:
                width, height = img.size

                if width < width_threshold or height < height_threshold:
                    os.remove(file_path)
                    print(f"Deleted '{file_name}' (Size: {width}x{height})")
                    deleted_count += 1
        except Exception as e:
            print(f"Error processing '{file_name}': {e}")

    print(f"Deleted {deleted_count} images. {len(os.listdir(folder_path))} Images left.")

def create_folder(name):
    try:
        os.mkdir(name)
        print(f"Folder '{name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    style = "Modernist"
    query = f"{style.capitalize()}"
    num_images = 450
    download_directory = f"./{style} style dataset"
    create_folder(download_directory)
    urls = get_image_urls_by_query(style, num_images)
    save_image_links(download_directory, urls)
    delete_small_images(download_directory, 500, 300)

if __name__ == "__main__":
    main()