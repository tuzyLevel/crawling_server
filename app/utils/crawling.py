import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import aiohttp
from bs4 import BeautifulSoup
import json
import re
from app.db.database import get_db
from app.db.crawled_data import crud


def get_random_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
    }

    return headers


# self.url = 'https://www.coupang.com/np/categories/497135?listSize=120&channel=user'
class AsyncCrawler:
    url: str
    headers: dict
    current_page: int

    def __init__(self, domain: str, path: str, param: str):
        self.current_page = 1
        self.domain = domain
        self.path = path
        self.param = param
        self.headers = get_random_headers()

    async def run(self):
        async with aiohttp.ClientSession() as http_session:
            while True:
                url = f"https://{self.domain}{self.path}?{
                    self.param}&page={self.current_page}"
                async with http_session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        baby_product_list = soup.select_one(
                            'ul.baby-product-list')
                        if baby_product_list is None:
                            print("Nothing")
                            break

                        baby_product_list = baby_product_list.select(
                            'li.baby-product')

                        if len(baby_product_list) == 0:
                            break

                        for baby_product in baby_product_list:
                            baby_product_a_tag = baby_product.select_one(
                                'li.baby-product > a.baby-product-link')

                            # product url
                            baby_product_url = baby_product_a_tag.get(
                                "href").strip() or ""
                            print(baby_product_url)
                            [baby_product_path, baby_product_params] = baby_product_url.split(
                                "?") if "?" in baby_product_url else [baby_product_url, ""]

                            # img thumbnail url
                            baby_product_img_tag = baby_product_a_tag.select_one(
                                'img')
                            img_thumbnail_url = baby_product_img_tag.get(
                                "src").lstrip('//').strip()
                            print(img_thumbnail_url)

                            # product_name
                            baby_product_div_name_tag = baby_product_a_tag.select_one(
                                "div.name")
                            baby_product_name = baby_product_div_name_tag.text.strip(
                            ) if baby_product_div_name_tag else ""
                            print(baby_product_name)

                            # discount rate
                            discount_rate = float(baby_product_a_tag.select_one(
                                "span.discount-percentage").text.lstrip().rstrip('%')) if baby_product_a_tag.select_one("span.discount-percentage") else 0
                            print(discount_rate)

                            # origin price
                            origin_price = int(baby_product_a_tag.select_one(
                                "del.base-price").text.strip().replace(',', '')) if baby_product_a_tag.select_one(
                                "del.base-price")else 0
                            print(origin_price)

                            # discounted price
                            discounted_price = int(baby_product_a_tag.select_one(
                                "strong.price-value").text.strip().replace(',', '')) if baby_product_a_tag.select_one(
                                "strong.price-value") else 0
                            print(discounted_price)

                            data = dict()
                            data.update(
                                {"domain": self.domain,
                                 "path": baby_product_path,
                                 "params": baby_product_params,
                                 "title": baby_product_name,
                                 "thumbnail_url": img_thumbnail_url,
                                 "origin_price": origin_price,
                                 "discounted_price": discounted_price,
                                 "discount_rate": discount_rate
                                 })

                            async with get_db() as session:
                                print(await crud.insert_crawled_data(db=session, data=data))

                    self.current_page += 1
                    print("3초 휴식")
                    await asyncio.sleep(3)


async def crawl_job():
    """
        크롤링 작업을 수행하는 함수입니다.
        DB에서 크롤링 할 대상 도메인을 가져옵니다.
    """

    crawler = AsyncCrawler(
        "www.coupang.com", "/np/categories/497135", "listSize=120&channel=user")
    await crawler.run()


