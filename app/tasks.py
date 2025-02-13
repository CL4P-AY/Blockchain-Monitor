import requests
from celery import shared_task
from django.utils.dateparse import parse_datetime
from .models import Currency, Provider, Block
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@shared_task
def fetch_btc_block():
    provider = __get_or_create_provider(
        "CoinMarketCap", api_key=settings.COINMARKETCAP_API_KEY
    )
    headers = {"X-CMC_PRO_API_KEY": provider.api_key, "Accept": "application/json"}
    __process_block_data(
        currency_name="BTC",
        provider=provider,
        api_url=settings.COINMARKETCAP_URL,
        headers=headers,
        block_number_key="total_blocks",
        created_at_key="first_block_timestamp",
    )


@shared_task
def fetch_eth_block():
    provider = __get_or_create_provider("BlockChair")
    __process_block_data(
        currency_name="ETH",
        provider=provider,
        api_url=settings.BLOCKCHAIR_URL,
        block_number_key="best_block_height",
        created_at_key="best_block_time",
        date_format="%Y-%m-%d %H:%M:%S",
    )


def __get_or_create_provider(name, **kwargs):
    try:
        provider = Provider.objects.get(name=name)
    except Provider.DoesNotExist:
        provider = Provider.objects.create(name=name, **kwargs)
    return provider


def __process_block_data(
    currency_name,
    provider,
    api_url,
    headers=None,
    block_number_key=None,
    created_at_key=None,
    date_format=None,
):
    response = (
        requests.get(api_url, headers=headers) if headers else requests.get(api_url)
    )
    if response.status_code == 200:
        data = response.json().get("data", {})

        if currency_name in data:
            data = data[currency_name]

        block_number = (
            data.get(block_number_key) if block_number_key else data.get("total_blocks")
        )
        created_at_str = (
            data.get(created_at_key)
            if created_at_key
            else data.get("first_block_timestamp")
        )
        created_at = None

        if created_at_str:
            created_at = (
                datetime.strptime(created_at_str, date_format)
                if date_format
                else parse_datetime(created_at_str)
            )

        currency, _ = Currency.objects.get_or_create(name=currency_name)
        if not Block.objects.filter(
            currency=currency, block_number=block_number
        ).exists():
            Block.objects.create(
                currency=currency,
                provider=provider,
                block_number=block_number,
                created_at=created_at,
            )
    else:
        logger.error(
            f"An error has occurred fetching data for {currency_name}: {response.status_code}"
        )
