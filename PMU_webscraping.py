# Program designed to scrape data from horse races on the website
# turf-fr.com
# Last edited 06/19/2020

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Transpose a 2D list


def transpose(my_list):
    return list(map(list, zip(*my_list)))


# Get a list of the races categories


def get_races_categories(my_soup):
    return [
        x['src'].split('/')[-1][:-4]
        for x in my_soup
        .find_all('img', id='icon_discipline_course')[1:]]


# Get a list of the races names


def get_races_names(my_soup):
    return [
        race.findChild('strong').contents[0]
        if race.findChild('strong').contents
        else '-'
        for race in my_soup.find_all('tr', class_='ligne_courses')]


# Get a list of the times (HH:MM) when the races run


def get_races_times(my_soup):
    return [
        race.contents[0]
        for race in my_soup.find_all('td', class_='center')[:-1]]


# Get lists of the races subcategories, prizes, lengths in meters
# and number of horses running.


def get_races_description(my_soup):
    return [
        [race.findChild('data').contents[0].split(' - ')]
        for race in my_soup
        .find_all('p', id='presentation_course')[1:]]


# Get list of horses ID numbers


def get_horses_ID(race_info_html):
    return [
        x.contents[0]
        for x in race_info_html.find_all('td', id='numero_cheval')[1:]]


# Get list of horses names


def get_horses_names(race_info_html):
    return [
        x.find('strong').contents[0]
        for x in race_info_html.find_all('td', id='nom_cheval')[1:]]


# Get list of distances covered by the horses


def get_horses_distances(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html
        .find_all('td', id='distance_course')[1:]]


# Get list of horses shoeing statuses


def get_horses_shoeing_statuses(race_info_html):
    return [
        'ND'
        if len(x['src']) == 0
        else x['src'].split('/')[-1][:-4]
        for x in race_info_html.find_all('img', alt='Déferrés')[1:]]


# Get list of jockey's weights


def get_jockeys_weights(race_info_html):
    return [
        (x.contents or ['n/a'])[0]
        for x in race_info_html.find_all('td', id='poid_cheval')[1:]]


# Get list of horses starting spot


def get_horses_barrier(race_info_html):
    return [
        (x.contents or ['n/a'])[0]
        for x in race_info_html.find_all('td', id='corde_cheval')[1:]]


# Get list of horses countries


def get_horses_countries(race_info_html):
    return [
        (x.contents or ['n/a'])[0]
        for x in race_info_html
        .find_all('sup', class_='originePays')[1:]]


# Get list of horses blinker statuses


def get_horses_blinkers_statuses(race_info_html):
    return [
        x.find('img')['src'].split('/')[-1][:-4]
        if x.find('img')
        else 'NB'
        for x in race_info_html.find_all('td', id='oeil_partant')[1:]]


# Get list of horses sex


def get_horses_sexes(race_info_html):
    return [
        x.contents[0][0]
        if len(x.contents[0]) > 1
        else 'n/a'
        for x in race_info_html
        .find_all('td', id='sexe_age_partant')[1:]]


# Get list of horses age


def get_horses_ages(race_info_html):
    return [
        x.contents[0][1]
        if len(x.contents[0]) > 1
        else 'n/a'
        for x in race_info_html
        .find_all('td', id='sexe_age_partant')[1:]]


# Get list of horses jockeys


def get_horses_jockeys(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html.find_all('td', id='jockey')[1:]]


# Get list of horses trainers


def get_horses_trainers(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html.find_all('td', id='entraineur')[1:]]


# Get list of horses average km timing


def get_horses_average_km_timings(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html
        .find_all('td', id='record_partant')[1:]]


# Get list of horses gains


def get_horses_gains(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html.find_all('td', id='gain_partant')[1:]]


# Get list of horses past performance


def get_horses_past_performances(race_info_html):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_info_html
        .find_all('td', id='musique_partant')[1:]]


