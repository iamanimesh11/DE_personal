import xml
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def xml_file_Read(filename):
    with open(filename,"r") as file:
        data=file.read()
        Bs_data = BeautifulSoup(data, "xml")
        b_unique = Bs_data.find_all('name')
        b_name = Bs_data.find('employee', {'number': '1'})
        # print(b_name)
        # using et library

        tree =ET.parse(filename)
        root=tree.getroot()
        print(root.tag)
        for i in root:
            print(i.tag,i.attrib)
            for j in i:
                print(j.tag,j.text)

xml_file_Read("data.xml")


# write a xml file:

def write_xml_file(filename):
    root = ET.Element('data')
    items = ET.SubElement(root, 'items')
    item1 = ET.SubElement(items, 'item')
    item1.set('name', 'item1')
    item1.text = 'item1description'

    tree = ET.ElementTree(root)
    tree.write(filename)



write_xml_file("write_xml.xml")