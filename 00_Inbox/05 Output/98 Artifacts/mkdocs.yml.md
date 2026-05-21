site_name: <site name>
site_url: <site url>

theme:
  name: material

  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.annotation
    - content.code.copy
    - navigation.tracking
    - navigation.indexes
    - navigation.footer
    - toc.follow

  language: en

  palette:
    - scheme: default
      toggle:
        icon: material/toggle-switch-off-outline
        name: Switch to dark mode
      primary: black
      accent: white
    - scheme: slate
      toggle:
        icon: material/toggle-switch
        name: Switch to light mode
      primary: black
      accent: white

plugins:
  - mkdocstrings
  - search:
      lang: en
      separator: '[\\s\\-,:!=\\[\\]()"/]+|(?!\\b)(?=[A-Z][a-z])|\\.(?!\\d)|&[lg]t;'

nav:
  - Home: index.md

extra:
  social:
    - icon: fontawesome/brands/github-alt
      link: <github userid link>
  consent:
    title: Cookie consent
    description: >-
      We use cookies to recognize your repeated visits and preferences, as well
      as to measure the effectiveness of our documentation and whether users
      find what they're searching for. With your consent, you're helping us to
      make our documentation better

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
      separator: '[\\s\\-,:!=\\[\\]()"/]+|(?!\\b)(?=[A-Z][a-z])|\\.(?!\\d)|&[lg]t;'

copyright: |
  &copy; 2024 <a href="<github userid link>"  target="_blank" rel="noopener"><Name></a>