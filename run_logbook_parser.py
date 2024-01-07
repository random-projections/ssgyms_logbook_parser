from simple_parsing import ArgumentParser
from dataclasses import dataclass
from parsing_utils import extract_tag_names, parse_website, workout_dataframe_from_soup
import os


@dataclass
class LogbookArgs:
    logbook_html_path: str # Path to the complete webpage html
    # file of your SS Gyms Logbook. Save it using "Complete Webpage" option in Chrome
    logbook_csv_output_path: str # Path to write the output
    # csv file of workouts


def main():
    parser = ArgumentParser()
    parser.add_arguments(LogbookArgs, 'options')
    logbook_args = parser.parse_args().options
    file_path = os.path.expanduser(logbook_args.logbook_html_path)
    (training_item_parent, training_item_date_name,
     training_item_row_name) = extract_tag_names(file_path)
    soup = parse_website(file_path)
    workouts_df = workout_dataframe_from_soup(
        soup=soup,
        training_item_parent=training_item_parent,
        training_item_date_name=training_item_date_name,
        training_item_row_name=training_item_row_name)
    workouts_df.to_csv(logbook_args.logbook_csv_output_path, index=False)


if __name__ == "__main__":
    main()