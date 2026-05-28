import os

def fix_cart(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content = content.replace('<a href="cart.html" class="cart-btn"><span class="cart-count"', '<a href="cart.html" class="cart-btn">Cart <span class="cart-count"')
                content = content.replace('<span></span>', '')
                
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(content)

fix_cart('.')
print("Fixed!")
