from app import App, AppCode
from component import BaseComponent
from factory import BaseFactory
import sys

class ComponentFactory(BaseFactory[BaseComponent]):
    _module = ['menu', 'tetris']
    _mapping = {
        'menu': 'MenuStructure',
        'game': 'Tetris'
    }

def main(args):
    app = App('FTetris', 400, 600)
    name = 'menu'
    kwords = {"screen": app.screen}

    while True:
        app.set_component(ComponentFactory.create(name, kwords))
        app.component.set_theme('assets/default.theme')

        match app.run():
            case AppCode.QUIT:
                sys.exit()
            case AppCode.EXIT:
                match name:
                    case 'menu':
                        sys.exit()
                    case 'game':
                        name = 'menu'
                        kwords = {}

            case AppCode.START:
                name = 'game'
                kwords = {'width': 10, 'height': 20}

if __name__ == '__main__':
    main(sys.argv[1:])
