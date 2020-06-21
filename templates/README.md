# Database tables templates


Version 0.5 (2020-03-21)\
(C) 2020 Przemyslaw Zbroch


This is the documentation for django html templates in this folder. The following templates are available:

* main.html
* menu.html
* table.html
* table_info.html
* table_edit.html

All templates can be used to represent the data from any database in various forms described later on.

## main.html

This template wraps other templates in standard html tags. Should not be called directly from django views, but from other templates that extend it. Requires `/static/css/style.css` file to be available in the django server to include styles. Also a `title` string key should be delivered in template input dictionary which will be used as a html page title shown in browser title bar and/or website tab.
This template also includes four blocks that optionally can by extended by other templates:

* menu block
* table block
* table_info block
* table_edit block

If any of the mentioned blocks will be omitted in the extending template it will simply be not shown.

## menu.html

This template is used for a website containing the menu only. It extends `main.html` template with the `menu` block. The following keys used in this template should be delivered with the template dictionary from django view:

* `title` string used for the webpage name (described in `main.html` template docstrings)
* `menu` dictionary with the following keys:
    * `title` - title of the menu or website. Will be placed above the menu table.
    * `width` - a width of the menu table. Should be corresponding to the styles.css file classes of `tabX` where `X` is a table width in percents. Example:
        * `{'menu': {'width': '50'}}` - this will set the table to use css class `tab50` to set the table style (in the original css file `tab50` class contains only `width: 50%;` parameter and there are other classes for `tab10`, `tab20` and so on up to `tab100`).
    * `options` - a tuple of menu options. They will be used as names in the menu (converted to uppercase) and also as clickable links (converted to lowercase) with the pattern of `/option/`.
* `menupage` - optional parameter containing a string which should correspond to the `title` of one of the menu options. If this is specified then the particular menu option will be highlited.

Example:
```
data = {'title': 'MOVIES DB',
        'menu': {'title':'MOVIE DATABASE','width':'50','options':('Movies','Persons','Genres','Search-movie')},
        'menupage': 'Movies'}
```
When such data will be passed to the template it will generate a website named `MOVIES DB` with menu on top of the page with `MOVIE DATABASE` title and a 50% width with four positions and `Movies` highlited.

## table.html

This template is dedicated for usage with any data received from the database that then will be put into a table. This template also contains optional filtering of the data in table and possibility to add buttons with links at the bottom. Also the buttons with links can be added in the first column of every table row. This template extends `main.html` template with optional `menu` block and `table` block. The following keys used in this template should be delivered with the template dictionary from django view:

* `menu` dictionary can be used the same as described in `menu.html` template docstrings. It is optional - if won't be provided no menu will be displayed on page.
* `menupage` string can be used the same as described in `menu.html` template docstrings
* `title` string which will be used as a page name (as described in `main.html` docstrings) and also as a title of the table containing data which will be shown above the table with `:` characted added at the end of the title string.
* `width` string - a width of the table containing the data. The usage is the same as the `menu.width` described in the `menu.html` docstrings.
* `headers` tuple containing strings of table headers. Number of tuple positions should be the same as predicted data columns received from the database. If any column should not have a header a simple empty string can be used. If you plan to use icons with links for every table position then you need to add a first column for that purpose and then use `icons` parameter described later on.
* `aligns` tuple containing string keywords corresponding to every column of the table and describing the text align for this column. The allowed values are the same as used in html/css style parameters for `text-align` variable. This is not an optional argument. If no aligns should be used every tuple position needs to be filled with an empty string! Mostly used aligns will be `left`, `right` and `center`. The prerequisite for this function is a custom template tag named `zip` and defined in `/templatetags/custom_tags.py` library.
* `sorts` tuple of strings.  This is optional key which allows to put sorting controls on top of selected columns. The strings in the tuple represent the variable under which the pressed sorting button will pass it's value. There should be a variable for every column - if any column does not need to have sorting controls then simply use an empty string in its place. The possible sorting values passed under the variables are the following:
    * `^` indicates ascending order
    * `v` indicates descending order
    * `=` indicates no order
