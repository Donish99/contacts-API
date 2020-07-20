# contacts-API

## Made by flask jsonify 

### Full List of Contacts   GET  __'url/display'__
returns list of contacts in database

### Create contact   POST __'url/create'__
body of request
  keys(required):
    name, number, year
returns success message

### Update contact by id   PUT  __'url/edit/(id)'__
body of request
  keys(optional):
    name, number, year 
returns succes message

### Delete contact by id   DELETE  __'url/contact/(id)'__
returns success message

