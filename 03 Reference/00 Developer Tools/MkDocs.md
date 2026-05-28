---
id: 1karusxvmvdk4ibes6s1hej
title: Mkdocs
desc: ''
updated: 1753021030083
created: 1753021020237
---
# Static Pages using MKDOCS and Github (Github Pages)

## Prerequisite

- Programming Language - Python
- Python Libraries - mkdocs and its dependencies

## MKDOCS Library

Make sure to install the following using pip:
```
- mkdocs                     1.5.3
- mkdocs-autorefs            1.0.1
- mkdocs-material            9.5.14
- mkdocs-material-extensions 1.3.1
- mkdocstrings               0.24.1
- mkdocstrings-python        1.9.0
```

## Steps

- Navigate to your desired location and run the following command in powershell/commandline:
``` 
mkdocs new <project name>
```
This will create a new folder at your desired location with the provided project name.
This folder will contain following content:
```
- <Project Name>
    - mkdocs.yml
    - docs
        - index.md
```

- Modify mkdocs.yml file by adding the following contents:
```
site_name: <site name>
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

nav:
  - Home: index.md 

extra:
  social:
    - icon: fontawesome/brands/github-alt
      link: <github userid link>

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
      
copyright: |
  &copy; 2024 <a href="<github userid link>"  target="_blank" rel="noopener"><Name></a>
```

- Create New Page:

    All pages should be in markdown language and formatting.<br>
    For Markdown guidelines, visit: [Markdown Guide](https://www.markdownguide.org/)<br>
    Create a new file under docs folder with a 'md' extension.<br>
    These files can be nested and grouped under folders.<br>
    Once file is created, you can add the link of this file in docs/index.md using `[Name](new_page.md)`<br>
    This file can be added in mkdocs.yml under nav to display in navigation bar in website with following structure:
    ```
    Name: new_page.md
    ```

- View Draft:

    To check how your website looks, run:
    ```
    mkdocs serve
    ```
    This will render your website in runtime, so any changes you do in your pages will get reflect here.<br>
    This will help in modify/add contents to your website.

- Build your website:

    Once you are satisfied on how your website looks, its time to build the website.<br>
    Run the following command to build:
    ```
    mkdocs build
    ```
    This will create a new folder named as 'Site' which will contain details and contents to build a static pages.<br>
    These content can be used anywhere to build your website.

- Deployment

    Once mkdocs build command gets complete, add your contents to github repository.<br>
    Initialize a git repository within the project folder.<br>
    Create a gitignore file and add site folder in it. This will avoid having duplicate content in github repository.<br>
    Now, add all the contents in git and commit it.<br>
    Create a github repository with the same project name and push your folder contents to it.<br>
    Now its time to deploy your website using github pages.<br>
    Run the following command:
    ```
    mkdocs gh-deploy
    ```
    This will create a gh_pages branch and push the content of site to it and run the github workflow for deployment.<br>
    After some time, your website will be deployed at the website link which will be provided when you run the mkdocs deploy command.

# Mkdocs

Best use case:  
Fast, Markdown-based documentation sites for developer tools/APIs with simple setup and Git-driven workflows.

Alternative: — [[Docusaurus]] when you need richer UI, versioning, and React-based customization.

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
babel==2.17.0
certifi==2025.1.31
cfgv==3.4.0
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
distlib==0.3.9
filelock==3.17.0
ghp-import==2.1.0
identify==2.6.7
idna==3.10
Jinja2==3.1.5
Markdown==3.7
MarkupSafe==3.0.2
mergedeep==1.3.4
mkdocs==1.6.1
mkdocs-get-deps==0.2.0
mkdocs-material==9.6.4
mkdocs-material-extensions==1.3.1
nodeenv==1.9.1
packaging==24.2
paginate==0.5.7
pathspec==0.12.1
platformdirs==4.3.6
pre_commit==4.1.0
Pygments==2.19.1
pymdown-extensions==10.14.3
python-dateutil==2.9.0.post0
PyYAML==6.0.2
pyyaml_env_tag==0.1
regex==2024.11.6
requests==2.32.3
six==1.17.0
urllib3==2.3.0
virtualenv==20.29.2
watchdog==6.0.0


```table-of-contents
```
# Prerequisite
- Programming Language - Python
- Python Libraries - mkdocs and its dependencies

# MKDOCS Library
Make sure to install the following using pip:
versions can be recent.

```
- mkdocs                     1.5.3
- mkdocs-autorefs            1.0.1
- mkdocs-material            9.5.14
- mkdocs-material-extensions 1.3.1
- mkdocstrings               0.24.1
- mkdocstrings-python        1.9.0
```

# Steps

1. Navigate to your desired location and run the following command in CLI tool

```
mkdocs new <project name>
```

This will create a new folder at your desired location with the provided project name. This folder will contain following content:

```
- <Project Name>
    - mkdocs.yml
    - docs
        - index.md
```

2. Modify [[mkdocs.yml]] file by adding the custom configurations or copy same file

3. Create New Page:
	1. All pages should be in markdown language and formatting.
    2. For Markdown guidelines, visit: [Markdown Guide](https://www.markdownguide.org/)   
    3. Create a new file under docs folder with a ‘md’ extension.    
    4. These files can be nested and grouped under folders.    
    5. Once file is created, you can add the link of this file in docs/index.md using `[Name](new_page.md)`    
    6. This file can be added in mkdocs.yml under nav to display in navigation bar in website with following structure: `Name: new_page.md`

4. View Draft:
	1. To check how your website looks, run: `mkdocs serve` This will render your website in runtime, so any changes you do in your pages will get reflect here.
	2. This will help in modify/add contents to your website.

5. Build your website:    
	1. Once you are satisfied on how your website looks, its time to build the website.
	2. Run the following command to build: `mkdocs build` This will create a new folder named as ‘Site’ which will contain details and contents to build a static pages.
	3. These content can be used anywhere to build your website.

6. Deployment:
	1. Once mkdocs build command gets complete, add your contents to github repository.
	2. Initialize a git repository within the project folder.
	3. Create a gitignore file and add site folder in it. This will avoid having duplicate content in github repository.
	4. Now, add all the contents in git and commit it.
	5. Create a github repository with the same project name and push your folder contents to it.
	6. Now its time to deploy your website using github pages.
	7. Run the following command: `mkdocs gh-deploy` This will create a gh_pages branch and push the content of site to it and run the github workflow for deployment.
	8. After some time, your website will be deployed at the website link which will be provided when you run the mkdocs deploy command.

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