# Welcome to the technical challenge repository!

In this repository, you will find a set of tasks designed to assess your technical skills and problem-solving abilities. Please read the instructions carefully and complete the challenges to the best of your ability.

### Getting Started

**Important**

The code, variables and comments should all be written in English.


**Fork the Repository**: Start by forking this repository and cloning it to your local machine.

```bash
git clone <your-forked-repo-url>
cd <repo-directory>
```

**Install Python Dependencies**:

This project utilizes `Python 3.11+` and `uv` to manage dependencies. Make sure you have Python and uv installed on your machine.

```bash
uv sync
```

**Install Node.js Dependencies**:

This project also uses Node.js (v20+). Ensure you have Node.js installed, then run:

```bash
npm install
```

**Build theme files**:
To build the theme files, run the following command:
```bash
npm run build-theme
```

Alternatively, you can `watch` for changes and automatically rebuild the theme files by running:
```bash
npm run watch-theme
```

**Running Database Migrations**:
To set up the database schema, run the following command:
```bash
uv run python manage.py migrate
```

This will create a sqlite database file named `db.sqlite3` in the project directory. Feel free to delete this file and re-run the migrations if needed.

**Load Sample Data**:
To populate the database with sample data, run the following command:
```bash
uv run python manage.py import_products
uv run python manage.py populate_orders --orders 100 --days 180
```

You should see no errors in the console output.

### Running the Application
To start the application, use the following command:
```bash
  uv run python manage.py runserver
```
Open your browser and navigate to `http://localhost:8000` to view the application.

If everything was done correctly, you should see the welcome page of the application.

# About the Challenges

### 🎯 Goal

This challenge evaluates your practical skills with:

- Django (Fullstack)
- HTMX (dynamic requests and partial updates)
- Alpine.js (reactivity and interactivity)
- HTML / CSS (clean, responsive layout)


### ⚙️ Stack

| Technology                       | Purpose                                        |
|----------------------------------|------------------------------------------------|
| Django                           | Backend and template rendering                 |
| TailwindCss (v3) + Daisy UI (v4) | UI components library                          |
| HTMX                             | AJAX-like dynamic requests and partial updates |
| Alpine.js                        | Lightweight interactivity and reactivity       |
| TailwindCSS (or Bootstrap)       | Simple, responsive styling                     |
| SQLite                           | Default local database                         |



### 🧱 Project Setup

The project already includes:
- Models: `Product`, `Cart`, `CartItem`, `Order`, `OrderItem`
- Base templates configured
- Sample data
- HTMX and Alpine.js imported in `base.html`



# 🚀 Tasks

You must complete the following **5 stages** with a 6th optional stage, it's up to you.

## ⚠️ Important:

Read all the tasks before starting, features you might assume you need to implement might be described in later stages.


=================================================================================

#### 🟢 Stage 1 — Product Listing

**Goal:**  
Create the `/products/` page to display the list of available products.

**Requirements:**
- Show products as cards or list items.
- Add a search input that filters products by name (live search using HTMX).
- Include a **"View details"** button (will open a modal in the next stage).
- Include an **"Add to cart"** button to add the product to the cart.

**Hint:**  
Use `hx-get` + `hx-target` to dynamically update the product list when filtering.

=================================================================================

#### 🟡 Stage 2 — Product Details Modal

**Goal:**  
When clicking “View details”, open a modal using HTMX with the product information.

**Requirements:**
- Display product name, image, price, description, and stock.
- Include an **“Add to cart”** button inside the modal.
- Use Daisy UI modal component (Daisy UI version 4).

=================================================================================

#### 🔴 Stage 3 - Dynamic Cart
# TODO TO AQUI
**Goal:**  
Make the **"Add to cart"** button dynamic and reactive, allowing users to update the quantity of the product in the cart.

**Requirements:**
- When adding the product to the cart, the cart item count in the navbar should update dynamically (using HTMX with oob-swap).
- If the product is out of stock, disable the **"Add to cart"** button.
- After adding the product to the cart, the button should be swapped to an input field allowing the user to update the quantity of that product in the cart.
    - The quantity input should have increment and decrement buttons.
    - If the quantity is set to zero, the product should be removed from the cart, and the input field should be swapped back to the **"Add to cart"** button.
    - If the user updates the quantity to a value higher than the available stock, force the quantity to the maximum available stock.

=================================================================================

#### 🟠 Stage 4 — Review Page

**Goal:**  
Create a `/review/` page to review the cart before checkout.

**Requirements:**
- List all products with name, price, quantity, and subtotal and image.
- Calculate total amount on the backend.
- Include a **“Place Order”** button.
  - Clicking on this button will create an order in the database, clear the cart and redirect to home screen.

=================================================================================

#### 🟡 Stage 5 — Order History Page

**Goal:**  
Create a `/order_history/` page to show the history of sales orders.

**Requirements:**
- List all orders with order id, date, total amount.

**Bonus**

- Add a click to expand to show order items in each order element (name, price, quantity, subtotal, image).

=================================================================================

#### 🟣 Stage 6 — Optional (UX & Interactivity)

**Enhancements:**
- HTMX loading spinner (`hx-indicator`)
- Flash messages dynamically injected (`hx-swap-oob`)
- Alpine.js animations
- Mobile-first responsive layout using Tailwind
- Unit tests for views


# References

- [Django Documentation](https://docs.djangoproject.com/en/5.2/)
- [HTMX Documentation](https://htmx.org/docs)
- [Alpine.js Documentation](https://alpinejs.dev)
- [Tailwind CSS Documentation](https://v3.tailwindcss.com/)
- [Daisy UI Documentation](https://v4.daisyui.com/components/)