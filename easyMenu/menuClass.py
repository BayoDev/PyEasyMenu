from lib2to3.pytree import Node
import os
import json
from tkinter import N
from unittest import expectedFailure

from pexpect import ExceptionPexpect
from urllib3 import Retry

class TreeNode:
    
    parentNode: object
    subMenu: dict
    childs: list

    def __init__(self,parent: object,data: dict) -> None:
        self.parentNode = parent
        childsNum = None
        if 'childs' in data.keys():    
            childsNum = len(data['childs'])
            data['childs'] = []
        self.subMenu = data
        self.childs = []
        if self.parentNode != None:
            self.__check_error(data,childsNum)

    def add_child(self,child:object) -> None:
        self.childs.append(child)

    def parse_childs(self,data: dict) -> None:
        if 'childs' in data.keys() and len(data['childs']) != 0:
            for sub in data['childs']:
                newChild = TreeNode(self,sub.copy())
                newChild.parse_childs(sub)
                self.add_child(newChild)

    def find_child(self,search: dict) -> object:
        if len(search.keys()) == 0:
            return None

        found = True
        for key in search.keys():
            if key not in self.subMenu.keys() or self.subMenu[key] != search[key]:
                found = False

        if found:
            return self

        if len(self.childs) == 0:
            return None

        for node in self.childs:
            result = node.find_child(search)
            if result != None:
                return result

        return None


    def __check_error(self,data:dict,childsNum: int) -> None:
        rules = {
            'allowedTypes':['options','input','custom','return','back'],
            'allowedActions':['back','continue','stay'],
            'globals': ['name','type'],
            'options':['childs'],
            'input': ['keyName','inputs'],
            'inputs':['prompt','keyName'],
            'custom':['content'],
            'return':[],
            'back':[]
        }

        for key in rules['globals']:
            if key not in data.keys():
                raise Exception(f"Missing '{key}' in:\n{data}")

        if data['type'] == 'back':
            return

        if data['type'] not in rules['allowedTypes']:
            raise Exception(f'Non existent type in:\n{data}')

        if 'action' in data.keys():
            if data['action'] not in rules['allowedActions']:
                raise Exception(f"Non existent action in:\n{data}")
            if data['action'] == 'continue' and (childsNum == 0 or childsNum == None):
                raise Exception(f'Action continue but no childs found in:\n{data}')

        if 'action' not in data.keys() and (childsNum == 0 or childsNum == None):
            raise Exception(f"Default action is 'continue' so element must have at least one child:\n{data}")

        for key in rules[data['type']]:
            if key not in data.keys():
                raise Exception(f"Missing required '{key}' field for {data['type']} in:\n{data}")

        # Exception handling for options menu
        if data['type'] == 'options':
            if (childsNum == 0 or childsNum == None):
                raise Exception(f'Options menu type must have at least one child element:\n{data}')

        # Exception handling for input menu
        if data['type'] == 'input':
            for input in data['inputs']:
                for field in rules['inputs']:
                    if field not in input.keys():
                        raise Exception(f"Missing required '{field}' field for 'inputs' item in:\n{data}")

        return

