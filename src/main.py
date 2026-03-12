from modules.loader.core import FileHandler
from modules.app.core import mainApp

def main():
    file_handler = FileHandler()
    main_app = mainApp(file_handler=file_handler)
    
    main_app.mainloop()
    
    
    
if __name__ == "__main__":
    main()