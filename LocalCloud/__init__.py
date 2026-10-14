from LocalCloud.CallBackFilter.Handlers import Handlers
from LocalCloud.Client.Managers.EventsManager.EventsManager import EventsManager
from LocalCloud.Client.Managers.FunctionsManager.FunctionsManager import FunctionsManager
from LocalCloud.Client.Managers.FileManager.FileManager import FileManager
from LocalCloud.Client.Managers.VariablesManager.VariablesManager import VariablesManager
from LocalCloud.Client.Server.Server import Server
from LocalCloud.Client.Managers.FileManager import Exceptions as FileManagerExceptions
from LocalCloud.Client.Managers.FileManager import Types as FileManagerTypes
from LocalCloud.Client.Managers.VariablesManager import Types as VariablesManagerTypes
from LocalCloud.Client.Managers.EventsManager import Types as EventManagerTypes
from LocalCloud.Client.Managers.FunctionsManager import Types as FunctionsManagerTypes


def get_all_handlers():
    handler = Handlers([])
    handler+=FileManager.get_file_handlers()
    handler+=FileManager.get_folder_handlers()
    handler+=FunctionsManager.get_handlers()
    handler+=EventsManager.get_handlers()
    return handler