{
  "projectName": "synthetichooman/vault",
  "projectRoot": "/Users/kimminpyo/Documents/Obsidian Vault/web dev via figma",
  "sessions": [
    {
      "date": "2025-08-27",
      "summary": "Initial setup, data management, and workflow automation.",
      "changes": [
        {
          "type": "refactor",
          "component": "build.py",
          "summary": "Introduced info.txt for metadata management.",
          "details": "Replaced hardcoded metadata with a system that reads from info.txt in each product folder. The build script now auto-generates a template if the file is missing."
        },
        {
          "type": "feature",
          "component": "build.py",
          "summary": "Added site statistics generation.",
          "details": "The build script now calculates total products, last build time, and total size, displaying them on index.html."
        },
        {
          "type": "feature",
          "component": "start_preview.command",
          "summary": "Automated local development workflow.",
          "details": "Created a command script to run the build and start a local server with a single action."
        }
      ]
    },
    {
      "date": "2025-08-28",
      "summary": "Gallery implementation, major Git repository repair, and CI/CD setup.",
      "changes": [
        {
          "type": "feature",
          "component": "article.html",
          "summary": "Replaced image viewer with Swiper.js gallery.",
          "details": "Modified build.py to generate a Swiper.js-based carousel for article images, improving mobile UX."
        },
        {
          "type": "style",
          "component": "css/style.css",
          "summary": "Updated global fonts and styles.",
          "details": "Changed the global font to a monospace stack and adjusted the main text color opacity. Added a formatted stats bar to the index page."
        },
        {
          "type": "fix",
          "component": ".git",
          "summary": "Corrected critical git repository misconfiguration.",
          "details": "Diagnosed and fixed the root cause of push failures: the git repository was incorrectly initialized in the user's home directory. Guided the user to safely remove the old .git directory and re-initialize it in the correct project subfolder. This resolved all pathing and file tracking issues."
        },
        {
          "type": "ci",
          "component": ".github/workflows/deploy.yml",
          "summary": "Set up automated deployment to GitHub Pages.",
          "details": "Created a new GitHub Actions workflow to build and deploy the site. Subsequently fixed the workflow to handle the project being in a subdirectory of the main git repository, and then corrected it again after the repository structure was fixed."
        }
      ]
    },
    {
      "date": "2025-08-30",
      "summary": "Added site-wide footer, favicon, and standardized titles. Postponed custom domain setup.",
      "changes": [
        {
          "type": "feature",
          "component": "build.py, css/style.css",
          "summary": "Added a site-wide footer with Instagram link.",
          "details": "Added a footer to all pages, styled it to match the header, and included an external link to Instagram."
        },
        {
          "type": "feature",
          "component": "build.py, assets",
          "summary": "Implemented site-wide favicon.",
          "details": "Created an assets directory, configured the build script to copy it, and linked the favicon in the HTML head for all pages."
        },
        {
          "type": "style",
          "component": "build.py",
          "summary": "Standardized site titles and enforced lowercase text rule.",
          "details": "Changed all page titles to a consistent '[brand] - hooman' format and saved a rule to use only lowercase for future frontend text."
        }
      ],
      "todo": [
        {
          "task": "Complete custom domain setup (Gabia)",
          "details": "Guide user through creating a CNAME file, updating build.py to include it, and configuring DNS records (A, CNAME) on Gabia to point to GitHub Pages."
        }
      ]
    },
    {
      "date": "2025-08-31",
      "summary": "Client-side filtering, data model extension, and an extensible Easter egg framework.",
      "changes": [
        {
          "type": "feature",
          "component": "build.py, css/style.css",
          "summary": "Added 'show only available' checkbox filter.",
          "details": "Implemented a checkbox on index.html that uses JavaScript to hide products with a 'sold' status, allowing users to filter the main grid."
        },
        {
          "type": "refactor",
          "component": "build.py",
          "summary": "Extended data model with 'category' field.",
          "details": "Updated the build script to process a new 'category' field from info.txt (top, bottom, etc.) and added a corresponding 'data-category' attribute to each product in the HTML for future filtering enhancements."
        },
        {
          "type": "feature",
          "component": "build.py",
          "summary": "Built an extensible, multi-platform Easter egg framework.",
          "details": "Implemented a scalable system for secret user interactions. The initial implementation includes two eggs: a Matrix-style animation and a red-text toggle. Each has a unique trigger for both keyboard (Konami code variations) and mobile (tap-based triggers on specific elements or the page body). The framework is designed for easy addition of future secrets."
        }
      ]
    }
  ]
}