import os
import json

class TreeNode:
    
    parentNode: object
    subMenu: dict
    childs: list

    def __init__(self,parent: object,data: dict) -> None:
        self.parentNode = parent
        if 'childs' in data.keys():    
            data.pop('childs')
        self.subMenu = data
        self.childs = []

    def add_child(self,child:object) -> None:
        self.childs.append(child)

    def find_childs(self,data: dict) -> None:
        if 'childs' in data.keys() and len(data['childs']) != 0:
            for sub in data['childs']:
                newChild = TreeNode(self,sub.copy())
                newChild.find_childs(sub)
                self.add_child(newChild)

class Menu:

    filePath: str
    banner: str
    _currentNode: TreeNode
    _input_data: dict

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

        self.__loop()

        return self._input_data

    def resume(self) -> dict:
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
                action = currentNode.subMenu['action']
                if action == 'return':
                    break
                if action == 'back':
                    currentNode = currentNode.parentNode
                if action == 'continue':
                    currentNode.childs[0]

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
        parentNode.find_childs(firstMenu)

        return parentNode

    # Fetch json file
    def __fetch_struct_file(self) -> dict:
        with open(self.filePath,"r") as file:
            data = json.load(file)

        return data

    # Clear screen
    def __cls(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    # Options menu
    def __options_menu(self,node: TreeNode) -> int:
        data = node.subMenu

        inp = -1
        while inp<0 or inp > len(node.childs):
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
        if "info" not in data.keys() or "struct" not in data.keys():
            return False

        return True  