#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.desktop.base import Base


class Home(Base):

    _page_title = "Add-ons for Firefox"
    _first_addon_locator = (By.CSS_SELECTOR, ".summary > a > h3")
    _other_applications_link_locator = (By.ID, "other-apps")

    #Most Popular List
    _most_popular_item_locator = (By.CSS_SELECTOR, "ol.toplist li")
    _most_popular_list_heading_locator = (By.CSS_SELECTOR, "#homepage > .secondary h2")

    _explore_side_navigation_header_locator = (By.CSS_SELECTOR, "#side-nav > h2:nth-child(1)")
    _explore_featured_link_locator = (By.CSS_SELECTOR, "#side-nav .s-featured a")
    _explore_popular_link_locator = (By.CSS_SELECTOR, "#side-nav .s-users a")
    _explore_top_rated_link_locator = (By.CSS_SELECTOR, "#side-nav .s-rating a")

    _featured_personas_see_all_link = (By.CSS_SELECTOR, "#featured-personas h2 a")
    _featured_personas_title_locator = (By.CSS_SELECTOR, "#featured-personas h2")
    _featured_personas_items_locator = (By.CSS_SELECTOR, "#featured-personas li")

    _featured_collections_locator = (By.CSS_SELECTOR, "#featured-collections h2")
    _featured_collections_elements_locator = (By.CSS_SELECTOR, "#featured-collections section:nth-child(1) li")

    _featured_extensions_title_locator = (By.CSS_SELECTOR, '#featured-extensions > h2')
    _featured_extensions_see_all_locator = (By.CSS_SELECTOR, '#featured-extensions > h2 > a')
    _featured_extensions_elements_locator = (By.CSS_SELECTOR, '#featured-extensions section:nth-child(1) > li')

    _category_list_locator = (By.CSS_SELECTOR, "ul#side-categories li")

    _extensions_menu_link = (By.CSS_SELECTOR, "#extensions > a")

    _promo_box_locator = (By.CSS_SELECTOR, "section#promos")

    _up_and_coming_locator = (By.ID, "upandcoming")

    def __init__(self, testsetup, open_url=True):
        """Creates a new instance of the class and gets the page ready for testing."""
        Base.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def hover_over_addons_home_title(self):
        home_item = self.selenium.find_element(*self._amo_logo_link_locator)
        ActionChains(self.selenium).\
            move_to_element(home_item).\
            perform()

    def click_featured_personas_see_all_link(self):
        self.selenium.find_element(*self._featured_personas_see_all_link).click()
        from pages.desktop.personas import Personas
        return Personas(self.testsetup)

    def click_featured_collections_see_all_link(self):
        self.selenium.find_element(*self._featured_collections_locator).find_element(By.CSS_SELECTOR, " a").click()
        from pages.desktop.collections import Collections
        return Collections(self.testsetup)

    def click_to_explore(self, what):
        what = what.replace(' ', '_').lower()
        self.selenium.find_element(*getattr(self, "_explore_%s_link_locator" % what)).click()
        from pages.desktop.extensions import ExtensionsHome
        return ExtensionsHome(self.testsetup)

    @property
    def most_popular_count(self):
        return len(self.selenium.find_elements(*self._most_popular_item_locator))

    @property
    def most_popular_list_heading(self):
        return self.selenium.find_element(*self._most_popular_list_heading_locator).text

    @property
    def featured_personas_count(self):
        return len(self.selenium.find_elements(*self._featured_personas_items_locator))

    @property
    def featured_personas_title(self):
        return self.selenium.find_element(*self._featured_personas_title_locator).text

    @property
    def featured_collections_title(self):
        return self.selenium.find_element(*self._featured_collections_locator).text

    @property
    def featured_collections_count(self):
        return len(self.selenium.find_elements(*self._featured_collections_elements_locator))

    @property
    def featured_extensions_see_all(self):
        return self.selenium.find_element(*self._featured_extensions_see_all_locator).text

    @property
    def featured_extensions_title(self):
        title = self.selenium.find_element(*self._featured_extensions_title_locator).text
        return title.replace(self.featured_extensions_see_all, '').strip()

    @property
    def featured_extensions_count(self):
        return len(self.selenium.find_elements(*self._featured_extensions_elements_locator))

    @property
    def up_and_coming_island(self):
        from pages.desktop.regions.island import Island
        return Island(self.testsetup, self.selenium.find_element(*self._up_and_coming_locator))

    @property
    def explore_side_navigation_header_text(self):
        return self.selenium.find_element(*self._explore_side_navigation_header_locator).text

    @property
    def explore_featured_link_text(self):
        return self.selenium.find_element(*self._explore_featured_link_locator).text

    @property
    def explore_popular_link_text(self):
        return self.selenium.find_element(*self._explore_popular_link_locator).text

    @property
    def explore_top_rated_link_text(self):
        return self.selenium.find_element(*self._explore_top_rated_link_locator).text

    def click_on_first_addon(self):
        self.selenium.find_element(*self._first_addon_locator).click()
        from pages.desktop.details import Details
        return Details(self.testsetup)

    def get_title_of_link(self, name):
        name = name.lower().replace(" ", "_")
        locator = getattr(self, "_%s_link_locator" % name)
        return self.selenium.find_element(*locator).get_attribute('title')

    @property
    def promo_box_present(self):
        return self.is_element_visible(*self._promo_box_locator)

    @property
    def categories(self):
        return [self.Categories(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_list_locator)]

    def category(self, web_element):
        return self.Categories(self.testsetup, web_element)

    @property
    def most_popular_items(self):
        return [self.MostPopularRegion(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._most_popular_item_locator)]

    class Categories(Page):
        _link_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.text

        def click_link(self):
            self._root_element.find_element(*self._link_locator).click()
            from pages.desktop.category import Category
            return Category(self.testsetup)

    class MostPopularRegion(Page):
        _name_locator = (By.TAG_NAME, "span")
        _users_locator = (By.CSS_SELECTOR, "small")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            self._root_element.find_element(*self._name_locator).text

        @property
        def users_number(self):
            users_text = self._root_element.find_element(*self._users_locator).text
            return int(users_text.split(' ')[0].replace(',', ''))

    @property
    def featured_extensions(self):
        return [self.FeaturedExtensions(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._featured_extensions_elements_locator)]

    class FeaturedExtensions(Page):

        _author_locator = (By.CSS_SELECTOR, 'div.addon > div.more > div.byline > a')
        _summary_locator = (By.CSS_SELECTOR, 'div.addon > div.more > .addon-summary')
        _link_locator = (By.CSS_SELECTOR, 'div.addon > .summary')

        def __init__(self, testsetup, web_element):
            Page.__init__(self, testsetup)
            self._root_element = web_element

        @property
        def author_name(self):
            self._move_to_addon_flyout()
            return [element.text for element in self._root_element.find_elements(*self._author_locator)]

        @property
        def summary(self):
            self._move_to_addon_flyout()
            return self._root_element.find_element(*self._summary_locator).text

        def _move_to_addon_flyout(self):
            ActionChains(self.selenium).\
                move_to_element(self._root_element).\
                perform()

        def click_first_author(self):
            author_item = self.selenium.find_element(*self._author_locator)
            ActionChains(self.selenium).\
                move_to_element(author_item).click().\
                perform()
            from pages.desktop.user import User
            return User(self.testsetup)
