from modules.loader.core import FileHandler
from modules.app.core import mainApp
from modules.analysis.core import Analyzer

def main():
    file_handler = FileHandler()
    analyzer = Analyzer()
    main_app = mainApp(file_handler=file_handler, analyzer=analyzer)
    
    main_app.mainloop()
    
    
    
if __name__ == "__main__":
    main()