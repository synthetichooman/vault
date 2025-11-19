# Project Architecture

This document outlines the architecture of the static portfolio website. The project is built using a Python script that acts as a static site generator.

## Core Concept

The project follows a static site generator pattern. A Python script (`build.py`) reads content and metadata from a structured directory (`/archive`), combines it with HTML templates defined within the script, and generates a complete, ready-to-deploy static website in the `/public` directory. There is no database or server-side rendering at runtime.

## Directory Structure

-   **`/` (Root)**: Contains the source code and configuration.
    -   `build.py`: The core Python script that builds the entire site.
    -   `archive/`: Contains the raw content (products). The structure is `[brand]/[designer]/[product_name]/`.
        -   `info.txt`: A key-value text file with product metadata (e.g., `status`, `category`, `size`).
        -   `*.webp`: Product images.
    -   `css/style.css`: The main stylesheet for the website. This is a source file that is copied directly by the build script.
    -   `contact.html`: A static HTML page for contact information. This is also a source file.
    -   `public/`: The output directory for the generated website. **This directory should not be edited directly**, as it is completely overwritten by `build.py`.
    -   `architecture.md`: This file.
    -   `protocol.md`: A file for logging project history for AI assistants.
    -   `CNAME`, `favicon.ico`: Static assets for domain configuration and site icon.

## Build Process (`build.py`)

1.  **Initialization**: The script starts by deleting the existing `/public` directory to ensure a clean build.
2.  **Content Discovery**: It recursively scans the `/archive` directory, identifying each product folder. For each product, it reads the metadata from `info.txt` and gathers all associated image paths.
3.  **HTML Generation**:
    -   **Article Pages**: For each product, it generates a dedicated HTML page (e.g., `public/rick-owens-blistered-lambskin-jacket.html`) using the `create_article_html` function. This function embeds the product's images and metadata into an HTML structure.
    -   **Index Page**: It generates the main `public/index.html` using the `create_index_html` function. This page includes a grid of all products and a sophisticated client-side filtering and search functionality written in JavaScript.
4.  **Asset Copying**: The script copies all directories listed in `STATIC_DIRS` (currently `css`, `js`, `archive`, `assets`) from the root to the `/public` directory. This is why changes to `css/style.css` are permanent.
5.  **Static File Copying**: It copies root-level static files like `contact.html`, `CNAME`, and `favicon.ico` into `/public`.
6.  **SEO**: It generates `robots.txt` and `sitemap.xml` in the `/public` directory for search engine optimization.

## Key Features & Recent Changes (as of 2025-11-13)

### 1. Client-Side Filtering

-   The main `index.html` page features a JavaScript-powered filtering system.
-   **"Now Available" Filter**:
    -   This checkbox (`#available-only-filter`) is now **checked by default** upon page load.
    -   The JavaScript function `updateFilters()` is called immediately on page load to apply this default filter, showing only items whose `data-status` does not begin with "sold".
-   Other filters include "For Sale", category, and size, which are dynamically generated based on the metadata of all products.

### 2. "Sold" Item Styling

-   Items marked with a `status` containing "sold" in their `info.txt` are given the `.sold-item` class in the HTML.
-   The styling for these items in `css/style.css` has been updated:
    -   The previous "frosted glass" effect (`backdrop-filter`) was removed to prevent the image from appearing too white.
    -   It now applies a direct blur to the image: `filter: blur(1px);`.
    -   A `3px` solid white inner border (`border: 3px solid #ffffff;`) is applied to the item's container.
    -   When a user hovers over a sold item, the blur effect is removed to show the clear image.

### 3. Recruitment Page Update

-   The recruitment drive has been closed.
-   The content of `contact.html` has been replaced with the message "금번의 모집은 마감되었습니다."
-   The "recruit" link in the navigation has been hidden using `style="display:none;"`. This change was applied in two places:
    -   In `build.py`, for the link on the main `index.html`.
    -   In the source `contact.html` file, for the link on the contact page itself.