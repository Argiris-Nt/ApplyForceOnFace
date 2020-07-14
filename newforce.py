import os
if ExtAPI.Context == 'Mechanical':
    import ansys

# Is called when the button is clicked.		
def createforce(currentAnalysis):
    ExtAPI.Log.WriteMessage("Clicked on newforce button...")
    load = currentAnalysis.CreateLoadObject("newforce", "newforce")

# Drop down menu if force is defined by components.
def show1(load,property):
	selection = load.Properties["Defined By"].ValueString
	if selection == "By Component":
	   return True
	else:
	   return False

# Drop down menu if force is defined by vector.	   
def show2(load,property):
	selection2 = load.Properties["Defined By"].ValueString
	if selection2 != "By Component":
	   return True
	else:
	   return False

# Select interior or exterior vector.
def changedirection(load,property,magnitude):
    selection3 = load.Properties["direction"].ValueString
    if selection3 == "interior":
	   return True
    else:
	   return False

def writeforce(load,stream):
    ExtAPI.Log.WriteMessage("Write newforce...")
    stream.Write("/com,\n")
    stream.Write("/com,*********** newforce "+load.Caption+" ***********\n")
    stream.Write("/com,\n")
	
    propGeo = load.Properties["Geometry"]

    geoType = propGeo.Properties['DefineBy'].Value
    FX = load.Properties["FX"].Value
    FY = load.Properties["FY"].Value
    FZ = load.Properties["FZ"].Value
    magnitude = load.Properties["magnitude"].Value
				
    if geoType == 'Named Selection':
        refName = propGeo.Value.SolverName
    else:
	    refIds = propGeo.Value.Ids
	 
    if changedirection(load,"direction",magnitude) == True:
        magnitude = -magnitude	
    stream.Write("FX="+FX.ToString()+"\n")
    stream.Write("FY="+FY.ToString()+"\n")
    stream.Write("FZ="+FZ.ToString()+"\n")
    stream.Write("magnitude="+magnitude.ToString()+"\n")
    mesh = load.Analysis.MeshData
    geo = load.Analysis.GeoData
    stream.Write("ALLSEL\n")
    face_id = propGeo.Value.Ids
    point = (.01,.015,0.)
    face = geo.GeoEntityById(face_id[0])
    u,v = face.ParamAtPoint(point)
    n = face.NormalAtParam(u,v)
    MX = n[0]*magnitude
    MY = n[1]*magnitude
    MZ = n[2]*magnitude
    stream.Write("MX="+MX.ToString()+"\n")
    stream.Write("MY="+MY.ToString()+"\n")
    stream.Write("MZ="+MZ.ToString()+"\n")
    if geoType != 'Named Selection':
	    ansys.createElementComponent(refIds, "frc" + load.Id.ToString(), mesh, stream, fromGeoIds=True)
		# If force is defined by components.
	    if show1(load,"defined by") == True:
	       stream.Write("CMSEL, S, frc"+ load.Id.ToString() + ",Node\n")
	       stream.Write("sfe, all, 1, press, 1, UX,"+ "FX\n")
	       stream.Write("sfe, all, 2, press, 1, UY,"+ "FY\n")
	       stream.Write("sfe, all, 3, press, 1, UZ,"+ "FZ\n")
	       stream.Write("ALLSEL\n")
		# If force is defined by vector.
	    elif show2(load,"defined by") == True: 
	       stream.Write("CMSEL, S, frc"+ load.Id.ToString() + ",Node\n")
	       stream.Write("sfe,all,1,press,1,UX,"+"MX\n")
	       
	       stream.Write("sfe,all,2,press,1,UY,"+"MY\n")
	       
	       stream.Write("sfe,all,3,press,1,UZ,"+"MZ\n")
	       stream.Write("ALLSEL\n")
    else:
	    # If force is defined by components.
        if show1(load,"defined by") == True:
            stream.Write("CMSEL,S,"+refName+",Node\n")
            stream.Write("sfe, all, 1, press, 1, UX,"+ "FX\n")
            stream.Write("sfe, all, 2, press, 1, UY,"+ "FY\n")
            stream.Write("sfe, all, 3, press, 1, UZ,"+ "FZ\n")
            stream.Write("ALLSEL\n")
		# If force is defined by vector.
        elif show2(load,"defined by") == True:
            stream.Write("CMSEL,S,"+refName+",Node\n")
            
            stream.Write("sfe,all,1,press,1,UX,"+"MX\n")
            
            stream.Write("sfe,all,2,press,1,UY,"+"MY\n")
            
            stream.Write("sfe,all,3,press,1,UZ,"+"MZ\n")
            stream.Write("ALLSEL\n")	