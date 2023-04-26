<div align="center">

# PhishTales
[![Report Issue on Jira](https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software)]([https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/DT/issues](https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/PHT/issues))
[![Deploy Docs](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml)
[![Documentation Website Link](https://img.shields.io/badge/-Documentation%20Website-brightgreen)](https://phishtales.net/aboutProject)


</div>


## Keywords

Section 704, Phishing, Machine Learning

## Project Abstract

The project was is a program and integrated web app and extension that inputs a URL and outputs a binary classification indicating if a URL is a phishing scam. From a user's point of view, the process is as simple as inputting a URL or, in the case of a browser extension, clicking a button. The output provides the reliability score of the website in question. The project uses machine learning to predict whether a URL is malicious or not.

![image](https://user-images.githubusercontent.com/70736675/232888073-d0f4e223-d67c-4968-a0f3-a35a0066a622.png)


## Installation Instructions

### ML Model
The machine learning model is written and implemented within the phish_tales_run.py program. The model was generated with 20000 phishing links and 20000 legitimate links. A DecisionTreeClassifier was used to the train the data after feature extraction was performed. The model is saved as model.pkl, and able to be used in other programs.

### Front End, locally hosted
For this, you just need to run the following to get all libraries needed:

`pip -r requirements.txt`

After that, in a command line, run the following:

`python -m flask --app app run`

The output should provide you with the IP to navigate to for the website.


### Chrome Extension

The extension can be accessed inside the extension folder. To load the unpacked extension, you can navigate to Settings>Extensions>Load unpacked and then select the extension folder.

## Conceptual Design

This project mainly used python, as it has many packages and libraries used for data science and machine learning. Models such as K—nearest neighbor, decision trees, naïve bayes, and support vector machines were be used for classification and trying to find the right model. XGBoost, polyfit, and linregress were be used for regression, with regplot from seaborn used to visualize data. These models can be obtained from NumPy, SciPy, pandas, matplotlib, and scikit-learn packages freely available using pip. Python3 was used for the actual data preprocessing, model training, model testing, an model evaluation. To implement a web app and extension, HTML, JavaScript, and CSS were be used. This creates a simple interface that detects the current web URL, passes it through the ML model, and outputs a classification and regression value indicating the reliability of the website in question. HTML and CSS were be used to build and style the extension, while JavaScript simply deals with user-interaction.

## Background

This tool checks URLs for domain squatting-- which is when a common website is registered under a different domain (ex: registering apple.io vs apple.com), URL hijacking-- which takes common website domain typos and registers them to make a website appear to be legitimate (ex: goggle.com vs google.com), also checking other details in the URL such as its length, the number of subdomains in the URL, and the Top-Level Domain (TLD). The project will also check the domain name and its IP address to see if it is blacklisted in any commonly known phishing databases (ex: https:openphish.com/phishing_database.html). Page-based features will be checked to determine how reliable the website seems, websites (ex: PageRank and AWS) can be used for reference data. Finally, content-based features can parse through the code used to develop the website and detect the reliability of said website. All these features combined use a decision-tree ML algorithm to create a score that assesses the likelihood that a given URL is a phishing scam or not. While other projects exist that use similar ideologies, this project employs updated models and uses newly updated data to train these models. With all of the different features used to create a predicted output, this project has potential to be more accurate than similar projects.

## Required Resources

Resources required for this project can be obtained with a simple internet connection and the ability to access open-source python libraries. Hardware requirements are quite simple as the model will be built on a well-equipped machine and further testing will not require much computing power. Software requirements are the ability to run python files, chrome browser, and either MacOS, Windows, or Linux.

## Collaborators

[//]: # ( readme: collaborators -start )
<table>
<tr>
    <td align="center">
        <a href="https://github.com/anthonyjromann">
            <img src="https://avatars.githubusercontent.com/u/76930172?v=4" width="100;" alt="Ant"/>
            <br />
            <sub><b>Anthony Roman</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/alishahidd">
            <img src="https://avatars.githubusercontent.com/u/76089708?v=4" width="100;" alt="ali"/>
            <br />
            <sub><b>Ali Shahid</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/trau3">
            <img src="https://avatars.githubusercontent.com/u/70736675?v=4" width="100;" alt="thomas"/>
            <br />
            <sub><b>Thomas Rau</b></sub>
        </a>
        </td>
    <td align="center">
        <a href="https://github.com/douedra1">
            <img src="https://avatars.githubusercontent.com/u/50376645?v=4" width="100;" alt="DJ"/>
            <br />
            <sub><b>Djakaridja Ouedraogo</b></sub>
        </a>
    </td>
    </td></tr>
</table>

[//]: # ( readme: collaborators -end )
