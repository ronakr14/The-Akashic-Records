---
id: 8e6mu6c1kn31ou42r5ahf2x
title: Template_confi
desc: ''
updated: 1753020830740
created: 1753020785803
---
site_name: The Akashic Records
site_url: https://ronakr14.github.io/The-Akashic-Records/
theme:
  name: material

  language: en

  palette:
    - scheme: default
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
      primary: black
      accent: white
    - scheme: slate 
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode    
      primary: black
      accent: white
    
  features:
    - navigation.tracking
    - navigation.tabs
    - navigation.indexes
    - navigation.sections
    - navigation.top
    - navigation.footer
    - toc.follow
    - toc.integrate
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.annotation
    - content.code.copy

nav:
  - Home: index.md
  - Projects: projects.md
  - Areas: areas.md
  - Resources: resources.md
  - Archive: archive.md
  - Portfolio: https://ronakr14.github.io
  
markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - admonition
  - pymdownx.arithmatex:
      generic: true
  - footnotes
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.mark
  - attr_list
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg

plugins:
  - search:
      lang: en
      separator: '[\s\-,:!=\[\]()"/]+|(?!\b)(?=[A-Z][a-z])|\.(?!\d)|&[lg]t;'

extra:
  consent:
    title: Cookie consent
    description: >- 
      We use cookies to recognize your repeated visits and preferences, as well
      as to measure the effectiveness of our documentation and whether users
      find what they're searching for. With your consent, you're helping us to
      make our documentation better.
  social:
    - icon: fontawesome/brands/github-alt
      link: https://github.com/ronakr14
    - icon: fontawesome/brands/linkedin
      link: https://linkedin.com/in/ronak-rathore05/
    - icon: fontawesome/brands/docker
      link: https://hub.docker.com/u/rastar14
    - icon: fontawesome/brands/python
      link: https://pypi.org/user/RonakR/
    - icon: fontawesome/brands/instagram
      link: https://instagram.com/rastar14/

copyright: |
  &copy; 2025 <a href="https://github.com/ronakr14"  target="_blank" rel="noopener">Ronak Rathore</a>