* `filters` tuple containing dictionaries. When used, it creates a text form fields on top of every column which then pass the input data as a POST form. The intention is to use those form fields input to filter the data generated to the table from the database. This is optional parameter - if it will not be included in the data passed to the template the row with forms will not be shown. Te number of dictionaries included in this tuple must correspond to the number of columns in the table. If any column should not have filter form field at the top an empty dictionary should be put in it's corresponding place. Every dictionary can have the following keys:
    * `type` string indicating the type of filter. Currently there are two:
        * `text` - one text field with one variable - one input form will be shown on top of the column
        * `2texts` - two text fields with two variables - may be used for numeric-data columns which may filter based on "from - to" range - two input forms will be shown on top of the column.
    * `variable` string (for `text` filter type) or tuple of two strings (for `2texts` filter type). Used to establish the variable name which will be gained from the POST form after submitting the input from that form-field. This variable can be then used in the view code while getting the data from the database.
    * `label` string (for `text` filter type) or tuple of two strings (for `2texts` filter type). Used as a placeholder text in the form field. It is optional.
    * `value` string (for `text` filter type) or tuple of two strings (for `2texts` filter type). Used to pass any predefined field value that will be put into this input-form. It can be used to keep the form field data user has input previously. It is also optional.
* `icons` tuple of dictionaries. This is optional key. If used it will generate first column of the table with provided icons and desired clickable links. The following keys must be passed within every dictionary:
    * `icon` - name of the icon file. This file must be accessible in the `/static/` path on the django server and have a `.png` extension. This name will also be included in image alternate name and a title
    * `link` - a link under the icon. Should not contain the trailing `/` character as it will be added automatically followed by the `id` of the table position. This `id` value needs to be provided in `values` as a first position on every row-list which will be described later on.
* `icons` parameter has two prerequisites:
    * A column header should be reserved for it in the beginning of `headers` list.
    * An `id` value of every database position must be the first value passed for every row data from the database in the `values` list of lists described later on. This `id` will be attached to every link provided in the `icons` dictionary.
* `values` list of lists. This is the main key. It should contain all the data gathered from the database. Every in-list is a representation of one row from the database. The resulting table will have as many rows as in-lists provided in the mother-list. If you plan to use icons with links in the first column of the table then the first value on every in-list must be the `id` of a database record - this way every action under the icon-link will contain the `id` of this record so every link will correspond to operations on this record. Predefined icons that are currently in the `/static/` folder are:
    * `info` - an info icon, can be used to link to the record detailed information view
    * `edit` - an edit icon, can be used to link to the record editing view
    * `delete` - a delete icon, can be used to link to the record deletion view
* `buttons` tuple of dictionaries. Those are optional buttons with links that can be put under the table to link to any other views if needed. If no such key will be provided then no buttons will appear. Every dictionary represents one button and should contain the following keys:
    * `name` - a string containing the text to be put on the button
    * `link` - a link that the button will redirect to using GET method

Example:
```
values = []
for movie in movies:
    value = []
    value.append(movie.id)
    value.append(movie.title)
    value.append(movie.year)
    value.append(movie.director.first_name + ' ' + movie.director.last_name)
    value.append(movie.rating)
    values.append(value)

data = {
        'menu': menu,
        'menupage': 'Movies',
        'title': 'Movies',
        'width': '80',
        'headers': ('','Title','Year','Director','Rating'),
        'aligns': ('center','left','center','left','center'),
        'sorts': ('','title_sort','year_sort','director_sort','rating_sort'),
        'filters': ({},
                    {'type': 'text', 'variable': 'title', 'label': 'filter', 'value': title},
                    {'type': '2texts', 'variable': ('year_from','year_to'), 'label': ('from','to'), 'value': (year_from,year_to)},
                    {'type': '2texts', 'variable': ('first_name','last_name'), 'label': ('first name','last name'), 'value': (first_name,last_name)},
                    {'type': '2texts', 'variable': ('rating_from','rating_to'), 'label': ('from','to'), 'value': (rating_from,rating_to)}),
        'icons': ({'icon':'info','link':'/movie-details'},
                  {'icon':'edit','link':'/edit-movie'},
                  {'icon':'delete','link':'/del-movie'}),
        'values': values,
        'buttons': ({'name':'ADD MOVIE','link':'/add-movie'},)
}
```

## table_info.html

This table template is intended for usage with one record from the database. It contains two columns - one for labels assigned to the values gathered from the database and another column for the particular values. It also can contain optional buttons with any links at the bottom. This template extends `main.html` template with optional `menu` block and `table_info` block. The following keys used in this template should be delivered with the template dictionary from django view:

* `menu` dictionary can be used the same as described in `menu.html` template docstrings. It is optional - if won't be provided no menu will be displayed on page.
* `menupage` string can be used the same as described in `menu.html` template docstrings
* `title` string which will be used as a page name (as described in `main.html` docstrings) and also as a title of the table containing data which will be shown above the table with `:` characted added at the end of the title string.
* `width` string - a width of the table containing the data. The usage is the same as the `menu.width` described in the `menu.html` docstrings.
* `header` string - any text that will be put into the single header of the table. For example it can be the name of the record being viewed.
* `values` dictionary - this is the main key. It should contain a dictionary from which the keys will be put in the first column and the corresponding values in the second column. The values can be any strings, also multiline. This is optional key - if for some reason no values are needed in the table (like maybe when only displaying some message) it can just be omitted.
* `message` string - any string that will be displayed at the bottom of the table. It can be used for any comments or maybe error messages that may show up while gathering the data from the database. If no message is needed it should contain an empty string.
* `buttons` tuple of dictionaries. Used the same as described in the `table.html` docstrings.

Example:
```
values = {}
values['Year:'] = movie.year
values['Director:'] = movie.director.first_name + ' ' + movie.director.last_name

data = {
        'menu': menu,
        'menupage': 'Movies',
        'title': 'Movie Details',
        'width': '50',
        'header': movie.title,
        'values': values,
        'message': '',
        'buttons': ({'name':'EDIT THIS MOVIE','link':'/edit-movie/'+str(id)},
                    {'name':'BACK','link':'/movies'})
}
```


## table_edit.html

This table template is similar to `table_info.html` but it allows to edit the desired record data gathered from the database. It also contains two columns - one for labels assigned to the values gathered from the database and another column for the particular values in the form fields. It contains a predefined form-submit button at the bottom and also can contain optional buttons with any links. This template extends `main.html` template with optional `menu` block and `table_edit` block. The following keys used in this template should be delivered with the template dictionary from django view:

* `menu` dictionary can be used the same as described in `menu.html` template docstrings. It is optional - if won't be provided no menu will be displayed on page.
* `menupage` string can be used the same as described in `menu.html` template docstrings
* `title` string which will be used as a page name (as described in `main.html` docstrings) and also as a title of the table containing data which will be shown above the table with `:` characted added at the end of the title string.
* `width` string - a width of the table containing the data. The usage is the same as the `menu.width` described in the `menu.html` docstrings.
* `header` string - any text that will be put into the single header of the table. For example it can be the name of the record being edited.
* `values` dictionary of dictionaries. This is a main key with data of the record from the database with additional variables which allow to modify this record. The keys of this dictionary are any strings, but the values of those keys must be dictionaries with the following keys:
    * `variable` - this is the variable name under which the data input from the corresponding form field will be passed with the POST method.
    * `options` (optional) - if this key is specified then the form field becomes a "select" type form, not the plain "text" form. It lets to choose a value from the predefined list. This key must be a list or a tuple which contain any number of dictionaries which represent the options to chose from the drop-down list in the form. The data structure of every dictionary is the following:
        * `id` - id of the position on the list - it is passed with the variable from the form.
        * `desc` - description or the name of the position on the list\
    * `data` (optional) - a string which represent the data to be put in the field - can be used to pre-fill the form-field with the data from the database to be then edited. If omitted the empty form field will appear. If the form is a "select" type then the `id` of the pre-selected option can be specified here.
    * `checkbox` (optional) - boolean field which specifies a checkbox-type field. A variable returns `on` string when checked. If the checkbox needs to be pre-checked this key should contain `True`. For an empty checkbox should be `False`.
    * `type` (optional) - string field that may indicate another special form fields. Currently it recognizes the following:
        * `date` - a date field supported by most browsers with pop-up calendar.
* `message` string - any string that will be displayed at the bottom of the table. It can be used for any comments or maybe error messages that may show up while operating on the database. If no message is needed it should contain an empty string.
* `buttons` tuple of dictionaries. Used the same as described in the `table.html` docstrings.

Example:
```
persons = []
pers = Person.objects.all().order_by('first_name')
for per in pers:
    person = {}
    person['id'] = per.id
    person['desc'] = per.first_name + ' ' + per.last_name
    persons.append(person)

values = {}
values['Title:'] = {'variable': 'title', 'data': movie.title}
values['Director:'] = {'variable': 'director_id', 'data': movie.director.id, 'options': persons}
values['Active:'] = {'variable': 'active', 'checkbox': False}
values['Date:'] = {'variable': 'date', 'type': 'date', 'data': movie.date}

data = {
        'menu': menu,
        'menupage': 'Movies',
        'title': 'Edit Movie',
        'width': '50',
        'header': movie.title,
        'values': values,
        'message': message,
        'buttons': ({'name':'DELETE','link':'/del-movie/'+str(id)},
                    {'name':'MOVIE DETAILS','link':'/movie-details/'+str(id)},
                    {'name':'BACK','link':'/movies'},)
}
```
