import maya.cmds as cmds
import maya.mel as mel

# Make a new window
windowID = 'obj++'

# Close if copy is open
if cmds.window(windowID, exists = True):
    cmds.deleteUI(windowID)

# Make window
window = cmds.window( windowID, title=windowID, widthHeight=(200, 30) )
cmds.columnLayout( adjustableColumn=True )
cmds.text('obj++ Exporter Importer')
cmds.button( label='Export', command=('Export()') )
cmds.button( label='Import', command=('Import()') )
cmds.setParent( '..' )
cmds.showWindow( window )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Opens dialog menu

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Dialog(mode):
	singleFilter = "SKL Files (*.skl)"
	
	if mode == "export":
	    path = cmds.fileDialog2(ff=singleFilter, fm=0, okc = "OK")[0].rpartition(".")[0]
	    
	if mode == "import":
	    path = cmds.fileDialog2(ff=singleFilter, fm=1, okc = "OK")[0].rpartition(".")[0]
	    
	return path + ".skl"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Exports the .skl ( rough support of vw )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Command run for exporting the SKL
def Export():
	# Open file for writing
	path = Dialog("export")
	openFile = open(path, 'w')
	openFile.write('# skeleton output' + '\n')

	# Select the bone hierarchy
	cmds.select( hi=True )
	bones = cmds.ls( type='joint', sl=True )

	# Get bone count
	count = len(bones)
	print ( count )
	# Iterate through bones writing each and it's parent
	for x in range(0, count):
	    if (x != 0):
	        WriteSKL(
	        	openFile, 
	        	bones[x],
	        	str( bones.index( cmds.listRelatives( [bones[x]], parent=True )[0] ) ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[0] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[1] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[2] )
	        	)
	    else:
	        WriteSKL(
	        	openFile, 
	        	bones[x], 
	        	str(-1), 
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[0] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[1] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[2] )
	        	)
	print ('SKL section written successfully')

	# Print a single WGT test
	openFile.write('\n')
	openFile.write('# weight output' + '\n')
	bs = ["j1", "j2"]
	ws = [str(0.333), str(0.6666)]
	WriteWGT(openFile, str(2), bs, ws)
	print ('WGT section written successfully')
		
	openFile.close()
	return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Writes SKL data to the file

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def WriteSKL (outputFile, boneName, parentIndex, x, y, z):				
    outputFile.write('bn' + ' ' + boneName + ' ' + parentIndex + ' ' + x + ' ' + y + ' ' + z + '\n')	
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Writes WGT data to the file

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def WriteWGT (outputFile, weightCount, bones, weights):
    boneWeights = ""
    for i in range(0, int(weightCount)):
        boneWeights += bones[i] + ' ' + weights[i] + ' '
				
    outputFile.write('vw' + ' ' + weightCount + ' ' + boneWeights + '\n')	
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Loads and constructs data from .skl

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Import():
    theBones = []
    path = Dialog("import")
    skl = open(path,'r')
    for line in skl.readlines():
        if not "bn" in line: continue
        print(line)
    	words = line.split()
    	theBones.append(words[1])
    	if (int(words[2]) == -1):
    	    cmds.joint(p=( words[3], words[4], words[5] ), n=words[1] )
    	else:
    	    cmds.joint(theBones[int(words[2])], p=( words[3], words[4], words[5] ), n=words[1] )
	        
    skl.close()
    return
