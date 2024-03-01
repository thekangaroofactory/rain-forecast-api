
import datetime
import sys

import requests


def download_observations(year=None, month=None, station="IDCJDW2124"):
    """
    Download weather observations from Australian BOM website
    Arguments:
        :param year: string to indicate year of observations (ex: '2024')
        :param month: string to indicate month of observations (ex: '02')
        :param station: string to indicate observation station code
    Returns:
        The sum of the two integer arguments
    """

    # get current date
    today = datetime.date.today()

    # check param
    if year is None:
        year = str(today.year)
        print("[INFO] Setting current year as default value:", year)

    # check param
    if month is None:
        month = '%02d' % today.month
        print("[INFO] Setting current month as default value:", month)

    # -- prepare target url
    target_url = "http://www.bom.gov.au/climate/dwo/"
    target_url = target_url + year + month + "/text/"
    target_url = target_url + station + "." + year + month + ".csv"
    print("Ready to download from", target_url)

    # -- define header (to avoid 403 forbidden)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}

    # -- download
    req = requests.get(target_url, headers=headers)
    url_content = req.content
    print("Request content size =", sys.getsizeof(url_content))

    # -- decode & replace carriage return
    url_text = url_content.decode("latin-1")
    url_text = url_text.replace('\r', '')

    # -- write to file
    target_file = "./" + station + "." + year + month + ".csv"
    print("Write output to:", target_file)
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(url_text)
