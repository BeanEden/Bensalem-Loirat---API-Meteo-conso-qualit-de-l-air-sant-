import pytest

from ..data_collection.getAPIMeteo import change_url

url_test = "https://www.infoclimat.fr/opendata/?version=2&method=get&format=csv&stations[]=07110&stations[]=07130&stations[]=07117&stations[]=STATIC0021&stations[]=000M7&stations[]=STATIC0191&stations[]=000I4&stations[]=000GX&stations[]=000GU&stations[]=000XE&stations[]=STATIC0218&stations[]=000WY&stations[]=STATIC0308&start=2024-11-17&end=2024-11-17&token="
new_start_date = "2000-00-00"
new_end_date = "2000-00-00"


def test_change_url():
    new_urk = change_url(url_test, new_start_date, new_end_date)
    assert new_urk == "https://www.infoclimat.fr/opendata/?version=2&method=get&format=csv&stations[]=07110&stations[]=07130&stations[]=07117&stations[]=STATIC0021&stations[]=000M7&stations[]=STATIC0191&stations[]=000I4&stations[]=000GX&stations[]=000GU&stations[]=000XE&stations[]=STATIC0218&stations[]=000WY&stations[]=STATIC0308&start=2000-00-00&end=2000-00-00&token="
