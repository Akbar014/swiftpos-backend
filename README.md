<h1 align="center" id="title">SWIFTPOS API</h1>

<p align="center"><img src="https://www.drpos.in/wp-content/uploads/2023/04/dr-pos-banner-1.jpg" alt="project-image"></p>

<p id="description">This is a simple POS software where authenticated user can manage products and product stock purchase products sale products. System user can track total purchase and sale amount from History. System owner can add manager or cashier for manage this POS software. Currently I am working this system for including new features to ensure make this system more comfortable. If you have moment you can login by given credentials: Username : Akbar Password : 12345678!a</p>

<h2>🚀 Demo</h2>

[https://swiftpos-delta.vercel.app/](https://swiftpos-delta.vercel.app/)

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Product manage
*   Category manage
*   Customer manage
*   Seller manage
*   Cashier & manager manage
*   Purchase Product
*   Sale Product
*   Purchase & Sales history

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone ripository</p>

```
git clone https://github.com/Akbar014/swiftpos-backend.git
```

<p>2. Enter into project directory</p>

```
cd directory_name
```

<p>3. Run command</p>

```
py manage.py runserver
```


<br>



## 🍰 API Endpoints

### Autehtication
- `POST /donate_blood/register/`
- `POST /donate_blood/login/`
- `POST /donate_blood/logout/`

### Customer
- `GET /personapp/customer/`
- `POST /personapp/customer/<int:customer_id>`
- `POST /personapp/customer/<int:customer_id>`

### Supplier
- `GET /personapp/supplier/`
- `POST /personapp/supplier/<int:customer_id>`
- `POST /personapp/supplier/<int:customer_id>`
  
### Users
- `GET /personapp/users/`
- `POST /personapp/users/<int:customer_id>`
- `POST /personapp/users/<int:customer_id>`
  
### Products
- `GET /productsapp/products/`
- `POST /productsapp/products/`
- `GET /productsapp/products/<int:products_id>`
- `PUT /productsapp/products/<int:products_id>`
  
### Category
- `GET /productsapp/category/`
- `POST /productsapp/category/`
- `GET /productsapp/category/<int:category_id>`
- `PUT /productsapp/category/<int:category_id>`

### Purchase
- `GET /purchaseapp/purchases/`
- `POST /purchaseapp/purchases/`

### Sales
- `GET /salesapp/sales/`
- `POST /salesapp/sales/`

### History
- `GET /historyapp/purchaseHistory/`
- `GET /historyapp/saleHistory/`
- `GET /historyapp/statistics/`


  
<h2>💻 Built with</h2>

Technologies used in the project:

*   django
*   django rest framwork
*   postgres
*   cloudinary
