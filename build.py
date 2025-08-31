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
    # --- Create Product Grid Items ---
    list_items = []
    all_sizes = set()
    for product in products:
        status = product.get('status', '').lower()
        category = product.get('category', '').lower()
        size = product.get('size', 'n/a').lower()
        if size != 'n/a':
            all_sizes.add(size)
        
        list_items.append(f'''
            <a href="{product['html_file']}" class="vault-item-link" data-status="{status}" data-category="{category}" data-size="{size}">
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

    size_filter_html = '<div id="size-filter" class="filter-controls" style="display: none;">'
    size_filter_html += '<span class="filter-label">size:</span>'
    for size in sorted(list(all_sizes)):
        size_filter_html += f'''
            <input type="checkbox" id="size-{size}" name="size-filter" value="{size}">
            <label for="size-{size}">{size}</label>
        '''
    size_filter_html += '</div>'

    # --- Create JS ---
    script_html = f'''
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // --- Available Filter Logic ---
            const availableCheckbox = document.getElementById('available-only-filter');
            const vaultItems = document.querySelectorAll('.vault-item-link');
            availableCheckbox.addEventListener('change', updateFilters);

            // --- Size Filter Logic ---
            const sizeFilterContainer = document.getElementById('size-filter');
            const sizeCheckboxes = document.querySelectorAll('input[name="size-filter"]');
            sizeCheckboxes.forEach(box => box.addEventListener('change', updateFilters));

            function updateFilters() {{
                const showOnlyAvailable = availableCheckbox.checked;
                const selectedSizes = Array.from(document.querySelectorAll('input[name="size-filter"]:checked')).map(cb => cb.value);

                vaultItems.forEach(item => {{
                    const status = item.dataset.status;
                    const size = item.dataset.size;
                    
                    const availableMatch = !showOnlyAvailable || status !== 'sold';
                    const sizeMatch = selectedSizes.length === 0 || selectedSizes.includes(size);

                    if (availableMatch && sizeMatch) {{
                        item.style.display = 'block';
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});
            }}

            // --- Easter Egg Framework ---
            const easterEggs = {{
                matrix: {{ keyboard: ['arrowup', 'arrowup', 'arrowdown', 'arrowdown', 'arrowleft', 'arrowright', 'arrowleft', 'arrowright', 'b', 'a'], mobile: {{ type: 'tap_anywhere', count: 13 }}, callback: triggerMatrixRain }},
                red_text: {{ keyboard: ['arrowup', 'arrowup', 'arrowdown', 'arrowdown', 'arrowleft', 'arrowright', 'arrowleft', 'arrowright', 'a', 'b'], mobile: {{ type: 'tap_element', elementId: 'welcome-trigger', count: 10 }}, callback: toggleRedText }},
                size_filter: {{ keyboard: ['arrowleft', 'arrowleft', 'arrowleft', 'arrowright'], mobile: {{ type: 'toggle_element', elementId: 'available-only-filter', count: 4 }}, callback: toggleSizeFilter }}
            }};

            // Keyboard Listener
            let keyHistory = [];
            document.addEventListener('keydown', (e) => {{
                keyHistory.push(e.key.toLowerCase());
                if (keyHistory.length > 10) keyHistory.shift();
                for (const egg in easterEggs) {{
                    if (keyHistory.join('').endsWith(easterEggs[egg].keyboard.join(''))) {{
                        easterEggs[egg].callback();
                        keyHistory = [];
                        return;
                    }}
                }}
            }});

            // Mobile Listeners
            let tapAnywhereCount = 0, lastTapAnywhere = 0;
            let tapElementCount = 0, lastTapElement = 0;
            let toggleCount = 0, lastToggle = 0;
            const tapTimeout = 800; // ms

            document.addEventListener('click', (e) => {{
                const now = new Date().getTime();
                // Listener for tap anywhere (Matrix)
                if (!e.target.closest('a, button, input, label')) {{
                    if (now - lastTapAnywhere > tapTimeout) tapAnywhereCount = 1; else tapAnywhereCount++;
                    lastTapAnywhere = now;
                    if (tapAnywhereCount >= easterEggs.matrix.mobile.count) {{
                        tapAnywhereCount = 0;
                        easterEggs.matrix.callback();
                    }}
                }}
                // Listener for welcome trigger (Red Text)
                if (e.target.id === easterEggs.red_text.mobile.elementId) {{
                    if (now - lastTapElement > tapTimeout) tapElementCount = 1; else tapElementCount++;
                    lastTapElement = now;
                    if (tapElementCount >= easterEggs.red_text.mobile.count) {{
                        tapElementCount = 0;
                        easterEggs.red_text.callback();
                    }}
                }}
            }});
            
            // Listener for toggle checkbox (Size Filter)
            const toggleTrigger = document.getElementById(easterEggs.size_filter.mobile.elementId);
            if (toggleTrigger) {{
                toggleTrigger.addEventListener('change', () => {{
                    const now = new Date().getTime();
                    if (now - lastToggle > tapTimeout * 2) toggleCount = 1; else toggleCount++;
                    lastToggle = now;
                    if (toggleCount >= easterEggs.size_filter.mobile.count) {{
                        toggleCount = 0;
                        easterEggs.size_filter.callback();
                    }}
                }});
            }}
        }});

        // --- Easter Egg Effect Functions ---
        function toggleSizeFilter() {{
            const filter = document.getElementById('size-filter');
            if (filter) {{
                const isHidden = filter.style.display === 'none';
                filter.style.display = isHidden ? 'block' : 'none';
            }}
        }}

        function triggerMatrixRain() {{ /* ... existing function ... */ }}
        function toggleRedText() {{ /* ... existing function ... */ }}

        function triggerMatrixRain() {{
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
            for (let x = 0; x < columns; x++) {{ rainDrops[x] = 1; }}
            let animationFrameId;
            const duration = 10000;
            const startTime = Date.now();
            const draw = () => {{
                if (Date.now() - startTime > duration) {{
                    cancelAnimationFrame(animationFrameId);
                    if (document.body.contains(canvas)) document.body.removeChild(canvas);
                    return;
                }}
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#0F0';
                ctx.font = fontSize + 'px monospace';
                for (let i = 0; i < rainDrops.length; i++) {{
                    const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                    ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                    if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) rainDrops[i] = 0;
                    rainDrops[i]++;
                }}
                animationFrameId = requestAnimationFrame(draw);
            }};
            draw();
        }}

        function toggleRedText() {{
            const styleId = 'red-text-easter-egg';
            if (!document.getElementById(styleId)) {{
                const style = document.createElement('style');
                style.id = styleId;
                style.innerHTML = `.red-text-mode, .red-text-mode * {{ color: red !important; }}`;
                document.head.appendChild(style);
            }}
            document.body.classList.toggle('red-text-mode');
        }}
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
        {available_filter_html}
        {size_filter_html}
        <div class="vault-grid">
            {'' .join(list_items)}
        </div>
    </main>
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
                                        f.write("era: \nstatus: \ncategory: \nsize: \n")
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
                                        'status': product_info.get('status', ''),
                                        'category': product_info.get('category', 'other'),
                                        'size': product_info.get('size', 'n/a')
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
