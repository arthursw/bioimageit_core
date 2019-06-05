# -*- coding: utf-8 -*-
"""BioImagePy metadata definitions.

This module contains classes that allows to describe the
metadata of scientific data, dataset 

Classes
------- 
BiData
BiRawData
BiProcessedData
BiDataSet
BiRawDataSet
BiProcessedDataSet


"""
from .core import BiObject
import json
import errno
import os
import ntpath
 
class BiMetaData(BiObject):
    """Abstract class that store a data metadata
    
    BiMetaData allows to read/write the metadata to file. This class
    should not be used directly.

    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """

    def __init__(self, md_file_url : str):

        self._objectname = "BiMetaData"
        self._md_file_url = md_file_url
        self.metadata = {}
        if os.path.isfile(md_file_url):
            self.read()
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), md_file_url) 

    def md_file_name(self) -> str:
        """get metadata file name (ie without the path)

        Returns
        ----------
        str
            The name of the metadata file

        """

        ntpath.basename(self._md_file_url)

    def md_file_path(self) -> str:
        """get metadata file directory name

        Returns
        ----------
        str
            The name of the metadata file directory

        """
        abspath = os.path.abspath(self._md_file_url)
        return os.path.dirname(abspath)

    def dir(self) -> str:
        """get metadata file directory name

        Returns
        ----------
        str
            The name of the metadata file directory

        """

        abspath = os.path.abspath(self._md_file_url)
        return os.path.dirname(abspath)    

    def read(self):
        """Read the metadata from the a json file at md_file_url"""
        if os.path.getsize(self._md_file_url) > 0:
            with open(self._md_file_url) as json_file:  
                self.metadata = json.load(json_file)

    def write(self):
        """Write the metadata to the a json file at md_file_url"""
        with open(self._md_file_url, 'w') as outfile:
            json.dump(self.metadata, outfile, indent=4)    

    def display(self):
        """Display inherited from BiObject"""

        super(BiMetaData, self).display()  


class BiData(BiMetaData): 
    """Abstract class that store a data metadata
    
    BiData allows to manipulate the common metadata. This class
    should not be used directly. BiRawData and BiProcessedData
    should be used as specific metadata containers

    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """

    def __init__(self, md_file_url : str):

        BiMetaData.__init__(self, md_file_url)
        self._objectname = "BiData"  

    def url(self) -> str:
        """get the data file
        
        This function returns the obsolute full path (or url) of 
        the data file. It is computed usting the metadata file path 

        Returns
        ----------
        str
            The path (or url) of the metadata file 

        """

        file = self.metadata["common"]['url']
        if os.path.isfile(file):
            return file
        else:    
            return os.path.join(self.md_file_path(), file)

    def url_as_stored(self) -> str:
        """get the data file
        
        This function returns the data file path as stored in the 
        metadata file. This path can be relative or absolute depending
        on how the metadata file was filled

        Returns
        ----------
        str
            The path (or url) of the metadata file 

        """

        return self.metadata["common"]['url']   

    def name(self) -> str:
        """get the data name

        Returns
        ----------
        str
            The data name

        """

        return self.metadata["common"]['name']  

    def author(self) -> str:
        """get the author name

        Returns
        ----------
        str
            The author name

        """

        return self.metadata["common"]['author']   

    def createddate(self) -> str:
        """get the created date

        Returns
        ----------
        str
            The created date

        """

        return self.metadata["common"]['createddate']          

    def origin_type(self):
        """get the origin type

        Returns
        ----------
        str
            The origin type

        """

        return self.metadata["origin"]['type'] 

    def thumbnail_as_stored(self):
        """get the data thumbnail

        Returns
        ----------
        str
            The thumbnail url

        """
        if 'thumbnail' in self.metadata["common"]:
            return self.metadata["common"]['thumbnail'] 
        else:
            return ''

    def thumbnail(self):
        file = self.thumbnail_as_stored()  
        if file == '' or os.path.isfile(file):
            return file
        else:    
            return os.path.join(self.md_file_path(), file)      

    def display(self):
        """Display inherited from BiObject"""

        super(BiData, self).display()  
        print('Data: ' + self._md_file_url)
        print('Common ---------------')
        print('Name: ' + self.metadata["common"]['name'])
        print('Url: ' + self.metadata["common"]['url'])
        print('Author: ' + self.metadata["common"]['author'])
        print('Datatype: ' + self.metadata["common"]['datatype'])
        print('Created Date: ' + self.metadata["common"]['createddate'])
        print('Origin ---------------')    
        print('Type: ' + self.metadata["origin"]['type'])
        

