import mysql.connector

def get_top_selling_products(config):
    conn = mysql.connector.connect(
        host=config["mysql"]["host"],
        user=config["mysql"]["user"],
        password=config["mysql"]["password"],
        database=config["mysql"]["database"]
    )
    cursor = conn.cursor()
    query = """
    SELECT p.ID, p.post_title AS name, SUM(oim.meta_value) AS quantity
    FROM wp_posts p
    JOIN wp_woocommerce_order_items oi ON oi.order_item_name = p.post_title
    JOIN wp_woocommerce_order_itemmeta oim ON oim.order_item_id = oi.order_item_id AND oim.meta_key = '_qty'
    WHERE p.post_type = 'product'
    GROUP BY p.ID
    ORDER BY quantity DESC
    LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    top_products = [{"id": row[0], "name": row[1], "quantity": int(row[2])} for row in results]
    return top_products
