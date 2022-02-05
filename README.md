# <div align="center">PyEasyMenu</div>

# <div align="center">:warning:THIS PROJECT IS IN AN EARLY DEVELOPMENT STAGE AND IT'S NOT AVAILABLE WITH PIP:warning:</div>

<div align="center">easyMenu is a python package used to easily create complex cmd menus just by writing a <a href="#json">json file</a></div>

## Content

- ### <a href="#install">How to install</a>
- ### <a href="#how">How to use</a>
- ### <a href="#json">JSON structure</a>

<div id="install"></div>

## How to install

Open  your cmd and type:

```python
pip install PyEasyMenu
```

<div id="how"></div>

## How to use

First of all you need to import the package by adding this to your python file:

```python
from PyEasyMenu import Menu
```
Then you need to create a Menu object instance passing the path of the JSON file as an argument by doing:

```python
instance = Menu("structure.json")
```

You can also define the path of a text file containing your banner:

```python
instance = Menu("structure.json",bannerPath="banner.txt")
```

After creating the object you can start the menu with the start() method, that will return when a <a href="#actions">'return' action</a> is met

```python
data = instance.start()
```

<div id="json"></div>

## Json structure

```json
{
    "struct": {
        "banner": "{Bool value}",
        "childs":[
            {
                "name":"{Displayed name}",
                "type":"{Menu type}",
                "valueName" : "{Value name in case of input}",
                "childs":[...]
            },
        ]
    }
}
```

## Global menu variables

This fields are needed in every menu 

Field name |Required|Description| Data type
:---------:|:------------:|-----------|:--------:|
name|:white_check_mark:| The name of the menu|str
type|:white_check_mark:|Specify the <a href="#">menu type</a>|str
banner|:x:| Print the banner (default true) | bool
action|:x:|<a href="#actions">Action</a> after menu (default continue)|str
return|:x:|If true return to the menu call (default false)|bool

## Menu types

Menu type |  Description |
:--------:|--------------|
options|Ask the user to choose among the child menus
<a href="#input">input</a>| Ask the user for an input
<a href="#custom">custom</a>|Show custom text
return|Exit from the menu and return all the store values
back| Go back to the previous menu (exit the program in case of main menu)

<a id="input"></a>

## Input menu

> Ask the user for an input

```json
{
    "name": "Input example",
    "type": "input",
    "inputs":[
        {
            "prompt": "Name: ",
            "keyName": "name"
        },
        {
            "prompt": "Surname: ",
            "keyName": "surname"
        }
    ],
    "childs": [...]
}
```

### Fields

Field Name | Required |Description|Data type
:---------:|:--------:|-----------|:----:
keyName| :white_check_mark:|The key name of the response dict containing  the inputs| str
inputs|:white_check_mark:|The list of inputs that you want to ask| list

### Inputs structure
> The items inside the "inputs" field

```json
{
    "prompt": "Your name: ",
    "keyName": "name"
}
```

Field Name | Required |Description|Data type
:---------:|:--------:|-----------|:----:
prompt|:white_check_mark:|The prompt asked when asking for the input| str
keyName|:white_check_mark:|The key name of the input value in the response dict| str

<div id="custom"></div>

## Custom menu

> A menu with custom text in it

### Fields

Field Name | Required |Description|Data type
:---------:|:--------:|-----------|:----:
content|:white_check_mark:|The content of the menu|str
prompt|:x:|The prompt showed while waiting for an input(default '...')|str

:warning:Note:warning:: The menu will wait for a key press and will execute what's stated in the <a href="#actions">'action'</a> field

<div id="actions"></div>

## Actions
> Actions define the behaviour of the program after the menu is completed

Name|Description
:---:|:---------:
back|Return to the parent menu
continue|Go to the first child menu
stay|Does not change the menu

### Note:
The "continue" action does not change the behaviour of the "options" menu