class Menu:

    filePath: str
    banner: str
    _currentNode: TreeNode
    _input_data: dict
    _root: TreeNode

    def __init__(self,filePath,bannerPath=None) -> None:

        # Check if file is valid
        if not self.__check_if_valid(filePath):
            raise Exception(f"File at {filePath} is not valid")

        banner = None
        if bannerPath!=None:
            try:
                with open(bannerPath,"r") as file:
                    banner = file.read()
            except:
                raise Exception(f"Unable to fetch the banner at {bannerPath}")

        if banner != None:
            self.banner = banner
        else:
            self.banner = None

        self.filePath = filePath
        self._currentNode = None
        self._input_data = {}

        return

    # --- Public methods ---

    def start(self) -> dict:

        try:
            data = self.__fetch_struct_file()
        except:
            raise Exception("Something went wrong while fetching the struct file")

        self._currentNode = self.__parse_data(data)

        self._currentNode.subMenu['type'] = 'options'

        self._root = self._currentNode

        self.__loop()

        return self._input_data

    def resume(self,search: dict = None) -> dict:
        if search != None:
            result = self._root.find_child(search)
            if result != None:
                self._currentNode = result
            else:
                raise Exception(f"Search with {search} parameters returned 0 results")

        self.__loop()
        return self._input_data

    def __loop(self) -> None:
        
        response = self._input_data
        currentNode = self._currentNode

        while True:
            
            if currentNode.subMenu['type'] == 'options':
                currentNode = currentNode.childs[self.__options_menu(currentNode)-1]

            if currentNode.subMenu['type'] == 'input':
                response[f"{currentNode.subMenu['keyName']}"] = self.__input_menu(currentNode,response)
                ret = self.__have_to_return(currentNode)
                if 'action' in currentNode.subMenu: 
                    action = currentNode.subMenu['action']
                else:
                    action = 'continue'
                if action == 'back':
                    currentNode = currentNode.parentNode
                if action == 'continue':
                    currentNode = currentNode.childs[0]
                if ret:
                    break

            if currentNode.subMenu['type'] == 'custom':
                self.__custom_menu(currentNode)
                ret = self.__have_to_return(currentNode)
                if 'action' in currentNode.subMenu: 
                    action = currentNode.subMenu['action']
                else:
                    action = 'continue'
                if action == 'back':
                    currentNode = currentNode.parentNode
                if action == 'continue':
                    currentNode = currentNode.childs[0]
                if ret:
                    break

            if currentNode.subMenu['type'] == 'return':
                break
            
            if currentNode.subMenu['type'] == 'back':
                if currentNode.parentNode.parentNode != None:
                    currentNode = currentNode.parentNode.parentNode
                else:
                    break

        self._input_data = response
        self._currentNode = currentNode

        return

    # --- Private methods ---

    # Parse the menus in a tree structure
    def __parse_data(self,data: dict) -> TreeNode:

        firstMenu = data['struct']
        parentNode = TreeNode(None,firstMenu.copy())
        parentNode.parse_childs(firstMenu)

        return parentNode

    # Fetch json file
    def __fetch_struct_file(self) -> dict:
        with open(self.filePath,"r") as file:
            data = json.load(file)

        return data

    # Clear screen
    def __cls(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    # Check if it has to return
    def __have_to_return(self,node:TreeNode) -> bool:
        if 'return' in node.subMenu.keys() and node.subMenu['return']:
            return True
        return False

    # Options menu
    def __options_menu(self,node: TreeNode) -> int:
        data = node.subMenu

        inp = -1
        while inp<=0 or inp > len(node.childs):
            self.__cls()

            self.__print_banner(data)
            
            for idx,child in enumerate(node.childs):
                    print(f"\t[{idx+1}]{child.subMenu['name']}")

            inp =  int(input("\n >>"))

        return inp

    # Input menu
    def __input_menu(self,node:TreeNode,resp: dict) -> None:
        data = node.subMenu

        self.__cls()

        self.__print_banner(data)

        response = {}

        for inp in data['inputs']:
            
            response[f"{inp['keyName']}"] = input(f"\t{inp['prompt']} ")

            print("")

        return response

    # Custom menu
    def __custom_menu(self,node:TreeNode) -> None:
        data = node.subMenu

        self.__cls()

        self.__print_banner(data)

        print(data['content']+"\n")

        if 'prompt' in data.keys():
            input(data['prompt'])
        else:
            input("...")

        return

    # Print banner
    def __print_banner(self,data:dict) -> None:
        if self.banner != None:
            if 'banner' not in data.keys() or data['banner']:
                print("\n"+self.banner+"\n")

    # Check if the file is valid
    def __check_if_valid(self,filePath) -> bool:

        # Check if file exists
        if not os.path.isfile(filePath):
            return False

        # Check if is a valid json file
        try:
            with open(filePath,"r") as file:
                data = json.load(file)
        except:
            return False

        # Check if structure is valid
        if "struct" not in data.keys():
            return False

        return True  