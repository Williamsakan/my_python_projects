# my_python_projects
In the `jiji_cleaned_car.py` script, you'll notice the module has several functions that reads the `.csv` file into a DataFrame (i.e the `read_data` function) and also creates new columns or features (like `cleaned_price_column`, `year_column`, `colour_column`, `brand_column`, `model_column` etc)
You'd have to call the `read_data` function first to be able to access/view the csv file, then call the output of  `read_data` as a parameter to other functions (preferably `cleaned_price_column`). subsequently, you'd continue passing the output of the previous function to a new function in the script.
You should ensure to call the `brand_column` first before calling the `model_column`, the output from the `brand_column` should be used as parameter for the `model_column` because I built the extraction of the car Model on the brand brand model. Implying that the *model_column* is dependent on the *brand_column*.
You will after import the functions in module this way on your jupyter notebook Google Colab or VS Code in the format below:
1. df = read_data()
2. df = cleaned_price_column(df)
3. df = colour_column(df)
4. df = year_column(df)
5. df = brand_column(df)
6. df = model_column(df)
   
Note that from step 2 to step 4 inclusive, you can interchange them since they are not dependent on each other. You will have to read the data first, then you'd have to call the *brand_column* function before calling the *model_column* function
Finally, you can decide to output only the columns **Brand**, **Model**, **Colour**, **Year**, **Type**, **Price** that is
|   | **Brand** | **Model** | **Colour** | **Year** | **Type**     | **Price** |
|---|-----------|-----------|------------|----------|--------------|-----------|
| 0 | Lexus     | IS        | 2014       | White    | Foreign Used | 23000000  |
| 1 | Lexus     | RX        | 2013       | white    |   Local Used | 21500000  |
| 2 | Toyota    | Camry     | 2010       | Black    |   Local Used |  8500000  |
| 3 | Toyota    | Tundra    | 2014       | Red      | Foreign Used | 38500000  |
| 4 | Lexus     | RX        | 2009       | Red      | Foreign Used | 13500000  |

- [x] Finish data cleaning
- [ ] Write analysis script
