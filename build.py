import os
import shutil
import json
from datetime import datetime

# --- CONFIGURATION ---
SRC_DIR = '.'
ARCHIVE_DIR = os.path.join(SRC_DIR, 'archive')
OUTPUT_DIR = os.path.join(SRC_DIR, 'public')
STATIC_DIRS = ['css', 'js', 'archive']

# --- HTML TEMPLATES ---

def create_index_html(products, stats):
    # --- Create Product Grid Items and Extract Filter Data ---
    list_items = []
    all_sizes = set()
    all_categories = set()
    for product in products:
        status = product.get('status', '').lower()
        category = product.get('category', 'other').lower()
        size = product.get('size', 'n/a').lower()
        
        all_categories.add(category)
        if size != 'n/a':
            all_sizes.add(size)
        
        # Create a searchable string
        search_text = f"{product['brand']} {product['designer']} {product['product_name']} {product.get('era', '')}".lower()

        list_items.append(f'''
            <a href="{product['html_file']}" class="vault-item-link" data-status="{status}" data-category="{category}" data-size="{size}" data-search="{search_text}">
                <div class="vault-item">
                    <img src="{product['thumbnail']}" alt="{product['product_name']}" loading="lazy">
                </div>
            </a>''')
    
    stats_text = f'{stats["product_count"]} articles, {stats["last_updated"]}, {stats["total_size"]}'

    # --- Create Filter UI ---
    available_filter_html = '''
        <div class="filter-controls">
            <input type="checkbox" id="available-only-filter" name="available-only-filter">
            <label for="available-only-filter">show only available</label>
        </div>
    '''

    category_filter_html = '<div id="category-filter" class="filter-controls" style="display: none;">'
    category_filter_html += '<span class="filter-label">category</span>'
    for cat in sorted(list(all_categories)):
        category_filter_html += f'''<span class="filter-option">
            <input type="checkbox" id="cat-{cat}" name="category-filter" value="{cat}">
            <label for="cat-{cat}">{cat}</label>
        </span>'''
    category_filter_html += '</div>'

    size_filter_html = '<div id="size-filter" class="filter-controls" style="display: none;">'
    size_filter_html += '<span class="filter-label">size</span>'
    for size in sorted(list(all_sizes)):
        size_filter_html += f'''<span class="filter-option">
            <input type="checkbox" id="size-{size}" name="size-filter" value="{size}">
            <label for="size-{size}">{size}</label>
        </span>'''
    size_filter_html += '</div>'

    # --- Create JS ---
    script_html = '''
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const vaultItems = document.querySelectorAll('.vault-item-link');
            const noResultsMessage = document.getElementById('no-results-message');

            // --- Filter Logic ---
            const availableCheckbox = document.getElementById('available-only-filter');
            const searchInput = document.getElementById('search-input');

            availableCheckbox.addEventListener('change', updateFilters);
            searchInput.addEventListener('input', updateFilters);
            document.querySelectorAll('input[name="category-filter"]').forEach(box => box.addEventListener('change', updateFilters));
            document.querySelectorAll('input[name="size-filter"]').forEach(box => box.addEventListener('change', updateFilters));

            function updateFilters() {
                const showOnlyAvailable = availableCheckbox.checked;
                const searchQuery = searchInput.value.toLowerCase();
                const selectedCategories = Array.from(document.querySelectorAll('input[name="category-filter"]:checked')).map(cb => cb.value);
                const selectedSizes = Array.from(document.querySelectorAll('input[name="size-filter"]:checked')).map(cb => cb.value);

                let visibleItemsCount = 0;

                vaultItems.forEach(item => {
                    const status = item.dataset.status;
                    const category = item.dataset.category;
                    const size = item.dataset.size;
                    const searchText = item.dataset.search || '';
                    
                    const availableMatch = !showOnlyAvailable || !status.startsWith('sold');
                    const searchMatch = searchText.includes(searchQuery);
                    const categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category);
                    const sizeMatch = selectedSizes.length === 0 || selectedSizes.includes(size);

                    if (availableMatch && searchMatch && categoryMatch && sizeMatch) {
                        item.style.display = 'block';
                        visibleItemsCount++;
                    } else {
                        item.style.display = 'none';
                    }
                });

                noResultsMessage.style.display = visibleItemsCount === 0 ? 'block' : 'none';
            }

            // --- Easter Egg Framework ---
            const easterEggs = {
                matrix: { keyboard: ['arrowup', 'arrowup', 'arrowdown', 'arrowdown', 'arrowleft', 'arrowright', 'arrowleft', 'arrowright', 'b', 'a'], mobile: { type: 'tap_anywhere', count: 13 }, callback: triggerMatrixRain },
                red_text: { keyboard: ['arrowup', 'arrowup', 'arrowdown', 'arrowdown', 'arrowleft', 'arrowright', 'arrowleft', 'arrowright', 'a', 'b'], mobile: { type: 'tap_element', elementId: 'welcome-trigger', count: 10 }, callback: toggleRedText },
                advanced_filters: { keyboard: ['arrowleft', 'arrowleft', 'arrowleft', 'arrowright'], mobile: { type: 'toggle_element', elementId: 'available-only-filter', count: 4 }, callback: toggleAdvancedFilters }
            };

            // Keyboard Listener
            let keyHistory = [];
            document.addEventListener('keydown', (e) => {
                keyHistory.push(e.key.toLowerCase());
                if (keyHistory.length > 10) keyHistory.shift();
                for (const egg in easterEggs) {
                    if (keyHistory.join('').endsWith(easterEggs[egg].keyboard.join(''))) {
                        easterEggs[egg].callback();
                        keyHistory = [];
                        return;
                    }
                }
            });

            // Mobile Listeners
            let tapAnywhereCount = 0, lastTapAnywhere = 0;
            let tapElementCount = 0, lastTapElement = 0;
            let toggleCount = 0, lastToggle = 0;
            const tapTimeout = 800; // ms

            document.addEventListener('click', (e) => {
                const now = new Date().getTime();
                if (!e.target.closest('a, button, input, label')) {
                    if (now - lastTapAnywhere > tapTimeout) tapAnywhereCount = 1; else tapAnywhereCount++;
                    lastTapAnywhere = now;
                    if (tapAnywhereCount >= easterEggs.matrix.mobile.count) {
                        tapAnywhereCount = 0;
                        easterEggs.matrix.callback();
                    }
                }
                if (e.target.id === easterEggs.red_text.mobile.elementId) {
                    if (now - lastTapElement > tapTimeout) tapElementCount = 1; else tapElementCount++;
                    lastTapElement = now;
                    if (tapElementCount >= easterEggs.red_text.mobile.count) {
                        tapElementCount = 0;
                        easterEggs.red_text.callback();
                    }
                }
            });
            
            const toggleTrigger = document.getElementById(easterEggs.advanced_filters.mobile.elementId);
            if (toggleTrigger) {
                toggleTrigger.addEventListener('change', () => {
                    const now = new Date().getTime();
                    if (now - lastToggle > tapTimeout * 2) toggleCount = 1; else toggleCount++;
                    lastToggle = now;
                    if (toggleCount >= easterEggs.advanced_filters.mobile.count) {
                        toggleCount = 0;
                        easterEggs.advanced_filters.callback();
                    }
                });
            }
        });

        // --- Easter Egg Effect Functions ---
        function toggleAdvancedFilters() {
            const catFilter = document.getElementById('category-filter');
            const sizeFilter = document.getElementById('size-filter');
            if (catFilter && sizeFilter) {
                const isHidden = catFilter.style.display === 'none';
                catFilter.style.display = isHidden ? 'block' : 'none';
                sizeFilter.style.display = isHidden ? 'block' : 'none';
            }
        }

        function triggerMatrixRain() { /* ... existing function ... */ }
        function toggleRedText() { /* ... existing function ... */ }

        function triggerMatrixRain() {
            if (document.querySelector('.matrix-canvas')) return;
            const canvas = document.createElement('canvas');
            canvas.classList.add('matrix-canvas');
            document.body.appendChild(canvas);
            const ctx = canvas.getContext('2d');
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '9999';
            canvas.style.pointerEvents = 'none';
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const alphabet = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const rainDrops = [];
            for (let x = 0; x < columns; x++) { rainDrops[x] = 1; }
            let animationFrameId;
            const duration = 10000;
            const startTime = Date.now();
            const draw = () => {
                if (Date.now() - startTime > duration) {
                    cancelAnimationFrame(animationFrameId);
                    if (document.body.contains(canvas)) document.body.removeChild(canvas);
                    return;
                }
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#0F0';
                ctx.font = fontSize + 'px monospace';
                for (let i = 0; i < rainDrops.length; i++) {
                    const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                    ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                    if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) rainDrops[i] = 0;
                    rainDrops[i]++;
                }
                animationFrameId = requestAnimationFrame(draw);
            };
            draw();
        }

        function toggleRedText() {
            const styleId = 'red-text-easter-egg';
            if (!document.getElementById(styleId)) {
                const style = document.createElement('style');
                style.id = styleId;
                style.innerHTML = `.red-text-mode, .red-text-mode * { color: red !important; }`;
                document.head.appendChild(style);
            }
            document.body.classList.toggle('red-text-mode');
        }
    </script>
    '''

    # --- Final HTML Assembly ---
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>vault - hooman</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="/favicon.ico" sizes="any">
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
            <a href="contact.html">recruit</a>
        </nav>
        {available_filter_html}
        {category_filter_html}
        {size_filter_html}
        <div class="vault-grid">
            {'' .join(list_items)}
        </div>
        <div id="no-results-message" style="display: none; text-align: center; padding: 40px 20px; font-size: 0.9rem; color: #888;">sell me one @hooman.log</div>
    </main>
    <div class="search-bar-container">
        <input type="search" id="search-input" placeholder="search...">
    </div>
    <footer class="main-footer">
        <div class="footer-bar">
            <p>suggestions for corrections and image redistribution are <span id="welcome-trigger">welcome</span></p>
            <p><a href="https://instagram.com/synthetic.hooman" target="_blank" rel="noopener noreferrer">instagram</a></p>
        </div>
    </footer>
    {script_html}
