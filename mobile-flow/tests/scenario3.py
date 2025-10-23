import pytest
import time
from pages.allow_popups_page import Allows #sem fluent pages inicialmente

def test_product_purchase_flow(driver):
    #initialize all pages at the beginning for now, fluent pages later
    allowpopup = Allows(driver)

    allowpopup.allow_all_permitions()


    time.sleep(5)