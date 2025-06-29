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

5. Run the development server:
```bash
python manage.py runserver
```