async def crawl_11st():
    """
        크롤링 작업을 수행하는 함수입니다.
        DB에서 크롤링 할 대상 도메인을 가져옵니다.
    """
    async with aiohttp.ClientSession() as http_session:
        # while True:
        # url = f"https://{self.domain}{self.path}?{
        #     self.param}&page={self.current_page}"
        url = ('https://www.11st.co.kr/category/DisplayCategory.tmall?method=getSearchFilterAjax'
               '&filterSearch=Y&pageLoadType=ajax&selectedFilterYn=Y&version=1.2&prdImgQuality='
               '&prdImgScale=&sellerNos=&dispCtgrType=&pageNo=1&benefits=&brandCd=&brandNm='
               '&attributes=&verticalType=ALL&fromPrice=&toPrice=&reSearchYN=N&method='
               'getDisplayCategory2Depth&dispCtgrLevel=2&dispCtgrNo=1002945&lCtgrNo=1001439'
               '&mCtgrNo=1002945&sCtgrNo=0&dCtgrNo=0&isAddDispCtgr=false&attrYearNavi='
               '&sortCd=NPC&pageSize=40&viewType=L&totalCount=7474&pageNum=40&researchFlag=false'
               '&kwd=&excptKwd=&minPrice=&maxPrice=&stPrice=&kwd2=&prevKwd2=&kwdExcept='
               '&clearAll=&kwdInCondition=&exceptKwdInCondition=&myPrdViewYN=Y&previousKwd='
               '&previousExcptKwd=&isPremiumItem=&xzone=&partnerSellerNos=&partnerFilterYN='
               '&dealPrdYN=N&brdParam=&catalogYN=N&ajaxYn=Y&engineRequestUrl=')
        async with http_session.get(url, headers=get_random_headers()) as response:
            print(response.status)
            if response.status == 200:
                html = await response.text()
                json_data = json.loads(html)
                for (key, value) in json_data.items():
                    if key == 'template':
                        soup = BeautifulSoup(value, 'html.parser')
                        total_listitems = soup.select('div.total_listitem')
                        for total_listitem in total_listitems:
                            # item link
                            a_tag = total_listitem.select_one(
                                'div.photo_wrap>a')
                            item_link = a_tag.get('href') if a_tag else ""
                            print(item_link)

                            # thumbnnail url
                            img_tag = a_tag.select_one('img')
                            thumbnail_url = img_tag.get(
                                'src') if img_tag else ""
                            print(thumbnail_url)

                            # title
                            list_info_div_tag = total_listitem.select_one(
                                'div.list_info')

                            if list_info_div_tag is None:
                                continue

                            info_a_tag = list_info_div_tag.select_one(
                                'p.info_tit>a[data-log-actionid-label="product"]')

                            # url
                            data_url = info_a_tag.get('href')
                            print(data_url)

                            # title
                            title = info_a_tag.text.strip() or ""
                            print(title)

                            list_price = total_listitem.select_one(
                                'div.list_price')
                            # origin_price
                            origin_price_tag = list_price.select_one(
                                'div.price_box>span.price_sale>s.normal_price')
                            origin_price = int(origin_price_tag.text.replace(',', '').rstrip(
                                '원').lstrip()) if origin_price_tag is not None else 0
                            print(f'{origin_price}원')

                            # sale_price
                            sale_price_tag = list_price.select_one(
                                'div.price_box>span.price_detail>strong.sale_price')
                            sale_price = int(
                                sale_price_tag.text.replace(',', '')) if sale_price_tag is not None else origin_price
                            print(sale_price)

                            discount_rate_tag = list_price.select_one(
                                'div.price_box>span.price_sale>span.sale'
                            )
                            discount_rate = discount_rate_tag.text.strip(
                            ) if discount_rate_tag is not None else "0"

                            percentage = re.match(
                                r'(\d+)%', discount_rate)
                            if percentage:
                                # Gets just the number 4
                                result = int(percentage.group(1))
                                print(result)  # 4

                            # data_log_body = info_a_tag.get(
                            #     'data-log-body') if info_a_tag else "{}"


if __name__ == "__main__":
    asyncio.run(crawl_11st())