class BiRawData(BiData):
    """Class to store and manipulate RawData metadata
  
    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """

    def __init__(self, md_file_url : str):

        self._objectname = "BiRawData"
        BiData.__init__(self, md_file_url)

    def tag(self, key: str):
        """get a tag value

        Parameters
        ----------
        key
            Tag name

        Returns
        ----------
        str
            The tag value for tag key

        """

        if 'tags' in self.metadata:
            if key in self.metadata['tags']:
                return self.metadata['tags'][key]
        return ''  

    def set_tag(self, key: str, value: str):
        """modify a tag or create it if not exists

        Parameters
        ----------
        key
            The tag name
        value
            The tag value

        """

        if 'tags' not in self.metadata:
            self.metadata['tags'] = dict()
        self.metadata['tags'][key] = value

    def set_url(self, url: str):
        """Set the data URL

        Parameters
        ----------
        url
            The data URL

        """

        self.metadata['common']['url'] = url

    def set_name(self, name: str):
        """Set the data name

        Parameters
        ----------
        name
            The data name

        """

        self.metadata['common']['name'] = name

    def set_author(self, author: str):
        """Set the data author

        Parameters
        ----------
        author
            The data author

        """

        self.metadata['common']['author'] = author

    def set_createddate(self, date: str):
        """Set the data created date

        Parameters
        ----------
        date
            The data created date

        """

        self.metadata['common']['createddate'] = date

    def set_datatype(self, datatype: str):
        """Set the data datatype

        Parameters
        ----------
        datatype
            The data datatype

        """

        self.metadata['common']['datatype'] = datatype
        
    def set_thumbnail(self, thumbnail: str):
        """Set the data thumbnail url

        Parameters
        ----------
        thumbnail
            The data thumbnail url

        """

        self.metadata['common']['thumbnail'] = thumbnail

    def display(self): 
        """Display inherited from BiObject"""

        super(BiRawData, self).display()
        print("tag:")
        if 'tags' in self.metadata:
            for key, value in self.metadata["tags"]:
                print(key, ":", value)
        print('')


def create_rawdata(file: str) -> BiRawData:
    f= open(file,"w+")
    f.close()
    data = BiRawData(file)
    data.metadata['common'] = dict()
    data.metadata['common']['author'] = ''
    data.metadata['common']['createddate'] = ''
    data.metadata['common']['datatype'] = ''
    data.metadata['common']['name'] = ''
    data.metadata['common']['thumbnail'] = ''
    data.metadata['common']['url'] = ''
    data.metadata['origin'] = dict()
    data.metadata['type'] = "raw"
    return data

class BiProcessedData(BiData):
    """Class to store and manipulate RawData metadata
  
    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """
    def __init__(self, md_file_url : str):

        self._objectname = "BiProcessedData"
        BiData.__init__(self, md_file_url)

    def display(self): 
        """Display inherited from BiObject"""

        super(BiProcessedData, self).display()  
        print('Runurl: ' + self.metadata["origin"]['runurl'])
        print('')



class BiDataSet(BiMetaData):
    """Abstract class that store a dataset metadata
    
    BiDataSet allows to manipulate the common metadata. This class
    should not be used directly. BiRawDataSet and BiProcessedDataSet
    should be used as specific metadata containers

    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """

    def __init__(self, md_file_url : str):

        BiMetaData.__init__(self, md_file_url)
        self._objectname = "BiDataSet"
        self.data_list = dict()

    def name(self) -> str:
        """get the name of the dataset
        
        Returns
        ----------
        str
            The name of the dataset 

        """

        if 'name' in self.metadata:
            return self.metadata["name"]
        else:
            return ''

    def size(self) -> int:
        """get the size of the dataset
        
        Returns
        ----------
        str
            The size of the dataset 

        """

        if 'urls' in self.metadata:
            return len(self.metadata["urls"]) 
        else:
            return 0

    def urls(self) -> list:
        """get the data urls
        
        Returns
        ----------
        list
            The list of the data urls 

        """

        if 'urls' in self.metadata:
            return self.metadata["urls"]
        else:
            return []    

    def url(self, i: int) -> str:
        """get one data url
        
        Parameters
        ----------
        i
            Index of the data in the dataset

        Returns
        ----------
        str
            The data url 

        """

        return self.metadata["urls"][i]

    def add_data_md_file(self, md_file_url: str):
        """add a md file to the data list

        Parameters
        ----------
        md_file_url
            the url (absolute path or relative path to the dataset) metadata file path

        """

        self.metadata["urls"].append(md_file_url)        

    def data(self, i: int) -> BiData:
        """get one data information
        
        Parameters
        ----------
        i
            Index of the data in the dataset

        Returns
        ----------
        BiData
            The data common information 

        """

        if i in self.data_list:
            return self.data_list[i]
        else:   
            self.data_list[i] = BiData(os.path.join(self.md_file_path(), self.url(i)))
            return self.data_list[i]  


