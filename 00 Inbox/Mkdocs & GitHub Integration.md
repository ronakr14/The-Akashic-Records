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