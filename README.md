# SI 664 - Asian Studies Books Project

## Purpose

For my final project in this course, I have created an application that leverages a MySQL database back end and a Django framework front end in order to allow users to discover the global and national reach of a set of Asian studies publications. Originally released over the last several decades, these titles are under consideration by Michigan Publishing Services (part of the University of Michigan Library) for digitization and redistribution as open access publications.

As I am interested in the humanities, academic libraries, publishing, and creating metadata for discovery, this dataset seems a suitable fit for my final project. Putting this data into a database will hopefully allow users to ask more complex questions than previously possible, such as which creators and/or publishers’ books are found in the most libraries or which publication date ranges tend to correspond to a larger global distribution.

## Data set

The underlying data for this application would be comprised of descriptive metadata for the approximately 350 books and additional data about which institutions worldwide have these books in their holdings. As part of an internship last summer, I gathered the library holdings data using the OCLC’s WorldCat Search API, and I also assisted in putting together, checking, and enriching the existing descriptive metadata records. I have been given permission by Michigan Publishing Services to use this data for my project. The raw data for this project is in the form of multiple JSON files, one containing the descriptive metadata, and another containing the results of API calls and technical details about how those calls were crafted.

## Data model

![Data model](/static/img/data_model.png)

Upon creating the data model, I discovered that there are a few complex entity relationships that need to be established. I identified many-to-many relationships between creators and books (a book can have multiple creators, and a creator can create multiple books) and books and holding institutions (a book can be in multiple institutions, and an institution can have multiple books). In total, I have implemented 11 different tables (representing entities or entity relationships). More could be down to extend the model with more geographic tables (possibly reusing data and structures from the SI 664 heritagesites application). This project gave me the chance to explore and work with a many-to-many table that also has a foreign key (the attribution table between creator and book, which also has a foreign key connecting it to the role table). This introduced some complications, but it seemed most accurate to have creator roles be specific to a book (a creator might be an editor for one book and a translator for another).

## Package dependencies

The following is the output of pip list in my virtual environment.

Package                Version   
---------------------- ----------
certifi                2018.11.29
chardet                3.0.4     
coreapi                2.3.3     
coreschema             0.0.4     
defusedxml             0.5.0     
Django                 2.1.4     
django-allauth         0.38.0    
django-cors-headers    2.4.0     
django-crispy-forms    1.7.2     
django-filter          2.0.0     
django-rest-auth       0.9.3     
django-rest-swagger    2.2.0     
djangorestframework    3.9.0     
idna                   2.8       
itypes                 1.1.0     
Jinja2                 2.10      
MarkupSafe             1.1.0     
mysqlclient            1.3.13    
oauthlib               2.1.0     
openapi-codec          1.3.2     
pip                    18.1      
PyJWT                  1.7.1     
python3-openid         3.1.0     
pytz                   2018.7    
PyYAML                 3.13      
requests               2.21.0    
requests-oauthlib      1.0.0     
setuptools             40.6.3    
simplejson             3.16.0    
six                    1.12.0    
social-auth-app-django 3.1.0     
social-auth-core       2.0.0     
uritemplate            3.0.0     
urllib3                1.24.1    
wheel                  0.32.3    
