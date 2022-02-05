

# JSON STRUCTURE

```json
{
    "info":{
        "authors" : [{
            "name" : "{Author name}",
            "nickname" : "{Author nickname}",
            "links" : ["{Author links}",...]
        }],
        "license": "{License type}",
        "version": "{Version number}",
    },
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

# Global menu variables

This fields are needed in every menu 

Field name |Required|Description| Data type
:---------:|:------------:|-----------|:--------:|
name|:white_check_mark:| The name of the menu|str
type|:white_check_mark:|Specify the <a href="#">menu type</a>|str
banner|:x:| Print the banner (default true) | bool
action|:x:|<a href="#actions">Action</a> after menu (default continue)|str

# Menu types

Menu type |  Description |
:--------:|--------------|
<a href="#options">options</a>|Ask the user to choose among the child menus
<a href="#input">input</a>| Ask the user for an input
<a href="#return">return</a>|Exit from the menu and return all the store values
<a href="#back">back</a>| Go back to the previous menu (exit the program in case of main menu)

<a id="options"></a>
# Options Menu

> Ask user to choose between the childs menus

## Fields

Field Name | Required |Description
:---------:|:--------:|-----------
Name|:white_check_mark:| The name of the menu
Value Name|:x:|

<a id="input"></a>
# Input menu

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

## Fields

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

<div id="actions"></div>

## Actions
> Actions define the behaviour of the program after the menu is completed

Name|Description
:---:|:---------:
return|Return to the menu start/resume call
back| Return to the parent menu
continue|Go to the first child menu

### Note:
The "continue" action does not change the behaviour of the "options" menu
