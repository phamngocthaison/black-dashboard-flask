# init_db.py

from apps import create_app, db
from apps.customer.models import Customer
from apps.employee.models import Employee
from apps.product.models import Products
from apps.sale.models import SaleOrder, OrderDetails
from apps.authentication.models import Users
from datetime import datetime
from apps.config import config_dict
import os

DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')

app = create_app(app_config)

with app.app_context():
    db.create_all()
    #drop all user
    db.session.query(Users).delete()
    db.session.query(Customer).delete()
    db.session.query(Employee).delete()
    db.session.query(Products).delete()
    db.session.query(SaleOrder).delete()
    db.session.query(OrderDetails).delete()
    db.session.commit()
    # Add user admin pass admin
    user = Users(username='admin', password='admin', email='admin@uit')
    db.session.add(user)
    db.session.commit()

    # Add sample customers
    customer1 = Customer(name='Phạm Văn A', phone='123-456-7890', email='apham@example.com', address='123 Main St')
    customer2 = Customer(name='Nguyễn Thị B', phone='987-654-3210', email='bnguyen@example.com', address='456 Elm St')
    customer3 = Customer(name='Trần Văn C', phone='555-123-4567', email='ctran@gmail.com', address='789 Maple St')
    customer4 = Customer(name='Lê Thị D', phone='555-987-6543', email='dle@gmail.com', address='321 Oak St')
    customer5 = Customer(name='Nguyễn Văn E', phone='555-555-5555', email='enguyen@gmail.com', address='654 Pine St')
    customer6 = Customer(name='Trần Thị F', phone='555-123-4567', email='ftran@gmail.com', address='987 Cedar St')
    customer7 = Customer(name='Lê Văn G', phone='555-987-6543', email='gle@gmail.com', address='147 Birch St')
    customer8 = Customer(name='Phạm Thị H', phone='555-555-5555', email='hpham@gmail.com', address='258 Spruce St')
    customer9 = Customer(name='Nguyễn Văn I', phone='555-123-4567', email='inguyen@gmail.com', address='369 Ash St')
    customer10 = Customer(name='Trần Thị K', phone='555-987-6543', email='ktran@gmail.com', address='654 Pine St')
    customer11 = Customer(name='Lê Văn L', phone='555-555-5555', email='lle@gmail.com', address='987 Cedar St')
    customer12 = Customer(name='Phạm Thị M', phone='555-123-4567', email='mpham@gmail.com', address='147 Birch St')
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(customer5)
    db.session.add(customer6)
    db.session.add(customer7)
    db.session.add(customer8)
    db.session.add(customer9)
    db.session.add(customer10)
    db.session.add(customer11)
    db.session.add(customer12)

    # Add sample employees
    employee1 = Employee(name='Sơn Phạm', position='Admin', phone='555-123-4567', email='23730043@uit.edu.vn',
                         hire_date=datetime.strptime('2023-01-01', '%Y-%m-%d').date())
    employee2 = Employee(name='Linh Nguyễn', position='Sales', phone='555-987-6543', email='23730027@uit.edu.vn',
                         hire_date=datetime.strptime('2023-02-01', '%Y-%m-%d').date())
    employee3 = Employee(name='Vũ Lê', position='Sales', phone='555-987-6543', email='23730058@uit.edu.vn',
                         hire_date=datetime.strptime('2023-02-01', '%Y-%m-%d').date())
    employee4 = Employee(name='Thiện Trần', position='Sales', phone='555-987-6543', email='thientran@example.com',
                         hire_date=datetime.strptime('2023-02-01', '%Y-%m-%d').date())
    employee5 = Employee(name='Hải Nguyễn', position='Sales', phone='555-987-6543', email='hainguyen@example.com',
                         hire_date=datetime.strptime('2023-02-01', '%Y-%m-%d').date())


    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)
    db.session.add(employee4)
    db.session.add(employee5)

    # Add sample products
    product1 = Products(name='IPhone 16 Pro Max', description='This is an example description for Iphone 16 ProMax, make the description a little bit longer to show off in the free text field', price=30000000, stock=100)
    product2 = Products(name='Samsung Fold 6', description='This is an example description for Samsung Fold 6, make the description a little bit longer to show off in the free text field', price=41000000, stock=200)
    product3 = Products(name='Xiaomi 12', description='This is an example description for Xiaomi 12, make the description a little bit longer to show off in the free text field', price=15000000, stock=300)
    product4 = Products(name='Oppo Reno 7', description='This is an example description for Oppo Reno 7, make the description a little bit longer to show off in the free text field', price=12000000, stock=400)
    product5 = Products(name='Vivo V23', description='This is an example description for Vivo V23, make the description a little bit longer to show off in the free text field', price=8000000, stock=500)
    product6 = Products(name='Realme 9', description='This is an example description for Realme 9, make the description a little bit longer to show off in the free text field', price=7000000, stock=600)
    product7 = Products(name='Nokia 9', description='This is an example description for Nokia 9, make the description a little bit longer to show off in the free text field', price=9000000, stock=700)
    product8 = Products(name='Huawei P50', description='This is an example description for Huawei P50, make the description a little bit longer to show off in the free text field', price=11000000, stock=800)
    product9 = Products(name='Sony Xperia 5', description='This is an example description for Sony Xperia 5, make the description a little bit longer to show off in the free text field', price=13000000, stock=900)
    product10 = Products(name='LG V60', description='This is an example description for LG V60, make the description a little bit longer to show off in the free text field', price=10000000, stock=1000)
    product11 = Products(name='Asus Zenfone 8', description='This is an example description for Asus Zenfone 8, make the description a little bit longer to show off in the free text field', price=14000000, stock=1100)
    product12 = Products(name='Google Pixel 6', description='This is an example description for Google Pixel 6, make the description a little bit longer to show off in the free text field', price=16000000, stock=1200)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.add(product7)
    db.session.add(product8)
    db.session.add(product9)
    db.session.add(product10)
    db.session.add(product11)
    db.session.add(product12)

    db.session.commit()
    # Add sample sale orders
    order1 = SaleOrder(customer_id=customer1.customer_id, order_date=datetime.strptime('2024-06-01', '%Y-%m-%d').date(), total_amount=product1.price * 5,
                       employee_id=employee2.employee_id)
    db.session.add(order1)
    db.session.commit()
    order_detail1 = OrderDetails(order_id=order1.id, product_id=product1.product_id, quantity=5, unit_price=product1.price)
    db.session.add(order_detail1)
    order2 = SaleOrder(customer_id=customer2.customer_id, order_date=datetime.strptime('2024-06-02', '%Y-%m-%d').date(), total_amount=product2.price * 10,
                       employee_id=employee3.employee_id)
    db.session.add(order2)
    db.session.commit()
    order_detail2 = OrderDetails(order_id=order2.id, product_id=product2.product_id, quantity=10, unit_price=product2.price)
    db.session.add(order_detail2)
    order3 = SaleOrder(customer_id=customer3.customer_id, order_date=datetime.strptime('2024-07-03', '%Y-%m-%d').date(), total_amount=product3.price * 15,
                          employee_id=employee4.employee_id)
    db.session.add(order3)
    db.session.commit()
    order_detail3 = OrderDetails(order_id=order3.id, product_id=product3.product_id, quantity=15, unit_price=product3.price)
    db.session.add(order_detail3)
    order4 = SaleOrder(customer_id=customer4.customer_id, order_date=datetime.strptime('2024-07-04', '%Y-%m-%d').date(), total_amount=product4.price * 20,
                          employee_id=employee5.employee_id)
    db.session.add(order4)
    db.session.commit()
    order_detail4 = OrderDetails(order_id=order4.id, product_id=product4.product_id, quantity=20, unit_price=product4.price)
    db.session.add(order_detail4)
    order5 = SaleOrder(customer_id=customer5.customer_id, order_date=datetime.strptime('2024-07-05', '%Y-%m-%d').date(), total_amount=product5.price * 25,
                          employee_id=employee1.employee_id)
    db.session.add(order5)
    db.session.commit()
    order_detail5 = OrderDetails(order_id=order5.id, product_id=product5.product_id, quantity=25, unit_price=product5.price)
    db.session.add(order_detail5)
    order6 = SaleOrder(customer_id=customer6.customer_id, order_date=datetime.strptime('2024-08-06', '%Y-%m-%d').date(), total_amount=product6.price * 30,
                          employee_id=employee2.employee_id)
    db.session.add(order6)
    db.session.commit()
    order_detail6 = OrderDetails(order_id=order6.id, product_id=product6.product_id, quantity=30, unit_price=product6.price)
    db.session.add(order_detail6)
    order7 = SaleOrder(customer_id=customer7.customer_id, order_date=datetime.strptime('2024-08-07', '%Y-%m-%d').date(), total_amount=product7.price * 35,
                          employee_id=employee3.employee_id)
    db.session.add(order7)
    db.session.commit()
    order_detail7 = OrderDetails(order_id=order7.id, product_id=product7.product_id, quantity=35, unit_price=product7.price)
    db.session.add(order_detail7)
    order8 = SaleOrder(customer_id=customer8.customer_id, order_date=datetime.strptime('2024-08-08', '%Y-%m-%d').date(), total_amount=product8.price * 40,
                          employee_id=employee4.employee_id)
    db.session.add(order8)
    db.session.commit()
    order_detail8 = OrderDetails(order_id=order8.id, product_id=product8.product_id, quantity=40, unit_price=product8.price)
    db.session.add(order_detail8)
    order9 = SaleOrder(customer_id=customer9.customer_id, order_date=datetime.strptime('2024-09-09', '%Y-%m-%d').date(), total_amount=product9.price * 45,
                          employee_id=employee5.employee_id)
    db.session.add(order9)
    db.session.commit()
    order_detail9 = OrderDetails(order_id=order9.id, product_id=product9.product_id, quantity=45, unit_price=product9.price)
    db.session.add(order_detail9)
    order10 = SaleOrder(customer_id=customer10.customer_id, order_date=datetime.strptime('2024-09-10', '%Y-%m-%d').date(), total_amount=product10.price * 50,
                          employee_id=employee1.employee_id)
    db.session.add(order10)
    db.session.commit()
    order_detail10 = OrderDetails(order_id=order10.id, product_id=product10.product_id, quantity=50, unit_price=product10.price)
    db.session.add(order_detail10)
    order11 = SaleOrder(customer_id=customer11.customer_id, order_date=datetime.strptime('2024-10-11', '%Y-%m-%d').date(), total_amount=product11.price * 55,
                          employee_id=employee2.employee_id)
    db.session.add(order11)
    db.session.commit()
    order_detail11 = OrderDetails(order_id=order11.id, product_id=product11.product_id, quantity=55, unit_price=product11.price)
    db.session.add(order_detail11)
    order12 = SaleOrder(customer_id=customer12.customer_id, order_date=datetime.strptime('2024-10-12', '%Y-%m-%d').date(), total_amount=product12.price * 60,
                          employee_id=employee3.employee_id)
    db.session.add(order12)
    db.session.commit()
    order_detail12 = OrderDetails(order_id=order12.id, product_id=product12.product_id, quantity=60, unit_price=product12.price)
    db.session.add(order_detail12)
    order13 = SaleOrder(customer_id=customer1.customer_id, order_date=datetime.strptime('2024-10-13', '%Y-%m-%d').date(), total_amount=product1.price * 65,
                            employee_id=employee4.employee_id)
    db.session.add(order13)
    db.session.commit()
    order_detail13 = OrderDetails(order_id=order13.id, product_id=product1.product_id, quantity=65, unit_price=product1.price)
    db.session.add(order_detail13)
    order14 = SaleOrder(customer_id=customer2.customer_id, order_date=datetime.strptime('2024-11-14', '%Y-%m-%d').date(), total_amount=product2.price * 70,
                            employee_id=employee5.employee_id)
    db.session.add(order14)
    db.session.commit()
    order_detail14 = OrderDetails(order_id=order14.id, product_id=product2.product_id, quantity=70, unit_price=product2.price)
    db.session.add(order_detail14)
    order15 = SaleOrder(customer_id=customer3.customer_id, order_date=datetime.strptime('2024-11-15', '%Y-%m-%d').date(), total_amount=product3.price * 75,
                            employee_id=employee1.employee_id)
    db.session.add(order15)
    db.session.commit()
    order_detail15 = OrderDetails(order_id=order15.id, product_id=product3.product_id, quantity=75, unit_price=product3.price)
    db.session.add(order_detail15)
    order16 = SaleOrder(customer_id=customer4.customer_id, order_date=datetime.strptime('2024-11-16', '%Y-%m-%d').date(), total_amount=product4.price * 80,
                            employee_id=employee1.employee_id)
    db.session.add(order16)
    db.session.commit()
    order_detail16 = OrderDetails(order_id=order16.id, product_id=product4.product_id, quantity=80, unit_price=product4.price)
    db.session.add(order_detail16)
    order17 = SaleOrder(customer_id=customer5.customer_id, order_date=datetime.strptime('2024-11-17', '%Y-%m-%d').date(), total_amount=product5.price * 85,
                            employee_id=employee2.employee_id)
    db.session.add(order17)
    db.session.commit()
    order_detail17 = OrderDetails(order_id=order17.id, product_id=product5.product_id, quantity=85, unit_price=product5.price)
    db.session.add(order_detail17)
    order18 = SaleOrder(customer_id=customer6.customer_id, order_date=datetime.strptime('2024-12-18', '%Y-%m-%d').date(), total_amount=product6.price * 90,
                            employee_id=employee1.employee_id)
    db.session.add(order18)
    db.session.commit()
    order_detail18 = OrderDetails(order_id=order18.id, product_id=product6.product_id, quantity=90, unit_price=product6.price)
    db.session.add(order_detail18)
    order19 = SaleOrder(customer_id=customer7.customer_id, order_date=datetime.strptime('2024-12-19', '%Y-%m-%d').date(), total_amount=product7.price * 95,
                            employee_id=employee2.employee_id)
    db.session.add(order19)
    db.session.commit()
    order_detail19 = OrderDetails(order_id=order19.id, product_id=product7.product_id, quantity=95, unit_price=product7.price)
    db.session.add(order_detail19)
    order20 = SaleOrder(customer_id=customer8.customer_id, order_date=datetime.strptime('2024-12-20', '%Y-%m-%d').date(), total_amount=product8.price * 100,
                            employee_id=employee1.employee_id)
    db.session.add(order20)
    db.session.commit()
    order_detail20 = OrderDetails(order_id=order20.id, product_id=product8.product_id, quantity=100, unit_price=product8.price)
    db.session.add(order_detail20)
    order21 = SaleOrder(customer_id=customer9.customer_id, order_date=datetime.strptime('2024-12-21', '%Y-%m-%d').date(), total_amount=product9.price * 105,
                            employee_id=employee2.employee_id)
    db.session.add(order21)
    db.session.commit()
    order_detail21 = OrderDetails(order_id=order21.id, product_id=product9.product_id, quantity=105, unit_price=product9.price)
    db.session.add(order_detail21)
    order22 = SaleOrder(customer_id=customer10.customer_id, order_date=datetime.strptime('2024-12-22', '%Y-%m-%d').date(), total_amount=product10.price * 110,
                            employee_id=employee3.employee_id)
    db.session.add(order22)
    db.session.commit()
    order_detail22 = OrderDetails(order_id=order22.id, product_id=product10.product_id, quantity=110, unit_price=product10.price)
    db.session.add(order_detail22)
    order23 = SaleOrder(customer_id=customer11.customer_id, order_date=datetime.strptime('2024-12-23', '%Y-%m-%d').date(), total_amount=product11.price * 115,
                            employee_id=employee4.employee_id)
    db.session.add(order23)
    db.session.commit()
    order_detail23 = OrderDetails(order_id=order23.id, product_id=product11.product_id, quantity=115, unit_price=product11.price)
    db.session.add(order_detail23)
    order24 = SaleOrder(customer_id=customer12.customer_id, order_date=datetime.strptime('2024-12-24', '%Y-%m-%d').date(), total_amount=product12.price * 120,
                            employee_id=employee5.employee_id)
    db.session.add(order24)
    db.session.commit()
    order_detail24 = OrderDetails(order_id=order24.id, product_id=product12.product_id, quantity=120, unit_price=product12.price)
    db.session.add(order_detail24)
    order25 = SaleOrder(customer_id=customer1.customer_id, order_date=datetime.strptime('2024-12-25', '%Y-%m-%d').date(), total_amount=product1.price * 125 + product2.price * 125,
                            employee_id=employee1.employee_id)
    db.session.add(order25)
    db.session.commit()
    order_detail25 = OrderDetails(order_id=order25.id, product_id=product1.product_id, quantity=125, unit_price=product1.price)
    db.session.add(order_detail25)
    order_detail25_2 = OrderDetails(order_id=order25.id, product_id=product2.product_id, quantity=125, unit_price=product2.price)
    db.session.add(order_detail25_2)
    order26 = SaleOrder(customer_id=customer2.customer_id, order_date=datetime.strptime('2024-12-26', '%Y-%m-%d').date(), total_amount=product2.price * 130 + product3.price * 130,
                            employee_id=employee1.employee_id)
    db.session.add(order26)
    db.session.commit()
    order_detail26 = OrderDetails(order_id=order26.id, product_id=product2.product_id, quantity=130, unit_price=product2.price)
    db.session.add(order_detail26)
    order_detail26_2 = OrderDetails(order_id=order26.id, product_id=product3.product_id, quantity=130, unit_price=product3.price)
    db.session.add(order_detail26_2)
    order27 = SaleOrder(customer_id=customer3.customer_id, order_date=datetime.strptime('2024-12-27', '%Y-%m-%d').date(), total_amount=product3.price * 135 + product4.price * 135,
                            employee_id=employee2.employee_id)
    db.session.add(order27)
    db.session.commit()
    order_detail27 = OrderDetails(order_id=order27.id, product_id=product3.product_id, quantity=135, unit_price=product3.price)
    db.session.add(order_detail27)
    order_detail27_2 = OrderDetails(order_id=order27.id, product_id=product4.product_id, quantity=135, unit_price=product4.price)
    db.session.add(order_detail27_2)
    db.session.commit()
    order27 = SaleOrder(customer_id=customer3.customer_id, order_date=datetime.strptime('2024-06-27', '%Y-%m-%d').date(), total_amount=product3.price * 135 + product4.price * 135,
                            employee_id=employee2.employee_id)
    db.session.add(order27)
    db.session.commit()
    order_detail27 = OrderDetails(order_id=order27.id, product_id=product3.product_id, quantity=135, unit_price=product3.price)
    db.session.add(order_detail27)
    order_detail27_2 = OrderDetails(order_id=order27.id, product_id=product4.product_id, quantity=135, unit_price=product4.price)
    db.session.add(order_detail27_2)
    order28 = SaleOrder(customer_id=customer4.customer_id, order_date=datetime.strptime('2024-06-28', '%Y-%m-%d').date(), total_amount=product4.price * 140 + product5.price * 140,
                            employee_id=employee3.employee_id)
    db.session.add(order28)
    db.session.commit()
    order_detail28 = OrderDetails(order_id=order28.id, product_id=product4.product_id, quantity=140, unit_price=product4.price)
    db.session.add(order_detail28)
    order_detail28_2 = OrderDetails(order_id=order28.id, product_id=product5.product_id, quantity=140, unit_price=product5.price)
    db.session.add(order_detail28_2)
    order29 = SaleOrder(customer_id=customer5.customer_id, order_date=datetime.strptime('2024-08-29', '%Y-%m-%d').date(), total_amount=product5.price * 145 + product6.price * 145,
                            employee_id=employee4.employee_id)
    db.session.add(order29)
    db.session.commit()
    order_detail29 = OrderDetails(order_id=order29.id, product_id=product5.product_id, quantity=145, unit_price=product5.price)
    db.session.add(order_detail29)
    order_detail29_2 = OrderDetails(order_id=order29.id, product_id=product6.product_id, quantity=145, unit_price=product6.price)
    db.session.add(order_detail29_2)
    order30 = SaleOrder(customer_id=customer6.customer_id, order_date=datetime.strptime('2024-08-30', '%Y-%m-%d').date(), total_amount=product6.price * 150 + product7.price * 150,
                            employee_id=employee5.employee_id)
    db.session.add(order30)
    db.session.commit()
    order_detail30 = OrderDetails(order_id=order30.id, product_id=product6.product_id, quantity=150, unit_price=product6.price)
    db.session.add(order_detail30)
    order_detail30_2 = OrderDetails(order_id=order30.id, product_id=product7.product_id, quantity=150, unit_price=product7.price)
    db.session.add(order_detail30_2)
    order31 = SaleOrder(customer_id=customer7.customer_id, order_date=datetime.strptime('2024-05-30', '%Y-%m-%d').date(), total_amount=product7.price * 155 + product8.price * 155,
                            employee_id=employee1.employee_id)
    db.session.add(order31)
    db.session.commit()
    order_detail31 = OrderDetails(order_id=order31.id, product_id=product7.product_id, quantity=155, unit_price=product7.price)
    db.session.add(order_detail31)
    order_detail31_2 = OrderDetails(order_id=order31.id, product_id=product8.product_id, quantity=155, unit_price=product8.price)
    db.session.add(order_detail31_2)
    order32 = SaleOrder(customer_id=customer8.customer_id, order_date=datetime.strptime('2024-05-31', '%Y-%m-%d').date(), total_amount=product8.price * 160 + product9.price * 160,
                            employee_id=employee2.employee_id)
    db.session.add(order32)
    db.session.commit()
    order_detail32 = OrderDetails(order_id=order32.id, product_id=product8.product_id, quantity=160, unit_price=product8.price)
    db.session.add(order_detail32)
    order_detail32_2 = OrderDetails(order_id=order32.id, product_id=product9.product_id, quantity=160, unit_price=product9.price)
    db.session.add(order_detail32_2)
    order33 = SaleOrder(customer_id=customer9.customer_id, order_date=datetime.strptime('2024-09-09', '%Y-%m-%d').date(), total_amount=product9.price * 165 + product10.price * 165,
                            employee_id=employee3.employee_id)
    db.session.add(order33)
    db.session.commit()
    order_detail33 = OrderDetails(order_id=order33.id, product_id=product9.product_id, quantity=165, unit_price=product9.price)
    db.session.add(order_detail33)
    order_detail33_2 = OrderDetails(order_id=order33.id, product_id=product10.product_id, quantity=165, unit_price=product10.price)
    db.session.add(order_detail33_2)
    order34 = SaleOrder(customer_id=customer10.customer_id, order_date=datetime.strptime('2024-09-10', '%Y-%m-%d').date(), total_amount=product10.price * 170 + product11.price * 170,
                            employee_id=employee4.employee_id)
    db.session.add(order34)
    db.session.commit()
    order_detail34 = OrderDetails(order_id=order34.id, product_id=product10.product_id, quantity=170, unit_price=product10.price)
    db.session.add(order_detail34)
    order_detail34_2 = OrderDetails(order_id=order34.id, product_id=product11.product_id, quantity=170, unit_price=product11.price)
    db.session.add(order_detail34_2)
    order35 = SaleOrder(customer_id=customer11.customer_id, order_date=datetime.strptime('2024-09-11', '%Y-%m-%d').date(), total_amount=product11.price * 175 + product12.price * 175,
                            employee_id=employee5.employee_id)
    db.session.add(order35)
    db.session.commit()
    order_detail35 = OrderDetails(order_id=order35.id, product_id=product11.product_id, quantity=175, unit_price=product11.price)
    db.session.add(order_detail35)
    order_detail35_2 = OrderDetails(order_id=order35.id, product_id=product12.product_id, quantity=175, unit_price=product12.price)
    db.session.add(order_detail35_2)
    order36 = SaleOrder(customer_id=customer12.customer_id, order_date=datetime.strptime('2024-09-12', '%Y-%m-%d').date(), total_amount=product12.price * 180 + product1.price * 180,
                            employee_id=employee1.employee_id)
    db.session.add(order36)
    db.session.commit()
    order_detail36 = OrderDetails(order_id=order36.id, product_id=product12.product_id, quantity=180, unit_price=product12.price)
    db.session.add(order_detail36)
    order_detail36_2 = OrderDetails(order_id=order36.id, product_id=product1.product_id, quantity=180, unit_price=product1.price)
    db.session.add(order_detail36_2)
    order37 = SaleOrder(customer_id=customer1.customer_id, order_date=datetime.strptime('2024-09-13', '%Y-%m-%d').date(), total_amount=product1.price * 185 + product2.price * 185,
                            employee_id=employee2.employee_id)
    db.session.add(order37)
    db.session.commit()
    order_detail37 = OrderDetails(order_id=order37.id, product_id=product1.product_id, quantity=185, unit_price=product1.price)
    db.session.add(order_detail37)
    order_detail37_2 = OrderDetails(order_id=order37.id, product_id=product2.product_id, quantity=185, unit_price=product2.price)
    db.session.add(order_detail37_2)
    order38 = SaleOrder(customer_id=customer2.customer_id, order_date=datetime.strptime('2024-09-14', '%Y-%m-%d').date(), total_amount=product2.price * 190 + product3.price * 190,
                            employee_id=employee3.employee_id)
    db.session.add(order38)
    db.session.commit()
    order_detail38 = OrderDetails(order_id=order38.id, product_id=product2.product_id, quantity=190, unit_price=product2.price)
    db.session.add(order_detail38)
    order_detail38_2 = OrderDetails(order_id=order38.id, product_id=product3.product_id, quantity=190, unit_price=product3.price)
    db.session.add(order_detail38_2)
    order39 = SaleOrder(customer_id=customer3.customer_id, order_date=datetime.strptime('2024-09-15', '%Y-%m-%d').date(), total_amount=product3.price * 195 + product4.price * 195,
                            employee_id=employee4.employee_id)
    db.session.add(order39)
    db.session.commit()
    order_detail39 = OrderDetails(order_id=order39.id, product_id=product3.product_id, quantity=195, unit_price=product3.price)
    db.session.add(order_detail39)
    order_detail39_2 = OrderDetails(order_id=order39.id, product_id=product4.product_id, quantity=195, unit_price=product4.price)
    db.session.add(order_detail39_2)
    


