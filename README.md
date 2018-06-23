# WResT : Website Response Time Calculator
___
WResT Calculator is an automation tool made with python to calculate page load/ page render time for websites.
It make use of Python-Selenium to automate the process and uses W3C Navigation APIs to calculate the timings.
The results are saved in a mysql database for futher analysis and visualization.
##### About
* **Sreenath Sivadas** - *Initial work* - [sreesdas](https://github.com/sreesdas)

##### License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Getting Started
***

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

__*Note:*__ *this project is made for windows platform, for linux, checkout this [project](https://github.com/cgoldberg/pageloadtimer)*

### Prerequisites

I assume you have a working python 2.7 environment in your machine with pip installed.
This project needs the following requirements
__Python__
- Python 2.7+ (_haven't tested with 3.6+_)
- System Dependencies
    - Google Chrome Browser
    - chromedriver.exe in $PATH
- Python Dependencies
    - selenium
    - MySQL-python

```
pip install selenium MySQL-python
```
* If MySQL-python gives error while installing, use a precompiled binary from [here](https://sourceforge.net/projects/mysql-python/)

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the Repo

```
git clone https://github.com/sreesdas/website_response_time
```

Edit the config.json file to edit the websites you want to test along with credentials(optional)

```
{
  "version": "0.1",
  "sites": [
    	{ "name": "Facebook",
          "url": "https://facebook.comn",
          "login": ""
        }
    ]
}
```

And run the main.py file

```
cd website_response_time
python main.py
```

## Acknowledgments

* cgoldberg/[pageloadtimer](https://github.com/cgoldberg/pageloadtimer)
* Navigation Timing API [W3C recommendation - Dec 2012]( http://www.w3.org/TR/navigation-timing/)
* Navigation Timing API [Moz://a Webdocs]( https://developer.mozilla.org/en-US/docs/Navigation_timing)
