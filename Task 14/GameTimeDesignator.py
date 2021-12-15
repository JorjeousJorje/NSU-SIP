import cv2 as cv
import os
import numpy as np
import collections

from itertools import zip_longest

from GameTournamentParser import GameTournamentAfterGameImageParser



class GameTimeDesignator:
    
    
    def __init__(self, templates_dir: str) -> None:
        assert os.path.isdir(templates_dir), "Please, transfer directory path!"
        
        self.templates_paths = os.listdir(templates_dir)
        self.templates: list[np.ndarray] = [cv.imread(templates_dir + os.sep + path, 0) for path in self.templates_paths]
        self.parser = GameTournamentAfterGameImageParser()
        
    def get_game_times(self, match_id: int) -> list[tuple[str, str]]:
        temporary_dir = "found_images_from_parsing"
        
        try:
            os.rmdir(temporary_dir)
        except OSError:
            pass
        
        os.mkdir(temporary_dir)
        
        try:
            self.parser.parse_image(match_id=match_id, folder=temporary_dir)
        except RuntimeError as err:
            print(err)
        
        images_paths = os.listdir(temporary_dir)
        
        result_times: list[str] = []
        for image_path in images_paths:
            img_rgb: np.ndarray = cv.imread(temporary_dir + os.sep + image_path)
            img_rgb: np.ndarray = cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB)
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
            
            loc_to_temp = {}
            for i, template in enumerate(self.templates):
                res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
                threshold = 0.93
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    x = pt[0]
                    loc_to_temp[x] = i
                    
            od = collections.OrderedDict(sorted(loc_to_temp.items()))
            numbers = list(od.values())
            minutes = "".join(str(minute_element) for minute_element in numbers[:2])
            seconds = "".join(str(second_element) for second_element in numbers[2:])
            result_times.append(f"{minutes}:{seconds}")
            os.remove(temporary_dir + os.sep + image_path)
        
        os.rmdir(temporary_dir)
            
        for (i, state), time in zip_longest(self.parser.result_states, result_times, fillvalue=None):
            if state:
                print(f"Game {i} lasted {time}")
            else:
                print("Game {i} doesn't have play time!")
        