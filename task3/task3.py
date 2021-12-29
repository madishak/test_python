import sqlite3

conn = sqlite3.connect(':memory:')
query = conn.cursor()

clients = [(1, 'Иван'), (2, 'Константин'), (3, 'Дмитрий'), (4, 'Александр')]
products = [(1, 'Мяч', 299.99), (2, 'Ручка', 18), (3, 'Кружка', 159.87), (4, 'Монитор', 18000), (5, 'Телефон', 9999.9),
            (6, 'Кофе', 159)]
orders = [(1, 2, 2, 'Закупка 1'), (1, 2, 5, 'Закупка 1'), (1, 2, 1, 'Закупка 1'), (2, 1, 1, 'Закупка 2'),
          (2, 1, 3, 'Закупка 2'), (2, 1, 6, 'Закупка 2'), (2, 1, 2, 'Закупка 2'), (3, 4, 5, 'Закупка 3'),
          (4, 3, 6, 'Закупка 4'), (4, 3, 3, 'Закупка 4'), (2, 1, 5, 'Закупка 2')]

# create tables
query.execute("""CREATE TABLE IF NOT EXISTS clients(
   id_users INT PRIMARY KEY,
   user_name TEXT);
""")

query.execute("""CREATE TABLE IF NOT EXISTS products(
   id_product INT PRIMARY KEY,
   product_name TEXT,
   price INT);
""")

query.execute("""CREATE TABLE IF NOT EXISTS orders(
   id_order INT,
   id_users INT,
   id_product INT,
   order_name TEXT,
   FOREIGN KEY(id_users) REFERENCES clients(id_users),
   FOREIGN KEY(id_product) REFERENCES products(id_product));
""")

# insert data
query.executemany("INSERT INTO clients VALUES(?, ?);", clients)
query.executemany("INSERT INTO products VALUES(?, ?, ?);", products)
query.executemany("INSERT INTO orders VALUES(?, ?, ?, ?);", orders)

# first query
query.execute("""SELECT user_name, SUM(products.price)  
    FROM clients INNER JOIN (products INNER JOIN orders ON products.id_product = orders.id_product)
    ON clients.id_users = orders.id_users
    GROUP BY clients.user_name;""")
results = query.fetchall()
print(results)

# second query
query.execute("""SELECT user_name
    FROM clients INNER JOIN (products INNER JOIN orders ON products.id_product = orders.id_product)
    ON clients.id_users = orders.id_users WHERE (orders.id_product = 5)
    GROUP BY clients.user_name, orders.id_product;""")
results = query.fetchall()
print(results)

# third query
query.execute("""SELECT product_name, COUNT(orders.id_product)
    FROM (products INNER JOIN orders ON products.id_product = orders.id_product)
    GROUP BY product_name;""")
results = query.fetchall()
print(results)

conn.commit()
