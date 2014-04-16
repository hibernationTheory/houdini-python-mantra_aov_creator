# define an imagePlane object (class) : done 
# have a render passes list that consists of ImagePlane names : done
# have a consturctor class, which would from a given name would return a imageplane object with predefined settings for that image plane : done
# you need a function that would create an image plane on a mantra node from a given imageplane object
# you need another function that would re-construct an imageplane object from the settings on a mantra node.
# you need a way to display those image planes to the user to give them a choice
# comment properly 
# tidy it up
# git
# pep

# import sys

# path = "E:\project\project-houdini_scripting\scripts"
# path = path.replace("\\", "/")

# x = sys.path.insert(0, path)

# import addImagePlanes as ai
# reload(ai)

# selected = hou.selectedNodes()[0]
# ai.MantaImagePlaneCreator(selected)

import hou
import time

class ImagePlaneGlobalVariables(object):
    renderPasses = ["Cf", "Of", "Af", "P", "Pz", "N", "Render_Time", "Shading_Samples", "Pixel_Samples", 
    "direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
    "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
    "sss_single", "sss_multi"
    ]


class ImagePlaneWrapper(object):
    def __init__(self, parent = None, variableName = None):
        self.DIAGNOSTIC = ["Shading_Samples", "Pixel_Samples"]
        self.NATIVE = ["Cf", "Of", "Af", "P", "Pz", "N", "Render_Time", "Shading_Samples", "Pixel_Samples", 
                "direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
                "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
                "sss_single", "sss_multi"
                ]
        #extrinsic attrs
        self.parent = None
        self.variableNumber = 1 # the list number
        #variable dependent
        self.isDiagnostic = False
        self.isNative = True
        self.imagePlane = ImagePlane(variableName = variableName)


class ImagePlane(object):
    def __init__(self, variableName = None):
        self.displayName(variableName)
        #intristic attrs
        self.vm_variable_plane = variableName
        self.vm_disable_plane = False
        self.vm_vextype_plane = "vector"
        self.vm_quantize_plane = "half"
        self.vm_sfilter_plane = "alpha"
        self.vm_lightexport = 0
        self.vm_lightexport_scope = "*"
        self.vm_lightexport_select = "*"

    def __str__(self): #?
        return str(self.displayName)

    def __repr__(self): #?
        return "ImagePlane(variableName=%r)" %(self.vm_variable_plane)

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def displayName(self, givenName):
        if not isinstance(givenName, str):
            return None
        resultantName = givenName.replace("_", " ")
        resultantName = resultantName.title()
        self.displayName = resultantName


class ImagePlaneCreator(object):

    def __init__(self, parent = None, imagePlaneName = None):
        #self.returnImagePlane(imagePlaneName)
            self.TYPE_FLOAT = ["Af", "Pz", "Render_Time", "Shading_Samples", "Pixel_Samples"]
            self.QUANTIZE_32F = ["P", "Pz"]
            self.PER_LIGHT_EXPORT = ["direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
                    "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
                    "sss_single", "sss_multi"]
            self.SAMPLE_FILTER = ["direct_emission", "indirect_emission"]
            self.imagePlane = self.returnImagePlane(imagePlaneName)

    def returnImagePlane(self, imagePlaneName):
        imagePlane = ImagePlane(imagePlaneName)
        if imagePlaneName in self.TYPE_FLOAT:
            imagePlane.vm_vextype_plane = "float"
        if imagePlaneName in self.QUANTIZE_32F:
            imagePlane.vm_quantize_plane = "float"
        if imagePlaneName in self.SAMPLE_FILTER:
            imagePlane.vm_sfilter_plane = "fullopacity"
        if imagePlaneName in self.SAMPLE_FILTER:
            imagePlane.vm_lightexport = 1

        return imagePlane


class MantaImagePlaneCreator(object):
    """Provides a given list of options to the user, and creates image planes on the selected mantra nodes,
    from the user selection
    """

    def __init__(self, selectedNodes = None):
        self.imagePlaneList = ImagePlaneGlobalVariables.renderPasses
        self.selection = hou.ui.selectFromList(choices=self.imagePlaneList)

        for i in hou.selectedNodes():
            if isinstance(i, hou.RopNode):
                self.run(i)
            else:
                print "%s is not a Rop Node" %i.name()


    def run(self, mantraNode):
        '''runs the operations necessary when the script is called'''
        currentList = self.returnExistingImagePlanes(mantraNode)
        self.houdiniImagePlaneMenu(self.selection, self.imagePlaneList, currentList, mantraNode)


    def returnImagePlaneAmount(self, mantraNode):
        '''given the mantra node, returns the amount of image planes on the node'''
        print "\nfunc returnImagePlaneAmount"

        mantraNumAuxSize = mantraNode.parm("vm_numaux").eval()

        #print "there are %s image planes on this node" %mantraNumAuxSize
        return mantraNumAuxSize


    def returnExistingImagePlanes(self, mantraNode):
        '''given the mantra node, return a list of image plane objects'''
        print "\nfunc returnExistingImagePlanes"

        count = 1
        existingImagePlanes = []
        mantraNumAuxSize = self.returnImagePlaneAmount(mantraNode)

        for i in range(mantraNumAuxSize):
            imagePlane = self.createImagePlane(mantraNode, count)
            existingImagePlanes.append(imagePlane)
            count += 1

        print "the image planes on this node are: %s" %existingImagePlanes
        return existingImagePlanes


    def createImagePlane(self, mantraNode, number):
        """creates an image plane object from the index number of an image plane on a mantraNode"""
        ip = ImagePlane()
        for i in ip.__dict__.iteritems():
            parmName = i[0]+"%s" %number
            parm = mantraNode.parm(parmName)
            if parm:
                ip.__dict__[i[0]] = parm.eval()

        ip.displayName(ip.vm_variable_plane)

        print "image plane %s is created" % ip.vm_variable_plane
        return ip


    def addImagePlane(self, mantraNode, imagePlane):
        """adds the given image plane to the given mantra node"""

        imagePlaneCount = self.returnImagePlaneAmount(mantraNode)
        targetNumber = imagePlaneCount + 1
        mantraNode.parm("vm_numaux").set(targetNumber)

        for i in imagePlane.__dict__.iteritems():
            parm = mantraNode.parm("%s%s" %(i[0], targetNumber))
            if parm:
                parm.set(i[1])


    def houdiniImagePlaneMenu(self, selection, imagePlaneList, currentList, mantraNode):

        selection = self.selection
        eligible = []

        for i in selection:
            iPlane = ImagePlaneCreator(imagePlaneName = imagePlaneList[i]).imagePlane
            if not iPlane in currentList:
                eligible.append(iPlane)
            else:
                print "image plane : %s is already existing on the mantra node: %s" %(iPlane, mantraNode)

        for i in eligible:
            self.addImagePlane(mantraNode, i)
            print "image plane: %s is added to the mantra node: %s" %(i, mantraNode)
