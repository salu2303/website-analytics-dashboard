import json
from ga4_report import get_device_stats
from woocommerce_report import get_top_selling_products
from email_report import generate_summary, send_email
from ga4_report import get_device_stats, get_custom_page_views, get_top_product_page_views,get_total_website_users,get_last_search_terms

def main():
    with open("config.json") as f:
        config = json.load(f)

    top_products = get_top_selling_products(config)
    device_stats = get_device_stats(config)
    page_views = get_custom_page_views(config)
    top_product_pages = get_top_product_page_views(config)
    total_website_users = get_total_website_users(config)
    

    summary = "This week’s traffic and product stats are now available. See breakdowns below."

    print("✉️ Sending email report...")

    # send_email(
    #     config=config,
    #     top_products=top_products,
    #     device_stats=device_stats,
    #     page_views=page_views,
    #     summary=summary,
    #     total_visitors=total_website_users,
    # )

    print("✅ Report sent successfully.")
    print("\n🌐 TOTAL WEBSITE VISITORS")
    print(f"   → {total_website_users:,} unique users in the past 7 days")

    print("\n📱 DEVICE BREAKDOWN")
    for device, users in device_stats.items():
        print(f"   - {device.capitalize():<10}: {int(users):,} users")

    # print("\n🛍 TOP 10 BEST-SELLING PRODUCTS (WooCommerce)")
    # for product in top_products:
    #     print(f"   - {product['name']:<40} → {product['quantity']} sold")

    print("\n📄 PAGE-SPECIFIC VISITS")
    label_map = {
        "/": "Homepage",
        "/my-account/education-webinars/": "Education Webinars",
        "/my-account/monographs/": "Product Monographs",
        "/insider-scoop/": "Insider Scoop"
    }
    for path, label in label_map.items():
        print(f"   - {label:<25}: {page_views.get(path, 0):,} visits")

    print("\n🔥 TOP 10 MOST VISITED PRODUCT PAGES")
    for path, views in top_product_pages:
        print(f"   - {path:<40} → {views:,} views")

    print("\n🔍 LAST 10 SEARCH TERMS")
    for term in get_last_search_terms(config):
        print(f"   - {term}")


if __name__ == "__main__":
    main()
