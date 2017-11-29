# econjobmarket-applications
Pull application data and files from EconJobMarket API.

1. Get your API credentials at backend.econjobmarket.org
2. Create a folder for your application packages and change to that.
3. Clone this repo: `git clone https://github.com/korenmiklos/econjobmarket-applications.git` and save `get_applications.py` and `settings.py`.
4. You need `requests` and `lxml` as dependencies, so if you don't have them installed, `pip install requests` and `pip install lxml`.
5. Set your credential parameters in `settings.py`
6. Run `python3 get_applications.py`. It will create folders with candidate names (lowercased) and save all attached files and recommendation letters there.