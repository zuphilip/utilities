# -*- coding: utf-8 -*-
# Python script to manage automatically generated dependents
# Author: Rintze M. Zelle
# Version: 2014-04-17
# * Requires lxml library (http://lxml.de/)

import os, glob, re, inspect
from lxml import etree

# http://stackoverflow.com/questions/50499
folderPath =  os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parentFolderPath = os.path.dirname (folderPath)
path = os.path.join(parentFolderPath, 'styles')
pathGeneratedStyles = os.path.join(parentFolderPath, 'utilities', 'generate_dependent_styles', 'generated_styles', 'frontiers')

dependentStyles = []
commentMatchingStyles = []
parentMatchingStyles = []
generatedStyles = []

for stylepath in glob.glob( os.path.join(path, 'dependent', 'frontiers*.csl') ):
    dependentStyles.append(os.path.join(stylepath))

for stylepath in glob.glob( os.path.join(pathGeneratedStyles, '*.csl') ):
    generatedStyles.append(os.path.basename(stylepath))

for style in dependentStyles:
    parser = etree.XMLParser(remove_blank_text=True)
    parsedStyle = etree.parse(style, parser)
    styleElement = parsedStyle.getroot()

    comments = styleElement.xpath("//comment()", namespaces={"cs": "http://purl.org/net/xbiblio/csl"})
    
    for comment in comments:
        if(comment.text == " Generated with https://github.com/citation-style-language/utilities/tree/master/generate_dependent_styles "):
            commentMatchingStyles.append(os.path.basename(style))
            #print os.path.basename(style)
    
    parentLink = styleElement.find(".//{http://purl.org/net/xbiblio/csl}link[@rel='independent-parent']")
    if(parentLink.attrib.get("href") == "http://www.zotero.org/styles/frontiers"):
        parentMatchingStyles.append(os.path.basename(style))

for style in parentMatchingStyles:
    if not (style in commentMatchingStyles):
        print "bad comment!"
    if not (style in generatedStyles):
        print "not generated!" 

#     counter = []
#     for infoNodeIndex, infoNode in enumerate(csInfo):
#         # check if node is an element
#         if isinstance(infoNode.tag, basestring):
#             # get rid of namespace
#             infoElement = infoNode.tag.replace("{http://purl.org/net/xbiblio/csl}","")
#             if(infoElement == "link"):
#                 infoElement += "[@" + infoNode.get("rel") + "]"
#             if((infoElement == "category") & (infoNode.get("citation-format") is not None)):
#                 infoElement += "[@citation-format]"
#             if((infoElement == "category") & (infoNode.get("field") is not None)):
#                 infoElement += "[@field]"
#         # check if node is a comment
#         elif (etree.tostring(infoNode, encoding='UTF-8', xml_declaration=False) == ("<!--" + infoNode.text.encode("utf-8") + "-->")):
#             # keep comments that precede any element at the top
#             if(sum(counter) == 0):
#                 counter.append(desiredOrder.index("preceding-comment"))
#             # keep a comment at the end at the end
#             elif(len(counter) == (len(csInfo) - 1)):
#                 counter.append(desiredOrder.index("end-comment"))
#             # keep other comments with preceding element
#             else:
#                 counter.append(counter[-1])
# 
#             # Possible improvements:
#             # * exceptions for recognizable comments (issn, category)
#         else:
#             print(infoNode)
# 
#     # Reorder attributes on cs:link
#     try:
#         links = styleElement.findall(".//{http://purl.org/net/xbiblio/csl}link")
#         for link in links:
#             rel = link.get("rel")
#             del link.attrib["rel"]
#             link.set("rel",rel)
#     except:
#         pass