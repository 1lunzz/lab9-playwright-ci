import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize("amount, zone, fee, total", [
    (0, "city", 1000, 1000),
    (9999, "city", 1000, 10999),
    (10000, "city", 0, 10000),
    (10001, "city", 0, 10001),
    (0, "region", 2000, 2000),
    (9999, "region", 2000, 11999),
    (10000, "region", 0, 10000),
    (10001, "region", 0, 10001),
])
def test_delivery(page, amount, zone, fee, total):
    page.get_by_label("Сумма заказа").fill(str(amount))
    page.get_by_label("Зона доставки").select_option(zone)
    page.get_by_role("button", name="Рассчитать").click()

    result = page.get_by_role("status")
    expect(result).to_be_visible()
    expect(result).to_have_text(
        f"Доставка: {fee} ₸. К оплате: {total} ₸."
    )
    expect(page.get_by_role("alert")).to_be_hidden()


@pytest.mark.parametrize("amount", ["", "-1", "12.5"])
def test_invalid_amount(page, amount):
    page.get_by_label("Сумма заказа").fill(amount)
    page.get_by_role("button", name="Рассчитать").click()

    error = page.get_by_role("alert")
    expect(error).to_be_visible()
    expect(error).to_have_text("Введите целое неотрицательное число")
    expect(page.get_by_role("status")).to_be_hidden()


def test_reset(page):
    page.get_by_label("Сумма заказа").fill("5000")
    page.get_by_label("Зона доставки").select_option("region")
    page.get_by_role("button", name="Рассчитать").click()
    expect(page.get_by_role("status")).to_have_text(
        "Доставка: 2000 ₸. К оплате: 7000 ₸."
    )

    page.get_by_role("button", name="Сбросить").click()
    expect(page.get_by_label("Сумма заказа")).to_have_value("")
    expect(page.get_by_label("Зона доставки")).to_have_value("city")
    expect(page.get_by_role("alert")).to_be_hidden()
    expect(page.get_by_role("status")).to_be_hidden()
