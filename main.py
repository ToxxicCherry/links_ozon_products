from requests_html import HTMLSession
from bs4 import BeautifulSoup
from typing import List
import json

START_URL = 'https://www.ozon.ru/seller/21vek-198419/krasota-i-zdorove-6500/?brand=135704519%2C18556218&miniapp=seller_198419&opened=brand'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'cookie': '__Secure-ETC=beeba88ecbf753fac48ff319f3c04f60; __Secure-user-id=0; __Secure-ab-group=76; __Secure-ext_xcid=03a9c9d19084918223840b32c6b8d1e9; abt_data=7.WnNUo1jBQU1kJmlq1_c3sA9g2uedWZmFx_98mUT_Fe5Y74gjWB_BBpt6Siz7FCPQlPKE169M6IeGO9H2hRK8hzehlJjHH0roGE_aIg7kIdzzT_9jwWcqSCvB5Za4-5W91F02wvApteuQhZB6-Dkoqdzkct_EEDKrNVsBMtXdZePj-CRZuc9FJ334P5u7DIBSeKwoy-sU8G8GQlW_ReZLr0ggr1-pFXc4YNumNZ2fxSHkM1Yu8tlE-lP7DZS01DqKMwEXn-fXqZkeMRq3rMgXdxDTcTy4nebGt6dUxIAlPcQP-OgMi_DAjyJKxsPYokZ2MM5NOoHhvUHerLbHBra2h5FKu54jo76j7GPCTfwSL3l9PLrlGD4Oe0jznSlMUKqWQhUvd-sT651KUzyMBTq2RBmNeTSNhFNNT8KUKAdLA8O1SB0A1AzXhg6GYCIt; is_cookies_accepted=1; __Secure-access-token=6.0.7Dc_SFzzQguPbpnurWJdFw.76.ARCi5YC6fIFlXaaDiN84VO3zqPD-msqpXwa7GKflLy9SYbrBZTBR2sOfxqcr_ffP3A..20241009190417.0ZynolNqMYhKzyNq8N9x0F61VreCK6xJrPAvA4xgZbU.1fa14c9da30af1bd9; __Secure-refresh-token=6.0.7Dc_SFzzQguPbpnurWJdFw.76.ARCi5YC6fIFlXaaDiN84VO3zqPD-msqpXwa7GKflLy9SYbrBZTBR2sOfxqcr_ffP3A..20241009190417.XaURXMmsbrsmDmuK94eXWiUdhVDQTT3nIrPQ6p37lU4.1421d660f9c21a779; xcid=0637edeca1336b2fc858c85ba9bc5e1e; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxOTA3MzMzOTM0LC0xLDE0MTIwMTI1OTAsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNamt1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsMTkwOTYxOTM4OCwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMyw0; guest=true',
}
PARAMS = {
    'layout_container': 'categorySearchMegapagination',
    'layout_page_index': 2,
    'page': 2,
}

session = HTMLSession()
session.headers.update(headers)


# /seller/21vek-198419/krasota-i-zdorove-6500/?brand=135704519%2C18556218&layout_container=categorySearchMegapagination&layout_page_index=3&miniapp=seller_198419&opened=brand&page=3


def get_products(s: HTMLSession, url: str, page: int = None) -> List[str] | None:
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    if not page:
        div_id = 'state-searchResultsV2-3547917-default-1'
    else:
        div_id = f'state-searchResultsV2-193750-categorySearchMegapagination-{page}'

    data = soup.find('div', id=div_id)

    try:
        serialized_data = json.loads(data.get('data-state'))
    except AttributeError:
        return None

    return ['https://ozon.ru'+item.get('action').get('link') for item in serialized_data.get('items')]


def get_links(s: HTMLSession) -> List[str]:
    links = []
    links += get_products(s, START_URL)
    s.params = PARAMS

    while True:
        links_to_add = get_products(s, START_URL, PARAMS['page'])

        if not links_to_add:
            break

        links += links_to_add
        PARAMS['page'] += 1
        PARAMS['layout_page_index'] += 1
        s.params = PARAMS

    return links


def ozon(s: HTMLSession):
    links = get_links(s)


if __name__ == '__main__':
    ozon(session)