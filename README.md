Zomato Restaurant Data Scraper
This project scrapes restaurant details (name, address, cuisines, ratings, pricing, phone numbers, etc.) from Zomato using Python, Selenium, and Pandas, and saves the data into an Excel file.

1.FEATURES
  a)Restaurant Name
  b)Address
  c)Cuisines
  d)Timing (opening/closing hours)
  e)Phone Number
  f)Price (for two / for one)
  g)Dining Rating
  h)Delivery Rating
2.Works for multiple restaurant URLs (entered interactively).
3.Saves results to Excel file.

Install Python
Download and install Python 3.9+

To Check installation: 
python --version

Install pip python -m ensurepip --upgrade

Create Virtual Environment
python -m venv selenium_env
source selenium_env/bin/activate   
selenium_env\Scripts\activate

Install Dependencies
pip install selenium pandas openpyxl

Browser & Driver Setup
This project uses Firefox with geckodriver.
Install Firefox (if not already installed).
Download geckodriver.
Add geckodriver to your PATH (or specify its path in the script).

To Check installation 
geckodriver --version
firefox --version

How to Run
1.Activate your environment:
a)source selenium_env/bin/activate
2.Run the script
a)python zomato_scraper.py
3.Provide the Excel file name and enter Zomato URLs interactively
a)Enter excel file name: zomato_data
b)Enter zomato url: https://www.zomato.com/chennai/habbat-global-cuisine-sholinganallur/info
c)Enter zomato url: https://www.zomato.com/chennai/macaw-by-stories-sholinganallur
d)Enter zomato url: https://www.zomato.com/chennai/guntur-gongura-egatoor
e)Enter zomato url: quit
4.Data will be saved in zomato_data.xlsx

