 Web Scraping and Data Processing Script

This Python script performs web scraping to gather data from various web pages, processes the data, and stores it in MongoDB. It also provides a Streamlit-based frontend to display the scraped data. The main components of the script include functions for scraping headings, descriptions, tables, and specific data structures from web pages. Additionally, it includes functionality for concurrent data scraping and storing the data in MongoDB. Detailed logging is implemented to keep track of the script's execution.

Usage

To run the script, ensure all required libraries are installed and execute the script. The Streamlit application will open in a web browser, allowing users to select and view scraped data.

Uncomment the appropriate function calls in the `main` function to run specific parts of the script independently for testing or development purposes.

Logging

The script logs its activities to a file named `scraping.log` with timestamps, log levels, and messages to help with debugging and tracking execution flow.

MongoDB

Ensure MongoDB is running locally on the default port (27017) before executing the script, as it stores the scraped data in MongoDB collections. Adjust the MongoDB connection string if necessary.

Streamlit

Run the script using Streamlit to access the web-based interface. Use the following command in Command Prompt to start the Streamlit app:


“streamlit run scraping_assignment.py”







Dependencies

The script requires the following Python libraries:
- `requests`: For making HTTP requests to web pages.
- `BeautifulSoup`: For parsing HTML content.
- `pandas`: For handling and manipulating tabular data.
- `numpy`: For numerical operations.
- `pymongo`: For interacting with MongoDB.
- `concurrent.futures`: For concurrent execution of tasks.
- `json`: For handling JSON data.
- `logging`: For logging messages and errors.
- `streamlit`: For creating a web-based user interface.
- `streamlit_option_menu`: For adding a sidebar menu in Streamlit.

 Functions

`beautify_strs(strings)`
Cleans a list of strings by removing newline characters and extra spaces.

`beautify_str(string)`
Cleans a single string by removing newline characters and extra spaces. Returns "N/A" if the input is `None`.

`scrap_heading(url)`
Scrapes the heading (`<h1>` tag) from a given URL.

`scrap_description(url)`
Scrapes the description (`<p>` tag with class `lead`) from a given URL.

`scrap_last(url)`
Scrapes structured content including headings (`<h3>` tags) and descriptions (`<p>` tags) from a given URL.


`scrap_tables(url)`
Scrapes table data from a local HTML file, cleans the data, and returns it as a pandas DataFrame.

`hockeyscraper(url)`
Scrapes hockey data from a given URL and returns it as a pandas DataFrame.

`movies_data(year)`
Scrapes movie data for a given year, stores it in MongoDB, and saves it as a JSON file.

`scrape_hockey(num)`
Scrapes hockey data for a given page number, stores it in MongoDB, and saves it as a JSON file.

`all_movies()`
Scrapes movie data for all years from 2010 to 2015 concurrently.

 `all_hockey()`
Scrapes hockey data for all pages from 1 to 24 concurrently.

 `front_end_selector1()`
Provides a Streamlit interface to select and display movie data for a specific year.

 `front_end_selector2()`
Provides a Streamlit interface to select and display hockey data for a specific page.

 `front_end_final()`
Displays advanced page content using Streamlit.

Main Function

`main()`
Sets up the Streamlit sidebar menu and calls the appropriate frontend function based on user selection. Logs the start and end of the script execution.














Tasks Achieved

Parallel Scraping

Parallel scraping is achieved using the `concurrent.futures` library. This allows multiple web pages to be scraped simultaneously, significantly reducing the total time required. The `ThreadPoolExecutor` is utilized to manage a pool of threads, each handling a separate web scraping task. For example, in the `all_movies()` function, movie data for different years is scraped concurrently by mapping the `movies_data` function across a range of years. Similarly, in the `all_hockey()` function, hockey data is scraped concurrently for multiple pages.

Frontend Navigation and Tabs

The frontend interface is built using Streamlit. The `streamlit_option_menu` library is used to create a sidebar menu with options for different types of data: "Movies Data", "Hockey Data", and "Pages Advanced". Depending on the user's selection, the corresponding frontend function (`front_end_selector1`, `front_end_selector2`, or `front_end_final`) is called to display the appropriate data. This menu-driven approach provides a user-friendly interface for navigating between different datasets and visualizations.

Automatic Conversion to MongoDB

The script automatically converts scraped table data into MongoDB collections. For example, in the `movies_data` and `scrape_hockey` functions, after scraping the data and converting it into a pandas DataFrame, the data is saved as a JSON file. This JSON file is then read and inserted into MongoDB using the `pymongo` library. Each dataset is stored in a dedicated MongoDB collection, with the collection name dynamically generated based on the year or page number. This ensures that all scraped tables are systematically stored in MongoDB for further analysis and retrieval.

Using Git to Manage and Push Code to GitHub
To manage the code effectively and collaborate with others, Git is used to version control the script, track changes, and push the code to GitHub. Additionally, a .gitignore file is used to exclude unnecessary files from being tracked by Git.