class BiRawDataSet(BiDataSet):
    """Class that store a dataset metadata for RawData
  
    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """
    
    def __init__(self, md_file_url : str):
        BiDataSet.__init__(self, md_file_url)
        self._objectname = 'BiRawDataSet'

    def raw_data(self, i: int) -> BiRawData:
        """get one data information
        
        Parameters
        ----------
        i
            Index of the data in the dataset

        Returns
        ----------
        BiRawData
            The data common information 

        """

        return BiRawData(os.path.join(self.md_file_path(), self.url(i)))
 
    def add_data(self, data: BiRawData):
        """Add one data to the dataset
        
        Parameters
        ----------
        md_file_url
            Path of the metadata file

        """
        
        self.data_list[self.size()] = data
        md_file_url = data.md_file_name()

        if 'urls' in self.metadata:
            self.metadata['urls'].append(md_file_url)
        else:
            self.metadata['urls'] = [md_file_url]    

    def to_list(self) -> list:
        """Get the metadata information as a list
        
        Returns
        -------
        list
            List of the data metadata stored in BiRawData objects

        """

        data_list = []
        for i in range(self.size()):
            data_list.append(BiRawData(os.path.join(self.md_file_path(), self.url(i))))   
        return data_list

    def data(self, i: int) -> BiRawData:
        """get one data information
        
        Parameters
        ----------
        i
            Index of the data in the dataset

        Returns
        ----------
        BiRawData
            The data common information 

        """

        if i in self.data_list:
            return self.data_list[i]
        else:   
            self.data_list[i] = BiRawData(os.path.join(self.md_file_path(), self.url(i)))
            return self.data_list[i]

class BiProcessedDataSet(BiDataSet):
    """Class that store a dataset metadata for ProcessedData
  
    Parameters
    ----------
    xml_file_url
        Path of the XML process file

    Attributes
    ----------
    metadata 
        dictionnary containing all the meatadata

    """
    
    def __init__(self, md_file_url : str):

        BiDataSet.__init__(self, md_file_url)
        self._objectname = "BiProcessedDataSet"    

    def processed_data(self, i: int) -> BiProcessedData:
        """Get the metadata information as a list
        
        Returns
        -------
        list
            List of the data metadata stored in BiProcessedData objects

        """

        return BiProcessedData(os.path.join(self.md_file_path(), self.url(i)))        
        
class BiRunParameter():
    def __init__(self, name : str = '', value: str = ''  ):
        self.name = name 
        self.value = value

class BiRun(BiMetaData):
    def __init__(self, md_file_url : str):
        BiRun.__init__(self, md_file_url)
        self._objectname = "BiDataSet"

    def process_name(self) -> str:
        return self.metadata["process"]['name']

    def set_process_name(self, name: str):
        self.metadata["process"]['name'] = name

    def process_url(self) -> str:
        return self.metadata["process"]['url']

    def set_process_url(self, url : str):
        self.metadata["process"]['url'] = url

    def processeddataset(self) -> str:
        return self.metadata["processeddataset"]

    def set_processeddataset(self, processeddataset: str):
        self.metadata["processeddataset"] = processeddataset

    def parameters_count(self) -> int:
        return len(self.metadata["parameters"])

    def clear_parameters(self):
        self.metadata["parameters"] = []

    def add_arameter(self, parameter: BiRunParameter):
        self.metadata["parameters"].append(parameter)

    def parameter(self, i: int) -> BiRunParameter:
        return self.metadata["parameters"][i]
    
        