# Get list of horses running / non-running status


def get_horses_running_statuses(race_info_html):
    return [
        'NP'
        if x.find('np', class_='non_partants')
        else 'P'
        for x in race_info_html.find_all('td', id='nom_cheval')[1:]]


# Get list of last minute odds placed on the horses


def get_horses_odds(race_html, df_size):
    return [
        x.contents[0]
        if len(x.contents) > 0
        else 'n/a'
        for x in race_html
        .find_all('data', id='cote_actuelle')[1:df_size+1]]


# Get list of the winning horses


def get_winners(results, race_participants_number):
    return [
        results.index(i)+1
        if i in results
        else 0
        for i in range(1, 1+race_participants_number)]


# Function to take in a valid race URL and output two dataframes, one
# with the races and the other with every horse attendance at a race


def retrieve_race(website_url):
    page = requests.get(website_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if len(soup.find_all(('td', id='course_numero')) <= 1:
        return None
    races_df = pd.DataFrame(transpose([
        get_races_categories(soup),
        get_races_names(soup),
        get_races_times(soup)]
        + transpose(transpose(get_races_description(soup))[0])),
        columns=[
            'race_category',
            'race_name',
            'race_time',
            'race_subcategory',
            'race_prize',
            'race_length',
            'race_horse_number'])
    races_df['race_date'] = [
        soup.find('input', type='hidden', id='dateReunion')['value']
        ]*len(races_df)
    print("Scraping "
          + soup
          .find('input', type='hidden', id='dateReunion')['value'])
    horses_df = retrieve_horses(soup, 0)
    for x in races_df.columns:
        horses_df[x] = races_df.iloc[0][x]
    for i in range(1, len(races_df)):
        horses_df_temp = retrieve_horses(soup, i)
        for x in races_df.columns:
            horses_df_temp[x] = races_df.iloc[i][x]
        horses_df = horses_df.append(horses_df_temp)
    return horses_df


# Function to take in a valid race soup and race number
# and extract information on the horses running:


def retrieve_horses(race_soup, race_number):
    race_info_html = race_soup.find(
        'aside', id='detail_course_partants_'+str(race_number))
    race_horses_html = race_info_html.find_all(
        'tr', class_='ligne_partant OrrangeHoverColor')
    race_result_text = race_info_html.find(
        'div', id='decompte_depart_course').find('strong').contents
    race_participants_number = len(
        set(get_horses_ID(race_info_html)))
    race_result = [0]*race_participants_number
    if len(race_result_text) > 0:
        race_result = [
            int(x.split(' / ')[0])
            if ' / ' in x
            else int(x)
            for x in race_info_html
            .find('div', id='decompte_depart_course')
            .find('strong').contents[0].split(' - ')]
    horses_df = pd.DataFrame(
        transpose([
            get_horses_ID(race_info_html),
            get_horses_names(race_info_html),
            get_horses_distances(race_info_html),
            get_horses_shoeing_statuses(race_info_html),
            get_jockeys_weights(race_info_html),
            get_horses_barrier(race_info_html),
            get_horses_countries(race_info_html),
            get_horses_blinkers_statuses(race_info_html),
            get_horses_sexes(race_info_html),
            get_horses_ages(race_info_html),
            get_horses_jockeys(race_info_html),
            get_horses_trainers(race_info_html),
            get_horses_average_km_timings(race_info_html),
            get_horses_gains(race_info_html),
            get_horses_past_performances(race_info_html),
            get_horses_running_statuses(race_info_html)]),
        columns=[
            'horse_ID',
            'horse_name',
            'running_distance',
            'unshoed',
            'jockeys_weight',
            'barrier',
            'country',
            'blinkers',
            'sex',
            'age',
            'jockey',
            'trainer',
            'average_km_timing',
            'wins',
            'former_performance',
            'running'])
    # This category added afterwards as we need to know first how many
    # entries are in the dataframe. Note this is different from the
    # number of running horses, as some tables on the website have
    # double entries for a given horse.
    horses_df['odds'] = get_horses_odds(race_info_html, len(horses_df))
    if len(horses_df) != race_participants_number:
        horses_df.drop_duplicates('horse_ID', inplace=True)
    horses_df['finish_position'] = get_winners(race_result,
                                               race_participants_number)
    return horses_df


years = [x for x in range(2004, 2020)]
months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
          'juillet', 'aout', 'septembre', 'octobre', 'novembre',
          'decembre']

for i in years:
    final_race_df = pd.DataFrame(columns=[
        'horse_ID',
        'horse_name',
        'running_distance',
        'unshoed',
        'jockeys_weight',
        'barrier',
        'country',
        'blinkers',
        'sex',
        'age',
        'jockey',
        'trainer',
        'average_km_timing',
        'wins',
        'former_performance',
        'odds',
        'running',
        'finish_position',
        'race_category',
        'race_name',
        'race_time',
        'race_subcategory',
        'race_prize',
        'race_length',
        'race_horse_number',
        'race_date'])
    final_race_df.to_csv(
        os.path.abspath(os.getcwd())+'\\race_df_'+str(i)+'.csv',
        encoding='utf-8-sig')
    for j in months[0:6]:
        print('Collecting races from '+j+' '+str(i))
        final_race_df = pd.DataFrame(columns=[
            'horse_ID',
            'horse_name',
            'running_distance',
            'unshoed',
            'jockeys_weight',
            'barrier',
            'country',
            'blinkers',
            'sex',
            'age',
            'jockey',
            'trainer',
            'average_km_timing',
            'wins',
            'former_performance',
            'odds',
            'running',
            'finish_position',
            'race_category',
            'race_name',
            'race_time',
            'race_subcategory',
            'race_prize',
            'race_length',
            'race_horse_number',
            'race_date'])
        month_page_url = 'https://www.turf-fr.com/archives/' \
                         'courses-pmu/' + str(i) + '/' + j
        month_page_html = requests.get(month_page_url)
        month_soup = BeautifulSoup(month_page_html.content,
                                   'html.parser')
        link_list = [
            x['href']
            for x
            in month_soup.find('tbody')
            .find_all('a', class_='button1', id='lien')]
        for k in link_list:
            final_race_df = final_race_df.append(retrieve_race(k))
        final_race_df.to_csv(
            os.path.abspath(os.getcwd())+'\\race_df_'+str(i)+'_1.csv',
            mode='a', header=False, encoding='utf-8-sig')

    for j in months[6:12]:
        print('Collecting races from '+j+' '+str(i))
        final_race_df = pd.DataFrame(columns=[
            'horse_ID',
            'horse_name',
            'running_distance',
            'unshoed',
            'jockeys_weight',
            'barrier',
            'country',
            'blinkers',
            'sex',
            'age',
            'jockey',
            'trainer',
            'average_km_timing',
            'wins',
            'former_performance',
            'odds',
            'running',
            'finish_position',
            'race_category',
            'race_name',
            'race_time',
            'race_subcategory',
            'race_prize',
            'race_length',
            'race_horse_number',
            'race_date'])
        month_page_url = 'https://www.turf-fr.com/archives/' \
                         'courses-pmu/' + str(i) + '/' + j
        month_page_html = requests.get(month_page_url)
        month_soup = BeautifulSoup(month_page_html.content, 'html.parser')
        link_list = [
            x['href']
            for x
            in month_soup.find('tbody')
            .find_all('a', class_='button1', id='lien')]
        for k in link_list:
            final_race_df = final_race_df.append(retrieve_race(k))
        final_race_df.to_csv(
            os.path.abspath(os.getcwd())+'\\race_df_'+str(i)+'_2.csv',
            mode='a', header=False, encoding='utf-8-sig')
