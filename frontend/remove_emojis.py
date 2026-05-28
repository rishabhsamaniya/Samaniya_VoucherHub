import os
import re
import emoji

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def clean_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.html') or f.endswith('.js'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = remove_emojis(content)
                # We might be left with empty .nav-logo-icon spans or ugly text like " Add to Cart" instead of "🛒 Add to Cart". 
                # Let's clean up some specific artifacts caused by emoji removal
                new_content = new_content.replace('<div class="nav-logo-icon"></div>', '<div class="nav-logo-icon">V</div>')
                new_content = new_content.replace('<span class="toast-icon"></span>', '<span class="toast-icon" style="display:none;"></span>')
                
                # For voucher details
                new_content = new_content.replace('<div class="vd-feature-item"><span></span>', '<div class="vd-feature-item">')
                
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(new_content)

clean_dir('.')
print("Cleaned!")
