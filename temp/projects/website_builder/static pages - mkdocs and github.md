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
