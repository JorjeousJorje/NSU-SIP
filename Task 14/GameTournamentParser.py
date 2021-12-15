import os
import re
import requests

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
    


class GameTournamentAfterGameImageParser:
    
    def onclick_match_pages_script(self, onclick):
        return onclick and re.compile(r"match_pages\('past',\d\)").search(onclick)

    def onclick_mvideo_script(self, onclick):
        return onclick and re.compile(r"mvideo\([2-9]\)").search(onclick)
    
    def get_soup_after_execute(self, script: str) -> BeautifulSoup:
        self.driver.execute_script(script)
        # TODO: fox this
        sleep(0.5)
        new_page_source = self.driver.page_source
        soup = BeautifulSoup(new_page_source, 'lxml')
        return soup
        
    def page_jump(self, page_num) -> None:
        a_tag = self.soup.find('a', {"onclick" : f"match_pages('past',{page_num})"})
        
        if a_tag is None:
            raise RuntimeError(f"<ImageParser>: page {page_num} does not exist!")
        
        script = a_tag["onclick"]
        self.soup = self.get_soup_after_execute(script)
        
    def traverse_all_games(self, match_soup: BeautifulSoup) -> list:
        games_results = []
        # current page result immediately available
        games_results.append(match_soup.find('a', {"class": "g-rezults fancybox"}, href=True))
        a_tags = match_soup.find_all('a', onclick=self.onclick_mvideo_script)
        
        for a_tag in a_tags:
            script = a_tag["onclick"]
            other_game_soup = self.get_soup_after_execute(script)
            games_results.append(other_game_soup.find('a', {"class": "g-rezults fancybox"}, href=True))
        return games_results
               
        
    def save_found_image(self, image_url: str) -> None:
        response = requests.get(image_url, stream=True)
        
        if not response.ok:
            print(response)
        img_name = image_url.split('/')[-1]
        
        with open(self.folder + os.sep + img_name, "wb") as img_file:
            img_file.write(response.content)
      
    def get_match_url(self, match_id) -> str:
        res = self.soup.find_all('a', {"class": "mlink"}, href=True)
        matches_urls: list[str] = [ match['href'] for match in res ]
        passed_matches_urls = matches_urls[self.games_per_page:]
        match_url: str = passed_matches_urls[match_id - 1]
        return match_url
    
    def get_match_page_soup(self, match_url) -> BeautifulSoup:
        self.driver.get(self.root_url + match_url)
        match_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return match_soup

    def collect_match_results(self, match_soup: BeautifulSoup):    
        games_results = self.traverse_all_games(match_soup)
        
        print(f"Results of match {self.initial_match_id} are:")
        
        self.result_states.clear()
        for i, res in enumerate(games_results, start=1):
            if not res:
                self.result_states.append((i, False))
                print(f"<ImageParser>: Result of game {i}/{len(games_results)} is not available!")
            else:
                image_url = res['href']
                
                if self.folder is not None:
                    self.save_found_image(self.root_url + image_url)
                    print(f"<ImageParser>: Result of game {i}/{len(games_results)} is saved to directory '{self.folder}'!")
                self.result_states.append((i, True))
        
    def parse_game_page(self, match_id):
        match_url: str = self.get_match_url(match_id)
        match_soup = self.get_match_page_soup(match_url)
        self.collect_match_results(match_soup)
            
    
    def __init__(self) -> None:
        self.root_url = 'https://game-tournaments.com'
        self.current_url = self.root_url + '/dota-2/matches'
        self.games_per_page = 20
        self.max_page_jump_distance = 3
        
        self.response = requests.get(self.current_url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        
        self.init_browser()
        self.initial_match_id: int = None
        self.folder: str = None   
        self.result_states: list[tuple[int, bool]] = []  
        
    def init_browser(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.current_url)

    def parse_image(self, match_id: int, folder: str):
        assert isinstance(match_id, int) and match_id >= 0, "Invalid game id!"
        self.initial_match_id = match_id
        self.folder = folder
        
        current_page_num = 1
        desired_page_num = match_id // self.games_per_page + 1
    
        if desired_page_num != current_page_num:
            match_id = self.reach_desired_page(desired_page_num, current_page_num, match_id)
        
        self.parse_game_page(match_id)
        self.driver.quit()
        
    def reach_desired_page(self, desired_page_num: int, current_page_num: int, match_id: int):
        pages_to_skip = desired_page_num - current_page_num 
        
        max_jump_occured = False 
        while pages_to_skip >= self.max_page_jump_distance:
            match_id -= self.max_page_jump_distance * self.games_per_page
            current_page_num += self.max_page_jump_distance
            
            self.page_jump(current_page_num)
            max_jump_occured = True
            pages_to_skip -= self.max_page_jump_distance
    

        if max_jump_occured and pages_to_skip == 2:
            self.page_jump(current_page_num + pages_to_skip + 1)
            self.page_jump(current_page_num + pages_to_skip)
        elif pages_to_skip > 1:
            self.page_jump(current_page_num + pages_to_skip)
    
        match_id -= pages_to_skip * self.games_per_page
        current_page_num += pages_to_skip
        return match_id
            
        
            
            


