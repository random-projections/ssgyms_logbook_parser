from bs4 import BeautifulSoup
import pandas as pd
from typing import Tuple, List
import re
import os


def parse_website(filename: os.path) -> BeautifulSoup:
    """
    Parse app.ssgyms.com/logbook user logbook
     website that has been saved using the "Complete Webpage" option in Chrome
    :param filename: path to local html file
    :return: parsed file as a BeautifulSoup object
    """
    with open(filename, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def extract_tag_names(filename: os.path) -> Tuple[str]:
    """
    Extract tag, this is quite specific to how the logbook is written
    :param filename:
    :return: names of the relevant tags
    """
    with open(filename, 'r') as file:
        html_content = file.read()

    training_item_parent = set(re.findall('TrainingItem_TrainingItem__\w{5}', html_content)).pop()
    training_item_date_name = set(re.findall("TrainingItem_Date__\w{5}", html_content)).pop()
    training_item_row_name = set(re.findall("TrainingItem_Row__\w{5}", html_content)).pop()

    return training_item_parent, training_item_date_name, training_item_row_name


def fetch_text_from_tag(div_tag, tag_name):
    div_tags = div_tag.find_all('div', tag_name)
    text_tags = []
    for div_tag in div_tags:
        text_tags.append(div_tag.text)
    return text_tags


def parse_exercise_string(text: str) -> List:
    """
    Parse the exercise string, which looks like this:
    example
    "Squat3X5@225lbs" -> ["Squat3X5", 3, 5, 225]
    :param text:
    :return:
    """
    match = re.match(r"(\D+)(\d+)x(\d+)@(\d+)", text)

    if match:
        exercise = match.group(1)
        sets = match.group(2)
        reps = match.group(3)
        weight = match.group(4)
    else:
        print("No match found")
    return [exercise, int(sets), int(reps), int(weight)]


def parse_date(date_str: str) -> str:
    return ' '.join(date_str.split()[1:])


def workout_dataframe_from_soup(
        soup: BeautifulSoup,
        training_item_parent: str,
        training_item_date_name: str,
        training_item_row_name: str) -> pd.DataFrame:
    """
    Convert parsed HTML soup into a Pandas DataFrame
    :param soup: parsed html file of SSGyms logbook
    :param training_item_parent: name of item parent, looks like TrainingItem_TrainingItem__...
    :param training_item_date_name: name of item date, looks like TrainingItem_Date__ ...
    :param training_item_row_name: name of tbe row with workout and values, looks like TrainingItem_Row__...
    :return:
    """
    workouts_df = pd.DataFrame(columns=['date', 'iso_date', 'exercise_name', 'sets', 'reps', 'weight_lbs'])
    indx = 0
    for div in soup.find_all('div', class_=training_item_parent):
        date_str = fetch_text_from_tag(div, training_item_date_name)[0]
        parsed_date = parse_date(date_str)
        iso_date = pd.to_datetime(parsed_date).date().isoformat()
        exercises = fetch_text_from_tag(div, training_item_row_name)
        for exercise in exercises:
            workouts_df.loc[indx, :] = [parsed_date, iso_date] + parse_exercise_string(exercise)
            indx += 1
    return workouts_df
