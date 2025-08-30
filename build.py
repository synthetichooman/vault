import os
import shutil
import json
from datetime import datetime

# --- CONFIGURATION ---
SRC_DIR = '.'
ARCHIVE_DIR = os.path.join(SRC_DIR, 'archive')
OUTPUT_DIR = os.path.join(SRC_DIR, 'public')
STATIC_DIRS = ['css', 'js', 'archive', 'assets']

# --- HTML TEMPLATES ---

def create_index_html(products, stats):
    list_items = []
    for product in products:
        list_items.append(f'''
            <a href="{product['html_file']}" class="vault-item-link">
                <div class="vault-item">
                    <img src="{product['thumbnail']}" alt="{product['product_name']}" loading="lazy">
                </div>
            </a>''')
    
    stats_text = f'{stats["product_count"]} articles, {stats["last_updated"]}, {stats["total_size"]}'

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>vault - hooman</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="assets/favicon.png" type="image/png">
</head>
<body>
    <header class="vault-header">
        <div class="stats-bar">
            <p>{stats_text}</p>
        </div>
    </header>
    <main class="vault">
        <div class="header-spacer"></div>
        <nav class="main-nav">
            <a href="index.html" class="active">vault</a>
            <a href="https://athoce.kr" target="_blank" rel="noopener noreferrer">shop</a>
        </nav>
        <div class="vault-grid">
            {'' .join(list_items)}
        </div>
    </main>
    <footer class="main-footer">
        <div class="footer-bar">
            <p>suggestions for corrections and image redistribution are welcome</p>
            <p><a href="https://instagram.com/synthetic.hooman" target="_blank" rel="noopener noreferrer">instagram</a></p>
        </div>
    </footer>
</body>
</html>'''

def create_article_html(product):
    slides_html = ''
    for image_path in product['images']:
        slides_html += f'            <div class="swiper-slide"><img src="{image_path}" alt="{product["product_name"]}"></div>\n'

    era = product.get('era', '')
    status = product.get('status', '')

    # NOTE: The curly braces for the Swiper JS init are escaped by doubling them (e.g., {{...}})
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['brand']} - hooman</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="assets/favicon.png" type="image/png">
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
</head>
<body>
    <main class="article">
        <header class="article-header">
            <a href="javascript:history.back()" class="back-arrow">&lt;</a>
        </header>
        <div class="header-spacer"></div>
        <section class="article-viewer">
            <!-- Slider main container -->
            <div class="swiper">
                <!-- Additional required wrapper -->
                <div class="swiper-wrapper">
                    <!-- Slides -->
{slides_html.strip()}
                </div>
                <!-- If we need navigation buttons -->
                <div class="swiper-button-prev"></div>
                <div class="swiper-button-next"></div>
            </div>
        </section>
        <section class="article-details">
            <p>{product['brand']}</p>
            <p>{product['designer']}</p>
            <p>{era}</p>
            <p>{status}</p>
        </section>
    </main>
    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
    <script>
        const swiper = new Swiper('.swiper', {{
            loop: true,
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
        }});
    </script>
    <footer class="main-footer">
        <div class="footer-bar">
            <p>suggestions for corrections and image redistribution are welcome</p>
            <p><a href="https://instagram.com/synthetic.hooman" target="_blank" rel="noopener noreferrer">instagram</a></p>
        </div>
    </footer>
</body>
</html>'''

# --- BUILD SCRIPT LOGIC ---

def main():
    print("Starting static site build...")
    # Updated time format to YYYY.MM.DD HH:MM:SS
    build_time = datetime.now().astimezone().strftime('%Y.%m.%d %H:%M:%S')

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    products = []
    if os.path.exists(ARCHIVE_DIR):
        for brand in os.listdir(ARCHIVE_DIR):
            brand_path = os.path.join(ARCHIVE_DIR, brand)
            if os.path.isdir(brand_path):
                for designer in os.listdir(brand_path):
                    designer_path = os.path.join(brand_path, designer)
                    if os.path.isdir(designer_path):
                        for product_name in os.listdir(designer_path):
                            product_path = os.path.join(designer_path, product_name)
                            if os.path.isdir(product_path):
                                info_path = os.path.join(product_path, 'info.txt')
                                product_info = {}
                                if os.path.exists(info_path):
                                    with open(info_path, 'r', encoding='utf-8') as f:
                                        for line in f:
                                            if ':' in line:
                                                key, value = line.split(':', 1)
                                                product_info[key.strip().lower()] = value.strip()
                                else:
                                    with open(info_path, 'w', encoding='utf-8') as f:
                                        f.write("era: \nstatus: \n")
                                    print(f"Created missing 'info.txt' in {product_path}")

                                images = sorted([
                                    os.path.join(product_path, f).replace(SRC_DIR, '.').lstrip('/') 
                                    for f in os.listdir(product_path) 
                                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
                                ])
                                
                                if images:
                                    product_slug = f"{brand}-{designer}-{product_name}".lower().replace(' ', '-')
                                    product_data = {
                                        'brand': brand,
                                        'designer': designer,
                                        'product_name': product_name,
                                        'images': images,
                                        'thumbnail': images[0],
                                        'html_file': f"{product_slug}.html",
                                        'era': product_info.get('era', ''),
                                        'status': product_info.get('status', '')
                                    }
                                    products.append(product_data)
    print(f"Found {len(products)} products.")

    for product in products:
        html_content = create_article_html(product)
        output_path = os.path.join(OUTPUT_DIR, product['html_file'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    print(f"Generated {len(products)} article pages.")

    for static_dir in STATIC_DIRS:
        src_path = os.path.join(SRC_DIR, static_dir)
        dest_path = os.path.join(OUTPUT_DIR, static_dir)
        if os.path.exists(src_path):
            shutil.copytree(src_path, dest_path)
    print("Copied static assets.")

    # Copy CNAME file if it exists
    cname_path = os.path.join(SRC_DIR, 'CNAME')
    if os.path.exists(cname_path):
        shutil.copy(cname_path, OUTPUT_DIR)
        print("Copied CNAME file.")

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(OUTPUT_DIR):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    # Updated size to KB
    total_size_kb = f"{round(total_size / 1024)}KB"

    stats = {
        "product_count": len(products),
        "last_updated": build_time,
        "total_size": total_size_kb
    }

    index_html = create_index_html(products, stats)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("Generated index.html.")

    print("Build complete! Output is in the 'public' directory.")

if __name__ == '__main__':
    main()
