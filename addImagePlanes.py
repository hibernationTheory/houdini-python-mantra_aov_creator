# define an imagePlane object (class) : done 
# have a render passes list that consists of ImagePlane names : done
# have a consturctor class, which would from a given name would return a imageplane object with predefined settings for that image plane : done
# you need a function that would create an image plane on a mantra node from a given imageplane object
# you need another function that would re-construct an imageplane object from the settings on a mantra node.
# you need a way to display those image planes to the user to give them a choice

class ImagePlaneGlobalVariables(object):
    renderPasses = ["Cf", "Of", "Af", "P", "Pz", "N", "Render_Time", "Shading_Samples", "Pixel_Samples", 
    "direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
    "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
    "sss_single", "sss_multi"
    ]

class ImagePlane(object):
    def __init__(self, parent = None, variableName = None):
        #extrinsic attrs
        self.parent = None
        self.variableNumber = 1 # the list number
        self.displayName = self.displayName(variableName)
        #intristic attrs
        self.vm_variable_name = variableName
        self.vm_disable_plane = False
        self.vm_vextype = "vector"
        self.vm_quantize = "half"
        self.vm_sfilter = "alpha"
        self.vm_lightexport = 0
        self.vm_lightexport_scope = "*"
        self.vm_lightexport_select = "*"
        #variable dependent
        self.isDiagnostic = False
        self.isNative = True

    def __str__(self): #?
        return self.displayName

    def __repr__(self): #?
        return "ImagePlane(parent=%r, variableName=%r)" %(self.parent, self.vm_variable_name)

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
        return resultantName



class ImagePlaneCreator(object):

    def __init__(self, parent = None, imagePlaneName = None):
        #self.returnImagePlane(imagePlaneName)
            self.DIAGNOSTIC = ["Shading_Samples", "Pixel_Samples"]
            self.NATIVE = ["Cf", "Of", "Af", "P", "Pz", "N", "Render_Time", "Shading_Samples", "Pixel_Samples", 
                    "direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
                    "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
                    "sss_single", "sss_multi"
                    ]
            self.TYPE_FLOAT = ["Af", "Pz", "Render_Time", "Shading_Samples", "Pixel_Samples"]
            self.QUANTIZE_32F = ["P", "Pz"]
            self.PER_LIGHT_EXPORT = ["direct_diffuse", "direct_reflect", "direct_refract","direct_volume", "direct_emission", 
                    "indirect_diffuse", "indirect_reflect", "indirect_refract", "indirect_volume", "indirect_emission",
                    "sss_single", "sss_multi"]
            self.SAMPLE_FILTER = ["direct_emission", "indirect_emission"]
            self.imagePlane = self.returnImagePlane(parent, imagePlaneName)

    def returnImagePlane(self, parent, imagePlaneName):
        imagePlane = ImagePlane(parent, imagePlaneName)
        if imagePlaneName in self.DIAGNOSTIC:
            imagePlane.isDiagnostic = True
        if imagePlaneName not in self.NATIVE:
            imagePlane.isNative = False
        if imagePlaneName in self.TYPE_FLOAT:
            imagePlane.vm_vextype = "float"
        if imagePlaneName in self.QUANTIZE_32F:
            imagePlane.quantize = "float"
        if imagePlaneName in self.SAMPLE_FILTER:
            imagePlane.vm_sfilter = "fullopacity"
        if imagePlaneName in self.SAMPLE_FILTER:
            imagePlane.vm_lightexport = 1

        return imagePlane

    
def houdiniImagePlaneMenu(imagePlaneList):
    if not isinstance(imagePlaneList, list):
        print "please provide a python list object"
        return None
    if not imagePlaneList:
        print "list is empty"
        return None

    selection = hou.ui.selectFromList(choices=imagePlaneList)

    for i in selection:
        imagePlane = ImagePlaneCreator(imagePlaneName = selection[i])