</body>
</html>'''

def create_article_html(product):
    slides_html = ''
    for image_path in product['images']:
        slides_html += f'            <div class="swiper-slide"><img src="{image_path}" alt="{product["product_name"]}"></div>\n'

    era = product.get('era', '')
    status = product.get('status', '')
    shop_link = product.get('shop_link', '')

    details_html = f"""<p>{product['brand']}</p>
            <p>{product['designer']}</p>
            <p>{era}</p>
            <p>{status}</p>"""

    if shop_link:
        details_html += f'\n            <p><a href="{shop_link}" target="_blank" rel="noopener noreferrer">buy now</a></p>'


    # NOTE: The curly braces for the Swiper JS init are escaped by doubling them (e.g., {{...}})
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['brand']} - hooman</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
    <link rel="icon" href="/favicon.ico" sizes="any">
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
            {details_html}
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
                                
                                # Read existing info.txt
                                if os.path.exists(info_path):
                                    with open(info_path, 'r', encoding='utf-8') as f:
                                        for line in f:
                                            if ':' in line:
                                                key, value = line.split(':', 1)
                                                product_info[key.strip().lower()] = value.strip()
                                
                                images_files = sorted([f for f in os.listdir(product_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])

                                if images_files:
                                    # Determine update_date from the first image's modification time
                                    first_image_path = os.path.join(product_path, images_files[0])
                                    update_date = datetime.fromtimestamp(os.path.getmtime(first_image_path)).strftime('%Y-%m-%d')
                                    
                                    # Update info.txt if needed
                                    info_changed = False
                                    if product_info.get('update_date') != update_date:
                                        product_info['update_date'] = update_date
                                        info_changed = True
                                    if 'shop_link' not in product_info:
                                        product_info['shop_link'] = ''
                                        info_changed = True

                                    if info_changed:
                                        with open(info_path, 'w', encoding='utf-8') as f:
                                            for key, value in product_info.items():
                                                f.write(f"{key}: {value}\n")
                                        print(f"Updated 'info.txt' in {product_path}")

                                    images = [os.path.join(product_path, f).replace(SRC_DIR, '.').lstrip('/') for f in images_files]

                                    product_slug = f"{brand}-{designer}-{product_name}".lower().replace(' ', '-')
                                    product_data = {
                                        'brand': brand,
                                        'designer': designer,
                                        'product_name': product_name,
                                        'images': images,
                                        'thumbnail': images[0],
                                        'html_file': f"{product_slug}.html",
                                        **product_info # Add all info from the txt file
                                    }
                                    products.append(product_data)
    print(f"Found {len(products)} products.")

    # Sort products by update_date (newest first)
    products.sort(key=lambda p: p.get('update_date', '1970-01-01'), reverse=True)

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

    # Copy favicon.ico file if it exists
    favicon_path = os.path.join(SRC_DIR, 'favicon.ico')
    if os.path.exists(favicon_path):
        shutil.copy(favicon_path, OUTPUT_DIR)
        print("Copied favicon.ico.")

    # Copy other static html files
    static_html_files = ['contact.html']
    for html_file in static_html_files:
        src_path = os.path.join(SRC_DIR, html_file)
        if os.path.exists(src_path):
            shutil.copy(src_path, OUTPUT_DIR)
            print(f"Copied {html_file}.")

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

    # --- SEO File Generation ---
    generate_seo_files(products, "https://hooman.kr")

    print("Build complete! Output is in the 'public' directory.")

# --- SEO FILE GENERATION ---
def generate_seo_files(products, domain):
    # Create robots.txt
    robots_content = f"""User-agent: *\nAllow: /\nSitemap: {domain}/sitemap.xml"""
    with open(os.path.join(OUTPUT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("Generated robots.txt.")

    # Create sitemap.xml
    sitemap_urls = []
    sitemap_urls.append(f"    <url><loc>{domain}/</loc></url>") # Add homepage
    for product in products:
        url = f"{domain}/{product['html_file']}"
        sitemap_urls.append(f"    <url><loc>{url}</loc></url>")
    
    sitemap_urls_string = "\n".join(sitemap_urls)
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls_string}
</urlset>"""
    with open(os.path.join(OUTPUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml.")


if __name__ == '__main__':
    main()
