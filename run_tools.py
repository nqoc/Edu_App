import os
from threading import Thread

def subcall(app):
    match app:
        case 'The Balancer':
            name = 'The_Balancer'
        case 'Atom Finder':
            name = 'Atom_Finder'
        case 'Function Drawer':
            name = 'Function_Drawer'
        case 'EQNs Solver':
              name = 'eqns'
    os.system(os.getcwd()+r'\tools'+rf'\{name}.exe')
def call(app):
     Thread(target=lambda:subcall(app)).start()