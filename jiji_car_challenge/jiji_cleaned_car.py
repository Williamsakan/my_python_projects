"""
jiji_cleaned_car_dataset.py
This Module handles the cleaning task for the jiji car challenge.
It reads in the excel file for the jiji car challenge, it also drops some column that has no data in the sheet. 

Functions:
    - cleaned_price_column: cleans a price column removing the non digit symbol and comverting it to integer
    - colour_column: creating a colour column from the Title column
    - year_column: creating a year column from the Title column
    - extract_brand: using regex to capture the brand from the Title column
    - brand_column: creating and applying the extract_brand column from the Title column
    - extract_model: using regex to capture the model from the Title column
    - model_column: creating and applying the extract_model the Title column
"""
import numpy as np
import pandas as pd
import re

# We will first read in the data from the excel file, then remove columns that are empty
def read_data():
    df = pd.read_csv("jiji_cars_challenge.csv")
    
    return df


# This function cleans the price column
def cleaned_price_column(df):
    """
    This function cleans a the price column of the DataFrame (df) by removing every non-digit in the cell and 
    converting it to an integer column
    Args:
        df (pandas.DataFrame): A Jiji_cars_Challenge DataFrame containing the the Price column to be cleaned

    Returns:
        pandas.DataFrame: A DataFrame containing the cleaned Price column
    """
    df['Price'] = df['Price'].replace(r'[^\d.]', '', regex=True).astype(int)
    return df


def colour_column(df):
    """
    this function creates a new column called Colour from the DataFrame (df) by using Regular expression on the
    Title column of the DataFrame. You will notice the the colour Burgundy is represented twice as Burgandy and 
    Burgundy, white is also represented twice, so will have to use the replace function to ensure it is represented
    once. We will check if one of the colour extracted is ommitted in the Title column but included in the Description
    column of the same sample (At index 1504, we will notice this). finally we will represent every missing 
    column with "Not Specified"

    Args:
        df (pandas.DataFrame): A Jiji_cars_Challenge DataFrame containing the Title column where the colour will
        be extracted from

    Returns:
        pandas.DataFrame: A DataFrame containing the new column named Colour
    """
    df['Colour'] = df['Title'].str.extract(r'(\b[A-Za-z]+)$') # the expression to filter from the Title column
    df['Colour'] = df['Colour'].replace(['white', 'Burgandy'],
                                        ['White', 'Burgundy']) # representing colour White and Burgundy once 
    # Checking to see if any colour in the Colour column will be seen in the description column of the missing
    # colour column
    a = list(df['Colour'].unique())
    b = df[df['Colour'].isna()]
    c = list(b.index)
    for i in c:
        for j in a:
            if str(j) in b.loc[i, 'Description']:
                df.loc[i, 'Colour'] = str(j) # It will only capture the colour Red from the Description column
            else:
                pass

    df['Colour'] = df['Colour'].fillna('Not Specified')
    return df


def year_column(df):
    """
    This function creates a "Year" Column from the "Title" Column. It uses regex to extract exactly 4 digits from
    the "Title" column where the year starts from 19 or 20. Because when you look deep into index '489' and '454',
    you'd notice 4 digit numbers which represents the Model of the car.

    Args:
        read_data() (pandas.DataFrame): A Jiji_cars_Challenge DataFrame from the read_data() function containing 
        the "Title" column where the Year will be extracted from

    Retuns:
        pandas.DataFrame: A DataFrame containing the new column "Year"
    """
    df['Year'] = df['Title'].str.extract(r'\b(19\d{2}|20\d{2})\b') 
    return df


def extract_brand(title):
    """
    this function extracts the brand from the "Title" Column. It first replaces the word "New" with empty string
    in the cells in the Title column. For brands with multi_word, we will capture it as a single brand name. In Index
    "1133" having Mini and "2646" having Car, you'll notice that the brand is not represented well in the Title column
    but it is well represented in the Description column, so we will change it
    """
    title = title.replace('New ', '', 1).strip()
    multi_word_brands = [
        'Land Rover', 'Mercedes-Benz', 'Alfa Romeo', 'Rolls Royce',
        'Aston Martin', 'Mini Cooper', 'Maserati Levante'
    ]
    # Define brand replacements (Mini → Mini Cooper, Car → Innoson)
    brand_replacements = {
        'Mini': 'Mini Cooper',
        'Car': 'Innoson'
    }

    # Check for known multi-word brands first
    for brand in multi_word_brands:
        pattern = rf'\b{re.escape(brand)}\b'
        if re.search(pattern, title, flags=re.IGNORECASE):
            return brand

    # Otherwise, take only the *first capitalized token* (the brand)
    m = re.match(r'^([A-Z][a-zA-Z]+(?:-[A-Z][a-zA-Z]+)?)', title)
    brand = m.group(1) if m else None
    
    # Apply replacement mapping if needed
    if brand in brand_replacements:
        brand = brand_replacements[brand]
    return brand

def brand_column(df):
    """
    this function creates a Brand Column by applying the extract_brand function.
    Args:
        read_data(): A Jiji_cars_Challenge DataFrame containing the "Title" column where the Brand will be 
        extracted from

    Return:
        pandas.DataFrame (df): A DataFrame containing the new column "Brand"
    """
    df['Brand'] = df['Title'].apply(extract_brand)
    return df





def extract_model(row):
    """
    this function extracts the Model from the "Title" Column. For brands with multi_word, we will capture it as a single Model name. 
    For index 454 we will notice that the Title has 1820 as it's car model, so we need to impute this manually. for index 1133 we
    will notice that the Title column as 'Countryman' as it's car model, so we need to impute this manually. Finally we would fill
    the empty Model cells with 'Not Specified
    """
    pattern_template = (
        r'\b' + r'{}' + r'\s+'
        r'([A-Za-z0-9][A-Za-z0-9\-]*(?:\s+[A-Za-z0-9][A-Za-z0-9\-]*)*?)'
    )
    
    multi_word_models = ['Land Cruiser', 'Range Rover']
    brand = str(row['Brand'])
    title = str(row['Title'])

    # check for multi_words model first
    for model in multi_word_models:
        pattern = rf'\b{re.escape(model)}\b'
        if re.search(pattern, title, flags=re.IGNORECASE):
            return model
            
    pattern = pattern_template.format(re.escape(brand))
    match = re.search(pattern, title, flags=re.IGNORECASE)
    
    if match:
        model = match.group(1).strip()
        # extra safety: exclude pure 4-digit years like "2014"
        if re.fullmatch(r'\d{4}', model):
            return None
        return model
    else:
        # fallback: first token after brand
        fallback = rf'\b{re.escape(brand)}\s+([A-Za-z0-9\-]+)'
        match2 = re.search(fallback, title, flags=re.IGNORECASE)
        if match2:
            model = match2.group(1).strip()
            if re.fullmatch(r'\d{4}', model):
                return None
            return model
        return None


def model_column(df):
    """
    this function creates a Model Column by applying the extract_model function.
    Args:
        read_data(): A Jiji_cars_Challenge DataFrame containing the "Title" column where the Model will be 
        extracted from

    Return:
        pandas.DataFrame (df): A DataFrame containing the new column "Model"
    """
    df['Model'] = df.apply(extract_model, axis=1)
    df.loc[454, 'Model'] = '1820'
    df.loc[1133, 'Model'] = 'Countryman'
    df['Model'] = df['Model'].fillna('Not Specified')
    return df
