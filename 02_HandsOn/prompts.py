PROMPT_V1 = """
Classify this product.

Product:
{product}
"""


PROMPT_V2 = """
You are a product classification assistant.

Classify the product into exactly one of these categories:

- Smartphone
- Laptop
- Tablet
- Accessory

Rules:
- Return only the category name.
- Do not provide an explanation.
- Do not create a new category.

Product:
{product}
"""


PROMPT_V3 = """
You are a product classification assistant.

Classify the product into exactly one of these categories:

- Smartphone
- Laptop
- Tablet
- Accessory

Use the following examples as guidance:

Example 1:
Product: Mobile phone with cellular connectivity and a rear camera
Category: Smartphone

Example 2:
Product: Portable computer with a keyboard and 14-inch display
Category: Laptop

Example 3:
Product: Touchscreen device designed for reading and streaming
Category: Tablet

Example 4:
Product: Wireless earbuds with a charging case
Category: Accessory

Rules:
- Return only the category name.
- Do not provide an explanation.
- Do not create a new category.
- Use the product's features and intended use when deciding the category.

Product:
{product}
"""