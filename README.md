# AVICOLE - Poultry E-commerce Platform

AVICOLE is a Django-based e-commerce platform designed specifically for the poultry industry. It connects different stakeholders in the poultry supply chain, including Alfissen (feed producers), Ouakkaha (chick producers), and customers.

## Features

- **Custom User System**:
  - Role-based user accounts: Admin, Alfissen, Ouakkaha, and Customer
  - User registration, login, and profile management
  - Role-specific permissions and access control

- **Product Management**:
  - Two main product types: Poussins (chicks) and Aliments Composés (compound feed)
  - Product listing with filtering and search capabilities
  - Detailed product pages with images and descriptions
  - CRUD operations for products (based on user roles)

- **Order System**:
  - Shopping cart functionality
  - Checkout process with shipping information
  - Order history and tracking
  - Role-based purchasing restrictions

- **Role-Specific Dashboards**:
  - Admin: Complete oversight of all products, users, and orders
  - Alfissen: Management of feed products and order tracking
  - Ouakkaha: Management of chick products and order tracking
  - Customer: Order history and personalized recommendations

- **Responsive Design**:
  - Clean, modern UI built with custom CSS
  - Mobile-friendly layout
  - Consistent styling across all pages

## Project Structure

```
AVICOLE/
├── avicole_project/    # Project settings and main URLs
├── core/              # Core app with home and dashboard views
├── users/             # Custom user model and authentication
├── products/          # Product management
├── orders/            # Shopping cart and order processing
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, and images
└── media/             # User-uploaded files
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/avicole.git
cd avicole
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Set up default users (admin, alfissen, and ouakkaha):
```bash
python manage.py setup_default_users
```

This will create the following default users:
- Admin: username=`admin`, password=`admin123`
- Alfissen: username=`alfissen`, password=`alfissen123`
- Ouakkaha: username=`ouakkaha`, password=`ouakkaha123`

6. Set up default products:
```bash
python manage.py setup_default_products
```

This will create:
- Poussins products (assigned to Ouakkaha user)
- Aliments Composés products for Volailles, Bovins, and Ovins categories (assigned to Alfissen user)

7. If you need to reset all users to defaults:
```bash
python manage.py reset_users
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Access the site at http://127.0.0.1:8000/

## Usage

### Admin
- Log in with username: `admin` and password: `admin123`
- Access the admin panel at `/admin/`
- Manage all users, products, and orders
- View comprehensive statistics on the admin dashboard

### Alfissen (Feed Producers)
- Log in with username: `alfissen` and password: `alfissen123`
- Add and manage feed products
- Process orders for their products
- Purchase products from Ouakkaha sellers

### Ouakkaha (Chick Producers)
- Log in with username: `ouakkaha` and password: `ouakkaha123`
- Add and manage chick products
- Process orders for their products
- Purchase products from Alfissen sellers

### Customers
- Register a new account (only customer role is available for registration)
- Browse all available products
- Add products to cart and place orders
- View order history and track orders

## Product Categories

### Poussins (Chicks)
- Poulet Roux Fonce
- Poulet Roux
- Poulet Beldi ouakkaha
- Poulet Cou Nu
- Poulet Gris barre
- Poulet de chair

### Aliments Composés (Compound Feed)
#### Volailles
- Aliments Poussin Démarrage A13
- Aliment Pré-Démarrage Pre-13
- Aliments Poussin Croissance A23
- Aliment Poulet Pré-Abattage A43
- Aliment Poule Pondeuse P 64
- Aliment Concentre Poulet De Chair Cdcf 43%
- Aliment Concentre Poule Pondeuse Ponte 44% Cc P204
- Aliments Pondeuse Et Reproductrice – PR64

#### Bovins
- Aliments Veaux Démarrage JBIO
- Aliments Jeunes Bovins Engraissement JB2O
- Aliments Bovins Top Engraissement JB3O
- Aliments Bovins Finition JB4O
- Aliments Génisse En Croissance GIO
- Aliments Vache Laitière 2L – VL20
- Aliments Vache Laitière 2.5L – VL25
- Aliments Vache Laitière 3L – VL30

#### Ovins
- Aliments Agneaux d'Engraissement O2O
- Aliments Ovins Finition O3O
- Aliments Brebis Gestante O4O
- Aliments Brebis Allaitante O5O

## License

This project is licensed under the MIT License - see the LICENSE file for details. 