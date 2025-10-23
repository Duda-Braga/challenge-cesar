from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Allows(BasePage):
    '''
    App permission popups on first launch
    '''
    class Locators:
        LOC_APROXIMATE_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_location_accuracy_radio_coarse")
        LOC_PRECISE_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_location_accuracy_radio_fine")
        LOC_ALLOW_WHILE_USING_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
        LOC_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button")
        LOC_DONT_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button")

        NOTIFICATION_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
        NOTIFICATION_DONT_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button")

        VIDEO_ALLOW_WHILE_USING_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
        VIDEO_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button")
        VIDEO_DONT_ALLOW_BTN = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button")

    def __init__(self,driver):
        super().__init__(driver)

    def allow_location(self):
        if self.is_element_displayed(*self.Locators.LOC_ALLOW_BTN):
            self.click_element(*self.Locators.LOC_ALLOW_BTN)

    def allow_notification(self):
        if self.is_element_displayed(*self.Locators.NOTIFICATION_ALLOW_BTN):
            self.click_element(*self.Locators.NOTIFICATION_ALLOW_BTN)
    
    def allow_video(self):
        if self.is_element_displayed(*self.Locators.VIDEO_ALLOW_BTN):
            self.click_element(*self.Locators.VIDEO_ALLOW_BTN)
    
    def allow_all_permitions(self):
        self.allow_location()
        self.allow_notification()
        self.allow_video()
