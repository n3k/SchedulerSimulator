from Scheduler import SystemManager
from UIPlotter import make_plot

def main():
    manager = SystemManager.SystemManager()
    manager.run()
    make_plot(manager)

if __name__ == "__main__":
    main()