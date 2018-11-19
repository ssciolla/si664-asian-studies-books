# Asian Studies Books and Library Holdings Analysis

## Purpose

For my final project in this course, I would like to create an application that leverages a MySQL database back end and a Django framework front end in order to allow users to discover the global and national reach of a set of Asian studies publications. Originally released over the last several decades, these titles are under consideration by Michigan Publishing Services (part of the University of Michigan Library) for digitization and redistribution as open access publications.

As I am interested in the humanities, academic libraries, publishing, and creating metadata for discovery, this dataset seems a suitable fit for my final project. Putting this data into a database will hopefully allow users to ask more complex questions than previously possible, such as which creators and/or publishers’ books are found in the most libraries or which publication date ranges tend to correspond to a larger global distribution.

## Data set

The underlying data for this application would be comprised of descriptive metadata for the approximately 350 books and additional data about which institutions worldwide have these books in their holdings. As part of an internship last summer, I gathered the library holdings data using the OCLC’s WorldCat Search API, and I also assisted in putting together, checking, and enriching the existing descriptive metadata records. I have been given permission by Michigan Publishing Services to use this data for my project. The raw data for this project is in the form of multiple JSON files, one containing the descriptive metadata, and another containing the results of API calls and technical details about how those calls were crafted.

## Data model

![Data model](/static/img/data_model.png)

Upon creating the data model, I discovered that there are a few complex entity relationships that need to be established. I identified many-to-many relationships between creators and books (a book can have multiple creators, and a creator can create multiple books) and books and holding institutions (a book can be in multiple institutions, and an institution can have multiple books). In total, I have identified 10 different tables (representing entities or entity relationships). It would make sense to connect this data with the country_area data from the heritagesites project, which would add an additional six tables to the database. In the submitted entity model, I tried to work out all these relationships as best I could, but some questions remain. I was a bit uncertain how to handle the relationship between books and series; I decided to create an intermediate table called series_membership between them, since the volume number did not seem to fit (be fully dependent on) either the series or book entity.

## Package dependencies
