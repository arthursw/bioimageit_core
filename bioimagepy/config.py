# -*- coding: utf-8 -*-
"""BioImagePy config module.

This module contains classes that allows to read
and manage configuration parameters

Example
-------
    You need to use the ConfigManager which is a singleton to read config

    >>> # first call to load the configuration
    >>> ConfigManager("config.json")
    >>> # or
    >>> ConfigManager.instance().load("config.json")
    >>>
    >>> # then to access the config variables
    >>> var = ConfigManager.instance().get('keyname')

Classes
------- 
Config
ConfigManager

"""

import os
import json

class ConfigKeyNotFoundError(Exception):
   """Raised when key is not found in the config"""
   pass

class Config():
    """Allows to access config variables
    
    The configuration can be instantiate manually but the
    usage is to instantiate it with the singloton ConfigManager

    Parameters
    ----------
    config_file
        File where the configuration is stored in JSON format

    Attributes
    ----------
    var
        Dictionnary containing the config variables
    
    
    """
    def __init__(self, config_file:str=''):
        self.config_file = config_file
        self.var = None
        if config_file is not '':
            self.load(config_file)

    def load(self, config_file:str):
        """Read the metadata from the a json file"""
        self.config_file = config_file
        if os.path.getsize(self.config_file) > 0:
            with open(self.config_file) as json_file:  
                self.var = json.load(json_file)     

    def is_key(self, key:str) -> bool:
        """Check if a key exists in the config dictionnary
        
        Parameters
        ----------
        key
            Key to check

        Returns
        -------
        bool
            True if the key exists, False otherwise    
        
        """
        if key in self.var:
            return True
        else:
            return False    

    def get(self, key:str) -> dict:
        """Read a variable from the config dictionnary

        Parameters
        ----------
        key
            Key of the variable to read

        Returns
        -------
        Value of the config variable   

        Raises
        ------
        ConfigKeyNotFoundError: if the configuration key does not exists 

        """
        if key in self.var:
            return self.var[key]
        else:
            raise ConfigKeyNotFoundError('No key ' + key + ' in the config')          


class ConfigManager:
    """Singleton to access the Config

    Parameters
    ----------
    config_file
        JSON file where the config is stored

    Raises
    ------
    Exception: if multiple instanciation of the Config is tried

    """
    __instance = None

    def __init__(self, config_file:str):
        """ Virtually private constructor. """
        if ConfigManager.__instance != None:
            raise Exception("ConfigManager can be initialized only once!")
        else:
            ConfigManager.__instance = Config(config_file)

    @staticmethod 
    def instance():
        """ Static access method to the Config. """
        if ConfigManager.__instance == None:
            ConfigManager.__instance = Config()
        return ConfigManager.__instance     
    